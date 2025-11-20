"""
PowerShell Bridge for MCP Server
Implements local and remote PowerShell script execution with JSON serialization and error handling.
Includes retry logic with exponential backoff for improved reliability.
"""
import subprocess
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from functools import wraps

try:
    from pypsrp.client import Client
    from pypsrp.powershell import PowerShell, RunspacePool
    PYPSRP_AVAILABLE = True
except ImportError:
    PYPSRP_AVAILABLE = False


def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator for retrying async functions with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        backoff_factor: Multiplier for delay between retries
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        # Get logger from self if available
                        logger = None
                        if args and hasattr(args[0], 'logger'):
                            logger = args[0].logger
                        
                        if logger:
                            logger.warning(
                                f"Attempt {attempt + 1}/{max_retries + 1} failed, retrying in {delay}s",
                                error=str(e)
                            )
                        
                        await asyncio.sleep(delay)
                        delay *= backoff_factor
                    else:
                        if logger:
                            logger.error(
                                f"All {max_retries + 1} attempts failed",
                                error=str(e)
                            )
                        raise last_exception
            
            raise last_exception
        return wrapper
    return decorator

class PowerShellBridge:
    def __init__(
        self, 
        logger: Optional[logging.Logger] = None,
        max_retries: int = 3,
        timeout: int = 300  # 5 minutes default timeout
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.max_retries = max_retries
        self.timeout = timeout

    async def execute_script(
        self,
        script_path: str,
        function: str,
        params: Dict[str, Any],
        remote: bool = False,
        remote_host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a PowerShell function from a script, locally or remotely.
        Returns output as dict (parsed from JSON).
        
        Args:
            script_path: Path to PowerShell script file
            function: Function name to execute
            params: Dictionary of function parameters
            remote: If True, execute on remote host via WinRM/PSRemoting
            remote_host: Remote host address (required if remote=True)
            username: Remote authentication username (optional)
            password: Remote authentication password (optional)
        """
        if remote:
            return await self._execute_remote(
                script_path=script_path,
                function=function,
                params=params,
                remote_host=remote_host,
                username=username,
                password=password
            )
        else:
            return await self._execute_local(
                script_path=script_path,
                function=function,
                params=params
            )
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
    async def _execute_local(
        self,
        script_path: str,
        function: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute PowerShell script locally with retry logic"""
        try:
            # Validate script exists
            import os
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"PowerShell script not found: {script_path}")
            
            # Build PowerShell command with proper parameter handling
            param_parts = []
            for k, v in params.items():
                if isinstance(v, bool):
                    # PowerShell booleans
                    param_parts.append(f"-{k} ${str(v).lower()}")
                elif isinstance(v, (dict, list)):
                    # Complex types as JSON strings
                    json_str = json.dumps(v).replace('"', '`"')
                    param_parts.append(f'-{k} "{json_str}"')
                elif isinstance(v, str):
                    # Strings with escaping
                    param_parts.append(f"-{k} '{v}'")
                else:
                    # Numbers
                    param_parts.append(f"-{k} {v}")
            
            param_str = ' '.join(param_parts)
            
            # Build command
            ps_script = f". '{script_path}'; {function} {param_str} | ConvertTo-Json -Depth 5"
            command = ["pwsh", "-NoProfile", "-Command", ps_script]
            
            self.logger.info("Executing PowerShell script", command=ps_script)
            
            try:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=self.timeout
                )
            except subprocess.TimeoutExpired:
                self.logger.error("PowerShell execution timeout", timeout=self.timeout)
                raise TimeoutError(f"PowerShell execution timed out after {self.timeout}s")
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                self.logger.error("PowerShell execution failed", stderr=error_msg, returncode=result.returncode)
                raise RuntimeError(f"PowerShell error (exit code {result.returncode}): {error_msg}")
            
            # Parse JSON output
            try:
                output = json.loads(result.stdout)
                self.logger.info("PowerShell execution successful", function=function)
                return output
            except json.JSONDecodeError as e:
                self.logger.error(
                    "Failed to parse PowerShell output as JSON", 
                    output=result.stdout[:500],  # Truncate for logging
                    error=str(e)
                )
                raise ValueError(f"Invalid JSON output from PowerShell: {str(e)}")
                
        except (FileNotFoundError, RuntimeError, ValueError, TimeoutError):
            # Re-raise known exceptions (will trigger retry if decorated)
            raise
        except Exception as e:
            self.logger.error("Unexpected PowerShell execution error", error=str(e), error_type=type(e).__name__)
            raise RuntimeError(f"PowerShell execution failed: {str(e)}")
    
    @retry_with_backoff(max_retries=3, initial_delay=2.0, backoff_factor=2.0)
    async def _execute_remote(
        self,
        script_path: str,
        function: str,
        params: Dict[str, Any],
        remote_host: str,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute PowerShell script on remote host via WinRM/PSRemoting with retry logic"""
        if not PYPSRP_AVAILABLE:
            raise RuntimeError(
                "pypsrp is not installed. Install it with: pip install pypsrp"
            )
        
        if not remote_host:
            raise ValueError("remote_host is required for remote execution")
        
        self.logger.info("Executing PowerShell script remotely", host=remote_host, function=function)
        
        try:
            # Validate script exists
            import os
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"PowerShell script not found: {script_path}")
            
            # Read script content
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Build parameter string
            param_parts = []
            for k, v in params.items():
                if isinstance(v, bool):
                    param_parts.append(f"-{k} ${str(v).lower()}")
                elif isinstance(v, (dict, list)):
                    json_str = json.dumps(v).replace('"', '`"')
                    param_parts.append(f'-{k} "{json_str}"')
                elif isinstance(v, str):
                    param_parts.append(f"-{k} '{v}'")
                else:
                    param_parts.append(f"-{k} {v}")
            
            param_str = ' '.join(param_parts)
            
            # Build PowerShell script to execute
            ps_script = f"""
{script_content}

{function} {param_str} | ConvertTo-Json -Depth 5
"""
            
            # Create WinRM client
            with Client(
                server=remote_host,
                username=username,
                password=password,
                cert_validation=False,  # For dev/test - set to True in production
                ssl=True
            ) as client:
                # Execute PowerShell script
                stdout, stderr, rc = client.execute_ps(ps_script)
                
                if rc != 0:
                    error_msg = stderr.strip() if stderr else "Unknown error"
                    self.logger.error(
                        "Remote PowerShell execution failed", 
                        stderr=error_msg, 
                        rc=rc,
                        host=remote_host
                    )
                    raise RuntimeError(f"Remote PowerShell error (exit code {rc}): {error_msg}")
                
                # Parse JSON output
                try:
                    output = json.loads(stdout)
                    self.logger.info("Remote PowerShell execution successful", function=function, host=remote_host)
                    return output
                except json.JSONDecodeError as e:
                    self.logger.error(
                        "Failed to parse remote PowerShell output as JSON", 
                        output=stdout[:500],
                        error=str(e),
                        host=remote_host
                    )
                    raise ValueError(f"Invalid JSON output from remote PowerShell: {str(e)}")
                
        except (FileNotFoundError, RuntimeError, ValueError):
            # Re-raise known exceptions (will trigger retry if decorated)
            raise
        except Exception as e:
            self.logger.error(
                "Unexpected remote PowerShell execution error", 
                error=str(e), 
                error_type=type(e).__name__,
                host=remote_host
            )
            raise RuntimeError(f"Remote PowerShell execution failed: {str(e)}")

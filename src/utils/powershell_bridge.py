"""
PowerShell Bridge for MCP Server
Implements local and remote PowerShell script execution with JSON serialization and error handling.
"""
import subprocess
import json
import logging
from typing import Dict, Any, Optional

try:
    from pypsrp.client import Client
    from pypsrp.powershell import PowerShell, RunspacePool
    PYPSRP_AVAILABLE = True
except ImportError:
    PYPSRP_AVAILABLE = False

class PowerShellBridge:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

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
    
    async def _execute_local(
        self,
        script_path: str,
        function: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute PowerShell script locally"""
        try:
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
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    self.logger.error("PowerShell execution failed", stderr=result.stderr)
                    raise RuntimeError(f"PowerShell error: {result.stderr}")
                # Parse JSON output
                try:
                    output = json.loads(result.stdout)
                except json.JSONDecodeError:
                    self.logger.error("Failed to parse PowerShell output as JSON", output=result.stdout)
                    raise
                return output
            except Exception as e:
                self.logger.error("PowerShellBridge execution error", error=str(e))
                raise

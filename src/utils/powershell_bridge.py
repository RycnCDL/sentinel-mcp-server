"""
PowerShell Bridge for MCP Server
Implements local and remote PowerShell script execution with JSON serialization and error handling.
"""
import subprocess
import json
import logging
from typing import Dict, Any, Optional

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
        """
        if remote:
            # Remote execution (WinRM/pypsrp) - placeholder for future implementation
            raise NotImplementedError("Remote PowerShell execution not yet implemented.")
        else:
            # Local execution
            try:
                # Build PowerShell command
                param_str = ' '.join([
                    f'-{k} "{json.dumps(v) if isinstance(v, (dict, list)) else v}"' for k, v in params.items()
                ])
                command = [
                    "pwsh", "-NoProfile", "-Command",
                    f". '{script_path}'; {function} {param_str} | ConvertTo-Json -Depth 5"
                ]
                self.logger.info("Executing PowerShell script", command=command)
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

"""
MCP Tool Wrappers für SentinelManager PowerShell-Funktionen
Alle Funktionen werden dynamisch als MCP-Tools registriert und nutzen die PowerShell Bridge.
"""
import os
import structlog
from typing import Dict, Any, Optional
from utils.powershell_bridge import PowerShellBridge

logger = structlog.get_logger(__name__)

# Liste der PowerShell-Funktionen (aus SentinelManager)
SENTINEL_FUNCTIONS = [
    # Tabellenverwaltung
    "New-SentinelTable",
    "Get-SentinelTables",
    "Remove-SentinelTable",
    "Update-TablePlan",
    "Update-TableRetention",
    "View-TableRetention",
    # Analytics Rules
    "Get-AnalyticsRules",
    "Get-AnalyticsRuleDetails",
    "Enable-AnalyticsRule",
    "Disable-AnalyticsRule",
    "Remove-AnalyticsRule",
    "New-AnalyticsRule",
    # Workbooks
    "Get-SentinelWorkbooks",
    "Get-WorkbookDetails",
    "Remove-SentinelWorkbook",
    "Export-SentinelWorkbook",
    "Import-SentinelWorkbook",
    # Incidents
    "Get-SentinelIncidents",
    "Show-IncidentDetails",
    "Close-SentinelIncident",
    "Assign-IncidentOwner",
    "Add-IncidentComment",
    "Get-IncidentComments",
    # Backup & Export
    "Export-AnalyticsRules",
    "Export-AutomationRules",
    "Export-Watchlists",
    "Export-Functions",
    "Export-SavedQueries",
    "Export-TableData",
    # DCR/DCE Management
    "Get-DataCollectionRules",
    "Get-DataCollectionEndpoints",
    "New-DCRForTable",
    "New-StandaloneDCR",
    "New-StandaloneDCE",
    "Remove-DataCollectionRule",
    "Remove-DataCollectionEndpoint",
    "Update-DCRTransformation",
    "Add-DCRDataSource",
    "Test-DCRIngestion"
]

SCRIPT_PATH = os.getenv("SENTINEL_MANAGER_SCRIPT", "SentinelManager_v3.ps1")

# Global bridge instance
_bridge: Optional[PowerShellBridge] = None


def get_bridge() -> PowerShellBridge:
    """Get or create PowerShell bridge instance"""
    global _bridge
    if _bridge is None:
        _bridge = PowerShellBridge(logger=logger)
    return _bridge


def register_powershell_tools(mcp):
    """
    Register all SentinelManager PowerShell functions as MCP tools
    
    Args:
        mcp: FastMCP server instance
    """
    logger.info("Registering PowerShell tools", function_count=len(SENTINEL_FUNCTIONS))
    
    # Register each function as an MCP tool
    for func_name in SENTINEL_FUNCTIONS:
        # Create a closure to capture func_name
        def make_tool_func(name):
            async def tool_func(**kwargs) -> dict:
                """Execute PowerShell function via bridge"""
                logger.info(f"Executing PowerShell function", function=name, params=kwargs)
                bridge = get_bridge()
                try:
                    result = await bridge.execute_script(
                        script_path=SCRIPT_PATH,
                        function=name,
                        params=kwargs,
                        remote=False
                    )
                    logger.info(f"PowerShell function completed", function=name)
                    return result
                except Exception as e:
                    logger.error(f"PowerShell function failed", function=name, error=str(e))
                    raise
            
            # Set function metadata
            tool_func.__name__ = name.replace("-", "_").lower()
            tool_func.__doc__ = f"Execute PowerShell function: {name}"
            return tool_func
        
        # Register tool with FastMCP
        tool_func = make_tool_func(func_name)
        mcp.tool()(tool_func)
    
    logger.info("PowerShell tools registered successfully")

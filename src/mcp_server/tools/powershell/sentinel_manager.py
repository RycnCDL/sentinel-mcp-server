"""
MCP Tool Wrappers für SentinelManager PowerShell-Funktionen
Generic tool approach - FastMCP compatible (no **kwargs)
"""
import os
import structlog
from typing import Dict, Any, Optional
from utils.powershell_bridge import PowerShellBridge

logger = structlog.get_logger(__name__)

# Liste der verfügbaren PowerShell-Funktionen (aus SentinelManager)
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
    Register generic PowerShell executor tools (FastMCP compatible)

    Args:
        mcp: FastMCP server instance
    """
    logger.info(
        "Registering PowerShell tools (generic approach)",
        function_count=len(SENTINEL_FUNCTIONS),
        available_functions=", ".join(SENTINEL_FUNCTIONS)
    )

    # Register local execution tool
    @mcp.tool()
    async def execute_sentinel_powershell(
        function_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a SentinelManager PowerShell function locally.

        This tool provides access to 39+ PowerShell functions for Microsoft Sentinel management.

        Available Functions:

        TABLE MANAGEMENT:
        - New-SentinelTable: Create new custom table
        - Get-SentinelTables: List all custom tables
        - Remove-SentinelTable: Delete custom table
        - Update-TablePlan: Change table pricing plan
        - Update-TableRetention: Modify retention settings
        - View-TableRetention: View current retention

        ANALYTICS RULES:
        - Get-AnalyticsRules: List all analytics rules
        - Get-AnalyticsRuleDetails: Get rule details
        - Enable-AnalyticsRule: Enable a rule
        - Disable-AnalyticsRule: Disable a rule
        - Remove-AnalyticsRule: Delete a rule
        - New-AnalyticsRule: Create new rule

        WORKBOOKS:
        - Get-SentinelWorkbooks: List workbooks
        - Get-WorkbookDetails: Get workbook details
        - Remove-SentinelWorkbook: Delete workbook
        - Export-SentinelWorkbook: Export workbook
        - Import-SentinelWorkbook: Import workbook

        INCIDENTS:
        - Get-SentinelIncidents: List incidents
        - Show-IncidentDetails: Get incident details
        - Close-SentinelIncident: Close an incident
        - Assign-IncidentOwner: Assign incident owner
        - Add-IncidentComment: Add comment to incident
        - Get-IncidentComments: List incident comments

        BACKUP & EXPORT:
        - Export-AnalyticsRules: Export all rules
        - Export-AutomationRules: Export automation rules
        - Export-Watchlists: Export watchlists
        - Export-Functions: Export functions
        - Export-SavedQueries: Export saved queries
        - Export-TableData: Export table data

        DCR/DCE MANAGEMENT:
        - Get-DataCollectionRules: List DCRs
        - Get-DataCollectionEndpoints: List DCEs
        - New-DCRForTable: Create DCR for table
        - New-StandaloneDCR: Create standalone DCR
        - New-StandaloneDCE: Create standalone DCE
        - Remove-DataCollectionRule: Delete DCR
        - Remove-DataCollectionEndpoint: Delete DCE
        - Update-DCRTransformation: Update DCR transformation
        - Add-DCRDataSource: Add data source to DCR
        - Test-DCRIngestion: Test DCR ingestion

        Args:
            function_name: Name of the PowerShell function to execute (e.g., "Get-AnalyticsRules")
            parameters: Dictionary of parameters to pass to the function (optional)

        Returns:
            Dictionary containing the function execution result

        Example:
            {
                "function_name": "Get-AnalyticsRules",
                "parameters": {
                    "WorkspaceName": "MyWorkspace",
                    "Enabled": true
                }
            }
        """
        if parameters is None:
            parameters = {}

        # Validate function name
        if function_name not in SENTINEL_FUNCTIONS:
            available = ", ".join(SENTINEL_FUNCTIONS)
            raise ValueError(
                f"Unknown function '{function_name}'. "
                f"Available functions: {available}"
            )

        logger.info(
            "Executing PowerShell function (local)",
            function=function_name,
            params=parameters
        )

        bridge = get_bridge()
        try:
            result = await bridge.execute_script(
                script_path=SCRIPT_PATH,
                function=function_name,
                params=parameters,
                remote=False
            )
            logger.info("PowerShell function completed", function=function_name)
            return {
                "success": True,
                "function": function_name,
                "result": result
            }
        except Exception as e:
            logger.error(
                "PowerShell function failed",
                function=function_name,
                error=str(e)
            )
            return {
                "success": False,
                "function": function_name,
                "error": str(e),
                "error_type": type(e).__name__
            }

    # Register remote execution tool
    @mcp.tool()
    async def execute_sentinel_powershell_remote(
        function_name: str,
        remote_host: str,
        parameters: Optional[Dict[str, Any]] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a SentinelManager PowerShell function on a remote host via WinRM/PSRemoting.

        Same functions available as execute_sentinel_powershell, but executed remotely.
        Requires WinRM to be enabled on the target host.

        Args:
            function_name: Name of the PowerShell function to execute
            remote_host: Remote host address (e.g., "server.domain.com")
            parameters: Dictionary of parameters to pass to the function (optional)
            username: Username for remote authentication (optional, uses current user if not provided)
            password: Password for remote authentication (optional)

        Returns:
            Dictionary containing the function execution result

        Example:
            {
                "function_name": "Get-AnalyticsRules",
                "remote_host": "sentinel-mgmt.contoso.com",
                "parameters": {
                    "WorkspaceName": "MyWorkspace"
                },
                "username": "admin@contoso.com"
            }
        """
        if parameters is None:
            parameters = {}

        # Validate function name
        if function_name not in SENTINEL_FUNCTIONS:
            available = ", ".join(SENTINEL_FUNCTIONS)
            raise ValueError(
                f"Unknown function '{function_name}'. "
                f"Available functions: {available}"
            )

        logger.info(
            "Executing PowerShell function (remote)",
            function=function_name,
            host=remote_host,
            params=parameters
        )

        bridge = get_bridge()
        try:
            result = await bridge.execute_script(
                script_path=SCRIPT_PATH,
                function=function_name,
                params=parameters,
                remote=True,
                remote_host=remote_host,
                username=username,
                password=password
            )
            logger.info(
                "Remote PowerShell function completed",
                function=function_name,
                host=remote_host
            )
            return {
                "success": True,
                "function": function_name,
                "remote_host": remote_host,
                "result": result
            }
        except Exception as e:
            logger.error(
                "Remote PowerShell function failed",
                function=function_name,
                host=remote_host,
                error=str(e)
            )
            return {
                "success": False,
                "function": function_name,
                "remote_host": remote_host,
                "error": str(e),
                "error_type": type(e).__name__
            }

    logger.info("PowerShell tools registered successfully (2 generic tools)")

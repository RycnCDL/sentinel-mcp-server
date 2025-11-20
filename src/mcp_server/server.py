"""
Microsoft Sentinel MCP Server

FastMCP-based server providing Microsoft Sentinel management and automation tools.
"""

import asyncio
from typing import Optional
import structlog
from fastmcp import FastMCP

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from utils.lighthouse import get_lighthouse_manager
from mcp_server.tools.management.health_check import check_sentinel_health
from mcp_server.tools.powershell.sentinel_manager import register_powershell_tools

logger = structlog.get_logger(__name__)

# Initialize settings
settings = get_settings()

# Setup logging
setup_logging(
    level=settings.log_level,
    format_type=settings.log_format,
    log_requests=settings.log_requests,
)

# Create MCP server
mcp = FastMCP(
    name=settings.mcp_server_name,
    version=settings.mcp_server_version,
)

# Register PowerShell tools
register_powershell_tools(mcp)

# Global authenticator and lighthouse manager (initialized on first request)
_authenticator = None
_lighthouse_manager = None


async def get_auth():
    """Get or create authenticator instance"""
    global _authenticator
    if _authenticator is None:
        azure_config = settings.get_azure_config()
        _authenticator = get_authenticator(
            tenant_id=azure_config.tenant_id,
            client_id=azure_config.client_id,
            client_secret=azure_config.client_secret,
        )
        logger.info("Authenticator initialized")
    return _authenticator


async def get_lighthouse():
    """Get or create lighthouse manager instance"""
    global _lighthouse_manager
    if _lighthouse_manager is None:
        auth = await get_auth()
        _lighthouse_manager = await get_lighthouse_manager(auth)
        logger.info("Lighthouse manager initialized")
    return _lighthouse_manager


@mcp.tool()
async def sentinel_health_check(
    tenant_scope: str = "all",
    check_depth: str = "quick",
) -> dict:
    """
    Check health status of Microsoft Sentinel workspaces across tenants.

    This tool performs comprehensive health checks on your Sentinel workspaces including:
    - Data connector status and counts
    - Analytics rules (enabled/disabled counts)
    - Data ingestion metrics (for detailed checks)
    - Overall workspace health status

    Args:
        tenant_scope: Scope of tenants to check. Use "all" for all tenants,
                     or provide a tenant name to filter. Default: "all"
        check_depth: Depth of the health check. Options:
                    - "quick": Fast check of connectors and rules
                    - "detailed": Includes data ingestion metrics (slower)
                    Default: "quick"

    Returns:
        Dictionary containing:
        - summary: Overall health summary with counts and status
        - workspaces: List of individual workspace health check results

    Examples:
        Check all workspaces (quick):
        >>> sentinel_health_check()

        Check specific tenant (detailed):
        >>> sentinel_health_check(tenant_scope="Customer A", check_depth="detailed")

    Raises:
        Authentication errors if Azure credentials are invalid
        Permission errors if access to workspaces is denied
    """
    logger.info(
        "sentinel_health_check called",
        tenant_scope=tenant_scope,
        check_depth=check_depth,
    )

    try:
        # Get authenticator and lighthouse manager
        auth = await get_auth()
        lighthouse = await get_lighthouse()

        # Perform health check
        result = await check_sentinel_health(
            authenticator=auth,
            lighthouse_manager=lighthouse,
            tenant_scope=tenant_scope,
            check_depth=check_depth,
        )

        logger.info(
            "sentinel_health_check completed",
            workspaces_checked=result["summary"]["workspaces_checked"],
            overall_status=result["summary"]["overall_status"],
        )

        return result

    except Exception as e:
        logger.error("sentinel_health_check failed", error=str(e))
        return {
            "summary": {
                "status": "error",
                "error": str(e),
            },
            "workspaces": [],
        }


@mcp.get_prompt("sentinel-health-report")
async def sentinel_health_report_prompt() -> str:
    """Generate a detailed health report for all Sentinel workspaces"""
    return """Please check the health of all Microsoft Sentinel workspaces and provide a detailed report.

Include:
1. Overall health status summary
2. Any workspaces with issues or warnings
3. Data connector and analytics rule statistics
4. Recommendations for any detected issues

Use the sentinel_health_check tool with check_depth='detailed' for comprehensive results."""


@mcp.get_prompt("sentinel-quick-status")
async def sentinel_quick_status_prompt() -> str:
    """Get a quick status overview of Sentinel workspaces"""
    return """Please provide a quick status overview of all Microsoft Sentinel workspaces.

Use the sentinel_health_check tool with check_depth='quick' and summarize:
- Total number of workspaces
- Overall health status
- Any critical issues that need immediate attention"""


def main():
    """Main entry point for the MCP server"""
    logger.info(
        "Starting Microsoft Sentinel MCP Server",
        name=settings.mcp_server_name,
        version=settings.mcp_server_version,
        debug_mode=settings.debug_mode,
    )

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()

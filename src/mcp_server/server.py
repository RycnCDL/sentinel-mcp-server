"""
Microsoft Sentinel MCP Server

FastMCP-based server providing Microsoft Sentinel management and automation tools.
"""

import asyncio
from datetime import datetime
from typing import Optional
import structlog
from fastmcp import FastMCP

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from utils.lighthouse import get_lighthouse_manager
from mcp_server.tools.management.health_check import check_sentinel_health
from mcp_server.tools.powershell.sentinel_manager import register_powershell_tools
from mcp_server.tools.exploration.analytics_rules import (
    list_analytics_rules,
    get_analytics_rule_details,
)

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


@mcp.tool()
async def sentinel_list_analytics_rules(
    workspace_filter: str = "",
    tenant_filter: str = "",
    enabled_only: bool = False,
) -> dict:
    """
    List Microsoft Sentinel Analytics Rules across workspaces.

    This tool retrieves all analytics rules (detection rules) from your Sentinel workspaces,
    showing their names, configurations, and status. Analytics rules are the detection logic
    that creates alerts and incidents when threats are detected.

    Args:
        workspace_filter: Optional workspace name filter. Only workspaces matching this
                         string will be included. Default: "" (all workspaces)
        tenant_filter: Optional tenant name filter. Only tenants matching this string
                      will be included. Default: "" (all tenants)
        enabled_only: If True, only return enabled rules. If False, return all rules.
                     Default: False (return all rules)

    Returns:
        Dictionary containing:
        - timestamp: When the query was executed
        - workspaces_queried: Number of workspaces checked
        - total_rules: Total number of rules found
        - workspaces: List of workspaces with their rules:
            - workspace_name: Name of the workspace
            - tenant_name: Name of the tenant
            - rules_count: Number of rules in this workspace
            - rules: List of rule objects with:
                - rule_id: Unique identifier
                - rule_name: Display name of the rule
                - kind: Type of rule (Scheduled, Fusion, MLBehaviorAnalytics, etc.)
                - enabled: Whether the rule is currently enabled
                - severity: Alert severity (High, Medium, Low, Informational)
                - tactics: MITRE ATT&CK tactics
                - description: Rule description
                - last_modified: When the rule was last modified

    Examples:
        List all analytics rules:
        >>> sentinel_list_analytics_rules()

        List only enabled rules:
        >>> sentinel_list_analytics_rules(enabled_only=True)

        List rules for a specific tenant:
        >>> sentinel_list_analytics_rules(tenant_filter="Customer A")

        List rules for a specific workspace:
        >>> sentinel_list_analytics_rules(workspace_filter="prod-sentinel")

    Raises:
        Authentication errors if Azure credentials are invalid
        Permission errors if access to workspaces is denied
    """
    logger.info(
        "sentinel_list_analytics_rules called",
        workspace_filter=workspace_filter,
        tenant_filter=tenant_filter,
        enabled_only=enabled_only,
    )

    try:
        # Get authenticator and lighthouse manager
        auth = await get_auth()
        lighthouse = await get_lighthouse()

        # List analytics rules
        result = await list_analytics_rules(
            authenticator=auth,
            lighthouse_manager=lighthouse,
            workspace_filter=workspace_filter or None,
            tenant_filter=tenant_filter or None,
            enabled_only=enabled_only,
        )

        logger.info(
            "sentinel_list_analytics_rules completed",
            workspaces_queried=result["workspaces_queried"],
            total_rules=result["total_rules"],
        )

        return result

    except Exception as e:
        logger.error("sentinel_list_analytics_rules failed", error=str(e))
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "workspaces_queried": 0,
            "total_rules": 0,
            "workspaces": [],
        }


@mcp.tool()
async def sentinel_get_analytics_rule(
    workspace_name: str,
    rule_id: str,
) -> dict:
    """
    Get detailed information about a specific Microsoft Sentinel Analytics Rule.

    This tool retrieves comprehensive details about a single analytics rule, including:
    - Full rule configuration
    - Detection query (KQL) for scheduled rules
    - Entity mappings
    - Incident creation settings
    - Alert grouping configuration
    - Custom details and overrides

    Use this after listing rules to get the complete detection logic and configuration.

    Args:
        workspace_name: Name of the Sentinel workspace containing the rule.
                       Use the exact workspace name from sentinel_list_analytics_rules.
        rule_id: The rule ID to retrieve. Use the rule_id from sentinel_list_analytics_rules.

    Returns:
        Dictionary containing:
        - timestamp: When the query was executed
        - rule: Detailed rule object with:
            - rule_id: Unique identifier
            - rule_name: Display name
            - kind: Rule type (Scheduled, Fusion, etc.)
            - enabled: Whether rule is enabled
            - severity: Alert severity
            - tactics: MITRE ATT&CK tactics
            - techniques: MITRE ATT&CK techniques
            - description: Rule description
            - configuration: Rule-specific configuration:
                For Scheduled rules:
                - query: The KQL detection query
                - query_frequency: How often the query runs
                - query_period: Time window for the query
                - trigger_operator: Threshold operator
                - trigger_threshold: Alert threshold
            - incident_configuration: Settings for incident creation
            - entity_mappings: How entities are extracted from alerts
            - alert_details_override: Custom alert formatting
            - custom_details: Additional custom fields

    Examples:
        Get details for a specific rule:
        >>> sentinel_get_analytics_rule(
        ...     workspace_name="prod-sentinel",
        ...     rule_id="12345678-1234-1234-1234-123456789012"
        ... )

    Raises:
        ValueError: If workspace or rule is not found
        Authentication errors if Azure credentials are invalid
        Permission errors if access is denied
    """
    logger.info(
        "sentinel_get_analytics_rule called",
        workspace_name=workspace_name,
        rule_id=rule_id,
    )

    try:
        # Get authenticator and lighthouse manager
        auth = await get_auth()
        lighthouse = await get_lighthouse()

        # Get rule details
        result = await get_analytics_rule_details(
            authenticator=auth,
            lighthouse_manager=lighthouse,
            workspace_name=workspace_name,
            rule_id=rule_id,
        )

        logger.info(
            "sentinel_get_analytics_rule completed",
            workspace_name=workspace_name,
            rule_id=rule_id,
        )

        return result

    except Exception as e:
        logger.error(
            "sentinel_get_analytics_rule failed",
            workspace_name=workspace_name,
            rule_id=rule_id,
            error=str(e),
        )
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "rule": None,
        }


# Prompts commented out - FastMCP prompt API usage needs review
# TODO: Implement prompts correctly in future version
#
# @mcp.get_prompt("sentinel-health-report")
# async def sentinel_health_report_prompt() -> str:
#     """Generate a detailed health report for all Sentinel workspaces"""
#     return """Please check the health of all Microsoft Sentinel workspaces..."""
#
# @mcp.get_prompt("sentinel-quick-status")
# async def sentinel_quick_status_prompt() -> str:
#     """Get a quick status overview of Sentinel workspaces"""
#     return """Please provide a quick status overview..."""


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

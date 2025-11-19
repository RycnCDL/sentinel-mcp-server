#!/usr/bin/env python3
"""
Test MCP Server Locally

This script tests the MCP server tools locally without running the full server.
Useful for development and debugging.
"""

import sys
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from utils.lighthouse import get_lighthouse_manager
from mcp_server.tools.management.health_check import check_sentinel_health
import structlog


async def main():
    """Test the MCP server tools"""

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type=settings.log_format,
        log_requests=settings.log_requests,
    )

    logger = structlog.get_logger(__name__)
    logger.info("Starting MCP Server test")

    # Test authentication
    logger.info("Testing authentication...")
    azure_config = settings.get_azure_config()
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    if not authenticator.validate_authentication():
        logger.error("❌ Authentication failed!")
        return 1

    logger.info("✅ Authentication successful")

    # Test lighthouse
    logger.info("Testing Lighthouse workspace enumeration...")
    lighthouse = await get_lighthouse_manager(authenticator)

    try:
        # Use specific subscription ID from config instead of listing all
        subscription_id = azure_config.subscription_id
        logger.info(f"Querying subscription: {subscription_id}")

        workspaces = await lighthouse.get_sentinel_workspaces(subscription_id=subscription_id)
        logger.info(f"✅ Found {len(workspaces)} Sentinel workspaces")

        for ws in workspaces:
            logger.info(
                "Workspace found",
                name=ws.workspace_name,
                tenant=ws.tenant_name,
                subscription=ws.subscription_id[:8] + "...",
            )

    except Exception as e:
        logger.error("❌ Lighthouse enumeration failed", error=str(e))
        return 1

    # Test health check
    if workspaces:
        logger.info("Testing health check on first workspace...")

        try:
            result = await check_sentinel_health(
                authenticator=authenticator,
                lighthouse_manager=lighthouse,
                tenant_scope="all",
                check_depth="quick",
            )

            logger.info(
                "✅ Health check completed",
                workspaces_checked=result["summary"]["workspaces_checked"],
                overall_status=result["summary"]["overall_status"],
            )

            # Display results
            print("\n" + "=" * 80)
            print("HEALTH CHECK RESULTS")
            print("=" * 80)
            print(f"\nOverall Status: {result['summary']['overall_status'].upper()}")
            print(f"Workspaces Checked: {result['summary']['workspaces_checked']}")
            print(f"Tenants Checked: {result['summary']['tenants_checked']}")

            print("\nStatus Breakdown:")
            for status, count in result["summary"]["status_breakdown"].items():
                print(f"  {status.capitalize()}: {count}")

            print("\nWorkspace Details:")
            for ws_result in result["workspaces"]:
                print(f"\n  Workspace: {ws_result['workspace_name']}")
                print(f"  Tenant: {ws_result['tenant_name']}")
                print(f"  Status: {ws_result['status']}")

                if ws_result.get("metrics"):
                    metrics = ws_result["metrics"]
                    if "data_connectors" in metrics:
                        print(
                            f"    Data Connectors: {metrics['data_connectors'].get('total', 0)}"
                        )
                    if "analytics_rules" in metrics:
                        rules = metrics["analytics_rules"]
                        print(
                            f"    Analytics Rules: {rules.get('enabled', 0)} enabled, {rules.get('disabled', 0)} disabled"
                        )

                if ws_result.get("issues"):
                    print(f"    ⚠️  Issues: {len(ws_result['issues'])}")
                    for issue in ws_result["issues"]:
                        print(f"      - {issue['message']}")

            print("\n" + "=" * 80)

        except Exception as e:
            logger.error("❌ Health check failed", error=str(e), exc_info=True)
            return 1
    else:
        logger.warning("No workspaces found to test health check")

    logger.info("✅ All tests completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

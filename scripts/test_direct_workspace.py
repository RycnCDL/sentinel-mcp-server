#!/usr/bin/env python3
"""
Direct Workspace Test

Test direct access to a specific Sentinel workspace without enumeration.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from utils.lighthouse import SentinelWorkspace
from mcp_server.tools.management.health_check import SentinelHealthChecker
import structlog
import asyncio


async def main():
    """Test direct workspace access"""

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type=settings.log_format,
        log_requests=settings.log_requests,
    )

    logger = structlog.get_logger(__name__)
    logger.info("Starting direct workspace test")

    # Get Azure config
    azure_config = settings.get_azure_config()

    # Test authentication
    logger.info("Testing authentication...")
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    if not authenticator.validate_authentication():
        logger.error("❌ Authentication failed!")
        return 1

    logger.info("✅ Authentication successful")

    # Create workspace object directly
    workspace = SentinelWorkspace(
        workspace_id=f"/subscriptions/{azure_config.subscription_id}/resourceGroups/pc-sentineldemo-rg/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW",
        workspace_name="PC-SentinelDemo-LAW",
        resource_group="pc-sentineldemo-rg",
        subscription_id=azure_config.subscription_id,
        tenant_id=azure_config.tenant_id,
        tenant_name="Direct Test",
    )

    logger.info(
        "Testing direct workspace access",
        workspace_name=workspace.workspace_name,
        resource_group=workspace.resource_group,
        subscription=workspace.subscription_id,
    )

    # Test health check on this specific workspace
    try:
        logger.info("Running health check...")

        health_checker = SentinelHealthChecker(authenticator)
        result = await health_checker.check_workspace_health(
            workspace=workspace,
            check_depth="quick",
        )

        logger.info("✅ Health check completed successfully!")

        # Display results
        print("\n" + "=" * 80)
        print("HEALTH CHECK RESULTS")
        print("=" * 80)
        print(f"\nWorkspace: {result['workspace_name']}")
        print(f"Status: {result['status'].upper()}")

        if result.get("metrics"):
            metrics = result["metrics"]
            print("\nMetrics:")
            if "data_connectors" in metrics:
                print(f"  Data Connectors: {metrics['data_connectors'].get('total', 0)}")
            if "analytics_rules" in metrics:
                rules = metrics["analytics_rules"]
                print(
                    f"  Analytics Rules: {rules.get('enabled', 0)} enabled, {rules.get('disabled', 0)} disabled"
                )

        if result.get("issues"):
            print(f"\n⚠️  Issues Found: {len(result['issues'])}")
            for issue in result["issues"]:
                print(f"  - [{issue['severity']}] {issue['message']}")
        else:
            print("\n✅ No issues found")

        print("\n" + "=" * 80)
        return 0

    except Exception as e:
        logger.error("❌ Health check failed", error=str(e), exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

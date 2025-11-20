#!/usr/bin/env python3
"""
Test Health Check with Azure CLI Credentials

This bypasses the Service Principal issue and uses your Azure CLI login.
Run 'az login' first on your local system.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from azure.identity import AzureCliCredential
from utils.lighthouse import SentinelWorkspace
from mcp_server.tools.management.health_check import SentinelHealthChecker
import structlog
import asyncio
import logging


async def main():
    """Test with Azure CLI credentials"""

    # Setup simple logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)

    print("=" * 80)
    print("SENTINEL HEALTH CHECK - AZURE CLI AUTHENTICATION")
    print("=" * 80)

    # Use Azure CLI credential directly
    logger.info("\n🔑 Using Azure CLI credentials (from 'az login')")

    try:
        credential = AzureCliCredential()

        # Test if we can get a token
        token = credential.get_token("https://management.azure.com/.default")
        logger.info("✅ Successfully authenticated with Azure CLI")

    except Exception as e:
        logger.error(f"❌ Azure CLI authentication failed: {e}")
        logger.error("\nPlease run 'az login' first on your system!")
        return 1

    # Create workspace object
    workspace = SentinelWorkspace(
        workspace_id="/subscriptions/f0519492-d4b0-40e3-930d-be49cdc3e624/resourceGroups/pc-sentineldemo-rg/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW",
        workspace_name="PC-SentinelDemo-LAW",
        resource_group="pc-sentineldemo-rg",
        subscription_id="f0519492-d4b0-40e3-930d-be49cdc3e624",
        tenant_id="1126248f-0b1d-43e8-a801-d48393b8d061",
        tenant_name="Azure CLI Test",
    )

    logger.info(f"\n📊 Testing workspace: {workspace.workspace_name}")
    logger.info(f"   Resource Group: {workspace.resource_group}")

    # Create a simple authenticator wrapper
    class CLIAuthenticator:
        def __init__(self, credential):
            self._credential = credential

        def get_credential(self):
            return self._credential

    authenticator = CLIAuthenticator(credential)

    # Run health check
    try:
        logger.info("\n🏥 Running health check...")

        health_checker = SentinelHealthChecker(authenticator)
        result = await health_checker.check_workspace_health(
            workspace=workspace,
            check_depth="quick",
        )

        # Display results
        print("\n" + "=" * 80)
        print("HEALTH CHECK RESULTS")
        print("=" * 80)
        print(f"\nWorkspace: {result['workspace_name']}")
        print(f"Status: {result['status'].upper()}")

        if result.get("metrics"):
            metrics = result["metrics"]
            print("\n📈 Metrics:")
            if "data_connectors" in metrics:
                dc = metrics["data_connectors"]
                print(f"  Data Connectors: {dc.get('total', 0)} (Status: {dc.get('status', 'N/A')})")
            if "analytics_rules" in metrics:
                rules = metrics["analytics_rules"]
                print(f"  Analytics Rules: {rules.get('total', 0)} total")
                print(f"    - Enabled: {rules.get('enabled', 0)}")
                print(f"    - Disabled: {rules.get('disabled', 0)}")

        if result.get("issues"):
            print(f"\n⚠️  Issues Found: {len(result['issues'])}")
            for issue in result["issues"]:
                print(f"  - [{issue.get('severity', 'unknown')}] {issue.get('message', 'N/A')}")
        else:
            print("\n✅ No issues found")

        print("\n" + "=" * 80)
        print("✅ PHASE 1 HEALTH CHECK - SUCCESS!")
        print("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\n❌ Health check failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

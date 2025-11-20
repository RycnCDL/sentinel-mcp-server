#!/usr/bin/env python3
"""
Advanced Sentinel Workspace Diagnostic

This script performs detailed diagnostics on Sentinel workspace access.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.auth import get_authenticator
import structlog
import json


def main():
    """Run advanced diagnostics"""

    settings = get_settings()
    azure_config = settings.get_azure_config()

    # Setup simple logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)

    logger.info("=" * 80)
    logger.info("SENTINEL WORKSPACE ACCESS DIAGNOSTIC")
    logger.info("=" * 80)

    # Authenticate
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    credential = authenticator.get_credential()

    # Get token and decode
    token = credential.get_token("https://management.azure.com/.default")

    import base64
    parts = token.token.split('.')
    payload = parts[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(payload)
    claims = json.loads(decoded)

    logger.info("\n📋 TOKEN INFORMATION:")
    logger.info(f"  App ID (Service Principal): {claims.get('appid', 'N/A')}")
    logger.info(f"  Tenant ID: {claims.get('tid', 'N/A')}")
    logger.info(f"  Token Expires: {token.expires_on}")

    # Test different API calls
    logger.info("\n🔍 TESTING AZURE API ACCESS:")

    # Test 1: Log Analytics Workspace API (older, more permissive)
    logger.info("\n1. Testing Log Analytics Workspace API...")
    try:
        import requests

        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }

        # Try older API version
        url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}/resourceGroups/pc-sentineldemo-rg/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW?api-version=2021-06-01"

        response = requests.get(url, headers=headers)
        logger.info(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            logger.info("   ✅ SUCCESS - Can access workspace via Log Analytics API")
            data = response.json()
            logger.info(f"   Workspace ID: {data.get('id', 'N/A')}")
            logger.info(f"   Location: {data.get('location', 'N/A')}")
        elif response.status_code == 403:
            logger.info("   ❌ FORBIDDEN - No access to workspace")
            logger.info(f"   Response: {response.text}")
        else:
            logger.info(f"   ⚠️  Unexpected status: {response.text}")

    except Exception as e:
        logger.error(f"   ❌ Error: {e}")

    # Test 2: Sentinel Data Connectors API
    logger.info("\n2. Testing Sentinel Data Connectors API...")
    try:
        # Try with different API versions
        api_versions = ["2023-02-01", "2022-08-01", "2021-10-01"]

        for api_version in api_versions:
            url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}/resourceGroups/pc-sentineldemo-rg/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW/providers/Microsoft.SecurityInsights/dataConnectors?api-version={api_version}"

            response = requests.get(url, headers=headers)
            logger.info(f"   API Version {api_version}: Status {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ SUCCESS with {api_version}")
                logger.info(f"   Data Connectors: {len(data.get('value', []))}")
                break
            elif response.status_code == 403:
                logger.info(f"   ❌ FORBIDDEN with {api_version}")

    except Exception as e:
        logger.error(f"   ❌ Error: {e}")

    # Test 3: Check if we need Reader role at subscription level
    logger.info("\n3. Testing Subscription-Level Access...")
    try:
        url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}/resourcegroups/pc-sentineldemo-rg?api-version=2021-04-01"

        response = requests.get(url, headers=headers)
        logger.info(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            logger.info("   ✅ Can access resource group - subscription Reader role is working")
        elif response.status_code == 403:
            logger.info("   ❌ Cannot access resource group - may need subscription-level Reader role")

    except Exception as e:
        logger.error(f"   ❌ Error: {e}")

    logger.info("\n" + "=" * 80)
    logger.info("DIAGNOSTIC COMPLETE")
    logger.info("=" * 80)

    logger.info("\n📝 RECOMMENDATIONS:")
    logger.info("If all tests show 403 Forbidden, you need to:")
    logger.info("1. Add 'Reader' role at SUBSCRIPTION level")
    logger.info("2. Keep 'Microsoft Sentinel Reader' at WORKSPACE level")
    logger.info("3. Wait 5-10 minutes for RBAC propagation")
    logger.info("\nCommand to add Reader role:")
    logger.info(f"az role assignment create \\")
    logger.info(f"  --assignee {azure_config.client_id} \\")
    logger.info(f"  --role 'Reader' \\")
    logger.info(f"  --scope '/subscriptions/{azure_config.subscription_id}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())

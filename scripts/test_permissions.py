#!/usr/bin/env python3
"""
Test Azure Permissions - Diagnostic Tool

This script helps diagnose permission issues by checking what the
Service Principal can actually access.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
import structlog


def main():
    """Test Azure permissions"""

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type=settings.log_format,
        log_requests=settings.log_requests,
    )

    logger = structlog.get_logger(__name__)
    logger.info("Starting Azure permissions diagnostic test")

    # Test authentication
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

    # Get credential
    credential = authenticator.get_credential()

    # Test 1: Try to list subscriptions
    logger.info("\n=== Test 1: List Subscriptions ===")
    try:
        from azure.mgmt.resource.subscriptions import SubscriptionClient

        sub_client = SubscriptionClient(credential)
        subscriptions = list(sub_client.subscriptions.list())

        logger.info(f"✅ Can list subscriptions: Found {len(subscriptions)}")
        for sub in subscriptions:
            logger.info(
                "Subscription",
                id=sub.subscription_id,
                name=sub.display_name,
                state=sub.state,
                tenant_id=sub.tenant_id,
            )

    except Exception as e:
        logger.error(f"❌ Cannot list subscriptions: {str(e)}")

    # Test 2: Try to access specific subscription
    logger.info(f"\n=== Test 2: Access Specific Subscription ===")
    logger.info(f"Configured Subscription ID: {azure_config.subscription_id}")

    try:
        from azure.mgmt.resource import ResourceManagementClient

        resource_client = ResourceManagementClient(
            credential, azure_config.subscription_id
        )

        # Try to list resource groups
        logger.info("Attempting to list resource groups...")
        resource_groups = list(resource_client.resource_groups.list())

        logger.info(f"✅ Can list resource groups: Found {len(resource_groups)}")
        for rg in resource_groups:
            logger.info("Resource Group", name=rg.name, location=rg.location)

    except Exception as e:
        logger.error(f"❌ Cannot access subscription: {str(e)}")

    # Test 3: Try to list all resources
    logger.info(f"\n=== Test 3: List Resources ===")

    try:
        from azure.mgmt.resource import ResourceManagementClient

        resource_client = ResourceManagementClient(
            credential, azure_config.subscription_id
        )

        logger.info("Attempting to list all resources...")
        resources = list(resource_client.resources.list())

        logger.info(f"✅ Can list resources: Found {len(resources)}")

        # Count by type
        resource_types = {}
        for resource in resources:
            resource_type = resource.type
            resource_types[resource_type] = resource_types.get(resource_type, 0) + 1

        logger.info("Resource types found:")
        for rtype, count in resource_types.items():
            logger.info(f"  {rtype}: {count}")

    except Exception as e:
        logger.error(f"❌ Cannot list resources: {str(e)}")

    # Test 4: Check for Log Analytics workspaces specifically
    logger.info(f"\n=== Test 4: Check Log Analytics Workspaces ===")

    try:
        from azure.mgmt.resource import ResourceManagementClient

        resource_client = ResourceManagementClient(
            credential, azure_config.subscription_id
        )

        logger.info("Filtering for Log Analytics workspaces...")
        la_workspaces = list(
            resource_client.resources.list(
                filter="resourceType eq 'Microsoft.OperationalInsights/workspaces'"
            )
        )

        logger.info(f"✅ Found {len(la_workspaces)} Log Analytics workspaces")
        for ws in la_workspaces:
            logger.info(
                "Log Analytics Workspace",
                name=ws.name,
                location=ws.location,
                id=ws.id,
            )

    except Exception as e:
        logger.error(f"❌ Cannot filter for workspaces: {str(e)}")

    logger.info("\n=== Diagnostic Test Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

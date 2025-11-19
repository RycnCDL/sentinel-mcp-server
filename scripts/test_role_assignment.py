#!/usr/bin/env python3
"""
Test Role Assignment

Check if the Service Principal has the correct role assignments.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from azure.mgmt.authorization import AuthorizationManagementClient
import structlog


def main():
    """Test role assignments"""

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type="text",  # Use text for easier reading
        log_requests=False,
    )

    logger = structlog.get_logger(__name__)
    logger.info("Checking role assignments...")

    # Get Azure config
    azure_config = settings.get_azure_config()

    # Create authenticator
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    credential = authenticator.get_credential()

    # Create authorization client
    auth_client = AuthorizationManagementClient(
        credential, azure_config.subscription_id
    )

    # Workspace scope
    workspace_scope = f"/subscriptions/{azure_config.subscription_id}/resourceGroups/pc-sentineldemo-rg/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"

    logger.info(f"Checking roles for scope: {workspace_scope}")

    try:
        # List role assignments for the workspace
        assignments = list(
            auth_client.role_assignments.list_for_scope(workspace_scope)
        )

        logger.info(f"Found {len(assignments)} role assignments")

        # Filter for our Service Principal
        our_principal_id = "e6d7f68a-ea68-4950-9045-7aa18322b4fd"  # From the role assignment output

        print("\n" + "=" * 80)
        print("ROLE ASSIGNMENTS FOR WORKSPACE")
        print("=" * 80)

        for assignment in assignments:
            if assignment.principal_id == our_principal_id:
                role_id = assignment.role_definition_id
                role_name = role_id.split("/")[-1]

                # Try to get role definition name
                try:
                    role_def = auth_client.role_definitions.get_by_id(role_id)
                    role_name = role_def.role_name
                except:
                    pass

                print(f"\n✅ Assignment found for our Service Principal:")
                print(f"   Principal ID: {assignment.principal_id}")
                print(f"   Role: {role_name}")
                print(f"   Scope: {assignment.scope}")

        print("\n" + "=" * 80)

    except Exception as e:
        logger.error(f"Failed to list role assignments: {e}")
        return 1

    # Also try a direct Sentinel API call to see the exact error
    print("\n" + "=" * 80)
    print("TESTING DIRECT SENTINEL API CALL")
    print("=" * 80)

    try:
        from azure.mgmt.securityinsight import SecurityInsights

        sentinel_client = SecurityInsights(
            credential, azure_config.subscription_id
        )

        print("\nAttempting to list data connectors...")
        connectors = list(
            sentinel_client.data_connectors.list(
                resource_group_name="pc-sentineldemo-rg",
                workspace_name="PC-SentinelDemo-LAW",
            )
        )

        print(f"✅ Successfully listed {len(connectors)} data connectors!")

    except Exception as e:
        print(f"❌ Failed to list data connectors: {e}")

        # Check if it's a permission error
        error_str = str(e)
        if "403" in error_str or "Forbidden" in error_str:
            print("\n⚠️  This is a permission error (403 Forbidden)")
            print("   Possible reasons:")
            print("   1. RBAC propagation delay (wait 5-10 minutes)")
            print("   2. Role assigned to wrong scope")
            print("   3. Need additional roles (e.g., 'Reader' at subscription level)")

    print("\n" + "=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())

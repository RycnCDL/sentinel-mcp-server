#!/usr/bin/env python3
"""
Test script for Analytics Rules functionality

This script tests the new analytics rules exploration tools:
- List all analytics rules across workspaces
- Get detailed information about specific rules
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import get_settings
from utils.auth import get_authenticator
from utils.lighthouse import get_lighthouse_manager
from mcp_server.tools.exploration.analytics_rules import (
    list_analytics_rules,
    get_analytics_rule_details,
)


async def main():
    """Main test function"""
    print("=" * 80)
    print("Testing Analytics Rules Functionality")
    print("=" * 80)
    print()

    # Initialize settings
    settings = get_settings()
    azure_config = settings.get_azure_config()

    # Create authenticator
    print("1. Creating authenticator...")
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )
    print("   ✓ Authenticator created")
    print()

    # Create lighthouse manager
    print("2. Creating lighthouse manager...")
    lighthouse_manager = await get_lighthouse_manager(authenticator)
    print("   ✓ Lighthouse manager created")
    print()

    # List all analytics rules
    print("3. Listing analytics rules across all workspaces...")
    try:
        result = await list_analytics_rules(
            authenticator=authenticator,
            lighthouse_manager=lighthouse_manager,
            enabled_only=False,
        )

        print(f"   ✓ Successfully retrieved rules")
        print(f"   - Workspaces queried: {result['workspaces_queried']}")
        print(f"   - Total rules found: {result['total_rules']}")
        print()

        # Display summary for each workspace
        print("4. Workspace Summary:")
        for ws in result["workspaces"]:
            if "error" in ws:
                print(f"   ✗ {ws['workspace_name']}: {ws['error']}")
            else:
                print(f"   ✓ {ws['workspace_name']}: {ws['rules_count']} rules")

                # Show first 3 rules as examples
                if ws['rules']:
                    print(f"      Sample rules:")
                    for rule in ws['rules'][:3]:
                        enabled = "✓" if rule['enabled'] else "✗"
                        severity = rule.get('severity', 'N/A')
                        print(f"        {enabled} {rule['rule_name']} ({rule['kind']}, {severity})")

                    if ws['rules_count'] > 3:
                        print(f"        ... and {ws['rules_count'] - 3} more")
        print()

        # Test getting details for first rule if available
        for ws in result["workspaces"]:
            if ws.get("rules") and len(ws["rules"]) > 0:
                first_rule = ws["rules"][0]
                print(f"5. Getting details for rule: {first_rule['rule_name']}")
                print(f"   Workspace: {ws['workspace_name']}")
                print(f"   Rule ID: {first_rule['rule_id']}")

                try:
                    details = await get_analytics_rule_details(
                        authenticator=authenticator,
                        lighthouse_manager=lighthouse_manager,
                        workspace_name=ws['workspace_name'],
                        rule_id=first_rule['rule_id'],
                    )

                    print(f"   ✓ Successfully retrieved rule details")
                    rule_data = details['rule']
                    print(f"   - Name: {rule_data['rule_name']}")
                    print(f"   - Kind: {rule_data['kind']}")
                    print(f"   - Enabled: {rule_data['enabled']}")

                    if 'configuration' in rule_data and rule_data['configuration']:
                        print(f"   - Configuration keys: {list(rule_data['configuration'].keys())}")

                        # Show query if it's a scheduled rule
                        if 'query' in rule_data['configuration']:
                            query = rule_data['configuration']['query']
                            query_preview = query[:200] + "..." if len(query) > 200 else query
                            print(f"   - Query preview: {query_preview}")

                    if 'entity_mappings' in rule_data:
                        print(f"   - Entity mappings: {len(rule_data['entity_mappings'])} entities")

                    print()

                except Exception as e:
                    print(f"   ✗ Failed to get rule details: {str(e)}")

                # Only test one rule
                break

        print("=" * 80)
        print("✓ All tests completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

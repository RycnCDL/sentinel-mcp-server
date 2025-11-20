#!/usr/bin/env python3
"""
Test Raw Azure REST API

Direct REST API calls to bypass SDK and test permissions.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.auth import get_authenticator
import requests
import json


def main():
    """Test raw REST API calls"""

    settings = get_settings()
    azure_config = settings.get_azure_config()

    print("=" * 80)
    print("TESTING RAW AZURE REST API")
    print("=" * 80)

    # Get token
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    credential = authenticator.get_credential()
    token = credential.get_token("https://management.azure.com/.default")

    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }

    # Test 1: Get workspace details
    print("\n1️⃣  Testing: Get Workspace Details")
    print("-" * 80)

    workspace_url = (
        f"https://management.azure.com"
        f"/subscriptions/{azure_config.subscription_id}"
        f"/resourceGroups/pc-sentineldemo-rg"
        f"/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"
        f"?api-version=2022-10-01"
    )

    print(f"URL: {workspace_url}")
    response = requests.get(workspace_url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS!")
        data = response.json()
        print(f"Workspace ID: {data.get('id')}")
        print(f"Location: {data.get('location')}")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 2: List Sentinel Incidents (using correct provider namespace)
    print("\n2️⃣  Testing: List Sentinel Incidents")
    print("-" * 80)

    incidents_url = (
        f"https://management.azure.com"
        f"/subscriptions/{azure_config.subscription_id}"
        f"/resourceGroups/pc-sentineldemo-rg"
        f"/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"
        f"/providers/Microsoft.SecurityInsights/incidents"
        f"?api-version=2023-02-01"
    )

    print(f"URL: {incidents_url}")
    response = requests.get(incidents_url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS!")
        data = response.json()
        incidents = data.get('value', [])
        print(f"Found {len(incidents)} incidents")
        if incidents:
            print(f"First incident: {incidents[0].get('properties', {}).get('title', 'N/A')}")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 3: List Data Connectors
    print("\n3️⃣  Testing: List Data Connectors")
    print("-" * 80)

    connectors_url = (
        f"https://management.azure.com"
        f"/subscriptions/{azure_config.subscription_id}"
        f"/resourceGroups/pc-sentineldemo-rg"
        f"/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"
        f"/providers/Microsoft.SecurityInsights/dataConnectors"
        f"?api-version=2023-02-01"
    )

    print(f"URL: {connectors_url}")
    response = requests.get(connectors_url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS!")
        data = response.json()
        connectors = data.get('value', [])
        print(f"Found {len(connectors)} data connectors")
        for conn in connectors:
            print(f"  - {conn.get('kind', 'Unknown')}")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 4: List Alert Rules
    print("\n4️⃣  Testing: List Alert Rules")
    print("-" * 80)

    rules_url = (
        f"https://management.azure.com"
        f"/subscriptions/{azure_config.subscription_id}"
        f"/resourceGroups/pc-sentineldemo-rg"
        f"/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"
        f"/providers/Microsoft.SecurityInsights/alertRules"
        f"?api-version=2023-02-01"
    )

    print(f"URL: {rules_url}")
    response = requests.get(rules_url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS!")
        data = response.json()
        rules = data.get('value', [])
        print(f"Found {len(rules)} alert rules")
        enabled = sum(1 for r in rules if r.get('properties', {}).get('enabled', False))
        print(f"  Enabled: {enabled}")
        print(f"  Disabled: {len(rules) - enabled}")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 5: Check if Sentinel is properly onboarded
    print("\n5️⃣  Testing: Check Sentinel Onboarding Status")
    print("-" * 80)

    # Try to get Sentinel settings
    settings_url = (
        f"https://management.azure.com"
        f"/subscriptions/{azure_config.subscription_id}"
        f"/resourceGroups/pc-sentineldemo-rg"
        f"/providers/Microsoft.OperationalInsights/workspaces/PC-SentinelDemo-LAW"
        f"/providers/Microsoft.SecurityInsights/settings"
        f"?api-version=2023-02-01"
    )

    print(f"URL: {settings_url}")
    response = requests.get(settings_url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ Sentinel is onboarded!")
        data = response.json()
        print(f"Settings: {json.dumps(data, indent=2)}")
    else:
        print(f"⚠️  Response: {response.text}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())

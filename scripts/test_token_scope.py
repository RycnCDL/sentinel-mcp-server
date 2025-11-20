#!/usr/bin/env python3
"""
Test Token Scope and Basic Azure Access
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.auth import get_authenticator
import requests
import json
import base64


def decode_token(token_string):
    """Decode JWT token"""
    parts = token_string.split('.')
    payload = parts[1]
    # Add padding if needed
    payload += '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(payload)
    return json.loads(decoded)


def main():
    """Test token scope"""

    settings = get_settings()
    azure_config = settings.get_azure_config()

    print("=" * 80)
    print("TOKEN SCOPE AND BASIC ACCESS TEST")
    print("=" * 80)

    # Get token
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    credential = authenticator.get_credential()
    token = credential.get_token("https://management.azure.com/.default")

    # Decode token
    claims = decode_token(token.token)

    print("\n📋 TOKEN CLAIMS:")
    print("-" * 80)
    print(f"App ID (aud): {claims.get('aud', 'N/A')}")
    print(f"Issuer (iss): {claims.get('iss', 'N/A')}")
    print(f"App ID (appid): {claims.get('appid', 'N/A')}")
    print(f"Tenant ID (tid): {claims.get('tid', 'N/A')}")
    print(f"Identity Provider (idp): {claims.get('idp', 'N/A')}")
    print(f"App ID ACR (appidacr): {claims.get('appidacr', 'N/A')}")
    print(f"Roles: {claims.get('roles', [])}")
    print(f"Scopes (scp): {claims.get('scp', 'N/A')}")

    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }

    # Test 1: List all subscriptions (most basic test)
    print("\n\n1️⃣  BASIC TEST: List Subscriptions")
    print("-" * 80)

    url = "https://management.azure.com/subscriptions?api-version=2022-01-01"
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS - Can list subscriptions")
        data = response.json()
        subs = data.get('value', [])
        print(f"Found {len(subs)} subscriptions")
        for sub in subs:
            print(f"  - {sub.get('displayName')} ({sub.get('subscriptionId')})")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 2: Get specific subscription
    print("\n\n2️⃣  TEST: Get Specific Subscription")
    print("-" * 80)

    url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}?api-version=2022-01-01"
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS - Can access subscription")
        data = response.json()
        print(f"Subscription: {data.get('displayName')}")
        print(f"State: {data.get('state')}")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 3: List resource groups
    print("\n\n3️⃣  TEST: List Resource Groups")
    print("-" * 80)

    url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}/resourcegroups?api-version=2022-01-01"
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS - Can list resource groups")
        data = response.json()
        rgs = data.get('value', [])
        print(f"Found {len(rgs)} resource groups")
        for rg in rgs:
            print(f"  - {rg.get('name')} ({rg.get('location')})")
    else:
        print(f"❌ FAILED: {response.text}")

    # Test 4: Get specific resource group
    print("\n\n4️⃣  TEST: Get Specific Resource Group")
    print("-" * 80)

    url = f"https://management.azure.com/subscriptions/{azure_config.subscription_id}/resourcegroups/pc-sentineldemo-rg?api-version=2022-01-01"
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS - Can access resource group")
        data = response.json()
        print(f"Resource Group: {data.get('name')}")
        print(f"Location: {data.get('location')}")
    else:
        print(f"❌ FAILED: {response.text}")

    print("\n" + "=" * 80)
    print("DIAGNOSIS:")
    print("=" * 80)

    if response.status_code == 403:
        print("\n⚠️  CRITICAL: Even basic operations return 403 Forbidden")
        print("\nPossible causes:")
        print("1. Conditional Access Policy blocking this IP/location")
        print("2. Service Principal requires admin consent for API permissions")
        print("3. Azure Resource Providers not registered")
        print("4. Wrong Azure Cloud (Commercial vs Government vs China)")
        print("\nRecommendation:")
        print("Check Azure Portal → Enterprise Applications")
        print(f"Find App ID: {azure_config.client_id}")
        print("Check 'Permissions' and ensure 'Azure Service Management' is granted")

    return 0


if __name__ == "__main__":
    sys.exit(main())

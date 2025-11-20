#!/usr/bin/env python3
"""
Quick Workspace Lister - Lists all Sentinel workspaces you have access to
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
from utils.lighthouse import LighthouseManager
import structlog
import asyncio


async def list_workspaces():
    """List all accessible Sentinel workspaces"""
    
    # Load settings
    settings = get_settings()
    
    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type="text",  # Use text for easier reading
        log_requests=False,
    )
    
    logger = structlog.get_logger(__name__)
    
    print("\n" + "="*80)
    print("SENTINEL WORKSPACE DISCOVERY")
    print("="*80 + "\n")
    
    # Get Azure config
    azure_config = settings.get_azure_config()
    
    # Check if credentials are configured
    if azure_config.client_id == "your-client-id":
        print("⚠️  Azure credentials not configured in .env file\n")
        print("Please edit .env and add:")
        print("  - AZURE_CLIENT_ID (your service principal app ID)")
        print("  - AZURE_CLIENT_SECRET (your service principal secret)\n")
        print("Or install Azure CLI and run: az login\n")
        return 1
    
    # Create authenticator
    logger.info("Initializing Azure authentication...")
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )
    
    if not authenticator.validate_authentication():
        logger.error("❌ Authentication failed!")
        print("\nAuthentication failed. Please check your credentials.\n")
        return 1
    
    logger.info("✅ Authentication successful")
    
    # Create Lighthouse manager
    lighthouse = LighthouseManager(authenticator)
    
    # Get all workspaces
    print("\n🔍 Searching for Sentinel workspaces...\n")
    
    try:
        workspaces = await lighthouse.get_sentinel_workspaces()
        
        if not workspaces:
            print("No Sentinel workspaces found.\n")
            print("This could mean:")
            print("  - No Sentinel workspaces in your subscription")
            print("  - Insufficient permissions to list workspaces")
            print("  - Need 'Reader' role at subscription level\n")
            return 0
        
        print(f"✅ Found {len(workspaces)} Sentinel workspace(s):\n")
        print("="*80)
        
        for i, ws in enumerate(workspaces, 1):
            print(f"\n{i}. {ws.workspace_name}")
            print(f"   Tenant: {ws.tenant_name}")
            print(f"   Resource Group: {ws.resource_group}")
            print(f"   Subscription: {ws.subscription_id}")
            print(f"   Location: {ws.location}")
            print(f"   Workspace ID: {ws.workspace_id}")
        
        print("\n" + "="*80)
        print(f"\n✅ Total: {len(workspaces)} workspace(s)\n")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to list workspaces: {e}")
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(list_workspaces()))

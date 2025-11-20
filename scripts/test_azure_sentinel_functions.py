"""
Test script for Azure Sentinel PowerShell functions
Tests real SentinelManager functions with Azure backend
"""
import sys
import os
import asyncio
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.powershell_bridge import PowerShellBridge
import structlog

logger = structlog.get_logger(__name__)

async def test_sentinel_functions():
    """Test real SentinelManager functions"""
    print("=== Sentinel PowerShell Functions Test ===\n")
    
    # Note: This assumes SentinelManager_v3.ps1 is available
    # and Azure authentication is configured
    
    sentinel_script = os.getenv(
        "SENTINEL_MANAGER_SCRIPT",
        r"C:\path\to\SentinelManager_v3.ps1"  # Update this path
    )
    
    if not os.path.exists(sentinel_script):
        print(f"⚠ SentinelManager script not found: {sentinel_script}")
        print("Please set SENTINEL_MANAGER_SCRIPT environment variable")
        print("or update the script path in this test file.")
        return
    
    bridge = PowerShellBridge(logger=logger)
    
    try:
        # Test 1: Get Sentinel Tables
        print("1. Testing Get-SentinelTables...")
        result1 = await bridge.execute_script(
            script_path=sentinel_script,
            function="Get-SentinelTables",
            params={"ShowHeader": False},
            remote=False
        )
        
        if result1:
            print(f"   ✓ Found {len(result1)} tables")
            if len(result1) > 0:
                print(f"   First table: {result1[0].get('name', 'N/A')}")
        else:
            print("   ⚠ No tables returned")
        
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # Test 2: Get Analytics Rules
        print("\n2. Testing Get-AnalyticsRules...")
        result2 = await bridge.execute_script(
            script_path=sentinel_script,
            function="Get-AnalyticsRules",
            params={"ShowHeader": False},
            remote=False
        )
        
        if result2:
            print(f"   ✓ Found {len(result2)} analytics rules")
            enabled_count = sum(1 for r in result2 if r.get('Enabled', False))
            print(f"   Enabled: {enabled_count}, Disabled: {len(result2) - enabled_count}")
        else:
            print("   ⚠ No rules returned")
            
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # Test 3: Get Sentinel Workbooks
        print("\n3. Testing Get-SentinelWorkbooks...")
        result3 = await bridge.execute_script(
            script_path=sentinel_script,
            function="Get-SentinelWorkbooks",
            params={},
            remote=False
        )
        
        if result3:
            print(f"   ✓ Found {len(result3)} workbooks")
        else:
            print("   ⚠ No workbooks returned")
            
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    print("Azure Sentinel function tests completed!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_sentinel_functions())

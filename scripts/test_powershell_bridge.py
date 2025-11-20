"""
Test script for PowerShell Bridge
Tests basic execution of PowerShell functions via the bridge
"""
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.powershell_bridge import PowerShellBridge

async def test_simple_command():
    """Test a simple PowerShell command"""
    print("Testing PowerShell Bridge with simple command...")
    
    bridge = PowerShellBridge()
    
    # Test 1: Simple PowerShell expression
    try:
        # Create a temporary test script
        test_script = """
function Test-HelloWorld {
    param([string]$Name = "World")
    @{
        Message = "Hello, $Name!"
        Timestamp = (Get-Date).ToString()
        Success = $true
    }
}
"""
        # Write test script
        script_path = os.path.join(os.path.dirname(__file__), 'test_temp.ps1')
        with open(script_path, 'w') as f:
            f.write(test_script)
        
        # Execute via bridge
        result = await bridge.execute_script(
            script_path=script_path,
            function="Test-HelloWorld",
            params={"Name": "Sentinel MCP Server"},
            remote=False
        )
        
        print("✓ Test passed!")
        print(f"Result: {result}")
        
        # Clean up
        os.remove(script_path)
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_command())

import subprocess
import json

print("Testing PowerShell availability...")
try:
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-Command", "Write-Output 'PowerShell OK'"], 
        capture_output=True, 
        text=True, 
        timeout=5
    )
    print(f"PowerShell test: {result.stdout.strip()}")
    print(f"Return code: {result.returncode}")
except Exception as e:
    print(f"PowerShell test failed: {e}")

print("\nTesting PowerShell JSON output...")
try:
    cmd = [
        "pwsh", "-NoProfile", "-Command", 
        "@{Message='Hello from PowerShell'; Success=$true} | ConvertTo-Json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    print(f"JSON output: {result.stdout}")
    print(f"Return code: {result.returncode}")
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        print(f"Parsed data: {data}")
        print("\n✓ PowerShell Bridge is working!")
except Exception as e:
    print(f"JSON test failed: {e}")
    import traceback
    traceback.print_exc()

# PowerShell Integration Guide

## Overview

The Sentinel MCP Server integrates PowerShell automation scripts from the `Sentinel-Tools` repository, allowing AI assistants to execute SOC workflows through natural language.

## Architecture

```
MCP Client (Claude/Copilot)
    │
    ├─→ Microsoft Sentinel MCP (Official) - Standard features
    │
    └─→ Custom MCP Server (This project)
        └─→ PowerShell Bridge
            ├─→ Local Execution (subprocess)
            └─→ Remote Execution (WinRM/pypsrp)
                └─→ SentinelManager PowerShell Scripts
```

## Features

### Implemented Functions (40+)

All SentinelManager functions are available as MCP tools:

**Table Management:**
- `new_sentineltable` - Create custom tables
- `get_sentineltables` - List all tables
- `remove_sentineltable` - Delete tables
- `update_tableplan` - Change tier plans
- `update_tableretention` - Configure retention
- `view_tableretention` - View retention details

**Analytics Rules:**
- `get_analyticsrules` - List all rules
- `get_analyticsruledetails` - View rule details
- `enable_analyticsrule` - Enable rules
- `disable_analyticsrule` - Disable rules
- `remove_analyticsrule` - Delete rules
- `new_analyticsrule` - Create rules

**Workbooks:**
- `get_sentinelworkbooks` - List workbooks
- `get_workbookdetails` - View details
- `remove_sentinelworkbook` - Delete workbooks
- `export_sentinelworkbook` - Export workbooks
- `import_sentinelworkbook` - Import workbooks

**Incidents:**
- `get_sentinelincidents` - List incidents
- `show_incidentdetails` - View details
- `close_sentinelincident` - Close incidents
- `assign_incidentowner` - Assign ownership
- `add_incidentcomment` - Add comments
- `get_incidentcomments` - List comments

**Backup & Export:**
- `export_analyticsrules` - Export analytics rules
- `export_automationrules` - Export automation
- `export_watchlists` - Export threat intel
- `export_functions` - Export KQL functions
- `export_savedqueries` - Export queries
- `export_tabledata` - Export table data

**DCR/DCE Management:**
- `get_datacollectionrules` - List DCRs
- `get_datacollectionendpoints` - List DCEs
- `new_dcrfortable` - Create DCR for table
- `new_standalonedcr` - Create standalone DCR
- `new_standalonedce` - Create standalone DCE
- `remove_datacollectionrule` - Delete DCR
- `remove_datacollectionendpoint` - Delete DCE
- `update_dcrtransformation` - Modify transformation
- `add_dcrdatasource` - Add data sources
- `test_dcringestion` - Test ingestion

## Setup

### Prerequisites

1. **PowerShell 7+**
   ```powershell
   # Install PowerShell Core
   winget install Microsoft.PowerShell
   ```

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **SentinelManager Scripts**
   - Clone or download from `RycnCDL/Sentinel-Tools`
   - Set environment variable:
     ```bash
     export SENTINEL_MANAGER_SCRIPT=/path/to/SentinelManager_v3.ps1
     ```

4. **Azure Authentication**
   - Azure CLI: `az login`
   - Or configure Service Principal in `.env`

### Configuration

Create `.env` file:
```bash
# Azure Configuration
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# PowerShell Configuration
SENTINEL_MANAGER_SCRIPT=/path/to/SentinelManager_v3.ps1

# Remote Execution (optional)
REMOTE_HOST=remote-server.domain.com
REMOTE_USERNAME=domain\user
REMOTE_PASSWORD=secure-password
```

## Usage

### Local Execution

```python
from utils.powershell_bridge import PowerShellBridge

bridge = PowerShellBridge()

# List Sentinel tables
result = await bridge.execute_script(
    script_path="/path/to/SentinelManager_v3.ps1",
    function="Get-SentinelTables",
    params={"ShowHeader": False},
    remote=False
)

print(f"Found {len(result)} tables")
```

### Remote Execution

```python
# Execute on remote server via WinRM
result = await bridge.execute_script(
    script_path="/path/to/SentinelManager_v3.ps1",
    function="Get-AnalyticsRules",
    params={},
    remote=True,
    remote_host="remote-server.domain.com",
    username="domain\\user",
    password="secure-password"
)
```

### MCP Integration

Tools are automatically registered when the MCP server starts:

```python
# In your MCP client (Claude Desktop, VS Code, etc.)
# Use natural language:
"Show me all Sentinel analytics rules"
"Create a new custom table for DNS logs"
"Export all workbooks to backup"
```

## Testing

### Unit Tests

```bash
# Test PowerShell Bridge
python scripts/test_powershell_bridge.py

# Test MCP Integration
python scripts/test_mcp_integration.py

# Test Azure Sentinel Functions
python scripts/test_azure_sentinel_functions.py
```

### Manual Testing

```python
import asyncio
from utils.powershell_bridge import PowerShellBridge

async def test():
    bridge = PowerShellBridge()
    result = await bridge.execute_script(
        script_path="SentinelManager_v3.ps1",
        function="Get-SentinelTables",
        params={},
        remote=False
    )
    print(result)

asyncio.run(test())
```

## Remote Execution Setup

### WinRM Configuration

On the remote Windows server:

```powershell
# Enable PSRemoting
Enable-PSRemoting -Force

# Configure WinRM for HTTPS (recommended)
$cert = New-SelfSignedCertificate -DnsName "server.domain.com" -CertStoreLocation Cert:\LocalMachine\My
New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $cert.Thumbprint -Force

# Configure firewall
New-NetFirewallRule -DisplayName "WinRM HTTPS" -Direction Inbound -LocalPort 5986 -Protocol TCP -Action Allow

# Set authentication
Set-Item WSMan:\localhost\Service\Auth\Basic $true
Set-Item WSMan:\localhost\Service\AllowUnencrypted $false
```

### Test Remote Connection

```bash
# From Python
python -c "
from pypsrp.client import Client

with Client('server.domain.com', username='domain\\user', password='pass', ssl=True) as client:
    stdout, stderr, rc = client.execute_cmd('whoami')
    print(stdout)
"
```

## Security Considerations

### Credential Management

1. **Never hardcode credentials** - Use environment variables or Azure Key Vault
2. **Use certificate-based auth** for production remote execution
3. **Enable HTTPS** for WinRM (port 5986)
4. **Audit all executions** - Logs are automatically generated

### Network Security

1. **Firewall rules** - Restrict WinRM access to specific IPs
2. **VPN/Private Network** - Don't expose WinRM to internet
3. **TLS encryption** - Always use SSL for remote execution

### Input Validation

All parameters are validated and sanitized before PowerShell execution to prevent command injection.

## Troubleshooting

### Common Issues

**PowerShell not found:**
```bash
# Check PowerShell installation
pwsh --version

# Install if missing
winget install Microsoft.PowerShell
```

**Remote execution fails:**
```bash
# Test WinRM connectivity
Test-WSMan -ComputerName remote-server.domain.com

# Check WinRM service
Get-Service WinRM
```

**JSON parsing errors:**
- Ensure PowerShell functions return valid JSON
- Use `ConvertTo-Json -Depth 5` in output
- Check for non-ASCII characters in output

**Authentication failures:**
- Verify Azure credentials: `az account show`
- Check Service Principal permissions
- Ensure SentinelManager is configured correctly

## Performance Optimization

### Caching

```python
# Cache PowerShell Bridge instance
_bridge = None

def get_bridge():
    global _bridge
    if _bridge is None:
        _bridge = PowerShellBridge()
    return _bridge
```

### Batch Operations

```python
# Execute multiple functions in parallel
import asyncio

async def batch_operations():
    bridge = get_bridge()
    tasks = [
        bridge.execute_script(..., function="Get-SentinelTables", ...),
        bridge.execute_script(..., function="Get-AnalyticsRules", ...),
        bridge.execute_script(..., function="Get-SentinelWorkbooks", ...)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## Best Practices

1. **Use async/await** for all PowerShell operations
2. **Log all executions** for audit trail
3. **Handle errors gracefully** with try/except
4. **Validate inputs** before execution
5. **Test locally first** before remote execution
6. **Use environment variables** for configuration
7. **Monitor performance** and optimize slow operations

## Examples

### Example 1: Bulk Table Management

```python
async def create_multiple_tables():
    bridge = get_bridge()
    
    tables = [
        {"name": "CustomLogs_DNS_CL", "schema": "DNSActivityLogs"},
        {"name": "CustomLogs_Web_CL", "schema": "WebActivityLogs"},
        {"name": "CustomLogs_Auth_CL", "schema": "AuthenticationLogs"}
    ]
    
    for table in tables:
        result = await bridge.execute_script(
            script_path=SENTINEL_SCRIPT,
            function="New-SentinelTable",
            params=table,
            remote=False
        )
        print(f"Created table: {table['name']}")
```

### Example 2: Health Check Workflow

```python
async def sentinel_health_check():
    bridge = get_bridge()
    
    # Get all tables
    tables = await bridge.execute_script(
        script_path=SENTINEL_SCRIPT,
        function="Get-SentinelTables",
        params={},
        remote=False
    )
    
    # Get analytics rules
    rules = await bridge.execute_script(
        script_path=SENTINEL_SCRIPT,
        function="Get-AnalyticsRules",
        params={},
        remote=False
    )
    
    # Generate report
    enabled_rules = sum(1 for r in rules if r.get('Enabled'))
    
    return {
        "tables_count": len(tables),
        "rules_total": len(rules),
        "rules_enabled": enabled_rules,
        "rules_disabled": len(rules) - enabled_rules
    }
```

### Example 3: Backup Automation

```python
async def automated_backup():
    bridge = get_bridge()
    
    # Export analytics rules
    await bridge.execute_script(
        script_path=SENTINEL_SCRIPT,
        function="Export-AnalyticsRules",
        params={"BackupPath": "./backups"},
        remote=False
    )
    
    # Export workbooks
    await bridge.execute_script(
        script_path=SENTINEL_SCRIPT,
        function="Export-AllWorkbooks",
        params={"BackupPath": "./backups"},
        remote=False
    )
    
    print("Backup completed successfully!")
```

## Roadmap

- [ ] Add retry logic with exponential backoff
- [ ] Implement connection pooling for remote execution
- [ ] Add progress tracking for long-running operations
- [ ] Support for certificate-based authentication
- [ ] Implement caching layer for frequently accessed data
- [ ] Add rate limiting for API calls
- [ ] Support for Azure Key Vault integration
- [ ] Implement detailed metrics and monitoring

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](../LICENSE) for details.

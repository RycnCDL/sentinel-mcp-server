# Claude Desktop Integration Guide

## Setup Instructions

### 1. Installation

**macOS:**
```bash
# Download from https://claude.ai/download
# Install Claude Desktop app
```

**Windows:**
```bash
# Download from https://claude.ai/download
# Install Claude Desktop app
```

### 2. Configuration

**Config File Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "command": "python",
      "args": ["-m", "src"],
      "cwd": "/absolute/path/to/sentinel-mcp-server",
      "env": {
        "AZURE_TENANT_ID": "your-tenant-id",
        "AZURE_CLIENT_ID": "your-client-id",
        "AZURE_CLIENT_SECRET": "your-client-secret",
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id",
        "SENTINEL_MANAGER_SCRIPT": "/path/to/SentinelManager_v3.ps1",
        "LOG_LEVEL": "INFO",
        "LOG_FORMAT": "json",
        "DEBUG_MODE": "false"
      }
    }
  }
}
```

**Important:**
- Replace `/absolute/path/to/sentinel-mcp-server` with actual path
- Replace Azure credentials with your values
- Ensure Python 3.10+ is in PATH
- Ensure PowerShell 7+ is installed

### 3. Testing

**Restart Claude Desktop** after configuration changes.

**Test Commands:**
```
1. "Check health of all Sentinel workspaces"
   → Should call sentinel_health_check tool

2. "List all Sentinel tables in PC-SentinelDemo-LAW"
   → Should call get_sentineltables PowerShell tool

3. "Show me all analytics rules"
   → Should call get_analyticsrules PowerShell tool
```

### 4. Verification

**Check Logs:**
- Claude Desktop logs available in app menu
- MCP Server logs in `sentinel-mcp-server/logs/`

**Expected Output:**
```
INFO: MCP Server started successfully
INFO: Registered 41 PowerShell tools
INFO: Health check tool registered
INFO: Ready to accept connections
```

### 5. Troubleshooting

**Problem: Server not starting**
```bash
# Test manually first
cd /path/to/sentinel-mcp-server
python -m src

# Check output for errors
```

**Problem: Tools not appearing**
```bash
# Verify FastMCP installation
pip show fastmcp

# Check server logs
tail -f logs/mcp-server.log
```

**Problem: Authentication failures**
```bash
# Test Azure credentials
az login
az account show

# Test PowerShell auth
pwsh -Command "Connect-AzAccount"
```

## Example Workflows

### Workflow 1: Health Check

**User:** "Check the health of all Sentinel workspaces"

**Expected Flow:**
1. Claude calls `sentinel_health_check` tool
2. Server queries Azure via Lighthouse
3. Returns health status for all workspaces
4. Claude formats results in natural language

### Workflow 2: Analytics Rules Management

**User:** "Show me disabled analytics rules in workspace PC-SentinelDemo-LAW"

**Expected Flow:**
1. Claude calls `get_analyticsrules` PowerShell tool
2. Server executes PowerShell function via bridge
3. Filters results for disabled rules
4. Returns structured data to Claude
5. Claude presents user-friendly summary

### Workflow 3: Multi-Workspace Query

**User:** "Which workspaces have more than 10 disabled analytics rules?"

**Expected Flow:**
1. Claude calls multiple PowerShell tools in sequence
2. Aggregates results across workspaces
3. Filters and analyzes data
4. Presents findings with recommendations

## Advanced Configuration

### Enable Debug Mode

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "env": {
        "DEBUG_MODE": "true",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Remote PowerShell Execution

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "env": {
        "POWERSHELL_REMOTE_HOST": "server.domain.com",
        "POWERSHELL_REMOTE_USER": "domain\\user",
        "POWERSHELL_REMOTE_PASSWORD": "secure-password"
      }
    }
  }
}
```

**Security Note:** Use environment variables instead of hardcoding credentials.

### Custom Timeout Settings

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "env": {
        "POWERSHELL_TIMEOUT": "600",
        "MCP_REQUEST_TIMEOUT": "120"
      }
    }
  }
}
```

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** for remote PowerShell
4. **Rotate secrets** regularly
5. **Audit all operations** via logging
6. **Limit permissions** to minimum required
7. **Use Azure Key Vault** in production

## Performance Tips

1. **Enable caching** for frequently accessed data
2. **Use batch operations** for multi-workspace tasks
3. **Monitor response times** via Application Insights
4. **Optimize KQL queries** for faster execution
5. **Connection pooling** for remote PowerShell

## Support & Documentation

- **Main Documentation**: `docs/`
- **PowerShell Integration**: `docs/powershell-integration.md`
- **Troubleshooting**: `docs/troubleshooting.md`
- **API Reference**: `docs/api-reference.md`

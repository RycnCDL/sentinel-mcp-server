# Setup Guide - Microsoft Sentinel MCP Server

## Quick Start

### Prerequisites ✅
- ✅ Python 3.10+
- ✅ PowerShell Core 7.4+
- ✅ Azure credentials (Service Principal or Azure CLI)
- ✅ Access to Microsoft Sentinel workspaces (via Azure Lighthouse)

### 1. Environment Setup

**Already completed:**
- ✅ Virtual environment created
- ✅ All dependencies installed
- ✅ Configuration files created

### 2. Configure Azure Authentication

Edit `.env` file and add your Azure credentials:

```bash
# Option A: Service Principal (Recommended for production)
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here
AZURE_SUBSCRIPTION_ID=your-default-subscription-id

# Option B: Azure CLI (For development)
# Just run: az login
# (Leave above variables empty)
```

### 3. Test Authentication

```bash
# Activate virtual environment
source venv/bin/activate

# Test authentication
python scripts/test_auth.py
```

Expected output:
```
✅ Authentication successful!
Token obtained successfully
```

### 4. Test Server Components

```bash
# Test MCP server tools locally
python scripts/test_server.py
```

This will:
- Validate authentication
- Enumerate Sentinel workspaces
- Run health check on all workspaces
- Display results

### 5. Run MCP Server

```bash
# Start the MCP server
python -m src
```

The server will start and be available for MCP clients (VS Code, Claude Desktop, etc.)

### 6. Configure VS Code

Add to your VS Code MCP settings (`~/.vscode/mcp-settings.json` or similar):

```json
{
  "mcpServers": {
    "sentinel": {
      "command": "/home/castiel/projects/mcp-server/venv/bin/python",
      "args": ["-m", "src"],
      "cwd": "/home/castiel/projects/mcp-server",
      "env": {
        "PYTHONPATH": "/home/castiel/projects/mcp-server/src"
      }
    }
  }
}
```

---

## Available Tools

### Tool #1: `sentinel_health_check`

Check health status of Microsoft Sentinel workspaces.

**Parameters:**
- `tenant_scope` (string, default: "all") - Filter by tenant name or "all"
- `check_depth` (string, default: "quick") - "quick" or "detailed"

**Example usage in VS Code:**

```
Check the health of all Sentinel workspaces
```

```
Check detailed health status for Customer A tenant
```

**Returns:**
```json
{
  "summary": {
    "timestamp": "2025-11-19T...",
    "tenants_checked": 10,
    "workspaces_checked": 15,
    "overall_status": "healthy",
    "status_breakdown": {
      "healthy": 12,
      "warning": 2,
      "error": 1,
      "unknown": 0
    }
  },
  "workspaces": [
    {
      "workspace_name": "customer-a-sentinel",
      "tenant_name": "Customer A",
      "status": "healthy",
      "metrics": {
        "data_connectors": {
          "total": 15
        },
        "analytics_rules": {
          "total": 45,
          "enabled": 43,
          "disabled": 2
        }
      },
      "issues": []
    }
  ]
}
```

---

## Troubleshooting

### Authentication Issues

**Problem:** `Authentication validation failed`

**Solutions:**
1. **Service Principal:**
   - Verify AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET in `.env`
   - Ensure Service Principal has permissions:
     - Microsoft Sentinel Reader
     - Log Analytics Reader
   - Check Service Principal isn't expired

2. **Azure CLI:**
   - Run `az login`
   - Verify: `az account show`

### No Workspaces Found

**Problem:** `Found 0 Sentinel workspaces`

**Solutions:**
1. Verify Azure Lighthouse delegation is configured
2. Check Service Principal has access via Lighthouse
3. Ensure you have at least one Sentinel workspace
4. Verify subscription access

### Permission Errors

**Problem:** `Failed to check data connectors` or similar

**Solutions:**
1. Ensure Service Principal has:
   - Microsoft Sentinel Reader role
   - Log Analytics Reader role
   - At workspace or resource group level
2. Check RBAC assignments in Azure Portal

---

## Development Workflow

### Making Changes

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Make changes to code**

3. **Test changes:**
   ```bash
   python scripts/test_server.py
   ```

4. **Run linting:**
   ```bash
   black src/
   ruff check src/
   mypy src/
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

### Adding New Tools

See `PHASE-1-IMPLEMENTATION-PLAN.md` for planned tools:
- Tool #2: `data_connector_status` (Next)
- Tool #3: `custom_kql_execute` (Next)

---

## Configuration Reference

### Environment Variables

See `.env.template` for all available configuration options.

**Key settings:**
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `LOG_FORMAT`: json, text
- `MAX_CONCURRENT_QUERIES`: Limit parallel workspace queries
- `QUERY_TIMEOUT_SECONDS`: Timeout for KQL queries
- `ENABLE_WORKSPACE_CACHE`: Cache workspace list

---

## Next Steps

1. ✅ Environment setup complete
2. ✅ Authentication configured
3. ✅ Tool #1 (`sentinel_health_check`) implemented
4. 🔄 Test with real workspaces
5. ⏳ Tool #2 (`data_connector_status`)
6. ⏳ Tool #3 (`custom_kql_execute`)

---

## Support

For issues or questions:
- Check `PHASE-1-IMPLEMENTATION-PLAN.md` for implementation details
- Check `PROJECT.md` for architecture decisions
- Create GitHub issue for bugs/features

---

**Version:** 0.1.0-alpha
**Status:** Phase 1 - MVP Development
**Last Updated:** 2025-11-19

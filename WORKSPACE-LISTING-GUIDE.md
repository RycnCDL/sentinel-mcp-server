# Quick Reference - List Sentinel Workspaces

## Current Setup

✅ **Script Created**: `list_workspaces.py`  
✅ **Configuration File**: `.env`  
✅ **Known Workspace**: PC-SentinelDemo-LAW

## To List All Workspaces

### Step 1: Configure Azure Credentials

Choose one option:

#### Option A: Service Principal (Production)
Edit `.env` file and replace:
- `AZURE_CLIENT_ID=your-client-id` with your service principal app ID
- `AZURE_CLIENT_SECRET=your-client-secret` with your service principal secret

#### Option B: Azure CLI (Quick Testing)
```bash
# Install Azure CLI from: https://aka.ms/installazurecliwindows
az login
# The script will auto-detect CLI credentials
```

### Step 2: Run the Script

```bash
python list_workspaces.py
```

## Expected Output

```
================================================================================
SENTINEL WORKSPACE DISCOVERY
================================================================================

🔍 Searching for Sentinel workspaces...

✅ Found 1 Sentinel workspace(s):

================================================================================

1. PC-SentinelDemo-LAW
   Tenant: <tenant-name>
   Resource Group: pc-sentineldemo-rg
   Subscription: f0519492-d4b0-40e3-930d-be49cdc3e624
   Location: <location>
   Workspace ID: /subscriptions/.../PC-SentinelDemo-LAW

================================================================================

✅ Total: 1 workspace(s)
```

## Files Modified

1. **`.env`** - Azure credentials configuration
2. **`list_workspaces.py`** - Workspace listing script (new)

## Known Workspace Details

- **Name**: PC-SentinelDemo-LAW
- **Resource Group**: pc-sentineldemo-rg
- **Subscription**: f0519492-d4b0-40e3-930d-be49cdc3e624
- **Tenant**: 1126248f-0b1d-43e8-a801-d48393b8d061

## Troubleshooting

### "Authentication failed"
- Verify credentials in `.env` file
- Check service principal has "Reader" role at subscription level
- Check service principal has "Microsoft Sentinel Reader" role at workspace level

### "No workspaces found"
- Verify you have access to the subscription
- Check that Sentinel is enabled on the workspace
- Verify RBAC permissions are propagated (can take 5-10 minutes)

## Alternative Scripts

- **`scripts/test_permissions.py`** - Detailed permission diagnostics
- **`scripts/diagnose_workspace_access.py`** - Advanced workspace access diagnostics

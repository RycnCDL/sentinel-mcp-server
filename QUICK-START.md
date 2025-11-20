# Quick Start Guide - Phase 3 Testing

## 🎯 Objective
Test the Microsoft Sentinel MCP Server end-to-end with Claude Desktop to verify all 41 tools work correctly.

---

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Claude Desktop** installed (download from anthropic.com)
- [ ] **Python 3.10+** installed
- [ ] **PowerShell 7+** installed
- [ ] **Azure Service Principal** with Sentinel permissions
- [ ] **SentinelManager.ps1** script downloaded
- [ ] **Git** installed (to clone this repository)

---

## 📦 Step 1: Clone and Setup Repository

**Hinweis**: Wenn du bereits in einem GitHub Codespace oder VS Code Remote bist, überspringe Schritt 1.1.

### 1.1 Clone Repository (nur für lokale Installation)
```powershell
# Clone to local directory (replace with actual GitHub URL)
git clone https://github.com/RycnCDL/sentinel-mcp-server.git
cd sentinel-mcp-server
```

### 1.2 Install Python Dependencies
```powershell
# Option 1: Install globally (einfacher für Tests)
python -m pip install -r requirements.txt

# Option 2: Mit Virtual Environment (empfohlen für Production)
# python -m venv venv
# .\venv\Scripts\Activate.ps1
# pip install -r requirements.txt
```

### 1.3 Download SentinelManager.ps1
```powershell
# Download SentinelManager.ps1 to a known location
# Example: C:\Scripts\SentinelManager.ps1
# Update the path in your .env file
```

---

## 🔑 Step 2: Configure Environment Variables

### 2.1 Create `.env` File
```powershell
# Copy example .env
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

### 2.2 Set Required Variables
```env
# Azure Authentication (REQUIRED)
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

# PowerShell Configuration (REQUIRED)
POWERSHELL_SCRIPT_PATH=C:\Scripts\SentinelManager.ps1

# Server Settings (OPTIONAL - defaults shown)
MCP_SERVER_NAME=sentinel-mcp-server
MCP_SERVER_VERSION=1.0.0
LOG_LEVEL=INFO
DEBUG_MODE=false
```

**How to get Azure credentials:**
1. Go to Azure Portal → Azure Active Directory → App Registrations
2. Create new registration or use existing
3. Copy: Application (client) ID, Directory (tenant) ID
4. Create client secret: Certificates & secrets → New client secret
5. Grant permissions: Microsoft Graph API, Azure Resource Manager

---

## 🖥️ Step 3: Configure Claude Desktop

### 3.1 Locate Claude Desktop Config File

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 3.2 Add MCP Server Configuration

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "src"
      ],
      "cwd": "C:\\Path\\To\\sentinel-mcp-server",
      "env": {
        "AZURE_TENANT_ID": "your-tenant-id",
        "AZURE_CLIENT_ID": "your-client-id",
        "AZURE_CLIENT_SECRET": "your-client-secret",
        "POWERSHELL_SCRIPT_PATH": "C:\\Scripts\\SentinelManager.ps1"
      }
    }
  }
}
```

**Important Notes:**
- Replace `C:\\Path\\To\\sentinel-mcp-server` with actual path (use double backslashes)
- Replace environment variable values with your actual credentials
- Ensure paths use double backslashes (`\\`) on Windows

### 3.3 Restart Claude Desktop
Close and reopen Claude Desktop to load the new configuration.

---

## 🧪 Step 4: Test MCP Server

### 4.1 Verify Server Connection

In Claude Desktop, try:
```
Can you list your available tools?
```

Expected response should include:
- `sentinel_health_check` (Python tool)
- 40+ PowerShell tools (e.g., `Get-SentinelTables`, `Get-AnalyticsRules`, etc.)

### 4.2 Test Health Check Tool

```
Check the health of all my Sentinel workspaces
```

Expected response:
- Summary of all workspaces
- Data connector counts
- Analytics rule counts
- Overall health status

### 4.3 Test PowerShell Tools

**List Analytics Rules:**
```
List all analytics rules in my Sentinel workspace
```

**Show Disabled Rules:**
```
Show me all disabled analytics rules
```

**Get Workspaces:**
```
Get all my Sentinel workspaces
```

**Export Rules:**
```
Export all analytics rules to a backup folder
```

### 4.4 Test Error Handling

Try invalid commands to verify error handling:
```
Get analytics rules for workspace that doesn't exist
```

Expected: Graceful error message, not a crash

---

## 🐛 Step 5: Troubleshooting

### Common Issues

#### Issue: "MCP server not found"
**Solution:**
- Check `claude_desktop_config.json` syntax (valid JSON)
- Verify `cwd` path points to repository root
- Restart Claude Desktop

#### Issue: "Authentication failed"
**Solution:**
- Verify Azure credentials in `.env` or `claude_desktop_config.json`
- Check Service Principal has Sentinel Reader/Contributor role
- Test credentials with Azure CLI: `az login --service-principal`

#### Issue: "PowerShell script not found"
**Solution:**
- Verify `POWERSHELL_SCRIPT_PATH` in environment variables
- Check file exists at specified path
- Ensure path uses double backslashes on Windows

#### Issue: "Module not found" errors
**Solution:**
- Install dependencies: `python -m pip install -r requirements.txt`
- Verify Python version: `python --version` (must be 3.10+)
- If using venv: Activate with `.\venv\Scripts\Activate.ps1` (falls erstellt)

#### Issue: "PowerShell execution failed"
**Solution:**
- Verify PowerShell 7+ installed: `pwsh --version`
- Check PowerShell execution policy: `Get-ExecutionPolicy`
- Install Az modules: `Install-Module -Name Az.Accounts, Az.SecurityInsights`

### Debug Mode

Enable debug logging in `.env`:
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Check logs for detailed error messages.

---

## 📊 Step 6: Validation Checklist

After testing, verify:

- [ ] **Server Connection**: Claude Desktop shows MCP server as connected
- [ ] **Tool Discovery**: All 41 tools appear in tool list
- [ ] **Health Check**: `sentinel_health_check` returns workspace data
- [ ] **PowerShell Execution**: PowerShell tools execute successfully
- [ ] **Error Handling**: Invalid requests return error messages (not crashes)
- [ ] **Authentication**: Azure credentials work correctly
- [ ] **Logging**: Structured logs appear in console/file

---

## 🎉 Success Criteria

**You're ready for production if:**

✅ All 41 tools are accessible  
✅ Health check returns accurate data  
✅ PowerShell tools execute without errors  
✅ Error messages are clear and actionable  
✅ Response times are acceptable (<3 seconds)  
✅ No crashes or unexpected behavior  

---

## 📝 Next Steps After Successful Testing

1. **Production Deployment**:
   - Set up systemd service for auto-start (Linux)
   - Configure Windows Service (Windows)
   - Deploy to Azure Container Instances (optional)

2. **Monitoring**:
   - Integrate Application Insights
   - Set up alerting for errors >5%
   - Monitor response times

3. **Advanced Features**:
   - Implement caching layer
   - Add batch operations
   - Build multi-tenant KQL aggregation

4. **Documentation**:
   - Write blog post 1: "Why MCP for Sentinel?"
   - Create video tutorial
   - Share with community

---

## 🆘 Getting Help

- **Documentation**: See `docs/` folder
- **FAQ**: See `docs/faq.md`
- **Troubleshooting**: See `docs/troubleshooting.md`
- **Issues**: Create issue on GitHub

---

**Happy Testing! 🚀**

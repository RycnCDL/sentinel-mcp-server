# Windows Troubleshooting Guide

This guide helps resolve common issues when running the Sentinel MCP Server on Windows.

## Server Disconnected / Won't Start

### Problem: "Server disconnected" Error in Claude Desktop

**Symptoms:**
- Server shows as "failed" in Claude Desktop
- Error message: "Server disconnected"
- Server doesn't start or crashes immediately

### Solution: Reinstall Dependencies

The most common cause is corrupted or incompatible Python dependencies, particularly the `cryptography` package.

**Step 1: Open PowerShell or Command Prompt as Administrator**

**Step 2: Navigate to your project directory**
```powershell
cd C:\Users\YourUsername\projects\sentinel-mcp-server
```

**Step 3: Activate your Python environment (if using venv)**
```powershell
# If you have a venv
.\.venv\Scripts\Activate.ps1
```

**Step 4: Reinstall dependencies**
```powershell
# First, uninstall problematic packages
pip uninstall -y cryptography cffi azure-identity

# Then reinstall everything
pip install --no-cache-dir -r requirements.txt

# Or install the full stack fresh
pip install --force-reinstall --no-cache-dir cryptography cffi azure-identity
```

**Step 5: Test the server manually**
```powershell
python -m src
```

You should see the FastMCP ASCII art and "Starting MCP server" message.

**Step 6: Restart Claude Desktop**
- Close Claude Desktop completely
- Reopen and check if the server connects

---

## Common Issues

### 1. Missing Build Tools

**Error:** `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution:**
Install Microsoft C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer
3. Select "Desktop development with C++"
4. Install
5. Restart your terminal
6. Reinstall dependencies: `pip install -r requirements.txt`

---

### 2. Python Version Issues

**Error:** `SyntaxError` or version-related errors

**Solution:**
Ensure you're using Python 3.10 or higher:
```powershell
python --version
```

If not, install Python 3.11 or 3.12 from https://www.python.org/downloads/

---

### 3. PowerShell ExecutionPolicy

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 4. Azure Authentication Issues

**Error:** `DefaultAzureCredential failed to retrieve a token`

**Solution:**
Check your `.env` file:
```bash
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

Or authenticate with Azure CLI:
```powershell
az login
```

---

### 5. Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'fastmcp'`

**Solution:**
```powershell
# Make sure you're in the project directory
cd C:\Users\YourUsername\projects\sentinel-mcp-server

# Install/reinstall all dependencies
pip install -r requirements.txt
```

---

## Claude Desktop Configuration

Ensure your Claude Desktop config is correct:

**Config location:** `%APPDATA%\Claude\claude_desktop_config.json`

**Correct configuration:**
```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "command": "python",
      "args": [
        "C:\\Users\\YourUsername\\projects\\sentinel-mcp-server\\src\\__main__.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\YourUsername\\projects\\sentinel-mcp-server\\src"
      }
    }
  }
}
```

**Important:** Use double backslashes (`\\`) in Windows paths!

---

## Manual Testing

Test the server works before connecting to Claude Desktop:

```powershell
# Activate your environment
.\.venv\Scripts\Activate.ps1

# Test import
python -c "from src.mcp_server.server import mcp; print('Import OK')"

# Test server startup
python -m src
```

You should see:
```
╭──────────────────────────────────────────╮
│        FastMCP 2.13.1                    │
│  🖥  Server name: sentinel-mcp-server     │
╰──────────────────────────────────────────╯
```

Press `Ctrl+C` to stop.

---

## Debug Logging

Enable debug logging in `.env`:
```bash
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Then check logs in Claude Desktop:
1. Open Claude Desktop
2. View → Developer → Developer Tools
3. Check Console tab for errors

---

## Still Having Issues?

1. **Check server logs:**
   - Look in Claude Desktop Developer Tools Console
   - Check for Python tracebacks

2. **Verify environment:**
   ```powershell
   python --version  # Should be 3.10+
   pip list | Select-String "fastmcp|azure|structlog"
   ```

3. **Clean install:**
   ```powershell
   # Remove virtual environment
   Remove-Item -Recurse -Force .venv

   # Create fresh environment
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Report issue:**
   - Include error messages from Claude Desktop console
   - Include output of `pip list`
   - Include Python version: `python --version`
   - Open issue at: https://github.com/RycnCDL/sentinel-mcp-server/issues

---

## Quick Fix Checklist

- [ ] Python 3.10+ installed
- [ ] In correct directory
- [ ] Virtual environment activated (if using)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file configured with Azure credentials
- [ ] Claude Desktop config has correct paths (double backslashes!)
- [ ] Server starts manually: `python -m src`
- [ ] Claude Desktop restarted after config changes

---

## Windows-Specific Tips

1. **Always use double backslashes in JSON config files**
   - ✅ `"C:\\Users\\Name\\project\\file.py"`
   - ❌ `"C:\Users\Name\project\file.py"`

2. **Run as Administrator when installing packages**
   - Right-click PowerShell → "Run as Administrator"

3. **Use raw strings in Python paths**
   - `r"C:\Users\Name\project"`

4. **Check Windows Defender**
   - Sometimes blocks Python executables
   - Add exception for Python and project folder

---

## Contact Support

If none of these solutions work, please:
1. Open an issue: https://github.com/RycnCDL/sentinel-mcp-server/issues
2. Include your operating system version
3. Include error messages from Claude Desktop console
4. Include output of these commands:
   ```powershell
   python --version
   pip --version
   pip list
   ```

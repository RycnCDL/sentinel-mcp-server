# VS Code Agent Instructions - Microsoft Sentinel MCP Server Project

**Project:** Microsoft Sentinel MCP Server with PowerShell Backend Integration
**Current Phase:** Phase 1 Complete ✅ | Starting Phase 2 - PowerShell Integration
**Repository:** RycnCDL/sentinel-mcp-server
**Date:** November 20, 2025

---

## 📋 Project Context

### What This Project Is

A **hybrid MCP (Model Context Protocol) Server** that combines:
1. **Microsoft's Official Sentinel MCP** - For standard Sentinel features
2. **Custom MCP Server** - For PowerShell-based custom SOC workflows

**Goal:** Enable AI assistants (Claude, Copilot) to interact with Microsoft Sentinel using natural language, with additional custom PowerShell automation tools.

---

## ✅ Current Status - Phase 1 COMPLETE

### What Works (Already Implemented & Tested)

✅ **Authentication System** (`src/utils/auth.py`)
- Service Principal authentication
- Azure CLI fallback (WORKING)
- Managed Identity support
- ChainedTokenCredential

✅ **Sentinel Health Check Tool** (`src/mcp_server/tools/management/health_check.py`)
- Successfully tested on real Sentinel workspace: `PC-SentinelDemo-LAW`
- Detects analytics rules: **16 rules found (11 enabled, 5 disabled)**
- Data connector monitoring
- Health status calculation

✅ **Lighthouse Manager** (`src/utils/lighthouse.py`)
- Multi-tenant workspace enumeration
- Workspace discovery and validation

✅ **Configuration Management** (`src/utils/config.py`)
- Environment-based configuration
- Pydantic models for type safety

✅ **Comprehensive Test Suite**
- 8 diagnostic and test scripts
- Works with Azure CLI authentication

### Known Issues

⚠️ **Service Principal API Access (403 Forbidden)**
- Service Principal with Client Credentials gets 403 on all Azure APIs
- Root cause: Azure AD tenant-level policy/configuration
- **Workaround:** Use Azure CLI authentication (`test_with_cli_auth.py`) - WORKS PERFECTLY
- Not a code issue - tenant security configuration

---

## 🎯 Phase 2 Objective - PowerShell Integration

### Goal

Integrate existing PowerShell automation tools from **RycnCDL/Sentinel-Tools** repository into the MCP Server.

### Architecture

```
VS Code / Claude Desktop
    │
    ├─→ Microsoft Sentinel MCP (Official)
    │   └─→ Standard Sentinel operations
    │
    └─→ Custom MCP Server (Our Code)
        └─→ Python-PowerShell Bridge
            └─→ SentinelManager PowerShell Scripts
                └─→ Custom SOC workflows
```

### What Needs to Be Built

1. **PowerShell Bridge Module** (`src/utils/powershell_bridge.py`)
   - Execute PowerShell scripts from Python
   - Support local and remote execution
   - Handle JSON serialization
   - Error handling

2. **MCP Tool Wrappers** (`src/mcp_server/tools/powershell/`)
   - Wrap each PowerShell function as MCP tool
   - Define JSON schemas for parameters
   - Integration with authentication

3. **Remote Execution Support**
   - PSRemoting configuration
   - Secure credential handling
   - Network communication

---

## 📁 Important Files & Their Purpose

### Core Implementation Files

```
src/
├── utils/
│   ├── auth.py              ✅ Authentication framework (COMPLETE)
│   ├── lighthouse.py        ✅ Multi-tenant management (COMPLETE)
│   ├── config.py            ✅ Configuration management (COMPLETE)
│   ├── logging.py           ✅ Structured logging (COMPLETE)
│   └── powershell_bridge.py ⏳ TO BUILD - Python-PowerShell bridge
│
├── mcp_server/
│   ├── server.py            ✅ MCP server core (COMPLETE)
│   └── tools/
│       ├── management/
│       │   └── health_check.py  ✅ Health check tool (WORKING)
│       └── powershell/      ⏳ TO BUILD - PowerShell tool wrappers
│           └── sentinel_manager.py
│
└── tests/                   ✅ Test framework (COMPLETE)
```

### Configuration Files

```
.env                         # Local config (gitignored)
.env.template               # Template for .env
requirements.txt            # Python dependencies
requirements-dev.txt        # Development dependencies
```

### Documentation

```
README.md                            # Main documentation
PHASE-1-COMPLETION.md               ✅ Phase 1 summary
PHASE-2-POWERSHELL-INTEGRATION.md   ⏳ Phase 2 plan
PROJECT.md                          # Original project plan
SETUP-GUIDE.md                      # Setup instructions
```

### Test Scripts

```
scripts/
├── test_auth.py                    ✅ Authentication test
├── test_with_cli_auth.py          ✅ Working CLI auth test
├── test_direct_workspace.py       ✅ Direct workspace test
└── test_*.py                       # Various diagnostic scripts
```

---

## 🔧 Technical Stack

### Python Dependencies
```python
fastmcp                 # MCP framework
azure-identity          # Azure authentication
azure-mgmt-*           # Azure management SDKs
structlog              # Structured logging
pydantic               # Configuration validation
asyncio                # Async operations
```

### PowerShell Requirements (For Phase 2)
```powershell
PowerShell 7+
Az modules
Microsoft.Graph modules
Custom SentinelManager module (from RycnCDL/Sentinel-Tools)
```

---

## 🚀 Next Steps for Phase 2

### Step 1: Access Sentinel-Tools Repository

**Action Required:**
User has PowerShell automation in `RycnCDL/Sentinel-Tools` repository.
Need to analyze the PowerShell functions to understand what to integrate.

**What to Ask User:**
1. What are the main PowerShell functions in SentinelManager?
2. What parameters do they expect?
3. Should execution be local or remote?
4. What are typical use cases?

### Step 2: Build PowerShell Bridge

**File to Create:** `src/utils/powershell_bridge.py`

**Key Features:**
```python
class PowerShellBridge:
    async def execute_script(
        script_path: str,
        function: str,
        params: dict,
        remote: bool = False
    ) -> dict:
        """Execute PowerShell function and return results"""
        pass
```

**Requirements:**
- Use `subprocess` for local execution
- Use `pypsrp` or `winrm` for remote execution
- Handle JSON serialization
- Proper error handling
- Logging integration

### Step 3: Create MCP Tool Wrappers

**File to Create:** `src/mcp_server/tools/powershell/sentinel_manager.py`

**Pattern:**
```python
from mcp.server import Server
from mcp.types import Tool

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="sentinel_bulk_update",
            description="Bulk update analytics rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace": {"type": "string"},
                    "updates": {"type": "object"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "sentinel_bulk_update":
        # Call PowerShell bridge
        bridge = PowerShellBridge()
        result = await bridge.execute_script(...)
        return result
```

### Step 4: Testing

**Test Approach:**
1. Test PowerShell execution locally first
2. Test with simple functions before complex ones
3. Test remote execution separately
4. Integration test with MCP server
5. Test with Claude Desktop / VS Code

---

## 🔐 Security Considerations

### Authentication
- ✅ Already implemented Azure AD authentication
- ⏳ Need to add PowerShell credential handling
- Use Azure Key Vault for secrets (recommended)
- No hardcoded credentials

### Remote Execution
- Use WinRM over HTTPS
- Certificate-based authentication preferred
- Audit all remote executions
- Rate limiting

### Input Validation
- Validate all user inputs
- Sanitize parameters before PowerShell execution
- Prevent command injection
- Log all operations

---

## 💻 Development Workflow

### Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/RycnCDL/sentinel-mcp-server.git
cd sentinel-mcp-server

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configure .env
cp .env.template .env
# Edit .env with your credentials

# 5. Test authentication
python scripts/test_with_cli_auth.py  # This WORKS
```

### Testing Workflow

```bash
# Run authentication test
python scripts/test_auth.py

# Run health check with CLI auth (WORKING)
python scripts/test_with_cli_auth.py

# Run full server test
python scripts/test_server.py

# Run specific diagnostic
python scripts/diagnose_workspace_access.py
```

### Git Workflow

```bash
# Current branch
git checkout claude/review-mcp-server-project-01QUEkrgL2GxFjX3XZcjNu6Z

# Make changes, then commit
git add .
git commit -m "Descriptive message"
git push -u origin claude/review-mcp-server-project-01QUEkrgL2GxFjX3XZcjNu6Z
```

---

## 📝 Code Conventions

### Python Style
- Follow PEP 8
- Use type hints
- Async/await for I/O operations
- Structured logging with structlog
- Comprehensive error handling

### Naming Conventions
```python
# Classes: PascalCase
class PowerShellBridge:

# Functions: snake_case
async def execute_script():

# Constants: UPPER_CASE
MAX_RETRIES = 3

# Private methods: _leading_underscore
def _internal_method():
```

### Logging Pattern
```python
logger.info("Operation started", workspace=ws_name, action="health_check")
logger.error("Operation failed", error=str(e), workspace=ws_name)
```

---

## 🎓 Important Context for AI Assistant

### What to Remember

1. **Phase 1 is COMPLETE and WORKING**
   - Don't rebuild authentication
   - Don't rebuild health check
   - Don't fix Service Principal issue (it's external)

2. **Focus on Phase 2: PowerShell Integration**
   - Build on existing foundation
   - New code goes in `src/utils/powershell_bridge.py`
   - New tools go in `src/mcp_server/tools/powershell/`

3. **User's Environment**
   - Has access to RycnCDL/Sentinel-Tools (PowerShell scripts)
   - Wants both local AND remote execution
   - Already tested Microsoft's official Sentinel MCP
   - Wants hybrid approach

4. **Authentication Works**
   - Azure CLI authentication is WORKING (`test_with_cli_auth.py`)
   - Use this for testing
   - Service Principal 403 issue is documented, not urgent

### What NOT to Do

❌ Don't try to "fix" the Service Principal 403 issue - it's a tenant config
❌ Don't rebuild Phase 1 components - they work
❌ Don't suggest alternative MCP frameworks - FastMCP is chosen
❌ Don't suggest rewriting in another language

### What TO Do

✅ Ask about PowerShell functions before implementing
✅ Build incrementally and test each component
✅ Use existing auth/logging/config patterns
✅ Follow the architecture in PHASE-2-POWERSHELL-INTEGRATION.md
✅ Write tests for new components

---

## 🔍 Quick Reference

### Test a Single Component
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from utils.auth import get_authenticator
# Test code here
"
```

### Check Logs
```bash
# Logs are output to stdout with structlog
# JSON format for parsing, text format for humans
```

### Workspace Details (For Testing)
```
Workspace: PC-SentinelDemo-LAW
Resource Group: pc-sentineldemo-rg
Subscription: f0519492-d4b0-40e3-930d-be49cdc3e624
Tenant: 1126248f-0b1d-43e8-a801-d48393b8d061
```

---

## 📞 When to Ask User

Ask the user when you need:
1. PowerShell function details from Sentinel-Tools repo
2. Specific use cases for tool implementation
3. Remote execution server details
4. Testing credentials or access
5. Clarification on requirements

---

## 🎯 Success Criteria for Phase 2

### Minimum Viable Product (MVP)
- [ ] PowerShell bridge executes local scripts
- [ ] At least 3 PowerShell functions wrapped as MCP tools
- [ ] Successfully tested with Claude Desktop or VS Code
- [ ] Documentation for new tools
- [ ] Integration tests passing

### Stretch Goals
- [ ] Remote execution working
- [ ] All PowerShell functions wrapped
- [ ] Performance optimization
- [ ] Comprehensive error handling
- [ ] Production deployment guide

---

## 📚 Additional Resources

### Documentation Links
- FastMCP: https://github.com/jlowin/fastmcp
- Model Context Protocol: https://modelcontextprotocol.io
- Microsoft Sentinel MCP: https://learn.microsoft.com/azure/sentinel/datalake/sentinel-mcp-overview
- Azure SDK for Python: https://learn.microsoft.com/python/api/overview/azure/

### Repository Links
- Main Project: github.com/RycnCDL/sentinel-mcp-server
- PowerShell Tools: github.com/RycnCDL/Sentinel-Tools (private)

---

## 🚦 Getting Started Checklist

When continuing work in VS Code:

- [ ] Review PHASE-1-COMPLETION.md (understand what's done)
- [ ] Review PHASE-2-POWERSHELL-INTEGRATION.md (understand what's next)
- [ ] Check git branch: `claude/review-mcp-server-project-01QUEkrgL2GxFjX3XZcjNu6Z`
- [ ] Ensure virtual environment is activated
- [ ] Test that `python scripts/test_with_cli_auth.py` still works
- [ ] Ask user for PowerShell function details
- [ ] Start with PowerShell bridge implementation
- [ ] Test incrementally

---

**Remember:** Phase 1 is COMPLETE and WORKING. Focus on Phase 2: PowerShell Integration!

*Last Updated: November 20, 2025*
*Version: 1.0*

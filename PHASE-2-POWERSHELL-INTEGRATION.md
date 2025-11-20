# Phase 2 - PowerShell Backend Integration Plan

**Goal:** Integrate existing PowerShell SentinelManager tools into MCP Server
**Strategy:** Hybrid approach - Microsoft Sentinel MCP + Custom PowerShell Tools
**Status:** Planning

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop / VS Code                  │
│                                                              │
│  ┌──────────────────┐              ┌───────────────────┐    │
│  │  Microsoft       │              │  Custom MCP       │    │
│  │  Sentinel MCP    │              │  Server           │    │
│  │  (Official)      │              │  (Our Code)       │    │
│  └──────────────────┘              └───────────────────┘    │
│         │                                    │               │
│         │ Standard Sentinel Features        │               │
│         │ - Incidents                        │               │
│         │ - Analytics Rules                  │               │
│         │ - Data Connectors                  │               │
│         │ - KQL Queries                      │               │
│         │                                    │               │
│         │                          ┌─────────▼──────────┐    │
│         │                          │  Python-PowerShell │    │
│         │                          │  Bridge            │    │
│         │                          └─────────┬──────────┘    │
│         │                                    │               │
│         │                          ┌─────────▼──────────┐    │
│         │                          │  PowerShell        │    │
│         │                          │  SentinelManager   │    │
│         │                          │  (RycnCDL/         │    │
│         │                          │   Sentinel-Tools)  │    │
│         │                          └────────────────────┘    │
│         │                                    │               │
│         │                          Custom SOC Functions:     │
│         │                          - Multi-tenant ops       │
│         │                          - Bulk operations         │
│         │                          - Custom workflows        │
│         │                          - Advanced automation     │
│         └────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Implementation Components

### 1. PowerShell Bridge Module

**File:** `src/utils/powershell_bridge.py`

**Purpose:**
- Execute PowerShell scripts from Python
- Handle parameter passing
- Parse PowerShell output (JSON, objects)
- Error handling and logging
- Remote execution support

**Features:**
```python
class PowerShellBridge:
    """Bridge between Python MCP Server and PowerShell scripts"""

    async def execute_script(
        self,
        script_path: str,
        function: str,
        params: dict,
        remote: bool = False
    ) -> dict:
        """Execute PowerShell function and return results"""
        pass

    async def execute_remote(
        self,
        host: str,
        script_path: str,
        function: str,
        params: dict
    ) -> dict:
        """Execute PowerShell on remote system"""
        pass
```

### 2. MCP Tools for PowerShell Functions

**File:** `src/mcp_server/tools/powershell/sentinel_manager.py`

**Purpose:**
- Wrap each PowerShell function as MCP Tool
- Provide JSON schema for parameters
- Handle authentication
- Return structured results

**Example Tool:**
```python
@mcp_tool(
    name="sentinel_bulk_update",
    description="Bulk update Sentinel analytics rules using PowerShell backend"
)
async def bulk_update_analytics_rules(
    workspace: str,
    rule_filter: str,
    updates: dict
) -> dict:
    """
    Update multiple analytics rules in bulk

    Args:
        workspace: Sentinel workspace name
        rule_filter: Filter for rules to update
        updates: Dictionary of updates to apply

    Returns:
        Results of bulk update operation
    """
    bridge = PowerShellBridge()
    result = await bridge.execute_script(
        script_path="SentinelManager.ps1",
        function="Update-AnalyticsRuleBulk",
        params={
            "Workspace": workspace,
            "Filter": rule_filter,
            "Updates": updates
        }
    )
    return result
```

### 3. Configuration

**Add to `.env`:**
```ini
# PowerShell Backend Configuration
# ==================================
# Local PowerShell execution
POWERSHELL_SCRIPTS_PATH=/path/to/Sentinel-Tools

# Remote PowerShell execution
POWERSHELL_REMOTE_HOST=your-server.domain.com
POWERSHELL_REMOTE_USER=your-username
POWERSHELL_USE_REMOTE=false

# PowerShell Modules
POWERSHELL_MODULES_PATH=/path/to/modules
```

---

## 📋 Integration Steps

### Step 1: Analyze SentinelManager Functions
- [ ] Clone RycnCDL/Sentinel-Tools repository
- [ ] Document all available functions
- [ ] Identify function parameters and return types
- [ ] Map to MCP tool requirements

### Step 2: Build PowerShell Bridge
- [ ] Implement `PowerShellBridge` class
- [ ] Support local execution
- [ ] Support remote execution (PSRemoting)
- [ ] Handle JSON serialization
- [ ] Implement error handling

### Step 3: Create MCP Tools
- [ ] Wrap each PowerShell function as MCP tool
- [ ] Define JSON schemas for parameters
- [ ] Add validation and error handling
- [ ] Write unit tests

### Step 4: Testing
- [ ] Test local PowerShell execution
- [ ] Test remote PowerShell execution
- [ ] Test with Claude Desktop
- [ ] Test with VS Code MCP
- [ ] Integration tests with Microsoft Sentinel MCP

### Step 5: Documentation
- [ ] API documentation for each tool
- [ ] Setup guide for PowerShell backend
- [ ] Troubleshooting guide
- [ ] Example workflows

---

## 🔐 Security Considerations

### Authentication
- Use Azure AD authentication for PowerShell
- Secure credential storage (Azure Key Vault)
- No hardcoded passwords

### Remote Execution
- Use WinRM over HTTPS
- Certificate-based authentication
- Restrict to specific hosts
- Audit logging

### Input Validation
- Validate all parameters
- Sanitize inputs to prevent injection
- Rate limiting
- Authorization checks

---

## 📊 Example Use Cases

### Use Case 1: Bulk Analytics Rules Update
```
User: "Update all analytics rules in workspace PC-SentinelDemo-LAW
       to use severity 'High' where they currently use 'Medium'"

MCP Server:
1. Parse natural language intent
2. Call PowerShell function: Update-AnalyticsRuleBulk
3. Execute on remote PowerShell host
4. Return results in structured format
```

### Use Case 2: Multi-Tenant Health Check
```
User: "Check health of all Sentinel workspaces in my tenant"

MCP Server:
1. Use Microsoft Sentinel MCP for standard checks
2. Use PowerShell backend for custom health metrics
3. Aggregate results from both sources
4. Present unified report
```

### Use Case 3: Custom Workflow Automation
```
User: "When a new incident is created with severity Critical,
       automatically assign to SOC lead and create Teams alert"

MCP Server:
1. Monitor incidents via Microsoft Sentinel MCP
2. Trigger PowerShell workflow on new critical incident
3. Execute custom assignment logic
4. Send Teams notification via PowerShell
```

---

## 🚀 Next Steps

1. **Immediate:**
   - Access RycnCDL/Sentinel-Tools repository
   - Document all PowerShell functions
   - Create function inventory

2. **Week 1:**
   - Implement PowerShell Bridge
   - Create first MCP tool wrapper
   - Test basic execution

3. **Week 2:**
   - Wrap all critical functions
   - Add remote execution support
   - Integration testing

4. **Week 3:**
   - Documentation
   - Performance optimization
   - Production deployment

---

## 📚 Technical Requirements

### Python Dependencies
```
- asyncio (built-in)
- subprocess (built-in)
- json (built-in)
- pypsrp (for remote PowerShell)
- winrm (for Windows Remote Management)
```

### PowerShell Requirements
```
- PowerShell 7+ recommended
- Az PowerShell modules
- Microsoft.Graph modules (if needed)
- Custom SentinelManager module
```

### System Requirements
```
- Windows, Linux, or macOS (PowerShell Core)
- Network access to Azure
- PSRemoting configured (for remote execution)
```

---

*Document Version: 1.0*
*Created: November 20, 2025*
*Status: Planning Phase*

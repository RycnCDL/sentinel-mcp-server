# End-to-End Testing Checklist

## 📋 Testing Overview

This checklist ensures comprehensive validation of the Microsoft Sentinel MCP Server before production deployment.

**Testing Date**: _____________  
**Tester**: _____________  
**Environment**: Dev / Staging / Production (circle one)

---

## ✅ Pre-Testing Setup

### Environment Configuration
- [ ] Python 3.10+ installed and verified (`python --version`)
- [ ] PowerShell 7+ installed and verified (`pwsh --version`)
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] Azure credentials configured in `.env`
- [ ] PowerShell script path set correctly
- [ ] SentinelManager.ps1 downloaded and accessible

### Azure Prerequisites
- [ ] Service Principal created with required permissions
- [ ] Sentinel Reader/Contributor role assigned
- [ ] Access to at least one Sentinel workspace verified
- [ ] Azure Lighthouse configured (if multi-tenant)
- [ ] Test credentials verified with Azure CLI

### MCP Client Setup
- [ ] Claude Desktop installed (or other MCP client)
- [ ] MCP server configuration added to `claude_desktop_config.json`
- [ ] Configuration paths use proper escaping (double backslashes on Windows)
- [ ] Claude Desktop restarted after configuration

---

## 🔌 Server Startup Tests

### Basic Startup
- [ ] Server starts without errors: `python -m src`
- [ ] Logs show "Starting Microsoft Sentinel MCP Server"
- [ ] No Python import errors
- [ ] No configuration validation errors
- [ ] Server listens for MCP connections

### Component Initialization
- [ ] PowerShell bridge initialized successfully
- [ ] Authenticator created (or lazy-loaded on first use)
- [ ] Lighthouse manager initialized (if configured)
- [ ] All 41 tools registered (1 Python + 40 PowerShell)

**Notes:**
```
_______________________________________________________________________
_______________________________________________________________________
```

---

## 🔍 Python Tool Tests

### sentinel_health_check (Quick Mode)
**Command in Claude Desktop:**
```
Check the health of all my Sentinel workspaces (quick check)
```

**Expected Results:**
- [ ] No errors or exceptions
- [ ] Returns JSON with `summary` and `workspaces` keys
- [ ] Summary includes: `workspaces_checked`, `overall_status`
- [ ] Each workspace has: name, resource_id, data_connectors, analytics_rules
- [ ] Response time < 10 seconds

**Actual Results:**
```
_______________________________________________________________________
_______________________________________________________________________
```

### sentinel_health_check (Detailed Mode)
**Command in Claude Desktop:**
```
Check the health of all my Sentinel workspaces with detailed metrics
```

**Expected Results:**
- [ ] Includes all quick mode data
- [ ] Additional ingestion metrics (if available)
- [ ] Response time < 30 seconds

**Actual Results:**
```
_______________________________________________________________________
_______________________________________________________________________
```

### sentinel_health_check (Tenant Filtering)
**Command in Claude Desktop:**
```
Check health of Customer A Sentinel workspaces
```

**Expected Results:**
- [ ] Only workspaces for specified tenant returned
- [ ] Correct filtering applied
- [ ] No errors for invalid tenant names (graceful handling)

**Actual Results:**
```
_______________________________________________________________________
_______________________________________________________________________
```

---

## ⚙️ PowerShell Tool Tests

### Table Management

#### Get-SentinelTables
**Command:**
```
List all tables in my Sentinel workspace
```

**Expected Results:**
- [ ] Returns list of tables with names and properties
- [ ] No PowerShell execution errors
- [ ] Response time < 5 seconds

**Actual Results:**
```
_______________________________________________________________________
```

#### View-TableRetention
**Command:**
```
Show me the retention settings for all tables
```

**Expected Results:**
- [ ] Returns table retention data
- [ ] Correctly parses PowerShell JSON output
- [ ] No JSON serialization errors

**Actual Results:**
```
_______________________________________________________________________
```

### Analytics Rules

#### Get-AnalyticsRules
**Command:**
```
List all analytics rules in my workspace
```

**Expected Results:**
- [ ] Returns list of analytics rules
- [ ] Includes rule names, enabled status, severity
- [ ] Response time < 10 seconds

**Actual Results:**
```
_______________________________________________________________________
```

#### Get-AnalyticsRuleDetails
**Command:**
```
Show me details for analytics rule "Suspicious Login Activity"
```

**Expected Results:**
- [ ] Returns detailed rule information
- [ ] Includes query, tactics, techniques
- [ ] Correct parameter passing (rule name)

**Actual Results:**
```
_______________________________________________________________________
```

#### Enable-AnalyticsRule / Disable-AnalyticsRule
**Command:**
```
Disable the analytics rule "Test Rule"
```

**Expected Results:**
- [ ] Rule successfully disabled
- [ ] Confirmation message returned
- [ ] No state corruption

**Verification Command:**
```
Get rule status for "Test Rule"
```

**Actual Results:**
```
_______________________________________________________________________
```

### Workbooks

#### Get-SentinelWorkbooks
**Command:**
```
List all workbooks in my Sentinel workspace
```

**Expected Results:**
- [ ] Returns workbook list with names
- [ ] No errors
- [ ] Response time < 5 seconds

**Actual Results:**
```
_______________________________________________________________________
```

#### Export-SentinelWorkbook
**Command:**
```
Export the "Security Overview" workbook
```

**Expected Results:**
- [ ] Workbook exported successfully
- [ ] JSON output valid
- [ ] Can be re-imported later

**Actual Results:**
```
_______________________________________________________________________
```

### Incidents

#### Get-SentinelIncidents
**Command:**
```
List all open incidents from the last 7 days
```

**Expected Results:**
- [ ] Returns incident list
- [ ] Correct filtering (open, 7 days)
- [ ] Includes incident numbers, titles, severity

**Actual Results:**
```
_______________________________________________________________________
```

#### Show-IncidentDetails
**Command:**
```
Show details for incident #12345
```

**Expected Results:**
- [ ] Returns detailed incident information
- [ ] Includes entities, alerts, comments
- [ ] No errors for invalid incident numbers (graceful handling)

**Actual Results:**
```
_______________________________________________________________________
```

### Backup & Export

#### Export-AnalyticsRules
**Command:**
```
Export all analytics rules to backup folder
```

**Expected Results:**
- [ ] All rules exported
- [ ] Files created in specified folder
- [ ] JSON format valid

**Actual Results:**
```
_______________________________________________________________________
```

### DCR/DCE Management

#### Get-DataCollectionRules
**Command:**
```
List all data collection rules
```

**Expected Results:**
- [ ] Returns DCR list
- [ ] No errors
- [ ] Response time < 10 seconds

**Actual Results:**
```
_______________________________________________________________________
```

---

## 🚨 Error Handling Tests

### Invalid Credentials
**Test:**
- [ ] Temporarily set invalid Azure credentials in `.env`
- [ ] Restart server
- [ ] Attempt health check

**Expected Results:**
- [ ] Clear authentication error message
- [ ] No stack traces exposed to user
- [ ] Server doesn't crash

**Actual Results:**
```
_______________________________________________________________________
```

### Missing PowerShell Script
**Test:**
- [ ] Set `POWERSHELL_SCRIPT_PATH` to non-existent file
- [ ] Attempt PowerShell tool call

**Expected Results:**
- [ ] Clear "script not found" error
- [ ] No PowerShell crash
- [ ] Server remains operational

**Actual Results:**
```
_______________________________________________________________________
```

### Invalid Parameters
**Test:**
- [ ] Call PowerShell tool with invalid parameters
- [ ] Example: `Get-AnalyticsRuleDetails` with non-existent rule name

**Expected Results:**
- [ ] Graceful error handling
- [ ] Helpful error message
- [ ] No server crash

**Actual Results:**
```
_______________________________________________________________________
```

### Timeout Handling
**Test:**
- [ ] Call long-running operation
- [ ] Observe timeout behavior (if > 300s)

**Expected Results:**
- [ ] Operation times out gracefully
- [ ] Timeout error message returned
- [ ] Server remains responsive

**Actual Results:**
```
_______________________________________________________________________
```

### Retry Logic
**Test:**
- [ ] Simulate transient failure (network issue)
- [ ] Observe retry behavior

**Expected Results:**
- [ ] 3 retry attempts with exponential backoff (1s, 2s, 4s)
- [ ] Success on retry (if transient)
- [ ] Final failure after 3 retries (if persistent)
- [ ] Logs show retry attempts

**Actual Results:**
```
_______________________________________________________________________
```

---

## 🔐 Security Tests

### Credential Handling
- [ ] `.env` file not committed to git
- [ ] No credentials in logs (even in DEBUG mode)
- [ ] Sensitive data masked in error messages
- [ ] Service Principal has minimum required permissions

### Multi-Tenant Isolation
- [ ] Can access only authorized tenants
- [ ] Cross-tenant data leakage prevented
- [ ] Lighthouse permissions respected

**Notes:**
```
_______________________________________________________________________
```

---

## ⚡ Performance Tests

### Response Times
- [ ] Health check (quick): < 10s
- [ ] Health check (detailed): < 30s
- [ ] Get-AnalyticsRules: < 10s
- [ ] Get-SentinelTables: < 5s
- [ ] Export operations: < 60s

**Measured Times:**
```
Health check (quick):    _____ seconds
Health check (detailed): _____ seconds
Get-AnalyticsRules:      _____ seconds
Get-SentinelTables:      _____ seconds
```

### Concurrent Requests
**Test:**
- [ ] Send 5 simultaneous tool calls
- [ ] Observe response times and errors

**Expected Results:**
- [ ] All requests complete successfully
- [ ] No deadlocks or race conditions
- [ ] Reasonable response time degradation

**Actual Results:**
```
_______________________________________________________________________
```

### Memory Usage
**Test:**
- [ ] Monitor memory usage over 1 hour
- [ ] Execute 50+ tool calls
- [ ] Check for memory leaks

**Expected Results:**
- [ ] Stable memory usage
- [ ] No significant leaks
- [ ] < 500MB memory footprint

**Actual Results:**
```
Start memory:  _____ MB
End memory:    _____ MB
Peak memory:   _____ MB
```

---

## 🧪 Integration Tests

### Claude Desktop Integration
- [ ] Server appears in Claude Desktop tools list
- [ ] All 41 tools visible and accessible
- [ ] Natural language queries work correctly
- [ ] Multi-step workflows execute properly

**Example Workflow Test:**
```
1. "Check health of all workspaces"
2. "Show me disabled analytics rules"
3. "Enable all disabled rules"
4. "Verify all rules are now enabled"
```

**Results:**
```
_______________________________________________________________________
_______________________________________________________________________
```

### VS Code Integration (if applicable)
- [ ] MCP server connects successfully
- [ ] Tools accessible via VS Code interface
- [ ] No conflicts with other extensions

---

## 📊 Test Summary

### Overall Results

**Total Tests**: _____  
**Passed**: _____  
**Failed**: _____  
**Skipped**: _____  

**Pass Rate**: _____% (Target: >95%)

### Critical Issues Found
```
Issue #1: ___________________________________________________________
Severity: Critical / High / Medium / Low
Status: Open / Fixed / Workaround

Issue #2: ___________________________________________________________
Severity: Critical / High / Medium / Low
Status: Open / Fixed / Workaround
```

### Recommendations
```
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

### Sign-Off

**Ready for Production?**: YES / NO / WITH CAVEATS

**Tested By**: _____________  
**Date**: _____________  
**Signature**: _____________

**Approved By**: _____________  
**Date**: _____________  
**Signature**: _____________

---

## 📎 Appendix

### Test Environment Details
```
OS: _________________________________________________________________
Python Version: ______________________________________________________
PowerShell Version: __________________________________________________
Azure Subscription: __________________________________________________
Sentinel Workspaces: _________________________________________________
Claude Desktop Version: ______________________________________________
```

### Known Limitations
```
_______________________________________________________________________
_______________________________________________________________________
```

### Future Test Improvements
```
_______________________________________________________________________
_______________________________________________________________________
```

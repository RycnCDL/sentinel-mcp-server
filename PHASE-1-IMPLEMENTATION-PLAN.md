# Phase 1 Implementation Plan - MVP

**Project:** Microsoft Sentinel MCP Server  
**Phase:** 1 - Foundation (MVP)  
**Timeline:** 2-3 Weeks  
**Status:** 🚀 Ready to Start  
**Date:** 2025-11-19

---

## 🎯 Phase 1 Goals

Build a working MCP server with 3 foundation tools that demonstrate:
- ✅ Hybrid architecture (Microsoft MCP + Custom Server)
- ✅ Multi-tenant capabilities via Azure Lighthouse
- ✅ PowerShell backend integration
- ✅ Real value for SOC team
- ✅ Foundation for future tools

---

## 🔧 Phase 1 Tools

### Tool #1: `sentinel_health_check` 
**Priority:** HIGH  
**Complexity:** Low-Medium  
**Impact:** Immediate visibility across tenants

**What it does:**
- Checks health status of Sentinel workspaces
- Validates data connectors are ingesting
- Checks analytics rules are enabled
- Verifies data retention settings
- Returns structured health report

**Technical Requirements:**
- Azure Management API calls
- KQL queries for ingestion checks
- Multi-tenant workspace enumeration via Lighthouse
- Error handling for permission issues

**Inputs:**
- Tenant scope (all/specific)
- Check depth (quick/detailed)

**Outputs:**
```json
{
  "timestamp": "2025-11-19T10:00:00Z",
  "tenants_checked": 10,
  "overall_status": "healthy",
  "workspaces": [
    {
      "workspace_id": "xxx",
      "tenant_name": "Customer A",
      "status": "healthy",
      "issues": [],
      "metrics": {
        "data_connectors_active": 15,
        "analytics_rules_enabled": 45,
        "ingestion_last_24h_gb": 12.5
      }
    }
  ]
}
```

---

### Tool #2: `data_connector_status`
**Priority:** HIGH  
**Complexity:** Medium  
**Impact:** Critical for data ingestion monitoring

**What it does:**
- Lists all data connectors across tenants
- Shows last ingestion timestamp
- Identifies broken/stale connectors
- Provides troubleshooting hints
- Aggregates status by connector type

**Technical Requirements:**
- Sentinel REST API for connector status
- KQL queries to check actual data ingestion
- Time-based analysis (last heartbeat)
- Connector type mapping

**Inputs:**
- Tenant scope
- Time window (e.g., last 24h)
- Connector type filter (optional)

**Outputs:**
```json
{
  "summary": {
    "total_connectors": 150,
    "healthy": 142,
    "warning": 5,
    "error": 3
  },
  "connectors": [
    {
      "workspace": "Customer A",
      "connector_name": "Azure AD",
      "status": "healthy",
      "last_ingestion": "2025-11-19T09:55:00Z",
      "ingestion_rate_gb_day": 2.3
    },
    {
      "workspace": "Customer B",
      "connector_name": "Office 365",
      "status": "error",
      "last_ingestion": "2025-11-17T14:23:00Z",
      "error": "No data received in 48 hours",
      "troubleshooting_hint": "Check connector configuration in Azure portal"
    }
  ]
}
```

---

### Tool #3: `custom_kql_execute`
**Priority:** HIGH  
**Complexity:** Medium-High  
**Impact:** Enables team to run queries across all tenants

**What it does:**
- Executes KQL query across multiple workspaces
- Aggregates results from all tenants
- Handles query timeouts gracefully
- Supports templated queries
- Returns combined results with tenant context

**Technical Requirements:**
- Azure Monitor Query API
- Query execution orchestration
- Result aggregation and deduplication
- Timeout and error handling
- Query validation/sanitization

**Inputs:**
- KQL query string
- Tenant scope
- Time range
- Max results per workspace

**Outputs:**
```json
{
  "query": "SecurityEvent | where TimeGenerated > ago(1h) | summarize count() by Computer",
  "execution_time_ms": 3450,
  "workspaces_queried": 10,
  "results": [
    {
      "workspace": "Customer A",
      "tenant_id": "xxx",
      "row_count": 1234,
      "data": [
        {"Computer": "SERVER01", "count_": 456},
        {"Computer": "SERVER02", "count_": 778}
      ]
    }
  ]
}
```

---

## 🏗️ Architecture Components

### 1. MCP Server (Python - FastMCP)
```
src/mcp_server/
├── server.py              # Main MCP server
├── config.py              # Configuration management
└── tools/
    └── management/
        ├── health_check.py
        ├── connector_status.py
        └── kql_execute.py
```

### 2. PowerShell Backend
```
src/powershell/
└── SentinelManager/
    ├── SentinelManager.psd1
    ├── SentinelManager.psm1
    └── Functions/
        ├── Get-SentinelHealth.ps1
        ├── Get-DataConnectorStatus.ps1
        └── Invoke-MultiTenantKQL.ps1
```

### 3. Utilities
```
src/utils/
├── auth.py               # Azure authentication
├── lighthouse.py         # Lighthouse workspace enumeration
├── kql_helper.py         # KQL execution wrapper
└── logging.py            # Structured logging
```

---

## 📋 Implementation Order

### Week 1: Foundation & Tool #1

**Days 1-2: Setup & Infrastructure**
- [ ] Setup development environment
- [ ] Create Python project structure
- [ ] Install dependencies (requirements.txt)
- [ ] Setup Azure authentication (Service Principal or Managed Identity)
- [ ] Test Lighthouse access to workspaces
- [ ] Create logging framework
- [ ] Setup basic MCP server skeleton

**Days 3-5: Tool #1 - sentinel_health_check**
- [ ] Implement PowerShell function `Get-SentinelHealth.ps1`
- [ ] Create MCP tool wrapper
- [ ] Add multi-tenant iteration
- [ ] Implement error handling
- [ ] Write unit tests
- [ ] Test with 2-3 workspaces
- [ ] Document tool usage

---

### Week 2: Tools #2 & #3

**Days 6-8: Tool #2 - data_connector_status**
- [ ] Research Sentinel Connector API endpoints
- [ ] Implement PowerShell function `Get-DataConnectorStatus.ps1`
- [ ] Add KQL queries for ingestion verification
- [ ] Create MCP tool wrapper
- [ ] Implement status aggregation logic
- [ ] Add troubleshooting hints logic
- [ ] Write unit tests
- [ ] Test across multiple tenants

**Days 9-11: Tool #3 - custom_kql_execute**
- [ ] Implement KQL execution wrapper
- [ ] Add query validation/sanitization
- [ ] Create result aggregation logic
- [ ] Handle timeouts and errors
- [ ] Implement PowerShell function `Invoke-MultiTenantKQL.ps1`
- [ ] Create MCP tool wrapper
- [ ] Add result formatting
- [ ] Write unit tests
- [ ] Test with various query types

---

### Week 3: Integration & Testing

**Days 12-14: Integration Testing**
- [ ] End-to-end testing with all 3 tools
- [ ] Performance testing with 10+ workspaces
- [ ] Error scenario testing
- [ ] Security review (authentication, authorization)
- [ ] Load testing (concurrent requests)

**Days 15-16: VS Code Integration**
- [ ] Configure MCP server in VS Code
- [ ] Test natural language prompts
- [ ] Document sample prompts
- [ ] Create usage guide for team

**Days 17-18: Documentation & Handoff**
- [ ] Update README with setup instructions
- [ ] Write tool reference documentation
- [ ] Create team training materials
- [ ] Record demo video (optional)
- [ ] Prepare handoff to team

**Days 19-21: Buffer & Polish**
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Additional testing
- [ ] Blog post #1 draft

---

## 🔒 Security Checklist

- [ ] Service Principal with least privilege
- [ ] Secrets in Azure Key Vault (not in code)
- [ ] RBAC validation per workspace
- [ ] Query input sanitization (prevent injection)
- [ ] Rate limiting implementation
- [ ] Audit logging for all operations
- [ ] Error messages don't leak sensitive info
- [ ] Token refresh handling

---

## 🧪 Testing Strategy

### Unit Tests
- Each PowerShell function has Pester tests
- Each Python tool has pytest tests
- Mock Azure API responses
- Test error conditions

### Integration Tests
- Test with real (test) workspaces
- Multi-tenant scenarios
- Authentication flows
- Error propagation

### Manual Testing
- VS Code MCP client testing
- Natural language prompt testing
- Edge cases and error scenarios
- Performance with many workspaces

---

## 📊 Success Metrics

### Technical Metrics
- [ ] All 3 tools working end-to-end
- [ ] <5 second response time for health_check
- [ ] <10 second response time for connector_status
- [ ] <30 second response time for kql_execute (10 workspaces)
- [ ] 95%+ success rate across tools
- [ ] Zero critical security issues

### Team Adoption Metrics
- [ ] 3+ team members trained
- [ ] 10+ successful natural language queries
- [ ] Positive feedback from team
- [ ] At least 1 "this saved me time" story

---

## 🎯 Definition of Done

Phase 1 is complete when:

1. **Functionality**
   - ✅ All 3 tools implemented and tested
   - ✅ Working in VS Code via MCP
   - ✅ Handles 10+ tenant workspaces
   - ✅ Graceful error handling

2. **Quality**
   - ✅ Unit tests passing
   - ✅ Integration tests passing
   - ✅ Security review completed
   - ✅ Performance meets targets

3. **Documentation**
   - ✅ Setup guide written
   - ✅ Tool reference documented
   - ✅ Sample prompts provided
   - ✅ Team can use independently

4. **Handoff**
   - ✅ Demo to team completed
   - ✅ Team members trained
   - ✅ Feedback collected
   - ✅ Issues/requests logged for Phase 2

---

## 🚧 Known Challenges & Mitigation

### Challenge 1: Azure API Rate Limits
**Mitigation:**
- Implement caching for workspace lists
- Batch API calls where possible
- Add retry logic with exponential backoff
- Monitor rate limit headers

### Challenge 2: KQL Query Timeouts
**Mitigation:**
- Set reasonable timeout limits (30s)
- Provide query optimization hints
- Allow limiting workspaces for complex queries
- Implement query result streaming

### Challenge 3: Multi-tenant Authentication
**Mitigation:**
- Use Azure Lighthouse delegation
- Implement token caching
- Handle token refresh gracefully
- Clear error messages for permission issues

### Challenge 4: PowerShell Integration
**Mitigation:**
- Use PowerShell Core (cross-platform)
- Handle PS errors in Python
- Log PS output for debugging
- Test on both Windows and Linux

---

## 📝 Development Environment

### Required Software
- Python 3.10+
- PowerShell Core 7.4+
- VS Code with MCP extension
- Git
- Azure CLI

### Required Access
- Azure Lighthouse delegation to customer tenants
- Service Principal with:
  - Microsoft Sentinel Reader
  - Log Analytics Reader
  - Azure Resource Graph Reader

### Configuration Files
- `.env` - Local development secrets
- `config/server.json` - Server configuration
- `config/workspaces.json` - Workspace mappings

---

## 🔄 Phase 1 → Phase 2 Transition

After Phase 1 completion:

1. **Retrospective**
   - What worked well?
   - What was harder than expected?
   - Architecture changes needed?
   - Performance bottlenecks?

2. **Feedback Integration**
   - Team suggestions
   - Missing features
   - UX improvements
   - Priority adjustments for Phase 2

3. **Blog Post #1**
   - Document Phase 1 journey
   - Share lessons learned
   - Announce Phase 2 roadmap

4. **Phase 2 Planning**
   - Finalize next 4 tools
   - Adjust timeline based on Phase 1
   - Address technical debt
   - Plan automation improvements

---

## 📞 Questions & Decisions Needed

### Before Starting
- [ ] Which Azure tenant for Service Principal?
- [ ] Which workspaces for initial testing?
- [ ] VS Code installed and configured?
- [ ] GitHub repo access confirmed?

### During Development
- Questions will be tracked in GitHub Issues
- Weekly sync for status updates
- Blockers escalated immediately

---

## 🎉 Let's Build!

**Next Immediate Steps:**

1. **Switch to Claude Code** - Better for actual implementation
2. **Setup dev environment** - Dependencies, auth, config
3. **Start with Tool #1** - `sentinel_health_check`
4. **Iterate quickly** - Small commits, frequent testing

**Ready to switch to Claude Code and start coding?** 🚀

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-19  
**Owner:** Phillipe (RycnCDL)  
**Status:** Approved & Ready to Execute

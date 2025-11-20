# Microsoft Sentinel MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/Status-In%20Development-orange)]()
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-blue)](https://modelcontextprotocol.io/)

> A Model Context Protocol (MCP) server for Microsoft Sentinel that enables natural language SOC operations and multi-tenant security management.

---

## 🎯 Overview

This project provides a comprehensive MCP server implementation for Microsoft Sentinel, designed to revolutionize multi-tenant SOC operations through natural language interfaces and standardized tool integration.

**Key Features:**
- 🔍 Natural language queries across multiple Sentinel workspaces
- 🔄 Automated compliance monitoring and reporting
- 📊 Multi-tenant health checks and drift detection
- 🛡️ Azure Lighthouse integration for managed SOC providers
- 🔐 Enterprise-grade security with Microsoft Entra authentication
- 📈 Built-in monitoring and audit logging

---

## 🚀 Quick Start

**Current Status**: Phase 2 COMPLETE ✅ | Ready for End-to-End Testing 🧪

### Prerequisites

- **Python 3.10+** and **PowerShell 7+** installed
- **Microsoft Sentinel workspace(s)** with Data Lake enabled
- **Azure Service Principal** with Sentinel Reader/Contributor role
- **SentinelManager.ps1** PowerShell script
- **Claude Desktop** or other MCP client (for testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/RycnCDL/sentinel-mcp-server.git
cd sentinel-mcp-server

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Azure credentials and PowerShell script path

# Run the server
python -m src
```

**For detailed setup instructions, see [QUICK-START.md](QUICK-START.md)**

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](QUICK-START.md)** - Step-by-step setup and testing instructions
- **[Server Status](SERVER-STATUS.md)** - Current implementation status and capabilities
- **[Getting Started with this Repo](GETTING-STARTED-WITH-THIS-REPO.md)** - Repository navigation

### Project Documentation
- **[Project Overview](PROJECT.md)** - Complete project overview, architecture decisions, and roadmap
- **[Blog Series](BLOG-IDEAS.md)** - Follow the development journey through our blog posts
- **[Setup Guide](SETUP-GUIDE.md)** - Detailed configuration guide

### Phase Documentation
- **[Phase 1 Completion](PHASE-1-COMPLETION.md)** - Core infrastructure (authentication, health check, logging)
- **[Phase 2 Completion](PHASE-2-COMPLETION.md)** - PowerShell integration (40+ tools)
- **[Phase 3 Plan](PHASE-3-PRODUCTION-READINESS.md)** - Production readiness roadmap

### Technical Documentation
- **[Architecture](docs/01-architecture.md)** - System design and components
- **[PowerShell Integration](docs/powershell-integration.md)** - PowerShell bridge implementation
- **[Claude Desktop Setup](docs/claude-desktop-setup.md)** - MCP client configuration
- **[Tool Reference](docs/03-tool-reference.md)** - Available MCP tools and their usage
- **[Multi-Tenant Setup](docs/04-multi-tenant-setup.md)** - Azure Lighthouse integration
- **[Security Considerations](docs/05-security-considerations.md)** - Security best practices
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[FAQ](docs/faq.md)** - Frequently asked questions

---

## 🛠️ Available Tools

### Python Tools (1)
- ✅ `sentinel_health_check` - Multi-tenant health status monitoring with quick/detailed modes

### PowerShell Tools (40+)

#### Table Management
- ✅ `New-SentinelTable` - Create custom log table
- ✅ `Get-SentinelTables` - List all tables in workspace
- ✅ `Remove-SentinelTable` - Delete custom table
- ✅ `Update-TablePlan` - Change table plan (Analytics/Basic)
- ✅ `Update-TableRetention` - Modify retention settings
- ✅ `View-TableRetention` - Show current retention

#### Analytics Rules
- ✅ `Get-AnalyticsRules` - List all analytics rules
- ✅ `Get-AnalyticsRuleDetails` - Show rule details
- ✅ `Enable-AnalyticsRule` - Enable specific rule
- ✅ `Disable-AnalyticsRule` - Disable specific rule
- ✅ `Remove-AnalyticsRule` - Delete rule
- ✅ `New-AnalyticsRule` - Create new rule

#### Workbooks
- ✅ `Get-SentinelWorkbooks` - List all workbooks
- ✅ `Get-WorkbookDetails` - Show workbook details
- ✅ `Remove-SentinelWorkbook` - Delete workbook
- ✅ `Export-SentinelWorkbook` - Export workbook to JSON
- ✅ `Import-SentinelWorkbook` - Import workbook from JSON

#### Incidents
- ✅ `Get-SentinelIncidents` - List incidents
- ✅ `Show-IncidentDetails` - Show incident details
- ✅ `Close-SentinelIncident` - Close incident
- ✅ `Assign-IncidentOwner` - Assign owner
- ✅ `Add-IncidentComment` - Add comment
- ✅ `Get-IncidentComments` - Show comments

#### Backup & Export
- ✅ `Export-AnalyticsRules` - Backup all analytics rules
- ✅ `Export-AutomationRules` - Backup automation rules
- ✅ `Export-Watchlists` - Backup watchlists
- ✅ `Export-Functions` - Backup saved functions
- ✅ `Export-SavedQueries` - Backup saved queries
- ✅ `Export-TableData` - Export table data

#### DCR/DCE Management
- ✅ 11+ additional functions for Data Collection Rules and Endpoints

**Total: 41 MCP Tools Available**

**For complete tool documentation, see [docs/03-tool-reference.md](docs/03-tool-reference.md)**

---

## 🏗️ Architecture

This project implements a hybrid approach:
- **FastMCP Python Server** - Core MCP server with health check and tool management
- **PowerShell Bridge** - Integrates with SentinelManager PowerShell module (40+ functions)
- **Azure SDK Integration** - Direct Azure API access for authentication and Lighthouse
- **Structured Logging** - Comprehensive logging with structlog

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP Client Layer                        │
│  (Claude Desktop, VS Code, Browser Extension, etc.)         │
└─────────────────────────────────────────────────────────────┘
                            ↓ MCP Protocol (JSON-RPC)
┌─────────────────────────────────────────────────────────────┐
│                Microsoft Sentinel MCP Server                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ FastMCP Server (Python)                              │   │
│  │ • Tool registration                                  │   │
│  │ • Request routing                                    │   │
│  │ • Error handling                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↓                          ↓                    │
│  ┌──────────────────┐      ┌─────────────────────────┐     │
│  │ Python Tools     │      │ PowerShell Bridge       │     │
│  │ • health_check   │      │ • Local/Remote exec     │     │
│  │ • lighthouse     │      │ • Retry logic          │     │
│  │ • auth           │      │ • JSON serialization   │     │
│  └──────────────────┘      └─────────────────────────┘     │
│              ↓                          ↓                    │
└──────────────│──────────────────────────│───────────────────┘
               │                          │
               ↓                          ↓
    ┌─────────────────┐      ┌──────────────────────┐
    │  Azure REST API │      │ PowerShell Scripts   │
    │  • Lighthouse   │      │ • SentinelManager    │
    │  • Sentinel API │      │ • 40+ Functions      │
    └─────────────────┘      └──────────────────────┘
```

**Key Features:**
- ✅ Retry logic with exponential backoff (3 retries: 1s → 2s → 4s)
- ✅ Timeout management (300s default)
- ✅ Comprehensive error handling
- ✅ Local and remote PowerShell execution
- ✅ Structured logging with correlation IDs
- ✅ Azure Lighthouse multi-tenant support

**For detailed architecture, see [docs/01-architecture.md](docs/01-architecture.md)**

---

## 🔒 Security

This project takes security seriously:
- ✅ Microsoft Entra authentication
- ✅ Azure RBAC integration via Lighthouse
- ✅ Multi-tenant data isolation
- ✅ Comprehensive audit logging
- ✅ Secrets management best practices
- ✅ Rate limiting and throttling

See [Security Considerations](docs/05-security-considerations.md) for details.

---

## 📈 Use Cases

### Managed SOC Providers
- Manage 10+ customer tenants from a single interface
- Standardized compliance checks across all customers
- Automated backup and disaster recovery
- Consistent analytics rule deployment

### Enterprise Security Teams
- Natural language incident investigation
- Cross-workspace threat hunting
- Configuration management at scale
- Simplified onboarding for junior analysts

### Security Architects
- Configuration drift detection
- Security posture assessment
- Cost optimization insights
- Best practices enforcement

---

## 🤝 Contributing

We welcome contributions! This project is being developed in the open to benefit the Microsoft Sentinel community.

> **Note:** Contribution guidelines will be published soon. For now, feel free to open issues for feedback and feature requests.

---

## 📝 Blog Serie

Follow the development journey through our blog post series:

1. **[Microsoft Sentinel meets MCP: Die Zukunft des SOC Management](blog/post-01-vision.md)** - Coming soon
2. **[Building a Sentinel MCP Server: Architecture & First Tool](blog/post-02-architecture.md)** - Coming soon
3. **[Multi-Tenant SOC Automation: Real-World Use Cases](blog/post-03-use-cases.md)** - Coming soon

---

## 🗓️ Roadmap

### ✅ Phase 1: Core Infrastructure (COMPLETE)
- [x] Project structure and documentation
- [x] Azure authentication with Service Principal
- [x] Azure Lighthouse integration for multi-tenant support
- [x] Health check tool with quick/detailed modes
- [x] Structured logging with structlog
- [x] Configuration management with pydantic

### ✅ Phase 2: PowerShell Integration (COMPLETE)
- [x] PowerShell bridge with local/remote execution
- [x] 40+ SentinelManager functions as MCP tools
- [x] Retry logic with exponential backoff
- [x] Comprehensive error handling and timeout management
- [x] Testing framework with all tests passing
- [x] Complete documentation (PowerShell integration guide)

### 🔄 Phase 3: Production Readiness (IN PROGRESS)
- [ ] End-to-end testing with Claude Desktop
- [ ] Production deployment setup (systemd/Windows Service)
- [ ] Monitoring and observability (Application Insights)
- [ ] Advanced features (caching, batch operations)
- [ ] Blog series publication (4 posts)
- [ ] Performance optimization

### 📅 Phase 4: Advanced Features (PLANNED)
- [ ] Multi-tenant KQL query aggregation
- [ ] Configuration drift detection
- [ ] Automated compliance reporting
- [ ] Real-time streaming for long-running operations
- [ ] Enhanced error messages with actionable suggestions

### 📅 Phase 5: Community & Adoption (PLANNED)
- [ ] Public beta release
- [ ] Video tutorials and workshops
- [ ] Community contributions and feedback
- [ ] Integration with other MCP clients

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Microsoft Sentinel Team for the MCP integration
- Anthropic for the Model Context Protocol
- The Microsoft Sentinel community

---

## 📞 Contact

**Author:** Phillipe  
**Role:** Senior IT Security Consultant, Microsoft Sentinel SME  
**LinkedIn:** [Connect with me](https://linkedin.com)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the project.

---

**Status:** ✅ Phase 2 Complete | 🧪 Ready for Testing | **Version:** 1.0.0-beta | **Last Updated:** 2024-12-24

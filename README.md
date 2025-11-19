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

> **Note:** This project is currently in active development. Production-ready releases coming soon.

### Prerequisites

- Microsoft Sentinel workspace(s) with Data Lake enabled
- Azure Lighthouse configuration (for multi-tenant scenarios)
- Microsoft Entra authentication
- Security Reader role minimum

### Installation

```bash
# Clone the repository
git clone https://github.com/RycnCDL/sentinel-mcp-server.git
cd sentinel-mcp-server

# Installation instructions coming soon
```

---

## 📚 Documentation

- **[Project Documentation](PROJECT.md)** - Complete project overview, architecture decisions, and roadmap
- **[Blog Serie](BLOG-IDEAS.md)** - Follow the development journey through our blog posts
- **[Architecture](docs/01-architecture.md)** - System design and components (coming soon)
- **[Getting Started](docs/02-getting-started.md)** - Setup and configuration guide (coming soon)
- **[Tool Reference](docs/03-tool-reference.md)** - Available MCP tools and their usage (coming soon)
- **[Multi-Tenant Setup](docs/04-multi-tenant-setup.md)** - Azure Lighthouse integration (coming soon)
- **[Security Considerations](docs/05-security-considerations.md)** - Security best practices (coming soon)

---

## 🛠️ Available Tools (Planned)

### Management & Operations
- `sentinel_backup_create` - Backup Analytics Rules, Workbooks, and configurations
- `sentinel_backup_restore` - Restore Sentinel components across workspaces
- `sentinel_compliance_check` - Automated compliance assessment
- `sentinel_health_check` - Multi-tenant health status monitoring
- `workspace_config_drift` - Configuration drift detection

### Data Exploration
- `custom_kql_execute` - Execute KQL across multiple workspaces
- `parser_validate` - ASIM parser testing and validation
- `data_connector_status` - Data connector health across tenants
- `log_ingestion_metrics` - Ingestion metrics and cost analysis

### Automation & Deployment
- `analytics_rule_deploy` - Deploy rules across multiple tenants
- `incident_bulk_action` - Bulk operations on incidents
- `workbook_deploy` - Multi-tenant workbook deployment
- `watchlist_sync` - Watchlist management and synchronization

### Reporting & Insights
- `tenant_summary_report` - Multi-tenant security posture summary
- `incident_trends_analysis` - Trend analysis across workspaces
- `data_connector_coverage` - Coverage and gap analysis

---

## 🏗️ Architecture

This project implements a hybrid approach:
- **Microsoft Sentinel MCP Server** - For native data exploration capabilities
- **Custom MCP Server** - For specialized management and automation tools
- **PowerShell Backend** - Integrates with existing Sentinel management modules

```
┌─────────────────┐
│   MCP Clients   │
│ (VS Code, etc.) │
└────────┬────────┘
         │
    ┌────┴────┐
    │   MCP   │
    │  Server │
    └────┬────┘
         │
    ┌────┴─────────────────┐
    │                      │
┌───┴────────┐  ┌─────────┴──────┐
│ Microsoft  │  │  Custom Tools  │
│  Sentinel  │  │  (PowerShell)  │
│ MCP Tools  │  │                │
└────────────┘  └────────────────┘
```

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

### Phase 1: Planning & Design (Current)
- [x] Project structure and documentation
- [ ] Architecture finalization
- [ ] Tool prioritization
- [ ] Security design

### Phase 2: MVP Development
- [ ] First 3 priority tools implementation
- [ ] PowerShell module integration
- [ ] Testing framework
- [ ] Initial documentation

### Phase 3: Production Ready
- [ ] Multi-tenant testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Public beta release

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

**Status:** 🚧 Active Development | **Version:** 0.1.0-alpha | **Last Updated:** 2025-11-19

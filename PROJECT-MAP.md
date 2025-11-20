# 🗺️ Microsoft Sentinel MCP Server - Project Map

**Quick navigation guide to all project resources**

---

## 📚 Start Here

### New to the Project?
1. **[README.md](README.md)** - Project overview and quick start
2. **[COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md)** - What we've built (start here!)
3. **[QUICK-START.md](QUICK-START.md)** - Get up and running in 15 minutes

### Want to Test It?
1. **[QUICK-START.md](QUICK-START.md)** - Step-by-step setup
2. **[TESTING-CHECKLIST.md](TESTING-CHECKLIST.md)** - Comprehensive test plan
3. **[docs/claude-desktop-setup.md](docs/claude-desktop-setup.md)** - Client configuration

### Want to Understand the Architecture?
1. **[SERVER-STATUS.md](SERVER-STATUS.md)** - Current capabilities
2. **[docs/01-architecture.md](docs/01-architecture.md)** - System design
3. **[docs/powershell-integration.md](docs/powershell-integration.md)** - PowerShell bridge

### Want to Deploy to Production?
1. **[PHASE-3-PRODUCTION-READINESS.md](PHASE-3-PRODUCTION-READINESS.md)** - Deployment plan
2. **[docs/05-security-considerations.md](docs/05-security-considerations.md)** - Security
3. **[docs/04-multi-tenant-setup.md](docs/04-multi-tenant-setup.md)** - Multi-tenant config

---

## 📂 Documentation Structure

### 📘 Root Documentation (Main Guides)

#### Getting Started
- **[README.md](README.md)** - Main project overview
- **[QUICK-START.md](QUICK-START.md)** - Quick start guide (15 min setup)
- **[SETUP-GUIDE.md](SETUP-GUIDE.md)** - Detailed setup instructions
- **[GETTING-STARTED-WITH-THIS-REPO.md](GETTING-STARTED-WITH-THIS-REPO.md)** - Repo navigation

#### Project Status
- **[COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md)** - 🎉 What we've accomplished
- **[SERVER-STATUS.md](SERVER-STATUS.md)** - Current capabilities and tools
- **[PROJECT.md](PROJECT.md)** - Original project vision and goals

#### Phase Documentation
- **[PHASE-1-COMPLETION.md](PHASE-1-COMPLETION.md)** - ✅ Core infrastructure
- **[PHASE-2-COMPLETION.md](PHASE-2-COMPLETION.md)** - ✅ PowerShell integration
- **[PHASE-3-PRODUCTION-READINESS.md](PHASE-3-PRODUCTION-READINESS.md)** - 🔄 Production plan

#### Planning & Progress
- **[PHASE-1-IMPLEMENTATION-PLAN.md](PHASE-1-IMPLEMENTATION-PLAN.md)** - Phase 1 plan
- **[PHASE-2-POWERSHELL-INTEGRATION.md](PHASE-2-POWERSHELL-INTEGRATION.md)** - Phase 2 plan
- **[REPO-STRUCTURE.md](REPO-STRUCTURE.md)** - Repository organization
- **[VSCODE-INSTRUCTIONS.md](VSCODE-INSTRUCTIONS.md)** - Development workflow
- **[SUMMARY.md](SUMMARY.md)** - Project summary

#### Testing & Quality
- **[TESTING-CHECKLIST.md](TESTING-CHECKLIST.md)** - Comprehensive test plan
- **[pytest.ini](pytest.ini)** - Pytest configuration

#### Blog & Community
- **[BLOG-IDEAS.md](BLOG-IDEAS.md)** - Blog series plan (4 posts)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

#### Legal & License
- **[LICENSE](LICENSE)** - MIT License

### 📗 Technical Documentation (docs/)

#### Core Documentation
- **[docs/README.md](docs/README.md)** - Documentation overview
- **[docs/01-architecture.md](docs/01-architecture.md)** - System architecture
- **[docs/02-getting-started.md](docs/02-getting-started.md)** - Developer guide
- **[docs/03-tool-reference.md](docs/03-tool-reference.md)** - Tool documentation

#### Setup & Configuration
- **[docs/claude-desktop-setup.md](docs/claude-desktop-setup.md)** - Claude Desktop config
- **[docs/04-multi-tenant-setup.md](docs/04-multi-tenant-setup.md)** - Multi-tenant setup
- **[docs/powershell-integration.md](docs/powershell-integration.md)** - PowerShell guide

#### Security & Operations
- **[docs/05-security-considerations.md](docs/05-security-considerations.md)** - Security guide
- **[docs/api-reference.md](docs/api-reference.md)** - API documentation

#### Support
- **[docs/06-use-cases.md](docs/06-use-cases.md)** - Use cases and examples
- **[docs/troubleshooting.md](docs/troubleshooting.md)** - Troubleshooting guide
- **[docs/faq.md](docs/faq.md)** - FAQ

### 📕 Blog Series (blog/)
- **[blog/README.md](blog/README.md)** - Blog overview
- **[blog/drafts/post-01-vision.md](blog/drafts/post-01-vision.md)** - Why MCP for Sentinel?
- **[blog/drafts/post-02-architecture.md](blog/drafts/post-02-architecture.md)** - Building the bridge
- **[blog/drafts/post-03-use-cases.md](blog/drafts/post-03-use-cases.md)** - Real-world workflows
- **[blog/drafts/post-04-lessons-learned.md](blog/drafts/post-04-lessons-learned.md)** - Lessons learned

### 📙 Examples (examples/)
- **[examples/README.md](examples/README.md)** - Example scripts and workflows

---

## 💻 Source Code Structure

### 📂 src/ - Main Application

#### Core Server
- **[src/__init__.py](src/__init__.py)** - Package initialization
- **[src/__main__.py](src/__main__.py)** - Entry point
- **[src/README.md](src/README.md)** - Source code overview

#### MCP Server
- **[src/mcp_server/__init__.py](src/mcp_server/__init__.py)** - Server initialization
- **[src/mcp_server/server.py](src/mcp_server/server.py)** - 🎯 Main server (FastMCP)

#### Tools
- **[src/mcp_server/tools/__init__.py](src/mcp_server/tools/__init__.py)** - Tools package
- **[src/mcp_server/tools/management/health_check.py](src/mcp_server/tools/management/health_check.py)** - Health check tool
- **[src/mcp_server/tools/powershell/sentinel_manager.py](src/mcp_server/tools/powershell/sentinel_manager.py)** - 🎯 40+ PowerShell tools

#### Utilities
- **[src/utils/__init__.py](src/utils/__init__.py)** - Utils package
- **[src/utils/auth.py](src/utils/auth.py)** - Azure authentication
- **[src/utils/config.py](src/utils/config.py)** - Configuration management
- **[src/utils/lighthouse.py](src/utils/lighthouse.py)** - Azure Lighthouse
- **[src/utils/logging.py](src/utils/logging.py)** - Structured logging
- **[src/utils/powershell_bridge.py](src/utils/powershell_bridge.py)** - 🎯 PowerShell bridge

#### Tests
- **[src/tests/__init__.py](src/tests/__init__.py)** - Tests package
- **[src/tests/conftest.py](src/tests/conftest.py)** - Pytest fixtures
- **[src/tests/test_auth.py](src/tests/test_auth.py)** - Auth tests
- **[src/tests/test_config.py](src/tests/test_config.py)** - Config tests
- **[src/tests/test_health_check.py](src/tests/test_health_check.py)** - Health check tests

---

## 🔧 Configuration & Scripts

### Configuration Files
- **[.env.example](.env.example)** - Environment variables template (COPY TO .env)
- **[config/example/server.example.json](config/example/server.example.json)** - Server config example
- **[config/claude_desktop_config.json](config/claude_desktop_config.json)** - Claude Desktop config
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[requirements-dev.txt](requirements-dev.txt)** - Development dependencies

### Scripts
- **[scripts/setup.sh](scripts/setup.sh)** - Setup script (Linux/Mac)
- **[scripts/setup_credentials.sh](scripts/setup_credentials.sh)** - Credentials setup
- **[scripts/test_server.py](scripts/test_server.py)** - Server test
- **[scripts/test_auth.py](scripts/test_auth.py)** - Auth test
- **[scripts/test_permissions.py](scripts/test_permissions.py)** - Permissions test
- **[scripts/test_server_manual.py](scripts/test_server_manual.py)** - Manual server test
- **[scripts/diagnose_workspace_access.py](scripts/diagnose_workspace_access.py)** - Diagnostics
- **[create-structure.sh](create-structure.sh)** - Create project structure

---

## 🎯 Quick Reference by Task

### I Want to...

#### ...Get Started Quickly
1. Read **[COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md)** - Understand what's built
2. Follow **[QUICK-START.md](QUICK-START.md)** - Setup in 15 minutes
3. Test with **[TESTING-CHECKLIST.md](TESTING-CHECKLIST.md)** - Verify it works

#### ...Understand the Code
1. Check **[SERVER-STATUS.md](SERVER-STATUS.md)** - What's implemented
2. Read **[src/mcp_server/server.py](src/mcp_server/server.py)** - Main server
3. Review **[src/utils/powershell_bridge.py](src/utils/powershell_bridge.py)** - PowerShell integration
4. Explore **[src/mcp_server/tools/powershell/sentinel_manager.py](src/mcp_server/tools/powershell/sentinel_manager.py)** - 40+ tools

#### ...Deploy to Production
1. Read **[PHASE-3-PRODUCTION-READINESS.md](PHASE-3-PRODUCTION-READINESS.md)** - Deployment plan
2. Review **[docs/05-security-considerations.md](docs/05-security-considerations.md)** - Security
3. Setup **[docs/04-multi-tenant-setup.md](docs/04-multi-tenant-setup.md)** - Multi-tenant
4. Configure monitoring (Application Insights)

#### ...Contribute to the Project
1. Read **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
2. Check **[GETTING-STARTED-WITH-THIS-REPO.md](GETTING-STARTED-WITH-THIS-REPO.md)** - Repo structure
3. Review **[VSCODE-INSTRUCTIONS.md](VSCODE-INSTRUCTIONS.md)** - Development workflow
4. Run tests with **pytest**

#### ...Troubleshoot Issues
1. Check **[docs/troubleshooting.md](docs/troubleshooting.md)** - Common issues
2. Review **[docs/faq.md](docs/faq.md)** - FAQ
3. See **[docs/claude-desktop-setup.md](docs/claude-desktop-setup.md)** - Client setup
4. Enable DEBUG mode in **.env**

#### ...Learn More
1. Read **[PROJECT.md](PROJECT.md)** - Project vision
2. Check **[BLOG-IDEAS.md](BLOG-IDEAS.md)** - Blog series (4 posts)
3. Explore **[docs/06-use-cases.md](docs/06-use-cases.md)** - Use cases
4. Review **[examples/README.md](examples/README.md)** - Examples

---

## 📊 Project Status Overview

### ✅ Completed (Phase 1 & 2)
- Core infrastructure (auth, logging, config)
- Health check tool
- PowerShell bridge (local + remote)
- 40+ PowerShell tools
- Comprehensive documentation
- Testing framework

### 🔄 In Progress (Phase 3)
- End-to-end testing with Claude Desktop
- Production deployment setup
- Monitoring integration
- Blog series writing

### 📅 Planned (Phase 4+)
- Advanced features (caching, batch ops)
- Multi-tenant KQL aggregation
- Config drift detection
- Public beta release

---

## 🏆 Key Files to Know

### Most Important Files
1. **[COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md)** - 🎉 Start here!
2. **[QUICK-START.md](QUICK-START.md)** - Get running fast
3. **[src/mcp_server/server.py](src/mcp_server/server.py)** - Main server
4. **[src/utils/powershell_bridge.py](src/utils/powershell_bridge.py)** - PowerShell integration
5. **[.env.example](.env.example)** - Configuration template

### Phase Documentation
1. **[PHASE-1-COMPLETION.md](PHASE-1-COMPLETION.md)** - What we built in Phase 1
2. **[PHASE-2-COMPLETION.md](PHASE-2-COMPLETION.md)** - What we built in Phase 2
3. **[PHASE-3-PRODUCTION-READINESS.md](PHASE-3-PRODUCTION-READINESS.md)** - Phase 3 plan

### Configuration Templates
1. **[.env.example](.env.example)** - Copy to **.env** and fill in
2. **[config/claude_desktop_config.json](config/claude_desktop_config.json)** - Claude Desktop

---

## 📞 Getting Help

### Documentation
- **Start**: [QUICK-START.md](QUICK-START.md)
- **Troubleshooting**: [docs/troubleshooting.md](docs/troubleshooting.md)
- **FAQ**: [docs/faq.md](docs/faq.md)

### Support
- **GitHub Issues**: Create issue in repository
- **Email**: Contact project maintainer

---

## 🎉 You're All Set!

**Navigate the project with confidence using this map!**

**Next Step**: Read **[COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md)** to see what we've accomplished! 🚀

---

**Last Updated**: December 24, 2024  
**Project Status**: Phase 2 Complete ✅ | Ready for Testing 🧪

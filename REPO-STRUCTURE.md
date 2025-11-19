# Repository Structure Guide

This document provides a comprehensive overview of the repository structure for the Microsoft Sentinel MCP Server project.

## 📁 Directory Tree

```
sentinel-mcp-server/
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Main project README
├── CHANGELOG.md               # Version history and changes
├── CONTRIBUTING.md            # Contribution guidelines
├── PROJECT.md                 # Detailed project planning and architecture decisions
├── BLOG-IDEAS.md             # Blog serie planning and outlines
├── REPO-STRUCTURE.md         # This file - repository structure documentation
├── requirements.txt          # Python production dependencies
├── requirements-dev.txt      # Python development dependencies
├── setup.py                  # Python package setup (coming soon)
├── pyproject.toml           # Python project configuration (coming soon)
│
├── docs/                     # 📚 Documentation
│   ├── README.md            # Documentation overview
│   ├── 01-architecture.md   # System architecture (planned)
│   ├── 02-getting-started.md # Setup guide (planned)
│   ├── 03-tool-reference.md  # MCP tools reference (planned)
│   ├── 04-multi-tenant-setup.md # Azure Lighthouse guide (planned)
│   ├── 05-security-considerations.md # Security best practices (planned)
│   ├── 06-use-cases.md      # Implementation examples (planned)
│   ├── api-reference.md     # API documentation (planned)
│   ├── troubleshooting.md   # Common issues (planned)
│   └── faq.md               # Frequently asked questions (planned)
│
├── src/                      # 💻 Source Code
│   ├── README.md            # Source code overview
│   ├── __init__.py
│   ├── mcp_server/          # MCP server implementation
│   │   ├── __init__.py
│   │   ├── server.py        # Main server logic
│   │   ├── config.py        # Configuration management
│   │   └── tools/           # MCP tool implementations
│   │       ├── __init__.py
│   │       ├── management/  # Management & Operations tools
│   │       ├── exploration/ # Data exploration tools
│   │       ├── automation/  # Automation & Deployment tools
│   │       └── reporting/   # Reporting & Insights tools
│   │
│   ├── powershell/          # PowerShell backend modules
│   │   ├── SentinelManager/ # Main Sentinel management module
│   │   ├── Backup/          # Backup/Restore functionality
│   │   └── Compliance/      # Compliance checking
│   │
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication helpers
│   │   ├── logging.py       # Logging configuration
│   │   ├── azure_client.py  # Azure SDK wrapper
│   │   └── config.py        # Configuration utilities
│   │
│   └── tests/               # Test suite
│       ├── __init__.py
│       ├── unit/            # Unit tests
│       ├── integration/     # Integration tests
│       ├── e2e/             # End-to-end tests
│       └── fixtures/        # Test fixtures and mocks
│
├── examples/                 # 📝 Usage Examples
│   ├── README.md            # Examples overview
│   ├── basic-setup/         # Getting started examples
│   ├── first-tool/          # First tool implementation
│   ├── vs-code-integration/ # VS Code setup
│   ├── multi-tenant-query/  # Multi-tenant examples
│   ├── compliance-check/    # Compliance monitoring
│   ├── backup-restore/      # Backup workflows
│   ├── incident-management/ # Incident operations
│   ├── custom-tool/         # Custom tool development
│   ├── powershell-integration/ # PowerShell integration
│   ├── security-copilot-agent/ # Agent creation
│   ├── config-templates/    # Configuration templates
│   └── azure-lighthouse/    # Lighthouse setup
│
├── blog/                     # ✍️ Blog Posts
│   ├── README.md            # Blog serie overview
│   ├── drafts/              # Work-in-progress posts
│   │   ├── post-01-vision.md
│   │   ├── post-02-architecture.md
│   │   ├── post-03-use-cases.md
│   │   └── post-04-lessons-learned.md
│   └── published/           # Published posts archive
│
├── config/                   # ⚙️ Configuration (coming soon)
│   ├── example/             # Example configurations
│   │   ├── server.example.json
│   │   ├── .env.example
│   │   └── azure.example.json
│   └── schemas/             # Configuration schemas
│       └── config.schema.json
│
├── scripts/                  # 🛠️ Utility Scripts (coming soon)
│   ├── setup.sh             # Initial setup script
│   ├── deploy.sh            # Deployment script
│   └── test.sh              # Testing automation
│
└── .github/                  # GitHub Configuration (coming soon)
    ├── workflows/           # GitHub Actions
    │   ├── ci.yml          # Continuous Integration
    │   ├── tests.yml       # Automated testing
    │   └── release.yml     # Release automation
    ├── ISSUE_TEMPLATE/      # Issue templates
    └── PULL_REQUEST_TEMPLATE.md # PR template
```

## 📋 File Purposes

### Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Main entry point, project overview, quick start |
| `PROJECT.md` | Detailed planning, architecture decisions, roadmap |
| `BLOG-IDEAS.md` | Blog serie planning, post outlines, content calendar |
| `CHANGELOG.md` | Version history, release notes |
| `CONTRIBUTING.md` | How to contribute to the project |
| `LICENSE` | MIT License text |
| `REPO-STRUCTURE.md` | This file - repository structure guide |
| `.gitignore` | Files/folders to ignore in git |
| `requirements.txt` | Python production dependencies |
| `requirements-dev.txt` | Python development dependencies |

### Directory Purposes

| Directory | Purpose | Status |
|-----------|---------|--------|
| `docs/` | Comprehensive documentation for users and developers | 📋 Planned |
| `src/` | All source code (MCP server, PowerShell modules, utils) | 🚧 In Progress |
| `examples/` | Practical usage examples and templates | 📋 Planned |
| `blog/` | Blog posts documenting the development journey | 📋 Planned |
| `config/` | Configuration files and templates | 📋 Planned |
| `scripts/` | Automation and utility scripts | 📋 Planned |
| `.github/` | GitHub-specific configuration (Actions, templates) | 📋 Planned |

## 🎯 Key Design Principles

### 1. **Separation of Concerns**
- **src/mcp_server/** - MCP protocol implementation
- **src/powershell/** - Sentinel business logic
- **src/utils/** - Shared utilities

### 2. **Documentation First**
- Every directory has a README
- Code is documented inline
- Examples are self-contained

### 3. **Test Coverage**
- Unit tests alongside code
- Integration tests for workflows
- E2E tests for critical paths

### 4. **Configuration Management**
- Example configs in repo
- Real configs in .gitignore
- Environment-based configuration

### 5. **Security by Design**
- No secrets in code
- .env files for local development
- Azure Key Vault for production

## 🚀 Getting Started with This Structure

### For New Contributors

1. **Start with:** `README.md` → `PROJECT.md` → `CONTRIBUTING.md`
2. **Browse:** `docs/` for detailed documentation
3. **Learn:** `examples/` for hands-on code
4. **Build:** `src/` to understand implementation

### For Users

1. **Start with:** `README.md`
2. **Setup:** `docs/02-getting-started.md`
3. **Explore:** `examples/` for your use case
4. **Reference:** `docs/03-tool-reference.md`

### For Developers

1. **Start with:** `CONTRIBUTING.md`
2. **Understand:** `PROJECT.md` and `docs/01-architecture.md`
3. **Setup:** Follow development environment guide
4. **Code:** `src/` with tests in `src/tests/`

## 📦 Adding New Components

### Adding a New MCP Tool

```
1. Create tool in: src/mcp_server/tools/[category]/your_tool.py
2. Write tests in: src/tests/unit/tools/test_your_tool.py
3. Add example in: examples/your-tool-usage/
4. Document in: docs/03-tool-reference.md
5. Update: CHANGELOG.md
```

### Adding New Documentation

```
1. Create file in: docs/your-topic.md
2. Add to: docs/README.md index
3. Link from: README.md if major topic
4. Update: CHANGELOG.md
```

### Adding a Blog Post

```
1. Create draft in: blog/drafts/post-XX-topic.md
2. Update: blog/README.md with status
3. When published: Move to blog/published/
4. Update: BLOG-IDEAS.md tracking
```

## 🔄 Maintenance

### Regular Updates Needed

- [ ] `CHANGELOG.md` - Update with every significant change
- [ ] `requirements.txt` - Update when dependencies change
- [ ] `README.md` - Update status badges and links
- [ ] `PROJECT.md` - Update decisions and roadmap

### Version Control Strategy

- **main** - Production-ready code
- **develop** - Integration branch
- **feature/** - Feature branches
- **hotfix/** - Urgent fixes

## 📊 Repository Metrics

### Current Status

- **Files:** 16+ documentation and structure files
- **Lines of Documentation:** 2000+
- **Code:** Implementation starting
- **Tests:** Coming soon
- **Examples:** Planned

### Goals

- [ ] 100% test coverage for critical paths
- [ ] All tools documented with examples
- [ ] Active community contributions
- [ ] Blog serie completed

## 🤝 Contributing to Structure

If you think the structure could be improved:

1. Open an issue describing the change
2. Explain the benefit
3. Propose migration path (if needed)
4. Wait for discussion before making large changes

## 📞 Questions?

If anything is unclear about the repository structure:
- Check the relevant README in each directory
- Review `PROJECT.md` for context
- Open an issue with the "question" label

---

**Last Updated:** 2025-11-19  
**Maintained by:** Phillipe (RycnCDL)  
**Version:** 0.1.0-alpha

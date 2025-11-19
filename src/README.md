# Source Code

This directory contains the source code for the Microsoft Sentinel MCP Server.

## 📁 Structure

```
src/
├── mcp_server/          # MCP server implementation
│   ├── __init__.py
│   ├── server.py        # Main server logic
│   └── tools/           # MCP tool implementations
├── powershell/          # PowerShell backend modules
│   ├── SentinelManager/
│   └── ...
├── utils/               # Utility functions
│   ├── auth.py          # Authentication helpers
│   ├── logging.py       # Logging configuration
│   └── config.py        # Configuration management
└── tests/               # Test suite
    ├── unit/
    └── integration/
```

## 🚧 Development Status

Source code is currently being developed. Initial implementations coming soon.

## 🛠️ Technology Stack

- **MCP Server:** Python with FastMCP framework
- **Backend Integration:** PowerShell Core
- **Authentication:** Microsoft Authentication Library (MSAL)
- **API Client:** Azure SDK for Python

## 📝 Code Standards

- Follow PEP 8 for Python code
- Use type hints
- Include docstrings for all public functions
- Write tests for new features
- Keep security best practices in mind

## 🧪 Testing

```bash
# Run tests (coming soon)
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 🚀 Quick Links

- [Back to Main README](../README.md)
- [Documentation](../docs/)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

**Status:** In Development | **Last Updated:** 2025-11-19

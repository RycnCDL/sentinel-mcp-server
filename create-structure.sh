#!/bin/bash
# create-structure.sh
# Creates the complete directory structure for sentinel-mcp-server
# Usage: bash create-structure.sh

set -e  # Exit on error

echo "🚀 Creating Microsoft Sentinel MCP Server directory structure..."
echo ""

# Root directories
mkdir -p docs
mkdir -p src/mcp_server/tools/{management,exploration,automation,reporting}
mkdir -p src/powershell/{SentinelManager,Backup,Compliance}
mkdir -p src/utils
mkdir -p src/tests/{unit,integration,e2e,fixtures}
mkdir -p examples/{basic-setup,first-tool,vs-code-integration,multi-tenant-query}
mkdir -p examples/{compliance-check,backup-restore,incident-management,custom-tool}
mkdir -p examples/{powershell-integration,security-copilot-agent,config-templates,azure-lighthouse}
mkdir -p blog/{drafts,published}
mkdir -p config/{example,schemas}
mkdir -p scripts
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

echo "✅ Directory structure created!"
echo ""

# Create __init__.py files for Python packages
echo "📝 Creating Python package files..."
touch src/__init__.py
touch src/mcp_server/__init__.py
touch src/mcp_server/tools/__init__.py
touch src/mcp_server/tools/management/__init__.py
touch src/mcp_server/tools/exploration/__init__.py
touch src/mcp_server/tools/automation/__init__.py
touch src/mcp_server/tools/reporting/__init__.py
touch src/utils/__init__.py
touch src/tests/__init__.py

echo "✅ Python package structure created!"
echo ""

# Create placeholder files for documentation
echo "📚 Creating documentation placeholders..."
touch docs/01-architecture.md
touch docs/02-getting-started.md
touch docs/03-tool-reference.md
touch docs/04-multi-tenant-setup.md
touch docs/05-security-considerations.md
touch docs/06-use-cases.md
touch docs/api-reference.md
touch docs/troubleshooting.md
touch docs/faq.md

echo "✅ Documentation placeholders created!"
echo ""

# Create placeholder files for blog posts
echo "✍️ Creating blog post placeholders..."
touch blog/drafts/post-01-vision.md
touch blog/drafts/post-02-architecture.md
touch blog/drafts/post-03-use-cases.md
touch blog/drafts/post-04-lessons-learned.md

echo "✅ Blog post placeholders created!"
echo ""

# Create example config files
echo "⚙️ Creating configuration templates..."
cat > config/example/.env.example << 'EOF'
# Azure Configuration
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Microsoft Sentinel
SENTINEL_WORKSPACE_ID=your-workspace-id
SENTINEL_SUBSCRIPTION_ID=your-subscription-id
SENTINEL_RESOURCE_GROUP=your-resource-group

# MCP Server
MCP_SERVER_PORT=3000
MCP_SERVER_HOST=localhost

# Logging
LOG_LEVEL=INFO
EOF

cat > config/example/server.example.json << 'EOF'
{
  "server": {
    "name": "sentinel-mcp-server",
    "version": "0.1.0",
    "port": 3000,
    "host": "localhost"
  },
  "azure": {
    "tenantId": "{{ AZURE_TENANT_ID }}",
    "clientId": "{{ AZURE_CLIENT_ID }}",
    "lighthouse": {
      "enabled": true
    }
  },
  "tools": {
    "enabled": [
      "sentinel_health_check",
      "sentinel_compliance_check",
      "sentinel_backup_create"
    ]
  },
  "logging": {
    "level": "INFO",
    "format": "json"
  }
}
EOF

echo "✅ Configuration templates created!"
echo ""

# Create setup script placeholder
cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# Setup script for sentinel-mcp-server
echo "Setting up Microsoft Sentinel MCP Server..."
# TODO: Add setup steps
EOF
chmod +x scripts/setup.sh

echo "✅ Script placeholders created!"
echo ""

# Create GitHub workflow placeholder
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    # TODO: Add test steps
EOF

echo "✅ GitHub Actions workflow created!"
echo ""

echo "🎉 Complete directory structure created successfully!"
echo ""
echo "📁 Structure:"
echo "   - docs/           Documentation files"
echo "   - src/            Source code"
echo "   - examples/       Usage examples"
echo "   - blog/           Blog posts"
echo "   - config/         Configuration templates"
echo "   - scripts/        Utility scripts"
echo "   - .github/        GitHub configuration"
echo ""
echo "Next steps:"
echo "1. Review the structure with: tree -L 2"
echo "2. Copy your downloaded files to this directory"
echo "3. Initialize git: git init"
echo "4. Add files: git add ."
echo "5. Commit: git commit -m 'Initial structure'"
echo "6. Push to GitHub"
echo ""
echo "Happy coding! 🚀"

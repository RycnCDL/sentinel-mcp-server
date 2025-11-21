# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Analytics Rules Exploration**: New tools to list and retrieve detailed information about Sentinel analytics rules
  - `sentinel_list_analytics_rules` - List all analytics rules across workspaces with filtering capabilities
  - `sentinel_get_analytics_rule` - Get detailed rule configuration including detection queries (KQL), entity mappings, and incident settings
- Comprehensive tool reference documentation in `docs/03-tool-reference.md`

### Changed
- Updated README.md to reflect 3 Python tools (was 1)
- Enhanced documentation with detailed examples and use cases for analytics rules

### Technical Details
- New module: `src/mcp_server/tools/exploration/analytics_rules.py`
- Support for all rule types: Scheduled, Fusion, MLBehaviorAnalytics, MicrosoftSecurityIncidentCreation
- Extraction of KQL queries, MITRE ATT&CK mappings, entity configurations, and alert settings

## [0.1.0-alpha] - 2025-11-19

### Added
- Initial project repository setup
- README and project documentation
- Blog serie planning and structure
- Contributing guidelines
- MIT License
- Development directory structure (docs/, src/, examples/, blog/)
- .gitignore for Python, PowerShell, and common IDEs

### Documentation
- PROJECT.md - Comprehensive project planning document
- BLOG-IDEAS.md - Blog serie outlines and content calendar
- README files for all major directories

### Infrastructure
- GitHub repository structure
- Documentation framework
- Example templates structure

---

## Version History

### Version Numbering

- **Major.Minor.Patch** (e.g., 1.2.3)
- **Major:** Breaking changes
- **Minor:** New features, backward compatible
- **Patch:** Bug fixes, backward compatible

### Pre-release Stages

- **alpha:** Early development, unstable
- **beta:** Feature complete, testing phase
- **rc:** Release candidate, final testing

---

## Upcoming Versions

### [0.2.0-alpha] - Planned
- First MCP tool implementation
- PowerShell module integration
- Basic authentication setup
- Development environment documentation

### [0.3.0-alpha] - Planned
- Additional priority tools
- Multi-tenant support
- Testing framework
- First blog post publication

### [1.0.0] - Future
- Production-ready release
- Complete tool suite
- Comprehensive documentation
- Security audit completed

---

**Note:** This changelog will be updated as the project progresses.

[Unreleased]: https://github.com/RycnCDL/sentinel-mcp-server/compare/v0.1.0-alpha...HEAD
[0.1.0-alpha]: https://github.com/RycnCDL/sentinel-mcp-server/releases/tag/v0.1.0-alpha

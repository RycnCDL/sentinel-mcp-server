# Tool Reference

This document provides detailed information about all available MCP tools in the Microsoft Sentinel MCP Server.

## Python-Based Tools

### Health Monitoring

#### `sentinel_health_check`

Check health status of Microsoft Sentinel workspaces across tenants.

**Parameters:**
- `tenant_scope` (string, optional): Scope of tenants to check. Use "all" for all tenants, or provide a tenant name to filter. Default: "all"
- `check_depth` (string, optional): Depth of the health check. Options:
  - `"quick"`: Fast check of connectors and rules
  - `"detailed"`: Includes data ingestion metrics (slower)
  - Default: "quick"

**Returns:**
- `summary`: Overall health summary with counts and status
- `workspaces`: List of individual workspace health check results

**Examples:**
```python
# Check all workspaces (quick)
sentinel_health_check()

# Check specific tenant (detailed)
sentinel_health_check(tenant_scope="Customer A", check_depth="detailed")
```

---

### Analytics Rules Exploration

#### `sentinel_list_analytics_rules`

List Microsoft Sentinel Analytics Rules across workspaces.

**Description:**
Retrieves all analytics rules (detection rules) from your Sentinel workspaces, showing their names, configurations, and status. Analytics rules are the detection logic that creates alerts and incidents when threats are detected.

**Parameters:**
- `workspace_filter` (string, optional): Optional workspace name filter. Only workspaces matching this string will be included. Default: "" (all workspaces)
- `tenant_filter` (string, optional): Optional tenant name filter. Only tenants matching this string will be included. Default: "" (all tenants)
- `enabled_only` (boolean, optional): If True, only return enabled rules. If False, return all rules. Default: False

**Returns:**
- `timestamp`: When the query was executed
- `workspaces_queried`: Number of workspaces checked
- `total_rules`: Total number of rules found
- `workspaces`: List of workspaces with their rules:
  - `workspace_name`: Name of the workspace
  - `tenant_name`: Name of the tenant
  - `rules_count`: Number of rules in this workspace
  - `rules`: List of rule objects with:
    - `rule_id`: Unique identifier
    - `rule_name`: Display name of the rule
    - `kind`: Type of rule (Scheduled, Fusion, MLBehaviorAnalytics, etc.)
    - `enabled`: Whether the rule is currently enabled
    - `severity`: Alert severity (High, Medium, Low, Informational)
    - `tactics`: MITRE ATT&CK tactics
    - `description`: Rule description
    - `last_modified`: When the rule was last modified

**Examples:**
```python
# List all analytics rules
sentinel_list_analytics_rules()

# List only enabled rules
sentinel_list_analytics_rules(enabled_only=True)

# List rules for a specific tenant
sentinel_list_analytics_rules(tenant_filter="Customer A")

# List rules for a specific workspace
sentinel_list_analytics_rules(workspace_filter="prod-sentinel")
```

**Use Cases:**
- Audit which detection rules are enabled/disabled across tenants
- Review rule coverage by MITRE ATT&CK tactics
- Identify rules that need configuration updates
- Generate compliance reports on detection capabilities

---

#### `sentinel_get_analytics_rule`

Get detailed information about a specific Microsoft Sentinel Analytics Rule.

**Description:**
Retrieves comprehensive details about a single analytics rule, including:
- Full rule configuration
- Detection query (KQL) for scheduled rules
- Entity mappings
- Incident creation settings
- Alert grouping configuration
- Custom details and overrides

Use this after listing rules to get the complete detection logic and configuration.

**Parameters:**
- `workspace_name` (string, required): Name of the Sentinel workspace containing the rule. Use the exact workspace name from `sentinel_list_analytics_rules`.
- `rule_id` (string, required): The rule ID to retrieve. Use the rule_id from `sentinel_list_analytics_rules`.

**Returns:**
- `timestamp`: When the query was executed
- `rule`: Detailed rule object with:
  - `rule_id`: Unique identifier
  - `rule_name`: Display name
  - `kind`: Rule type (Scheduled, Fusion, etc.)
  - `enabled`: Whether rule is enabled
  - `severity`: Alert severity
  - `tactics`: MITRE ATT&CK tactics
  - `techniques`: MITRE ATT&CK techniques
  - `description`: Rule description
  - `configuration`: Rule-specific configuration:
    - For Scheduled rules:
      - `query`: The KQL detection query
      - `query_frequency`: How often the query runs
      - `query_period`: Time window for the query
      - `trigger_operator`: Threshold operator
      - `trigger_threshold`: Alert threshold
  - `incident_configuration`: Settings for incident creation
  - `entity_mappings`: How entities are extracted from alerts
  - `alert_details_override`: Custom alert formatting
  - `custom_details`: Additional custom fields

**Examples:**
```python
# Get details for a specific rule
sentinel_get_analytics_rule(
    workspace_name="prod-sentinel",
    rule_id="12345678-1234-1234-1234-123456789012"
)
```

**Use Cases:**
- Review detection query logic (KQL) for a specific rule
- Understand how entities are mapped from alerts
- Audit incident creation and grouping settings
- Export rule configurations for documentation
- Compare rule settings across environments

---

## PowerShell-Based Tools

For PowerShell tools documentation, see [PowerShell Integration Guide](powershell-integration.md).

### Categories:
- **Table Management**: Create, list, delete, and manage custom log tables
- **Watchlist Management**: Manage threat intelligence watchlists
- **Analytics Rule Management**: Create and manage analytics rules (via PowerShell)
- **Incident Management**: Query and manage security incidents
- **Threat Intelligence**: Manage threat indicators
- **Data Connector Management**: Configure and manage data connectors
- **Workspace Configuration**: Manage workspace settings and configurations

---

## Error Handling

All tools implement comprehensive error handling:

- **Authentication Errors**: Returned when Azure credentials are invalid
- **Permission Errors**: Returned when access to workspaces is denied
- **Not Found Errors**: Returned when requested resources don't exist
- **Validation Errors**: Returned when input parameters are invalid

Error responses include:
- `error`: Human-readable error message
- `timestamp`: When the error occurred
- Partial results when some operations succeed

---

## Best Practices

### Performance
- Use `enabled_only=True` when you only need active rules
- Use workspace/tenant filters to limit scope
- Use `check_depth="quick"` for health checks when you don't need ingestion metrics

### Security
- All tools respect Azure RBAC permissions
- Credentials are managed via Azure Identity
- Logs are structured and include audit trails

### Multi-Tenant Operations
- Always specify tenant filters when working with specific customers
- Use workspace filters to target specific environments (prod/dev/test)
- Review permissions before running operations across all tenants

---

## Next Steps

- See [Getting Started Guide](02-getting-started.md) for setup instructions
- Review [Use Cases](06-use-cases.md) for practical examples
- Check [API Reference](api-reference.md) for detailed API documentation

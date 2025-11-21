"""
Sentinel Analytics Rules Tool

Provides functionality to explore and retrieve Microsoft Sentinel Analytics Rules:
- List all analytics rules with basic information
- Get detailed rule configuration and detection logic
- Filter rules by status, type, or workspace
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import structlog
from azure.mgmt.securityinsight import SecurityInsights
from azure.core.exceptions import AzureError

from utils.lighthouse import SentinelWorkspace, LighthouseManager
from utils.auth import AzureAuthenticator

logger = structlog.get_logger(__name__)


class AnalyticsRulesExplorer:
    """Explores and retrieves Analytics Rules from Sentinel workspaces"""

    def __init__(self, authenticator: AzureAuthenticator):
        """
        Initialize Analytics Rules Explorer

        Args:
            authenticator: AzureAuthenticator instance
        """
        self.authenticator = authenticator
        self.credential = authenticator.get_credential()

    async def list_rules(
        self,
        workspace: SentinelWorkspace,
        enabled_only: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        List all analytics rules in a workspace

        Args:
            workspace: SentinelWorkspace to query
            enabled_only: If True, only return enabled rules

        Returns:
            List of rule summaries with basic information
        """
        logger.info(
            "Listing analytics rules",
            workspace_name=workspace.workspace_name,
            enabled_only=enabled_only,
        )

        try:
            sentinel_client = SecurityInsights(
                self.credential,
                workspace.subscription_id,
            )

            # Get all alert rules
            rules = list(
                sentinel_client.alert_rules.list(
                    resource_group_name=workspace.resource_group,
                    workspace_name=workspace.workspace_name,
                )
            )

            logger.info(
                "Retrieved analytics rules",
                workspace_name=workspace.workspace_name,
                total_count=len(rules),
            )

            # Process rules into a standardized format
            rule_list = []
            for rule in rules:
                # Filter by enabled status if requested
                enabled = getattr(rule, "enabled", False)
                if enabled_only and not enabled:
                    continue

                rule_info = self._extract_rule_summary(rule, workspace)
                rule_list.append(rule_info)

            logger.info(
                "Analytics rules processed",
                workspace_name=workspace.workspace_name,
                returned_count=len(rule_list),
            )

            return rule_list

        except Exception as e:
            logger.error(
                "Failed to list analytics rules",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            raise

    async def get_rule_details(
        self,
        workspace: SentinelWorkspace,
        rule_id: str,
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific analytics rule

        Args:
            workspace: SentinelWorkspace containing the rule
            rule_id: The rule ID (name) to retrieve

        Returns:
            Detailed rule information including configuration and detection logic
        """
        logger.info(
            "Getting rule details",
            workspace_name=workspace.workspace_name,
            rule_id=rule_id,
        )

        try:
            sentinel_client = SecurityInsights(
                self.credential,
                workspace.subscription_id,
            )

            # Get the specific rule
            rule = sentinel_client.alert_rules.get(
                resource_group_name=workspace.resource_group,
                workspace_name=workspace.workspace_name,
                rule_id=rule_id,
            )

            logger.info(
                "Retrieved rule details",
                workspace_name=workspace.workspace_name,
                rule_id=rule_id,
            )

            # Extract detailed information
            rule_details = self._extract_rule_details(rule, workspace)

            return rule_details

        except Exception as e:
            logger.error(
                "Failed to get rule details",
                workspace_name=workspace.workspace_name,
                rule_id=rule_id,
                error=str(e),
            )
            raise

    def _extract_rule_summary(
        self, rule: Any, workspace: SentinelWorkspace
    ) -> Dict[str, Any]:
        """
        Extract summary information from a rule object

        Args:
            rule: Alert rule object from Azure SDK
            workspace: SentinelWorkspace the rule belongs to

        Returns:
            Dictionary with rule summary information
        """
        # Get the rule kind (type)
        kind = getattr(rule, "kind", "Unknown")

        # Basic information available for all rule types
        summary = {
            "rule_id": rule.name,
            "rule_name": getattr(rule, "display_name", rule.name),
            "kind": kind,
            "enabled": getattr(rule, "enabled", False),
            "workspace_name": workspace.workspace_name,
            "workspace_id": workspace.workspace_id,
        }

        # Add type-specific information
        if hasattr(rule, "severity"):
            summary["severity"] = rule.severity

        if hasattr(rule, "tactics"):
            summary["tactics"] = rule.tactics if rule.tactics else []

        if hasattr(rule, "techniques"):
            summary["techniques"] = rule.techniques if rule.techniques else []

        if hasattr(rule, "description"):
            summary["description"] = rule.description

        if hasattr(rule, "last_modified_utc"):
            summary["last_modified"] = rule.last_modified_utc.isoformat() if rule.last_modified_utc else None

        return summary

    def _extract_rule_details(
        self, rule: Any, workspace: SentinelWorkspace
    ) -> Dict[str, Any]:
        """
        Extract detailed information from a rule object

        Args:
            rule: Alert rule object from Azure SDK
            workspace: SentinelWorkspace the rule belongs to

        Returns:
            Dictionary with detailed rule information
        """
        # Start with summary information
        details = self._extract_rule_summary(rule, workspace)

        # Get the rule kind
        kind = getattr(rule, "kind", "Unknown")

        # Add detailed configuration based on rule type
        details["configuration"] = {}

        # Scheduled query rules (most common type)
        if kind == "Scheduled":
            if hasattr(rule, "query"):
                details["configuration"]["query"] = rule.query

            if hasattr(rule, "query_frequency"):
                details["configuration"]["query_frequency"] = str(rule.query_frequency)

            if hasattr(rule, "query_period"):
                details["configuration"]["query_period"] = str(rule.query_period)

            if hasattr(rule, "trigger_operator"):
                details["configuration"]["trigger_operator"] = rule.trigger_operator

            if hasattr(rule, "trigger_threshold"):
                details["configuration"]["trigger_threshold"] = rule.trigger_threshold

            if hasattr(rule, "suppression_enabled"):
                details["configuration"]["suppression_enabled"] = rule.suppression_enabled

            if hasattr(rule, "suppression_duration"):
                details["configuration"]["suppression_duration"] = str(rule.suppression_duration)

        # Microsoft Security Incident Creation rules
        elif kind == "MicrosoftSecurityIncidentCreation":
            if hasattr(rule, "product_filter"):
                details["configuration"]["product_filter"] = rule.product_filter

            if hasattr(rule, "display_name_filter"):
                details["configuration"]["display_name_filter"] = rule.display_name_filter

        # Fusion rules
        elif kind == "Fusion":
            if hasattr(rule, "alert_rule_template_name"):
                details["configuration"]["template_name"] = rule.alert_rule_template_name

        # Machine Learning Behavioral Analytics
        elif kind == "MLBehaviorAnalytics":
            if hasattr(rule, "alert_rule_template_name"):
                details["configuration"]["template_name"] = rule.alert_rule_template_name

        # Add incident configuration if available
        if hasattr(rule, "incident_configuration"):
            incident_config = rule.incident_configuration
            details["incident_configuration"] = {
                "create_incident": getattr(incident_config, "create_incident", False),
            }

            if hasattr(incident_config, "grouping_configuration"):
                grouping = incident_config.grouping_configuration
                details["incident_configuration"]["grouping"] = {
                    "enabled": getattr(grouping, "enabled", False),
                    "reopen_closed_incidents": getattr(grouping, "reopen_closed_incident", False),
                    "lookback_duration": str(getattr(grouping, "lookback_duration", "PT5H")),
                    "matching_method": getattr(grouping, "matching_method", "AllEntities"),
                }

                if hasattr(grouping, "group_by_entities"):
                    details["incident_configuration"]["grouping"]["group_by_entities"] = grouping.group_by_entities

                if hasattr(grouping, "group_by_alert_details"):
                    details["incident_configuration"]["grouping"]["group_by_alert_details"] = grouping.group_by_alert_details

        # Add alert details configuration if available
        if hasattr(rule, "alert_details_override"):
            alert_override = rule.alert_details_override
            details["alert_details_override"] = {}

            if hasattr(alert_override, "alert_display_name_format"):
                details["alert_details_override"]["display_name_format"] = alert_override.alert_display_name_format

            if hasattr(alert_override, "alert_description_format"):
                details["alert_details_override"]["description_format"] = alert_override.alert_description_format

            if hasattr(alert_override, "alert_severity_column_name"):
                details["alert_details_override"]["severity_column"] = alert_override.alert_severity_column_name

            if hasattr(alert_override, "alert_tactics_column_name"):
                details["alert_details_override"]["tactics_column"] = alert_override.alert_tactics_column_name

        # Add entity mappings if available
        if hasattr(rule, "entity_mappings") and rule.entity_mappings:
            details["entity_mappings"] = []
            for mapping in rule.entity_mappings:
                entity_map = {
                    "entity_type": getattr(mapping, "entity_type", None),
                    "field_mappings": []
                }

                if hasattr(mapping, "field_mappings"):
                    for field_map in mapping.field_mappings:
                        entity_map["field_mappings"].append({
                            "identifier": getattr(field_map, "identifier", None),
                            "column_name": getattr(field_map, "column_name", None),
                        })

                details["entity_mappings"].append(entity_map)

        # Add custom details if available
        if hasattr(rule, "custom_details") and rule.custom_details:
            details["custom_details"] = dict(rule.custom_details)

        return details


async def list_analytics_rules(
    authenticator: AzureAuthenticator,
    lighthouse_manager: LighthouseManager,
    workspace_filter: Optional[str] = None,
    tenant_filter: Optional[str] = None,
    enabled_only: bool = False,
) -> Dict[str, Any]:
    """
    List analytics rules across workspaces

    Args:
        authenticator: AzureAuthenticator instance
        lighthouse_manager: LighthouseManager instance
        workspace_filter: Optional workspace name filter
        tenant_filter: Optional tenant name filter
        enabled_only: If True, only return enabled rules

    Returns:
        Dictionary containing rules grouped by workspace
    """
    logger.info(
        "Listing analytics rules across workspaces",
        workspace_filter=workspace_filter,
        tenant_filter=tenant_filter,
        enabled_only=enabled_only,
    )

    explorer = AnalyticsRulesExplorer(authenticator)

    # Get workspaces
    workspaces = await lighthouse_manager.get_sentinel_workspaces()

    # Apply filters
    if tenant_filter:
        workspaces = [
            ws
            for ws in workspaces
            if ws.tenant_name and tenant_filter.lower() in ws.tenant_name.lower()
        ]

    if workspace_filter:
        workspaces = [
            ws
            for ws in workspaces
            if workspace_filter.lower() in ws.workspace_name.lower()
        ]

    logger.info("Workspaces to query", count=len(workspaces))

    # Collect rules from all workspaces
    results = []
    total_rules = 0

    for workspace in workspaces:
        try:
            rules = await explorer.list_rules(workspace, enabled_only=enabled_only)

            workspace_result = {
                "workspace_name": workspace.workspace_name,
                "workspace_id": workspace.workspace_id,
                "tenant_name": workspace.tenant_name,
                "rules_count": len(rules),
                "rules": rules,
            }

            results.append(workspace_result)
            total_rules += len(rules)

        except Exception as e:
            logger.error(
                "Failed to list rules for workspace",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            results.append({
                "workspace_name": workspace.workspace_name,
                "workspace_id": workspace.workspace_id,
                "tenant_name": workspace.tenant_name,
                "rules_count": 0,
                "rules": [],
                "error": str(e),
            })

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "workspaces_queried": len(workspaces),
        "total_rules": total_rules,
        "enabled_only": enabled_only,
        "workspaces": results,
    }


async def get_analytics_rule_details(
    authenticator: AzureAuthenticator,
    lighthouse_manager: LighthouseManager,
    workspace_name: str,
    rule_id: str,
) -> Dict[str, Any]:
    """
    Get detailed information about a specific analytics rule

    Args:
        authenticator: AzureAuthenticator instance
        lighthouse_manager: LighthouseManager instance
        workspace_name: Name of the workspace containing the rule
        rule_id: The rule ID to retrieve

    Returns:
        Detailed rule information

    Raises:
        ValueError: If workspace not found
    """
    logger.info(
        "Getting analytics rule details",
        workspace_name=workspace_name,
        rule_id=rule_id,
    )

    explorer = AnalyticsRulesExplorer(authenticator)

    # Find the workspace
    workspaces = await lighthouse_manager.get_sentinel_workspaces()
    workspace = None

    for ws in workspaces:
        if ws.workspace_name.lower() == workspace_name.lower():
            workspace = ws
            break

    if not workspace:
        raise ValueError(f"Workspace '{workspace_name}' not found")

    # Get rule details
    rule_details = await explorer.get_rule_details(workspace, rule_id)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "rule": rule_details,
    }

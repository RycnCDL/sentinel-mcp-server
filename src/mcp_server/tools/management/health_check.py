"""
Sentinel Health Check Tool

Checks the health status of Microsoft Sentinel workspaces including:
- Data connector status
- Analytics rules status
- Data ingestion metrics
- Overall workspace health
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import structlog
from azure.mgmt.securityinsight import SecurityInsights
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.core.exceptions import AzureError

from utils.lighthouse import SentinelWorkspace, LighthouseManager
from utils.auth import AzureAuthenticator

logger = structlog.get_logger(__name__)


class HealthStatus(str, Enum):
    """Health status levels"""

    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"


class SentinelHealthChecker:
    """Performs health checks on Sentinel workspaces"""

    def __init__(self, authenticator: AzureAuthenticator):
        """
        Initialize health checker

        Args:
            authenticator: AzureAuthenticator instance
        """
        self.authenticator = authenticator
        self.credential = authenticator.get_credential()

    async def check_workspace_health(
        self, workspace: SentinelWorkspace, check_depth: str = "quick"
    ) -> Dict[str, Any]:
        """
        Check health of a single workspace

        Args:
            workspace: SentinelWorkspace to check
            check_depth: Depth of check ("quick" or "detailed")

        Returns:
            Health check result dictionary
        """
        logger.info(
            "Starting health check",
            workspace_name=workspace.workspace_name,
            check_depth=check_depth,
        )

        result = {
            "workspace_id": workspace.workspace_id,
            "workspace_name": workspace.workspace_name,
            "tenant_name": workspace.tenant_name,
            "subscription_id": workspace.subscription_id,
            "resource_group": workspace.resource_group,
            "timestamp": datetime.utcnow().isoformat(),
            "status": HealthStatus.UNKNOWN,
            "issues": [],
            "metrics": {},
        }

        try:
            # Initialize clients
            sentinel_client = SecurityInsights(
                self.credential,
                workspace.subscription_id,
            )

            # Check data connectors
            connector_status = await self._check_data_connectors(
                sentinel_client, workspace
            )
            result["metrics"]["data_connectors"] = connector_status

            # Check analytics rules
            rules_status = await self._check_analytics_rules(sentinel_client, workspace)
            result["metrics"]["analytics_rules"] = rules_status

            # Check data ingestion (if detailed check)
            if check_depth == "detailed":
                ingestion_status = await self._check_data_ingestion(workspace)
                result["metrics"]["data_ingestion"] = ingestion_status

            # Determine overall status
            result["status"] = self._calculate_overall_status(result["metrics"])

            logger.info(
                "Health check completed",
                workspace_name=workspace.workspace_name,
                status=result["status"],
            )

        except Exception as e:
            logger.error(
                "Health check failed",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            result["status"] = HealthStatus.ERROR
            result["issues"].append(
                {
                    "type": "health_check_error",
                    "message": f"Health check failed: {str(e)}",
                    "severity": "high",
                }
            )

        return result

    async def _check_data_connectors(
        self, sentinel_client: SecurityInsights, workspace: SentinelWorkspace
    ) -> Dict[str, Any]:
        """Check data connectors status"""
        try:
            connectors = list(
                sentinel_client.data_connectors.list(
                    resource_group_name=workspace.resource_group,
                    workspace_name=workspace.workspace_name,
                )
            )

            total_count = len(connectors)
            # Note: Actual connector health requires querying data tables
            # For quick check, we just count connectors

            logger.info(
                "Data connectors checked",
                workspace_name=workspace.workspace_name,
                count=total_count,
            )

            return {
                "total": total_count,
                "status": "checked",
            }

        except Exception as e:
            logger.error(
                "Failed to check data connectors",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            return {
                "total": 0,
                "status": "error",
                "error": str(e),
            }

    async def _check_analytics_rules(
        self, sentinel_client: SecurityInsights, workspace: SentinelWorkspace
    ) -> Dict[str, Any]:
        """Check analytics rules status"""
        try:
            # Get alert rules
            rules = list(
                sentinel_client.alert_rules.list(
                    resource_group_name=workspace.resource_group,
                    workspace_name=workspace.workspace_name,
                )
            )

            total_count = len(rules)
            enabled_count = sum(
                1 for rule in rules if getattr(rule, "enabled", False)
            )
            disabled_count = total_count - enabled_count

            logger.info(
                "Analytics rules checked",
                workspace_name=workspace.workspace_name,
                total=total_count,
                enabled=enabled_count,
                disabled=disabled_count,
            )

            return {
                "total": total_count,
                "enabled": enabled_count,
                "disabled": disabled_count,
                "status": "checked",
            }

        except Exception as e:
            logger.error(
                "Failed to check analytics rules",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            return {
                "total": 0,
                "enabled": 0,
                "disabled": 0,
                "status": "error",
                "error": str(e),
            }

    async def _check_data_ingestion(
        self, workspace: SentinelWorkspace
    ) -> Dict[str, Any]:
        """Check data ingestion over last 24 hours"""
        try:
            logs_client = LogsQueryClient(self.credential)

            # KQL query to check ingestion
            query = """
            Usage
            | where TimeGenerated > ago(24h)
            | summarize TotalGB = sum(Quantity) / 1000
            """

            # Query the workspace
            response = logs_client.query_workspace(
                workspace_id=workspace.workspace_id.split("/")[-1],  # Extract ID
                query=query,
                timespan=timedelta(days=1),
            )

            if response.status == LogsQueryStatus.SUCCESS:
                table = response.tables[0]
                total_gb = 0

                if table.rows:
                    total_gb = float(table.rows[0][0]) if table.rows[0][0] else 0

                logger.info(
                    "Data ingestion checked",
                    workspace_name=workspace.workspace_name,
                    total_gb=total_gb,
                )

                return {
                    "last_24h_gb": round(total_gb, 2),
                    "status": "checked",
                }
            else:
                return {
                    "last_24h_gb": 0,
                    "status": "partial",
                    "message": "Query did not complete successfully",
                }

        except Exception as e:
            logger.error(
                "Failed to check data ingestion",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            return {
                "last_24h_gb": 0,
                "status": "error",
                "error": str(e),
            }

    def _calculate_overall_status(self, metrics: Dict[str, Any]) -> HealthStatus:
        """
        Calculate overall health status from metrics

        Args:
            metrics: Health check metrics

        Returns:
            Overall HealthStatus
        """
        # Check for any errors
        for metric_name, metric_data in metrics.items():
            if isinstance(metric_data, dict):
                if metric_data.get("status") == "error":
                    return HealthStatus.ERROR

        # Check for warnings
        rules = metrics.get("analytics_rules", {})
        if rules.get("total", 0) == 0:
            return HealthStatus.WARNING

        connectors = metrics.get("data_connectors", {})
        if connectors.get("total", 0) == 0:
            return HealthStatus.WARNING

        # If no errors or warnings, status is healthy
        return HealthStatus.HEALTHY


async def check_sentinel_health(
    authenticator: AzureAuthenticator,
    lighthouse_manager: LighthouseManager,
    tenant_scope: Optional[str] = None,
    check_depth: str = "quick",
) -> Dict[str, Any]:
    """
    Check health of Sentinel workspaces

    Args:
        authenticator: AzureAuthenticator instance
        lighthouse_manager: LighthouseManager instance
        tenant_scope: Optional tenant filter ("all" or tenant name)
        check_depth: Check depth ("quick" or "detailed")

    Returns:
        Health check results for all workspaces
    """
    logger.info(
        "Starting multi-workspace health check",
        tenant_scope=tenant_scope or "all",
        check_depth=check_depth,
    )

    health_checker = SentinelHealthChecker(authenticator)

    # Get workspaces
    workspaces = await lighthouse_manager.get_sentinel_workspaces()

    # Filter by tenant if specified
    if tenant_scope and tenant_scope != "all":
        workspaces = [
            ws
            for ws in workspaces
            if ws.tenant_name
            and tenant_scope.lower() in ws.tenant_name.lower()
        ]

    logger.info("Workspaces to check", count=len(workspaces))

    # Check health for each workspace
    results = []
    for workspace in workspaces:
        result = await health_checker.check_workspace_health(workspace, check_depth)
        results.append(result)

    # Calculate summary
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "tenants_checked": len(set(ws.tenant_id for ws in workspaces)),
        "workspaces_checked": len(results),
        "overall_status": _calculate_summary_status(results),
        "status_breakdown": {
            "healthy": sum(1 for r in results if r["status"] == HealthStatus.HEALTHY),
            "warning": sum(1 for r in results if r["status"] == HealthStatus.WARNING),
            "error": sum(1 for r in results if r["status"] == HealthStatus.ERROR),
            "unknown": sum(1 for r in results if r["status"] == HealthStatus.UNKNOWN),
        },
    }

    return {"summary": summary, "workspaces": results}


def _calculate_summary_status(results: List[Dict[str, Any]]) -> str:
    """Calculate overall summary status"""
    if any(r["status"] == HealthStatus.ERROR for r in results):
        return "degraded"
    if any(r["status"] == HealthStatus.WARNING for r in results):
        return "warning"
    if all(r["status"] == HealthStatus.HEALTHY for r in results):
        return "healthy"
    return "unknown"

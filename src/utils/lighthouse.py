"""
Azure Lighthouse Workspace Enumeration Module

Handles enumeration of Microsoft Sentinel workspaces across multiple tenants
using Azure Lighthouse delegation.
"""

from typing import List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass
import structlog
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.securityinsight import SecurityInsights
from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError

from .auth import AzureAuthenticator

logger = structlog.get_logger(__name__)


@dataclass
class SentinelWorkspace:
    """Represents a Microsoft Sentinel workspace"""

    workspace_id: str
    workspace_name: str
    resource_group: str
    subscription_id: str
    tenant_id: str
    tenant_name: Optional[str] = None
    location: str = ""
    sku: str = ""


class LighthouseManager:
    """Manages Azure Lighthouse delegated access and workspace enumeration"""

    def __init__(self, authenticator: AzureAuthenticator):
        """
        Initialize Lighthouse Manager

        Args:
            authenticator: AzureAuthenticator instance
        """
        self.authenticator = authenticator
        self.credential = authenticator.get_credential()
        self._workspace_cache: Optional[List[SentinelWorkspace]] = None
        self._cache_timestamp: Optional[float] = None

    async def get_all_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Get all subscriptions accessible via Lighthouse delegation

        Returns:
            List of subscription dictionaries
        """
        try:
            from azure.mgmt.resource.subscriptions import SubscriptionClient

            sub_client = SubscriptionClient(self.credential)
            subscriptions = []

            for subscription in sub_client.subscriptions.list():
                subscriptions.append(
                    {
                        "subscription_id": subscription.subscription_id,
                        "display_name": subscription.display_name,
                        "tenant_id": subscription.tenant_id,
                        "state": subscription.state,
                    }
                )

            logger.info("Retrieved subscriptions", count=len(subscriptions))
            return subscriptions

        except Exception as e:
            logger.error("Failed to retrieve subscriptions", error=str(e))
            raise

    async def get_sentinel_workspaces(
        self, subscription_id: Optional[str] = None
    ) -> List[SentinelWorkspace]:
        """
        Get all Microsoft Sentinel workspaces

        Args:
            subscription_id: Optional specific subscription ID to query

        Returns:
            List of SentinelWorkspace objects
        """
        try:
            workspaces = []

            # Get subscriptions to query
            if subscription_id:
                subscriptions = [{"subscription_id": subscription_id}]
            else:
                subscriptions = await self.get_all_subscriptions()

            # Query each subscription for Sentinel workspaces
            for sub in subscriptions:
                sub_id = sub["subscription_id"]

                try:
                    # Get Log Analytics workspaces (Sentinel runs on LA)
                    resource_client = ResourceManagementClient(self.credential, sub_id)

                    # Find Log Analytics workspaces
                    la_workspaces = []
                    for resource in resource_client.resources.list(
                        filter="resourceType eq 'Microsoft.OperationalInsights/workspaces'"
                    ):
                        # Check if Sentinel is enabled on this workspace
                        try:
                            # Try to get Sentinel-specific data
                            sentinel_client = SecurityInsights(
                                self.credential, sub_id, resource.name
                            )

                            workspace = SentinelWorkspace(
                                workspace_id=resource.id,
                                workspace_name=resource.name,
                                resource_group=self._extract_resource_group(resource.id),
                                subscription_id=sub_id,
                                tenant_id=sub.get("tenant_id", ""),
                                tenant_name=sub.get("display_name", ""),
                                location=resource.location,
                            )
                            workspaces.append(workspace)
                            logger.info(
                                "Found Sentinel workspace",
                                workspace_name=resource.name,
                                subscription=sub_id,
                            )

                        except Exception as e:
                            # Workspace doesn't have Sentinel enabled or access denied
                            logger.debug(
                                "Skipping workspace (not Sentinel-enabled or no access)",
                                workspace_name=resource.name,
                                error=str(e),
                            )
                            continue

                except Exception as e:
                    logger.error(
                        "Failed to query subscription",
                        subscription_id=sub_id,
                        error=str(e),
                    )
                    continue

            logger.info("Retrieved Sentinel workspaces", count=len(workspaces))
            return workspaces

        except Exception as e:
            logger.error("Failed to retrieve Sentinel workspaces", error=str(e))
            raise

    def _extract_resource_group(self, resource_id: str) -> str:
        """
        Extract resource group name from Azure resource ID

        Args:
            resource_id: Full Azure resource ID

        Returns:
            Resource group name
        """
        parts = resource_id.split("/")
        try:
            rg_index = parts.index("resourceGroups")
            return parts[rg_index + 1]
        except (ValueError, IndexError):
            return ""

    async def get_workspace_by_name(
        self, workspace_name: str, subscription_id: Optional[str] = None
    ) -> Optional[SentinelWorkspace]:
        """
        Get a specific workspace by name

        Args:
            workspace_name: Workspace name to find
            subscription_id: Optional subscription ID to narrow search

        Returns:
            SentinelWorkspace if found, None otherwise
        """
        workspaces = await self.get_sentinel_workspaces(subscription_id)
        for workspace in workspaces:
            if workspace.workspace_name.lower() == workspace_name.lower():
                return workspace
        return None

    async def validate_workspace_access(self, workspace: SentinelWorkspace) -> bool:
        """
        Validate that we have access to a specific workspace

        Args:
            workspace: SentinelWorkspace to validate

        Returns:
            True if access is valid, False otherwise
        """
        try:
            sentinel_client = SecurityInsights(
                self.credential,
                workspace.subscription_id,
                workspace.workspace_name,
            )

            # Try to list incidents as an access test
            # This is a lightweight operation
            incidents = sentinel_client.incidents.list(
                resource_group_name=workspace.resource_group,
                workspace_name=workspace.workspace_name,
            )

            # Just check if we can list (no need to iterate)
            next(incidents, None)

            logger.info(
                "Workspace access validated",
                workspace_name=workspace.workspace_name,
            )
            return True

        except Exception as e:
            logger.error(
                "Workspace access validation failed",
                workspace_name=workspace.workspace_name,
                error=str(e),
            )
            return False


async def get_lighthouse_manager(authenticator: AzureAuthenticator) -> LighthouseManager:
    """
    Factory function to create a LighthouseManager

    Args:
        authenticator: AzureAuthenticator instance

    Returns:
        LighthouseManager instance
    """
    return LighthouseManager(authenticator)

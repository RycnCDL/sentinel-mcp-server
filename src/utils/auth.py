"""
Azure Authentication Module

Handles authentication to Azure using:
- Service Principal (Client ID + Secret)
- Managed Identity (for Azure-hosted deployments)
- Azure CLI (for local development)
"""

import os
from typing import Optional
import structlog
from azure.identity import (
    DefaultAzureCredential,
    ClientSecretCredential,
    AzureCliCredential,
    ManagedIdentityCredential,
    ChainedTokenCredential,
)
from azure.core.credentials import TokenCredential

logger = structlog.get_logger(__name__)


class AzureAuthenticator:
    """Manages Azure authentication across different methods"""

    def __init__(
        self,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        use_managed_identity: bool = False,
    ):
        """
        Initialize Azure Authenticator

        Args:
            tenant_id: Azure AD Tenant ID
            client_id: Service Principal Client ID
            client_secret: Service Principal Client Secret
            use_managed_identity: Use Managed Identity instead
        """
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
        self.use_managed_identity = use_managed_identity or os.getenv(
            "AZURE_USE_MANAGED_IDENTITY", "false"
        ).lower() == "true"

        self._credential: Optional[TokenCredential] = None
        logger.info("Azure Authenticator initialized")

    def get_credential(self) -> TokenCredential:
        """
        Get Azure credentials using the configured authentication method

        Returns:
            TokenCredential: Azure credential object

        The authentication priority is:
        1. Service Principal (if tenant_id, client_id, client_secret provided)
        2. Managed Identity (if use_managed_identity is True)
        3. Azure CLI (fallback for local development)
        """
        if self._credential:
            return self._credential

        credentials = []

        # Option 1: Service Principal
        if self.tenant_id and self.client_id and self.client_secret:
            logger.info(
                "Using Service Principal authentication",
                tenant_id=self.tenant_id,
                client_id=self.client_id[:8] + "...",
            )
            credentials.append(
                ClientSecretCredential(
                    tenant_id=self.tenant_id,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )

        # Option 2: Managed Identity
        if self.use_managed_identity:
            logger.info("Using Managed Identity authentication")
            credentials.append(ManagedIdentityCredential())

        # Option 3: Azure CLI (fallback)
        logger.info("Adding Azure CLI authentication as fallback")
        credentials.append(AzureCliCredential())

        # Create chained credential that tries each method in order
        if len(credentials) > 1:
            self._credential = ChainedTokenCredential(*credentials)
            logger.info(
                "Using ChainedTokenCredential",
                methods=len(credentials),
            )
        else:
            self._credential = credentials[0] if credentials else DefaultAzureCredential()

        return self._credential

    def validate_authentication(self) -> bool:
        """
        Validate that authentication is working

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            credential = self.get_credential()
            # Try to get a token for Azure Resource Manager
            token = credential.get_token("https://management.azure.com/.default")
            logger.info("Authentication validation successful")
            return True
        except Exception as e:
            logger.error("Authentication validation failed", error=str(e))
            return False


def get_authenticator(
    tenant_id: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> AzureAuthenticator:
    """
    Factory function to create and return an AzureAuthenticator instance

    Args:
        tenant_id: Azure AD Tenant ID
        client_id: Service Principal Client ID
        client_secret: Service Principal Client Secret

    Returns:
        AzureAuthenticator: Configured authenticator instance
    """
    return AzureAuthenticator(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )

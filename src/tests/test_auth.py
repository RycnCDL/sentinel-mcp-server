"""
Unit tests for authentication module
"""

import pytest
from unittest.mock import Mock, patch
from utils.auth import AzureAuthenticator, get_authenticator


class TestAzureAuthenticator:
    """Test AzureAuthenticator class"""

    def test_init_with_credentials(self):
        """Test initialization with explicit credentials"""
        auth = AzureAuthenticator(
            tenant_id="test-tenant",
            client_id="test-client",
            client_secret="test-secret",
        )

        assert auth.tenant_id == "test-tenant"
        assert auth.client_id == "test-client"
        assert auth.client_secret == "test-secret"
        assert auth.use_managed_identity is False

    def test_init_with_managed_identity(self):
        """Test initialization with managed identity"""
        auth = AzureAuthenticator(use_managed_identity=True)

        assert auth.use_managed_identity is True

    @patch.dict("os.environ", {"AZURE_TENANT_ID": "env-tenant"})
    def test_init_from_environment(self):
        """Test initialization from environment variables"""
        auth = AzureAuthenticator()

        assert auth.tenant_id == "env-tenant"

    def test_get_credential_with_service_principal(self):
        """Test getting credential with service principal"""
        auth = AzureAuthenticator(
            tenant_id="test-tenant",
            client_id="test-client",
            client_secret="test-secret",
        )

        credential = auth.get_credential()
        assert credential is not None

    def test_get_credential_caching(self):
        """Test that credential is cached"""
        auth = AzureAuthenticator(
            tenant_id="test-tenant",
            client_id="test-client",
            client_secret="test-secret",
        )

        cred1 = auth.get_credential()
        cred2 = auth.get_credential()

        assert cred1 is cred2  # Same object

    def test_factory_function(self):
        """Test get_authenticator factory function"""
        auth = get_authenticator(
            tenant_id="test-tenant",
            client_id="test-client",
            client_secret="test-secret",
        )

        assert isinstance(auth, AzureAuthenticator)
        assert auth.tenant_id == "test-tenant"

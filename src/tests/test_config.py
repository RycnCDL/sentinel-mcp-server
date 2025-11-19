"""
Unit tests for configuration module
"""

import pytest
from unittest.mock import patch
from utils.config import (
    Settings,
    get_settings,
    reload_settings,
    AzureConfig,
    PerformanceConfig,
    CacheConfig,
)


class TestSettings:
    """Test Settings class"""

    @patch.dict(
        "os.environ",
        {
            "AZURE_TENANT_ID": "test-tenant",
            "AZURE_CLIENT_ID": "test-client",
            "LOG_LEVEL": "DEBUG",
            "MCP_SERVER_NAME": "test-server",
        },
    )
    def test_settings_from_env(self):
        """Test loading settings from environment"""
        settings = Settings()

        assert settings.azure_tenant_id == "test-tenant"
        assert settings.azure_client_id == "test-client"
        assert settings.log_level == "DEBUG"
        assert settings.mcp_server_name == "test-server"

    def test_settings_defaults(self):
        """Test default settings values"""
        settings = Settings()

        assert settings.log_level in ["INFO", "DEBUG"]  # May vary by .env
        assert settings.max_concurrent_queries > 0
        assert settings.query_timeout_seconds > 0

    def test_get_azure_config(self):
        """Test get_azure_config method"""
        settings = Settings()
        azure_config = settings.get_azure_config()

        assert isinstance(azure_config, AzureConfig)

    def test_get_performance_config(self):
        """Test get_performance_config method"""
        settings = Settings()
        perf_config = settings.get_performance_config()

        assert isinstance(perf_config, PerformanceConfig)
        assert perf_config.max_concurrent_queries > 0

    def test_get_cache_config(self):
        """Test get_cache_config method"""
        settings = Settings()
        cache_config = settings.get_cache_config()

        assert isinstance(cache_config, CacheConfig)
        assert isinstance(cache_config.enable_workspace_cache, bool)


class TestSettingsGlobals:
    """Test global settings functions"""

    def test_get_settings_singleton(self):
        """Test that get_settings returns singleton"""
        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_reload_settings(self):
        """Test settings reload"""
        settings1 = get_settings()
        settings2 = reload_settings()

        # Should be new instance but same values
        assert settings1 is not settings2
        assert settings1.mcp_server_name == settings2.mcp_server_name

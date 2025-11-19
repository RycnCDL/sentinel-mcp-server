"""
Configuration Management Module

Handles loading and validation of configuration from:
- Environment variables (.env file)
- JSON configuration files
- Command-line arguments
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import structlog

logger = structlog.get_logger(__name__)


class AzureConfig(BaseModel):
    """Azure authentication configuration"""

    tenant_id: Optional[str] = Field(None, description="Azure AD Tenant ID")
    client_id: Optional[str] = Field(None, description="Service Principal Client ID")
    client_secret: Optional[str] = Field(None, description="Service Principal Client Secret")
    subscription_id: Optional[str] = Field(None, description="Default Azure Subscription ID")
    use_managed_identity: bool = Field(False, description="Use Managed Identity")


class PerformanceConfig(BaseModel):
    """Performance and resource limits configuration"""

    max_concurrent_queries: int = Field(5, description="Maximum concurrent workspace queries")
    query_timeout_seconds: int = Field(30, description="Query timeout in seconds")
    kql_result_limit: int = Field(1000, description="KQL result limit per workspace")


class CacheConfig(BaseModel):
    """Cache configuration"""

    enable_workspace_cache: bool = Field(True, description="Enable caching for workspace lists")
    workspace_cache_ttl: int = Field(300, description="Workspace cache TTL in seconds")


class LoggingConfig(BaseModel):
    """Logging configuration"""

    level: str = Field("INFO", description="Logging level")
    format: str = Field("json", description="Log format (json or text)")
    log_requests: bool = Field(True, description="Log all requests")


class MCPServerConfig(BaseModel):
    """MCP Server configuration"""

    name: str = Field("sentinel-mcp-server", description="Server name")
    version: str = Field("0.1.0-alpha", description="Server version")
    debug_mode: bool = Field(False, description="Enable debug mode")


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file
    """

    # Azure Configuration
    azure_tenant_id: Optional[str] = Field(None, env="AZURE_TENANT_ID")
    azure_client_id: Optional[str] = Field(None, env="AZURE_CLIENT_ID")
    azure_client_secret: Optional[str] = Field(None, env="AZURE_CLIENT_SECRET")
    azure_subscription_id: Optional[str] = Field(None, env="AZURE_SUBSCRIPTION_ID")
    azure_use_managed_identity: bool = Field(False, env="AZURE_USE_MANAGED_IDENTITY")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    log_requests: bool = Field(True, env="LOG_REQUESTS")

    # MCP Server
    mcp_server_name: str = Field("sentinel-mcp-server", env="MCP_SERVER_NAME")
    mcp_server_version: str = Field("0.1.0-alpha", env="MCP_SERVER_VERSION")
    debug_mode: bool = Field(False, env="DEBUG_MODE")

    # Performance
    max_concurrent_queries: int = Field(5, env="MAX_CONCURRENT_QUERIES")
    query_timeout_seconds: int = Field(30, env="QUERY_TIMEOUT_SECONDS")
    kql_result_limit: int = Field(1000, env="KQL_RESULT_LIMIT")

    # Cache
    enable_workspace_cache: bool = Field(True, env="ENABLE_WORKSPACE_CACHE")
    workspace_cache_ttl: int = Field(300, env="WORKSPACE_CACHE_TTL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_azure_config(self) -> AzureConfig:
        """Get Azure configuration"""
        return AzureConfig(
            tenant_id=self.azure_tenant_id,
            client_id=self.azure_client_id,
            client_secret=self.azure_client_secret,
            subscription_id=self.azure_subscription_id,
            use_managed_identity=self.azure_use_managed_identity,
        )

    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration"""
        return PerformanceConfig(
            max_concurrent_queries=self.max_concurrent_queries,
            query_timeout_seconds=self.query_timeout_seconds,
            kql_result_limit=self.kql_result_limit,
        )

    def get_cache_config(self) -> CacheConfig:
        """Get cache configuration"""
        return CacheConfig(
            enable_workspace_cache=self.enable_workspace_cache,
            workspace_cache_ttl=self.workspace_cache_ttl,
        )

    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration"""
        return LoggingConfig(
            level=self.log_level,
            format=self.log_format,
            log_requests=self.log_requests,
        )

    def get_server_config(self) -> MCPServerConfig:
        """Get MCP server configuration"""
        return MCPServerConfig(
            name=self.mcp_server_name,
            version=self.mcp_server_version,
            debug_mode=self.debug_mode,
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create the global settings instance

    Returns:
        Settings: Application settings
    """
    global _settings
    if _settings is None:
        _settings = Settings()
        logger.info(
            "Settings loaded",
            log_level=_settings.log_level,
            debug_mode=_settings.debug_mode,
        )
    return _settings


def reload_settings() -> Settings:
    """
    Force reload settings from environment

    Returns:
        Settings: Fresh settings instance
    """
    global _settings
    _settings = Settings()
    logger.info("Settings reloaded")
    return _settings

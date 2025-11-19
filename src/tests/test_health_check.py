"""
Unit tests for health check module
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from mcp_server.tools.management.health_check import (
    SentinelHealthChecker,
    HealthStatus,
    _calculate_summary_status,
)
from utils.lighthouse import SentinelWorkspace


@pytest.fixture
def mock_workspace():
    """Create a mock SentinelWorkspace"""
    return SentinelWorkspace(
        workspace_id="/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.OperationalInsights/workspaces/test-ws",
        workspace_name="test-workspace",
        resource_group="test-rg",
        subscription_id="test-sub-id",
        tenant_id="test-tenant-id",
        tenant_name="Test Tenant",
        location="westeurope",
    )


@pytest.fixture
def mock_authenticator():
    """Create a mock authenticator"""
    auth = Mock()
    auth.get_credential = Mock(return_value=Mock())
    return auth


class TestSentinelHealthChecker:
    """Test SentinelHealthChecker class"""

    def test_init(self, mock_authenticator):
        """Test health checker initialization"""
        checker = SentinelHealthChecker(mock_authenticator)

        assert checker.authenticator == mock_authenticator
        assert checker.credential is not None

    @pytest.mark.asyncio
    async def test_check_workspace_health_structure(
        self, mock_authenticator, mock_workspace
    ):
        """Test that check_workspace_health returns correct structure"""
        checker = SentinelHealthChecker(mock_authenticator)

        # Mock the internal check methods
        checker._check_data_connectors = AsyncMock(
            return_value={"total": 5, "status": "checked"}
        )
        checker._check_analytics_rules = AsyncMock(
            return_value={"total": 10, "enabled": 8, "disabled": 2, "status": "checked"}
        )

        result = await checker.check_workspace_health(mock_workspace, "quick")

        assert "workspace_id" in result
        assert "workspace_name" in result
        assert "timestamp" in result
        assert "status" in result
        assert "issues" in result
        assert "metrics" in result
        assert isinstance(result["issues"], list)
        assert isinstance(result["metrics"], dict)

    def test_calculate_overall_status_healthy(self):
        """Test status calculation for healthy workspace"""
        checker = SentinelHealthChecker(Mock())

        metrics = {
            "data_connectors": {"total": 5, "status": "checked"},
            "analytics_rules": {
                "total": 10,
                "enabled": 10,
                "disabled": 0,
                "status": "checked",
            },
        }

        status = checker._calculate_overall_status(metrics)
        assert status == HealthStatus.HEALTHY

    def test_calculate_overall_status_warning(self):
        """Test status calculation for warning condition"""
        checker = SentinelHealthChecker(Mock())

        metrics = {
            "data_connectors": {"total": 0, "status": "checked"},
            "analytics_rules": {
                "total": 10,
                "enabled": 10,
                "disabled": 0,
                "status": "checked",
            },
        }

        status = checker._calculate_overall_status(metrics)
        assert status == HealthStatus.WARNING

    def test_calculate_overall_status_error(self):
        """Test status calculation for error condition"""
        checker = SentinelHealthChecker(Mock())

        metrics = {
            "data_connectors": {"total": 0, "status": "error", "error": "Test error"},
        }

        status = checker._calculate_overall_status(metrics)
        assert status == HealthStatus.ERROR


class TestSummaryCalculation:
    """Test summary status calculation"""

    def test_calculate_summary_healthy(self):
        """Test summary when all workspaces are healthy"""
        results = [
            {"status": HealthStatus.HEALTHY},
            {"status": HealthStatus.HEALTHY},
        ]

        status = _calculate_summary_status(results)
        assert status == "healthy"

    def test_calculate_summary_warning(self):
        """Test summary when some workspaces have warnings"""
        results = [
            {"status": HealthStatus.HEALTHY},
            {"status": HealthStatus.WARNING},
        ]

        status = _calculate_summary_status(results)
        assert status == "warning"

    def test_calculate_summary_degraded(self):
        """Test summary when some workspaces have errors"""
        results = [
            {"status": HealthStatus.HEALTHY},
            {"status": HealthStatus.ERROR},
        ]

        status = _calculate_summary_status(results)
        assert status == "degraded"

    def test_calculate_summary_unknown(self):
        """Test summary with unknown status"""
        results = [{"status": HealthStatus.UNKNOWN}]

        status = _calculate_summary_status(results)
        assert status == "unknown"

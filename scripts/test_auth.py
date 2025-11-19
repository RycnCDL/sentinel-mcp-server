#!/usr/bin/env python3
"""
Test Azure Authentication

This script tests Azure authentication using configured credentials.
Run this after setting up your .env file to verify authentication works.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_settings
from utils.logging import setup_logging
from utils.auth import get_authenticator
import structlog


def main():
    """Test Azure authentication"""

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(
        level=settings.log_level,
        format_type=settings.log_format,
        log_requests=settings.log_requests,
    )

    logger = structlog.get_logger(__name__)
    logger.info("Starting Azure authentication test")

    # Display configuration
    azure_config = settings.get_azure_config()
    logger.info(
        "Azure configuration",
        has_tenant_id=bool(azure_config.tenant_id),
        has_client_id=bool(azure_config.client_id),
        has_client_secret=bool(azure_config.client_secret),
        has_subscription_id=bool(azure_config.subscription_id),
        use_managed_identity=azure_config.use_managed_identity,
    )

    # Create authenticator
    authenticator = get_authenticator(
        tenant_id=azure_config.tenant_id,
        client_id=azure_config.client_id,
        client_secret=azure_config.client_secret,
    )

    # Test authentication
    logger.info("Testing authentication...")
    is_valid = authenticator.validate_authentication()

    if is_valid:
        logger.info("✅ Authentication successful!")

        # Get credential for further testing
        credential = authenticator.get_credential()
        logger.info("Credential obtained", credential_type=type(credential).__name__)

        # Try to get a token
        try:
            token = credential.get_token("https://management.azure.com/.default")
            logger.info(
                "Token obtained successfully",
                token_length=len(token.token),
                expires_on=token.expires_on,
            )
            return 0
        except Exception as e:
            logger.error("Failed to obtain token", error=str(e))
            return 1
    else:
        logger.error("❌ Authentication failed!")
        logger.info(
            """
Please check your configuration:
1. Ensure .env file exists with correct values
2. For Service Principal:
   - AZURE_TENANT_ID should be set
   - AZURE_CLIENT_ID should be set
   - AZURE_CLIENT_SECRET should be set
3. For Azure CLI:
   - Run 'az login' first
4. For Managed Identity:
   - Set AZURE_USE_MANAGED_IDENTITY=true
   - Ensure running in Azure with MI enabled
"""
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())

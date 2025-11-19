#!/bin/bash
# Interactive script to setup Azure credentials in .env file

set -e

echo "=================================="
echo "Azure Credentials Setup"
echo "=================================="
echo ""
echo "This script will help you configure your Azure Service Principal credentials."
echo "Your credentials will be stored in the .env file (which is gitignored)."
echo ""

# Read current .env file
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# Prompt for credentials
echo "Please enter your Azure credentials:"
echo ""

read -p "Azure Tenant ID: " TENANT_ID
read -p "Azure Client ID: " CLIENT_ID
read -s -p "Azure Client Secret: " CLIENT_SECRET
echo ""
read -p "Azure Subscription ID (optional): " SUBSCRIPTION_ID
echo ""

# Validate inputs
if [ -z "$TENANT_ID" ] || [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo ""
    echo "Error: Tenant ID, Client ID, and Client Secret are required!"
    exit 1
fi

# Update .env file
echo ""
echo "Updating .env file..."

# Create a temporary file
TMP_FILE=$(mktemp)

# Read the existing .env and update the Azure credentials
while IFS= read -r line; do
    if [[ $line == AZURE_TENANT_ID=* ]]; then
        echo "AZURE_TENANT_ID=$TENANT_ID" >> "$TMP_FILE"
    elif [[ $line == AZURE_CLIENT_ID=* ]]; then
        echo "AZURE_CLIENT_ID=$CLIENT_ID" >> "$TMP_FILE"
    elif [[ $line == AZURE_CLIENT_SECRET=* ]]; then
        echo "AZURE_CLIENT_SECRET=$CLIENT_SECRET" >> "$TMP_FILE"
    elif [[ $line == AZURE_SUBSCRIPTION_ID=* ]]; then
        if [ -n "$SUBSCRIPTION_ID" ]; then
            echo "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID" >> "$TMP_FILE"
        else
            echo "AZURE_SUBSCRIPTION_ID=" >> "$TMP_FILE"
        fi
    else
        echo "$line" >> "$TMP_FILE"
    fi
done < "$ENV_FILE"

# Replace the original file
mv "$TMP_FILE" "$ENV_FILE"

echo ""
echo "✅ Credentials saved to .env file"
echo ""
echo "Next steps:"
echo "1. Test authentication: python scripts/test_auth.py"
echo "2. Test server: python scripts/test_server.py"
echo ""

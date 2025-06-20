#!/bin/bash

# Azure Deployment Helper Script for Teams Productivity Bot
# This script helps you deploy the bot to Azure step by step

set -e  # Exit on any error

echo "🚀 Teams Productivity Bot - Azure Deployment Helper"
echo "=================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}[STEP $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "1" "Checking Prerequisites"
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first:"
        echo "  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    print_success "Azure CLI is installed"
    
    # Check if logged into Azure
    if ! az account show &> /dev/null; then
        print_warning "Not logged into Azure. Please run: az login"
        exit 1
    fi
    print_success "Logged into Azure"
    
    # Check if Terraform is installed (optional)
    if command -v terraform &> /dev/null; then
        print_success "Terraform is installed"
        TERRAFORM_AVAILABLE=true
    else
        print_warning "Terraform not found. Will use Azure CLI for deployment"
        TERRAFORM_AVAILABLE=false
    fi
    
    echo ""
}

# Get configuration from user
get_configuration() {
    print_step "2" "Configuration Setup"
    
    # Get basic configuration
    read -p "📝 Enter your Azure subscription ID: " SUBSCRIPTION_ID
    read -p "📝 Enter resource group name [rg-teams-bot]: " RESOURCE_GROUP
    RESOURCE_GROUP=${RESOURCE_GROUP:-rg-teams-bot}
    
    read -p "📝 Enter Azure region [australiaeast]: " LOCATION
    LOCATION=${LOCATION:-australiaeast}
    
    read -p "📝 Enter app name [teams-productivity-bot]: " APP_NAME
    APP_NAME=${APP_NAME:-teams-productivity-bot}
    
    # Bot configuration
    echo ""
    echo "🤖 Bot Framework Configuration"
    read -p "📝 Enter Bot App ID: " BOT_APP_ID
    read -s -p "🔐 Enter Bot App Password: " BOT_APP_PASSWORD
    echo ""
    
    # Graph API configuration
    echo ""
    echo "📊 Microsoft Graph API Configuration (for Teams manifest upload)"
    read -p "📝 Enter Tenant ID: " TENANT_ID
    read -p "📝 Enter Graph Client ID: " GRAPH_CLIENT_ID
    read -s -p "🔐 Enter Graph Client Secret: " GRAPH_CLIENT_SECRET
    echo ""
    echo ""
    
    print_success "Configuration collected"
}

# Deploy infrastructure
deploy_infrastructure() {
    print_step "3" "Deploying Infrastructure"
    
    # Set subscription
    az account set --subscription "$SUBSCRIPTION_ID"
    
    # Create resource group
    echo "Creating resource group..."
    az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
    print_success "Resource group created"
    
    # Create App Service Plan
    echo "Creating App Service Plan..."
    az appservice plan create \
        --name "${APP_NAME}-plan" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --sku B1 \
        --is-linux
    print_success "App Service Plan created"
    
    # Create Web App
    echo "Creating Web App..."
    az webapp create \
        --name "$APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --plan "${APP_NAME}-plan" \
        --runtime "PYTHON:3.11"
    print_success "Web App created"
    
    # Configure app settings
    echo "Configuring app settings..."
    az webapp config appsettings set \
        --name "$APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --settings \
            MicrosoftAppId="$BOT_APP_ID" \
            MicrosoftAppPassword="$BOT_APP_PASSWORD" \
            FLASK_ENV="production" \
            PORT="8000" \
            WEBSITES_ENABLE_APP_SERVICE_STORAGE="false" \
            SCM_DO_BUILD_DURING_DEPLOYMENT="true"
    print_success "App settings configured"
    
    # Create Application Insights
    echo "Creating Application Insights..."
    az monitor app-insights component create \
        --app "${APP_NAME}-insights" \
        --location "$LOCATION" \
        --resource-group "$RESOURCE_GROUP" \
        --application-type web || print_warning "Application Insights creation failed (optional)"
    
    echo ""
}

# Get publish profile
get_publish_profile() {
    print_step "4" "Getting Publish Profile"
    
    PUBLISH_PROFILE=$(az webapp deployment list-publishing-profiles \
        --name "$APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --xml)
    
    # Save to file for GitHub secrets
    echo "$PUBLISH_PROFILE" > publish-profile.xml
    print_success "Publish profile saved to publish-profile.xml"
    echo ""
}

# Display GitHub setup instructions
show_github_setup() {
    print_step "5" "GitHub Secrets Configuration"
    
    echo "🔧 Configure these secrets in your GitHub repository:"
    echo "   Repository → Settings → Secrets and Variables → Actions"
    echo ""
    echo "Required secrets:"
    echo "AZURE_WEBAPP_NAME=$APP_NAME"
    echo "BOT_APP_ID=$BOT_APP_ID"
    echo "BOT_APP_PASSWORD=***hidden***"
    echo "TENANT_ID=$TENANT_ID"
    echo "GRAPH_CLIENT_ID=$GRAPH_CLIENT_ID"
    echo "GRAPH_CLIENT_SECRET=***hidden***"
    echo ""
    echo "AZURE_WEBAPP_PUBLISH_PROFILE="
    echo "  (Copy content from publish-profile.xml file)"
    echo ""
    print_warning "Keep the publish-profile.xml file secure and delete it after copying to GitHub!"
    echo ""
}

# Show next steps
show_next_steps() {
    print_step "6" "Next Steps"
    
    echo "1. 📋 Copy GitHub secrets from the information above"
    echo "2. 🚀 Push your code to the main branch to trigger deployment"
    echo "3. 👀 Monitor deployment in GitHub Actions"
    echo "4. 🧪 Test your bot at: https://${APP_NAME}.azurewebsites.net"
    echo "5. 📱 Upload Teams manifest and install in Microsoft Teams"
    echo ""
    echo "🎯 Bot endpoint for Teams registration:"
    echo "   https://${APP_NAME}.azurewebsites.net/api/messages"
    echo ""
    print_success "Deployment setup complete!"
    echo ""
    echo "📖 For detailed troubleshooting, see the README.md file"
}

# Main execution
main() {
    check_prerequisites
    get_configuration
    deploy_infrastructure
    get_publish_profile
    show_github_setup
    show_next_steps
}

# Run main function
main "$@"

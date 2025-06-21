#!/bin/bash

# =============================================================================
# Teams Bot Infrastructure Deployment Script
# =============================================================================
# This script deploys the complete Azure infrastructure for the Teams Bot
# including App Service, Application Insights, and proper configuration.
# 
# Requirements:
# - Azure CLI installed and logged in
# - .env file with required variables
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if logged into Azure
check_azure_login() {
    if ! az account show >/dev/null 2>&1; then
        log_error "Not logged into Azure CLI. Please run 'az login' first."
        exit 1
    fi
    
    # Check Azure CLI version for compatibility
    local az_version
    az_version=$(az version --output json 2>/dev/null | grep -o '"azure-cli": "[^"]*"' | cut -d'"' -f4 || echo "unknown")
    log_info "Using Azure CLI version: $az_version"
}

# Function to load environment variables
load_env_vars() {
    local env_file="${1:-.env}"
    
    if [ ! -f "$env_file" ]; then
        log_error "Environment file '$env_file' not found."
        log_info "Please copy .env.template to .env and fill in your values."
        exit 1
    fi
    
    log_info "Loading environment variables from $env_file"
    
    # Load variables from .env file
    set -a  # Automatically export variables
    # shellcheck source=/dev/null
    source "$env_file"
    set +a  # Stop automatically exporting
    
    # Validate required variables
    REQUIRED_VARS=(
        "AZURE_WEBAPP_NAME"
        "MicrosoftAppId"
        "MicrosoftAppPassword"
        "TENANT_ID"
    )
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Required environment variable '$var' is not set in $env_file"
            exit 1
        fi
    done
}

# Function to set default values
set_defaults() {
    # Set default values if not provided
    RESOURCE_GROUP="${RESOURCE_GROUP:-rg-teams-bot}"
    LOCATION="${LOCATION:-eastus}"
    APP_SERVICE_PLAN="${APP_SERVICE_PLAN:-${AZURE_WEBAPP_NAME}-plan}"
    APP_INSIGHTS_NAME="${APP_INSIGHTS_NAME:-${AZURE_WEBAPP_NAME}-insights}"
    PYTHON_VERSION="${PYTHON_VERSION:-3.11}"
    SKU="${SKU:-B1}"
    
    log_info "Using configuration:"
    log_info "  Resource Group: $RESOURCE_GROUP"
    log_info "  Location: $LOCATION"
    log_info "  App Name: $AZURE_WEBAPP_NAME"
    log_info "  App Service Plan: $APP_SERVICE_PLAN"
    log_info "  Application Insights: $APP_INSIGHTS_NAME"
    log_info "  Python Version: $PYTHON_VERSION"
    log_info "  SKU: $SKU"
}

# Function to check if resource exists
resource_exists() {
    local resource_type="$1"
    local resource_name="$2"
    local resource_group="$3"
    
    case "$resource_type" in
        "group")
            az group show --name "$resource_name" >/dev/null 2>&1
            ;;
        "webapp")
            az webapp show --name "$resource_name" --resource-group "$resource_group" >/dev/null 2>&1
            ;;
        "appservice-plan")
            az appservice plan show --name "$resource_name" --resource-group "$resource_group" >/dev/null 2>&1
            ;;
        "app-insights")
            az monitor app-insights component show --app "$resource_name" --resource-group "$resource_group" >/dev/null 2>&1
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to create resource group
create_resource_group() {
    log_info "Creating resource group: $RESOURCE_GROUP"
    
    if resource_exists "group" "$RESOURCE_GROUP"; then
        log_warning "Resource group '$RESOURCE_GROUP' already exists. Skipping creation."
        return 0
    fi
    
    az group create \
        --name "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --tags "project=teams-bot" "environment=production" "created-by=deploy-script"
    
    if [ $? -eq 0 ]; then
        log_success "Resource group '$RESOURCE_GROUP' created successfully"
    else
        log_error "Failed to create resource group '$RESOURCE_GROUP'"
        exit 1
    fi
}

# Function to create Application Insights
create_application_insights() {
    log_info "Creating Application Insights: $APP_INSIGHTS_NAME"
    
    if resource_exists "app-insights" "$APP_INSIGHTS_NAME" "$RESOURCE_GROUP"; then
        log_warning "Application Insights '$APP_INSIGHTS_NAME' already exists. Skipping creation."
        return 0
    fi
    
    az monitor app-insights component create \
        --app "$APP_INSIGHTS_NAME" \
        --location "$LOCATION" \
        --resource-group "$RESOURCE_GROUP" \
        --kind "web" \
        --tags "project=teams-bot" "environment=production"
    
    if [ $? -eq 0 ]; then
        log_success "Application Insights '$APP_INSIGHTS_NAME' created successfully"
        
        # Get instrumentation key
        INSTRUMENTATION_KEY=$(az monitor app-insights component show \
            --app "$APP_INSIGHTS_NAME" \
            --resource-group "$RESOURCE_GROUP" \
            --query instrumentationKey -o tsv)
        
        log_info "Application Insights Instrumentation Key: $INSTRUMENTATION_KEY"
    else
        log_error "Failed to create Application Insights '$APP_INSIGHTS_NAME'"
        exit 1
    fi
}

# Function to create App Service Plan
create_app_service_plan() {
    log_info "Creating App Service Plan: $APP_SERVICE_PLAN"
    
    if resource_exists "appservice-plan" "$APP_SERVICE_PLAN" "$RESOURCE_GROUP"; then
        log_warning "App Service Plan '$APP_SERVICE_PLAN' already exists. Skipping creation."
        return 0
    fi
    
    az appservice plan create \
        --name "$APP_SERVICE_PLAN" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --sku "$SKU" \
        --is-linux \
        --tags "project=teams-bot" "environment=production"
    
    if [ $? -eq 0 ]; then
        log_success "App Service Plan '$APP_SERVICE_PLAN' created successfully"
    else
        log_error "Failed to create App Service Plan '$APP_SERVICE_PLAN'"
        exit 1
    fi
}

# Function to create Web App
create_web_app() {
    log_info "Creating Web App: $AZURE_WEBAPP_NAME"
    
    if resource_exists "webapp" "$AZURE_WEBAPP_NAME" "$RESOURCE_GROUP"; then
        log_warning "Web App '$AZURE_WEBAPP_NAME' already exists. Skipping creation."
        return 0
    fi
    
    az webapp create \
        --resource-group "$RESOURCE_GROUP" \
        --plan "$APP_SERVICE_PLAN" \
        --name "$AZURE_WEBAPP_NAME" \
        --runtime "PYTHON|$PYTHON_VERSION" \
        --deployment-local-git \
        --tags "project=teams-bot" "environment=production"
    
    if [ $? -eq 0 ]; then
        log_success "Web App '$AZURE_WEBAPP_NAME' created successfully"
    else
        log_error "Failed to create Web App '$AZURE_WEBAPP_NAME'"
        exit 1
    fi
}

# Function to configure Web App settings
configure_web_app() {
    log_info "Configuring Web App settings"
    
    # Set startup command
    az webapp config set \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AZURE_WEBAPP_NAME" \
        --startup-file "startup.sh" \
        --linux-fx-version "PYTHON|$PYTHON_VERSION"
    
    # Enable basic authentication for deployment (try multiple methods for compatibility)
    log_info "Enabling basic authentication for deployment"
    
    # Method 1: Try the newer command first
    if az webapp auth config-version upgrade --name "$AZURE_WEBAPP_NAME" --resource-group "$RESOURCE_GROUP" --config-file-path /dev/null 2>/dev/null; then
        log_info "Using newer authentication configuration"
        az webapp auth update \
            --name "$AZURE_WEBAPP_NAME" \
            --resource-group "$RESOURCE_GROUP" \
            --enabled true \
            --action AllowAnonymous 2>/dev/null || true
    fi
    
    # Method 2: Enable basic auth via resource update (more reliable)
    log_info "Configuring basic authentication for deployments"
    az resource update \
        --resource-group "$RESOURCE_GROUP" \
        --name ftp \
        --namespace Microsoft.Web \
        --resource-type basicPublishingCredentialsPolicies \
        --parent sites/"$AZURE_WEBAPP_NAME" \
        --set properties.allow=true 2>/dev/null || true
    
    az resource update \
        --resource-group "$RESOURCE_GROUP" \
        --name scm \
        --namespace Microsoft.Web \
        --resource-type basicPublishingCredentialsPolicies \
        --parent sites/"$AZURE_WEBAPP_NAME" \
        --set properties.allow=true 2>/dev/null || true
    
    # Configure application settings
    log_info "Setting application configuration"
    
    az webapp config appsettings set \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AZURE_WEBAPP_NAME" \
        --settings \
            "MicrosoftAppId=$MicrosoftAppId" \
            "MicrosoftAppPassword=$MicrosoftAppPassword" \
            "MicrosoftAppTenantId=$TENANT_ID" \
            "APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY" \
            "WEBSITE_RUN_FROM_PACKAGE=1" \
            "SCM_DO_BUILD_DURING_DEPLOYMENT=true" \
            "ENABLE_ORYX_BUILD=true" \
            "DISABLE_COLLECTSTATIC=1" \
            "PYTHONPATH=/home/site/wwwroot"
    
    if [ $? -eq 0 ]; then
        log_success "Web App configuration completed successfully"
    else
        log_error "Failed to configure Web App settings"
        exit 1
    fi
}

# Function to configure CORS (if needed)
configure_cors() {
    log_info "Configuring CORS settings"
    
    az webapp cors add \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AZURE_WEBAPP_NAME" \
        --allowed-origins "https://teams.microsoft.com" "https://teamsnoauth.azurewebsites.net" \
        >/dev/null 2>&1 || true
    
    log_success "CORS configuration completed"
}

# Function to get deployment information
get_deployment_info() {
    log_info "Retrieving deployment information"
    
    # Get Web App URL
    WEBAPP_URL=$(az webapp show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AZURE_WEBAPP_NAME" \
        --query defaultHostName -o tsv)
    
    # Get Application Insights details
    APP_INSIGHTS_APP_ID=$(az monitor app-insights component show \
        --app "$APP_INSIGHTS_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query appId -o tsv)
    
    # Get publish profile (for GitHub Actions)
    log_info "Generating publish profile"
    PUBLISH_PROFILE=$(az webapp deployment list-publishing-profiles \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AZURE_WEBAPP_NAME" \
        --xml)
    
    # Save publish profile to file
    echo "$PUBLISH_PROFILE" > "${AZURE_WEBAPP_NAME}-publish-profile.xml"
    
    log_success "Publish profile saved to: ${AZURE_WEBAPP_NAME}-publish-profile.xml"
}

# Function to display deployment summary
display_summary() {
    echo ""
    echo "================================================================="
    echo "           TEAMS BOT DEPLOYMENT COMPLETED SUCCESSFULLY"
    echo "================================================================="
    echo ""
    echo "🎉 Infrastructure Details:"
    echo "   Resource Group:      $RESOURCE_GROUP"
    echo "   Location:           $LOCATION"
    echo "   Web App Name:       $AZURE_WEBAPP_NAME"
    echo "   Web App URL:        https://$WEBAPP_URL"
    echo "   Bot Endpoint:       https://$WEBAPP_URL/api/messages"
    echo ""
    echo "📊 Monitoring:"
    echo "   Application Insights: $APP_INSIGHTS_NAME"
    echo "   App Insights App ID:  $APP_INSIGHTS_APP_ID"
    echo "   Instrumentation Key:  $INSTRUMENTATION_KEY"
    echo ""
    echo "🔧 Next Steps:"
    echo "   1. Update your Bot Framework registration with the endpoint:"
    echo "      https://$WEBAPP_URL/api/messages"
    echo ""
    echo "   2. Configure GitHub Secrets for CI/CD:"
    echo "      - AZURE_WEBAPP_NAME: $AZURE_WEBAPP_NAME"
    echo "      - AZURE_WEBAPP_PUBLISH_PROFILE: (content of ${AZURE_WEBAPP_NAME}-publish-profile.xml)"
    echo "      - BOT_APP_ID: $MicrosoftAppId"
    echo "      - BOT_APP_PASSWORD: [your bot password]"
    echo "      - TENANT_ID: $TENANT_ID"
    echo ""
    echo "   3. Deploy your code using GitHub Actions or manual deployment"
    echo ""
    echo "   4. Test the health endpoint:"
    echo "      curl https://$WEBAPP_URL/api/health"
    echo ""
    echo "================================================================="
}

# Main deployment function
main() {
    echo "================================================================="
    echo "           TEAMS BOT INFRASTRUCTURE DEPLOYMENT"
    echo "================================================================="
    echo ""
    
    # Check prerequisites
    log_info "Checking prerequisites"
    
    if ! command_exists az; then
        log_error "Azure CLI is not installed. Please install it first."
        log_info "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    check_azure_login
    load_env_vars "$1"
    set_defaults
    
    # Confirmation prompt
    echo ""
    log_warning "This will create Azure resources that may incur costs."
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled by user."
        exit 0
    fi
    
    # Deploy infrastructure
    log_info "Starting infrastructure deployment"
    
    create_resource_group
    create_application_insights
    create_app_service_plan
    create_web_app
    configure_web_app
    configure_cors
    get_deployment_info
    
    # Display summary
    display_summary
    
    log_success "Deployment completed successfully! 🎉"
}

# Script usage
usage() {
    echo "Usage: $0 [ENV_FILE]"
    echo ""
    echo "Deploy Teams Bot infrastructure to Azure"
    echo ""
    echo "Arguments:"
    echo "  ENV_FILE    Path to environment file (default: .env)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Use .env file"
    echo "  $0 .env.production    # Use custom env file"
    echo ""
    echo "Required environment variables:"
    echo "  AZURE_WEBAPP_NAME     - Name of the Azure Web App"
    echo "  MicrosoftAppId        - Bot Framework App ID"
    echo "  MicrosoftAppPassword  - Bot Framework App Password"
    echo "  TENANT_ID             - Azure AD Tenant ID"
    echo ""
    echo "Optional environment variables:"
    echo "  RESOURCE_GROUP        - Azure Resource Group (default: rg-teams-bot)"
    echo "  LOCATION              - Azure Region (default: eastus)"
    echo "  SKU                   - App Service Plan SKU (default: B1)"
    echo "  PYTHON_VERSION        - Python version (default: 3.11)"
}

# Handle command line arguments
case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
    *)
        main "$1"
        ;;
esac

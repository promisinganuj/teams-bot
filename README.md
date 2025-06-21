# Teams Productivity Bot 🤖

A comprehensive AI-powered Microsoft Teams bot built with Python Flask and the Bot Framework SDK. Features advanced calculator, weather information, task management, and team utilities.

[![GitHub Actions](https://github.com/promisinganuj/teams-bot/workflows/Deploy%20Teams%20Bot%20to%20Azure/badge.svg)](https://github.com/promisinganuj/teams-bot/actions)

## 📋 Prerequisites

Before deploying your Teams bot, ensure you have:

### Required Accounts & Subscriptions
- **Azure Subscription** with Owner or Contributor permissions
- **Microsoft 365 Tenant** with Teams admin access
- **GitHub Account** for source code and CI/CD

### Required Tools
- **Azure CLI** (version 2.0.81 or later recommended)
  ```bash
  # Install Azure CLI
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  
  # Or via Homebrew on macOS
  brew install azure-cli
  
  # Check version
  az --version
  
  # Update to latest version
  az upgrade
  ```

- **Git** for version control
  ```bash
  git --version  # Should be 2.0 or higher
  ```

### Microsoft Bot Framework App Registration

The Bot Framework App ID and Password are essential credentials that authenticate your bot with Microsoft's services.

#### Create Bot Registration

**Method 1: Azure Portal (Recommended)**

1. **Navigate to Azure Portal**
   - Go to [Azure Portal](https://portal.azure.com)
   - Sign in with your Azure account

2. **Create Azure Bot Resource**
   - Click "Create a resource" → Search for "Azure Bot"
   - Select "Azure Bot" → Click "Create"
   - Fill in the details:
     - **Bot handle**: `teams-productivity-bot` (must be globally unique)
     - **Subscription**: Select your Azure subscription
     - **Resource group**: Create new: `rg-teams-bot`
     - **Location**: Choose your preferred region
     - **Pricing tier**: `F0` (Free) for development, `S1` for production
     - **Microsoft App ID**: Select "Create new Microsoft App ID"

3. **Complete Registration**
   - Click "Review + create" → "Create"
   - Wait for deployment to complete (~2-3 minutes)

**Method 2: Azure CLI**

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-teams-bot --location eastus

# Create bot registration
az bot create \
  --resource-group rg-teams-bot \
  --name teams-productivity-bot \
  --kind registration \
  --sku F0 \
  --appid $(uuidgen) \
  --password $(openssl rand -base64 32)
```

#### Retrieve Bot Credentials

1. **Get App ID**
   - Go to your Bot resource in Azure Portal
   - Navigate to "Settings" → "Configuration"
   - Copy the **Microsoft App ID** (format: `12345678-1234-1234-1234-123456789012`)

2. **Create App Secret**
   - In the Configuration page, click "Manage" next to Microsoft App ID
   - This opens Azure AD App Registration
   - Go to "Certificates & secrets" → "Client secrets"
   - Click "New client secret"
   - Description: `Teams Bot Secret`
   - Expiration: `24 months` (recommended)
   - Click "Add" and **immediately copy the secret value**
   - ⚠️ **Critical**: You cannot retrieve this value again!

3. **Configure Microsoft Graph Permissions**
   - In the same Azure AD App Registration, go to "API permissions"
   - Click "Add a permission" → "Microsoft Graph" → "Application permissions"
   - Search and add: `AppCatalog.ReadWrite.All`
   - Click "Grant admin consent for [Your Organization]"
   - Wait for status to show "Granted"

#### Configure Bot Endpoint

1. **Set Messaging Endpoint**
   - Return to your Bot resource → "Settings" → "Configuration"
   - Set **Messaging endpoint**: `https://your-app-name.azurewebsites.net/api/messages`
   - Replace `your-app-name` with your planned Azure App Service name
   - Click "Apply"

2. **Enable Teams Channel**
   - Go to "Channels" in your Bot resource
   - Add "Microsoft Teams" channel
   - Accept the terms and configure
   - Click "Save"

## 🚀 Initial Infrastructure Deployment

### Option 1: Automated Deployment Script (Recommended)

The easiest way to deploy your infrastructure is using the provided deployment script that reads from your `.env` file.

**Step 1: Prepare Environment File**

```bash
# Copy the template and fill in your values
cp .env.template .env

# Edit the .env file with your actual values
nano .env
```

**Required variables in `.env`:**
```bash
# Bot Configuration (Required)
MicrosoftAppId=12345678-1234-1234-1234-123456789012
MicrosoftAppPassword=your-bot-app-password-here
TENANT_ID=87654321-4321-4321-4321-210987654321

# Azure Infrastructure Configuration (Required)
AZURE_WEBAPP_NAME=teams-productivity-bot

# Optional Configuration (will use defaults if not set)
RESOURCE_GROUP=rg-teams-bot
LOCATION=eastus
SKU=B1
PYTHON_VERSION=3.11
```

**Step 2: Run Deployment Script**

```bash
# Make sure you're logged into Azure CLI
az login

# Verify your subscription (optional)
az account show

# Run the deployment script
./deploy_infra.sh

# Or with a custom environment file
./deploy_infra.sh .env.production
```

> **💡 Compatibility Note**: The script is compatible with bash 3.2+ (including macOS default bash). It uses POSIX-compliant shell features for maximum compatibility.

**Example deployment output:**
```bash
=================================================================
           TEAMS BOT INFRASTRUCTURE DEPLOYMENT
=================================================================

[INFO] Checking prerequisites
[INFO] Loading environment variables from .env
[INFO] Using configuration:
  Resource Group: rg-teams-bot
  Location: eastus
  App Name: teams-productivity-bot
  App Service Plan: teams-productivity-bot-plan
  Application Insights: teams-productivity-bot-insights
  Python Version: 3.11
  SKU: B1

[INFO] Creating resource group: rg-teams-bot
[SUCCESS] Resource group 'rg-teams-bot' created successfully
[INFO] Creating Application Insights: teams-productivity-bot-insights
[SUCCESS] Application Insights 'teams-productivity-bot-insights' created successfully
[INFO] Creating App Service Plan: teams-productivity-bot-plan
[SUCCESS] App Service Plan 'teams-productivity-bot-plan' created successfully
[INFO] Creating Web App: teams-productivity-bot
[SUCCESS] Web App 'teams-productivity-bot' created successfully
[INFO] Configuring Web App settings
[SUCCESS] Web App configuration completed successfully

=================================================================
           TEAMS BOT DEPLOYMENT COMPLETED SUCCESSFULLY
=================================================================

🎉 Infrastructure Details:
   Resource Group:      rg-teams-bot
   Location:           eastus
   Web App Name:       teams-productivity-bot
   Web App URL:        https://teams-productivity-bot.azurewebsites.net
   Bot Endpoint:       https://teams-productivity-bot.azurewebsites.net/api/messages

📊 Monitoring:
   Application Insights: teams-productivity-bot-insights
   Instrumentation Key:  abc123-def456-789...

🔧 Next Steps:
   1. Update your Bot Framework registration with the endpoint
   2. Configure GitHub Secrets for CI/CD
   3. Deploy your code using GitHub Actions
   4. Test the health endpoint
=================================================================
```

**What the script creates:**
- ✅ **Resource Group** - Container for all resources
- ✅ **Application Insights** - Monitoring and telemetry
- ✅ **App Service Plan** - Hosting plan with Linux and Python 3.11
- ✅ **Web App** - Your bot application hosting
- ✅ **Configuration** - All required app settings and environment variables
- ✅ **Publish Profile** - For GitHub Actions CI/CD deployment

The script will:
1. Validate all prerequisites and environment variables
2. Create all Azure resources with proper configuration
3. Set up Application Insights monitoring
4. Configure the Web App with your bot credentials
5. Generate a publish profile for GitHub Actions
6. Provide you with all the necessary information for next steps

### Option 2: Manual Azure CLI Deployment

If you prefer to run commands manually:

```bash
# Set variables
RESOURCE_GROUP="rg-teams-bot"
APP_NAME="teams-productivity-bot"  # Must be globally unique
LOCATION="eastus"
PYTHON_VERSION="3.11"

# Create App Service Plan
az appservice plan create \
  --name "${APP_NAME}-plan" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan "${APP_NAME}-plan" \
  --name $APP_NAME \
  --runtime "PYTHON|3.11" \
  --deployment-local-git

# Configure startup command
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --startup-file "startup.sh"

# Enable basic authentication for deployment
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --basic-auth-enabled true
```

**Configure Application Settings:**

```bash
# Set bot credentials
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    MicrosoftAppId="YOUR_BOT_APP_ID" \
    MicrosoftAppPassword="YOUR_BOT_APP_PASSWORD" \
    MicrosoftAppTenantId="YOUR_TENANT_ID" \
    WEBSITE_RUN_FROM_PACKAGE="1" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    ENABLE_ORYX_BUILD="true"
```

### Option 2: Deploy via Azure Portal

1. **Create App Service**
   - Go to Azure Portal → "Create a resource"
   - Search for "Web App" → Select "Web App"
   - Fill in details:
     - **Resource Group**: `rg-teams-bot`
     - **Name**: `teams-productivity-bot` (must be unique)
     - **Runtime Stack**: `Python 3.11`
     - **Operating System**: `Linux`
     - **Region**: Choose your preferred region
     - **Pricing Plan**: `Basic B1` (or higher for production)

2. **Configure Application Settings**
   - Go to your App Service → "Configuration" → "Application settings"
   - Add the following settings:
     - `MicrosoftAppId`: Your Bot App ID
     - `MicrosoftAppPassword`: Your Bot App Password
     - `MicrosoftAppTenantId`: Your Azure AD Tenant ID
     - `WEBSITE_RUN_FROM_PACKAGE`: `1`
     - `SCM_DO_BUILD_DURING_DEPLOYMENT`: `true`

### Option 3: Create Application Insights (Optional but Recommended)

```bash
# Create Application Insights
az monitor app-insights component create \
  --app $APP_NAME \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --kind web

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Add to App Service settings
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="$INSTRUMENTATION_KEY"
```

## 🔄 CI/CD using GitHub Actions

### Step 1: Fork and Clone Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/teams-bot.git
cd teams-bot

# Add upstream remote
git remote add upstream https://github.com/promisinganuj/teams-bot.git
```

### Step 2: Get Azure Publish Profile

**Method 1: Azure Portal**
1. Go to your App Service in Azure Portal
2. Click "Get publish profile" in the overview
3. Download the `.PublishSettings` file
4. Open the file and copy the entire XML content

**Method 2: Azure CLI**
```bash
az webapp deployment list-publishing-profiles \
  --resource-group rg-teams-bot \
  --name teams-productivity-bot \
  --xml > publish-profile.xml

# Copy the content of publish-profile.xml
cat publish-profile.xml
```

### Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions

**Add the following Repository Secrets:**

| Secret Name | Description | Example Value | Where to Find |
|-------------|-------------|---------------|---------------|
| `AZURE_WEBAPP_NAME` | Your Azure Web App name | `teams-productivity-bot` | Azure Portal → App Service name |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Complete publish profile XML | `<publishData>...</publishData>` | Azure Portal → Get publish profile |
| `BOT_APP_ID` | Bot Framework App ID | `12345678-1234-1234-1234-123456789012` | Bot resource → Configuration |
| `BOT_APP_PASSWORD` | Bot Framework App Secret | `abc123XYZ_secret_value` | Azure AD → App registrations |
| `TENANT_ID` | Azure AD Tenant ID | `87654321-4321-4321-4321-210987654321` | Azure AD → Properties |

**Optional Secrets (for Teams app auto-upload):**
| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `GRAPH_CLIENT_ID` | Microsoft Graph App ID | Same as `BOT_APP_ID` |
| `GRAPH_CLIENT_SECRET` | Microsoft Graph App Secret | Same as `BOT_APP_PASSWORD` |

### Step 4: Understand the CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:

1. **Triggers on:**
   - Push to `main` branch
   - Pull requests to `main` branch
   - Manual workflow dispatch

2. **Test Phase (for PRs):**
   - Sets up Python 3.11 environment
   - Installs dependencies using `uv`
   - Runs pytest test suite
   - Validates code quality

3. **Build & Deploy Phase (for main branch):**
   - Builds Python application
   - Runs tests
   - Deploys to Azure App Service
   - Creates Teams app package
   - Uploads manifest to Teams (if configured)

### Step 5: Trigger Your First Deployment

```bash
# Make a small change to trigger deployment
echo "# Teams Bot Deployment" >> README.md

# Commit and push
git add .
git commit -m "Initial deployment setup"
git push origin main
```

### Step 6: Monitor Deployment

1. **GitHub Actions**
   - Go to your repository → "Actions" tab
   - Watch the "Deploy Teams Bot to Azure" workflow
   - Each step should complete successfully

2. **Azure App Service**
   - Go to Azure Portal → Your App Service → "Deployment Center"
   - Monitor deployment logs
   - Check "Log stream" for real-time logs

3. **Verify Deployment**
   ```bash
   # Test health endpoint
   curl https://your-app-name.azurewebsites.net/api/health
   
   # Expected response:
   # {"status": "healthy", "service": "teams-productivity-bot", "version": "2.0.0"}
   ```

### Step 7: Configure Teams App Upload (Optional)

If you want automatic Teams app upload:

1. **Ensure Graph API Permissions**
   - Your Bot App Registration needs `AppCatalog.ReadWrite.All` permission
   - Admin consent must be granted

2. **Add Upload Secrets**
   - `GRAPH_CLIENT_ID`: Same as your Bot App ID
   - `GRAPH_CLIENT_SECRET`: Same as your Bot App Password

3. **Workflow will automatically:**
   - Package your Teams app
   - Upload to your tenant's app catalog
   - Make it available for installation

### Troubleshooting CI/CD

**Common Issues:**

1. **"Basic Authentication is Disabled"**
   ```bash
   az webapp config set --resource-group rg-teams-bot --name teams-productivity-bot --basic-auth-enabled true
   ```

2. **"Invalid publish profile"**
   - Re-download publish profile from Azure Portal
   - Ensure entire XML content is copied to GitHub secret
   - Check for any extra characters or formatting issues

3. **"Build failed"**
   - Check Python version compatibility
   - Verify requirements.txt is valid
   - Review GitHub Actions logs for specific errors

4. **"App not responding"**
   - Check Azure App Service logs
   - Verify environment variables are set correctly
   - Ensure startup.sh is executable

5. **"App not responding"**
   - Check Azure App Service logs
   - Verify environment variables are set correctly
   - Ensure startup.sh is executable

6. **"Teams app upload failed"**
   - Verify Microsoft Graph API permissions
   - Check if admin consent is granted
   - Validate Teams manifest.json format

### Azure CLI Compatibility Issues

**❌ "unrecognized arguments: --basic-auth-enabled"**

This occurs with older versions of Azure CLI that don't support the `--basic-auth-enabled` flag.

**Solution**: The deployment script now uses multiple methods for compatibility:
```bash
# Update your Azure CLI to the latest version
az upgrade

# Or install the latest version
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

The script automatically falls back to alternative methods for enabling basic authentication that work with older Azure CLI versions.

## ✨ Bot Features

### 🧮 Advanced Calculator
- **Basic arithmetic**: `calc 5 + 3 * 2` → **11**
- **Advanced functions**: `calc sqrt(16) + 2^3` → **12**
- **Trigonometry**: `calc sin(45 * pi / 180)` → **0.707**
- **Logarithms**: `calc log(100)` → **2**
- **Direct expressions**: `2 + 3 * 4` → **14**

### 🌤️ Weather Information
- **Current conditions**: `weather Sydney`
- **5-day forecast**: `forecast Melbourne`
- **Multiple cities**: Detailed weather info for any location

### 📝 Task Management
- **Add tasks**: `task add Buy groceries`
- **List tasks**: `task list`
- **Complete tasks**: `task complete abc123`
- **Delete tasks**: `task delete abc123`
- **Persistent storage** with unique IDs

### 🎉 Fun & Entertainment
- **Programming jokes**: `joke`
- **Inspirational quotes**: `quote`
- **Team building content**

### 🔧 Productivity Tools
- **QR Codes**: `qr https://example.com`
- **Password Generator**: `password 16`
- **Polls**: `poll What's for lunch? Pizza, Burger, Sushi`
- **Random Picker**: `pick Alice, Bob, Charlie`

### 🤖 Smart Features
- **Natural Language Understanding**
- **Context Awareness**
- **Interactive Menus**: Use `menu` for easy navigation
- **Comprehensive Help**: Type `help` for full command list

## 📱 Teams App Installation

### Method 1: Manual Installation (Recommended)

1. **Download App Package**
   - Go to your repository → Actions → Latest successful deployment
   - Download "teams-bot-app-package" artifact
   - Extract the `teams-bot-app.zip` file

2. **Upload to Teams**
   - Open Microsoft Teams
   - Go to **Apps** → **Manage your apps**
   - Click **"Upload an app"** → **"Upload a custom app"**
   - Select the `teams-bot-app.zip` file
   - Follow installation prompts

3. **Start Using**
   - Add the bot to a team or use it personally
   - Type `help` to see all available commands
   - Start with `calc 2+2` or `weather your-city`

### Method 2: Admin Installation

For organization-wide deployment:

1. **Teams Admin Center**
   - Go to [Teams Admin Center](https://admin.teams.microsoft.com)
   - Navigate to **Teams apps** → **Manage apps**
   - Click **"Upload new app"**
   - Upload the `teams-bot-app.zip` file

2. **App Policies**
   - Set up app permission policies
   - Configure setup policies for automatic installation
   - Assign to specific users or groups

## 🧪 Testing Your Bot

Test all features in Microsoft Teams:

```bash
# Basic commands
hi                          # Welcome message
help                        # Complete command list
menu                        # Interactive menu

# Calculator
calc 2^3 + sqrt(16)        # Advanced math: 12
calc sin(30 * pi/180)      # Trigonometry: 0.5
5 * (3 + 2)                # Direct expression: 25

# Weather
weather London             # Current weather
forecast Tokyo             # 5-day forecast

# Task management
task add Buy groceries     # Add new task
task list                  # Show all tasks
task complete abc123       # Mark task complete
task delete def456         # Delete task

# Utilities
password 16                # Generate secure password
qr https://example.com     # Create QR code
poll Lunch? Pizza, Burger  # Create team poll
pick Alice, Bob, Charlie   # Random selection

# Fun
joke                       # Programming humor
quote                      # Inspirational quote
```

## 🔧 Local Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/teams-bot.git
cd teams-bot

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.template .env

# Edit .env with your bot credentials
nano .env
```

### Required Environment Variables

Create a `.env` file with:

```bash
# Bot Framework Credentials
MicrosoftAppId=your-bot-app-id
MicrosoftAppPassword=your-bot-app-password
MicrosoftAppTenantId=your-tenant-id

# Optional: Development settings
FLASK_ENV=development
FLASK_DEBUG=true
PORT=3978
```

### Run Locally

```bash
# Start the bot
python app.py

# Bot will be available at http://localhost:3978
```

### Test with Bot Framework Emulator

1. Download [Bot Framework Emulator](https://github.com/Microsoft/BotFramework-Emulator)
2. Open emulator and connect to `http://localhost:3978/api/messages`
3. Enter your Bot App ID and Password
4. Start testing bot commands

## 📊 Monitoring & Troubleshooting

### Health Checks

```bash
# Check bot health
curl https://your-app-name.azurewebsites.net/api/health

# Expected response:
{
  "status": "healthy",
  "service": "teams-productivity-bot",
  "version": "2.0.0"
}
```

### Azure App Service Logs

```bash
# View real-time logs
az webapp log tail --name teams-productivity-bot --resource-group rg-teams-bot

# Download log files
az webapp log download --name teams-productivity-bot --resource-group rg-teams-bot
```

### Common Issues & Solutions

1. **Bot not responding in Teams**
   - Verify bot endpoint URL in Bot Framework registration
   - Check Azure App Service is running
   - Validate MicrosoftAppId and MicrosoftAppPassword

2. **GitHub Actions deployment fails**
   - Check all GitHub secrets are correctly set
   - Verify publish profile is valid XML
   - Ensure basic authentication is enabled on App Service

3. **Teams app upload fails**
   - Confirm Microsoft Graph API permissions are granted
   - Verify admin consent for AppCatalog.ReadWrite.All
   - Check Teams manifest.json is valid

4. **Calculator not working**
   - Ensure mathematical expressions use proper syntax
   - Use `sqrt()` not `square_root()`
   - Check parentheses in complex expressions

### Application Insights

If you configured Application Insights, monitor:
- Request performance and failures
- Custom telemetry and logging
- User interaction patterns
- Error tracking and diagnostics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m 'Add calculator history feature'`
5. Push to your branch: `git push origin feature/amazing-feature`
6. Open a Pull Request with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Create an issue in this repository
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check Microsoft Teams Platform documentation
- **Azure Support**: Use Azure support channels for infrastructure issues

---

**Built with ❤️ for Microsoft Teams productivity**


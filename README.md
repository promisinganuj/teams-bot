# Teams Productivity Bot - AI-Powered Assistant 🤖

A comprehensive AI-powered Microsoft Teams bot that transforms your team's productivity. Built with Python Flask and the Bot Framework SDK, featuring advanced calculator, weather information, task management, and much more!

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fpromisinganuj%2Fteams-bot%2Fmain%2Fazure-deploy.json)
[![GitHub Actions](https://github.com/promisinganuj/teams-bot/workflows/Deploy%20Teams%20Bot%20to%20Azure/badge.svg)](https://github.com/promisinganuj/teams-bot/actions)

> **Note**: The Deploy to Azure button will work once the ARM template (`azure-deploy.json`) is committed to the main branch of this repository.

## 🚀 Deployment Guide

### 📋 Prerequisites

Before deploying, ensure you have:

- **Azure subscription** with appropriate permissions to create resources
- **Microsoft Bot Framework App ID and Password** (explained in detail below)
- **GitHub repository access** (for CI/CD setup)

> **💡 What is Bot Framework App ID and Password?**
> - **App ID**: A unique GUID that identifies your bot to Microsoft's Bot Framework service
> - **App Password**: A secret key that authenticates your bot's requests to Microsoft services
> - **Purpose**: These credentials allow your bot to send/receive messages through Microsoft Teams and other channels
> - **Security**: The password is only shown once when created, so save it immediately!

### 🎯 Initial Deployment

Choose your preferred deployment method:

#### Option A: One-Click Azure Deployment (Recommended)

**🔄 Status**: Available after ARM template is pushed to repository

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fpromisinganuj%2Fteams-bot%2Fmain%2Fazure-deploy.json)

**What this creates:**
- ✅ Azure App Service with Python 3.11
- ✅ Application Insights monitoring
- ✅ All necessary configurations
- ✅ Automatic code deployment

#### Option B: Manual ARM Template Deployment

If the one-click button doesn't work:

1. **Download the ARM template**
   ```bash
   curl -o azure-deploy.json https://raw.githubusercontent.com/promisinganuj/teams-bot/main/azure-deploy.json
   curl -o azure-deploy.parameters.json https://raw.githubusercontent.com/promisinganuj/teams-bot/main/azure-deploy.parameters.json
   ```

2. **Deploy via Azure CLI**
   ```bash
   az group create --name rg-teams-bot --location australiaeast
   az deployment group create \
     --resource-group rg-teams-bot \
     --template-file azure-deploy.json \
     --parameters azure-deploy.parameters.json \
     --parameters botAppId="YOUR_BOT_APP_ID" \
     --parameters botAppPassword="YOUR_BOT_PASSWORD"
   ```

#### Option C: Interactive Deployment Script

Use the helper script for guided deployment:
```bash
./scripts/deploy-azure.sh
```

### 🔄 Setting up CI/CD

After initial deployment, set up continuous deployment for ongoing updates:

## ✨ Features

### 🧮 **Advanced Calculator**
- Basic arithmetic: `calc 5 + 3 * 2`
- Advanced functions: `calc sqrt(16) + 2^3`
- Trigonometry: `calc sin(45 * pi / 180)`
- Logarithms: `calc log(100)` or `calc ln(10)`
- Direct expressions: Just type `2 + 3 * 4`

### 🌤️ **Weather Information**
- Current conditions: `weather Sydney`
- 5-day forecast: `forecast Melbourne`
- Multiple city support with detailed info

### 📝 **Task Management**
- Add tasks: `task add Buy groceries`
- List tasks: `task list`
- Complete tasks: `task complete abc123`
- Delete tasks: `task delete abc123`
- Persistent storage with unique IDs

### 🎉 **Fun & Entertainment**
- Programming jokes: `joke`
- Inspirational quotes: `quote`
- Random content for team building

### � **Productivity Tools**
- **QR Codes**: `qr https://example.com`
- **Password Generator**: `password 16`
- **Text Analysis**: Word counts, character analysis
- **Time Zones**: Convert times across zones

### 👥 **Team Utilities**
- **Polls**: `poll What's for lunch? Pizza, Burger, Sushi`
- **Random Picker**: `pick Alice, Bob, Charlie`
- **Team Decisions**: Fair random selection

### 🤖 **Smart Features**
- **Natural Language**: Understands various command formats
- **Context Awareness**: Remembers user preferences
- **Error Handling**: Helpful error messages
- **Interactive Menus**: Easy navigation with `menu`

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Microsoft     │    │   Azure App     │    │   Bot Framework │
│     Teams       │◄──►│    Service      │◄──►│      SDK        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Application   │
                    │    Insights     │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Azure subscription
- Microsoft Teams app registration
- GitHub repository with secrets configured

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/teams-bot.git
   cd teams-bot
   ```

2. **Set up environment**
   ```bash
   # Install uv (recommended) or use pip
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv pip install -r requirements.txt
   
   # Or with pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your values
   ```

4. **Run locally**
   ```bash
   python app.py
   # Or use make commands
   make dev
   ```

## 🤖 Bot Commands

### 🧮 Calculator Commands
| Command | Description | Example |
|---------|-------------|---------|
| `calc <expression>` | Advanced calculator | `calc 2^3 + sqrt(16)` → **12** |
| `calc sin(30)` | Trigonometry | `calc sin(30 * pi / 180)` → **0.5** |
| `calc log(100)` | Logarithm | `calc log(100)` → **2** |
| `5 + 3 * 2` | Direct math | `5 + 3 * 2` → **11** |

### 🌤️ Weather Commands
| Command | Description | Example |
|---------|-------------|---------|
| `weather <city>` | Current weather | `weather Sydney` |
| `forecast <city>` | 5-day forecast | `forecast Melbourne` |

### 📝 Task Commands
| Command | Description | Example |
|---------|-------------|---------|
| `task add <description>` | Add new task | `task add Buy groceries` |
| `task list` | Show all tasks | `task list` |
| `task complete <id>` | Complete task | `task complete abc123` |
| `task delete <id>` | Delete task | `task delete abc123` |

### 🎉 Fun Commands
| Command | Description | Example |
|---------|-------------|---------|
| `joke` | Programming joke | `joke` |
| `quote` | Inspirational quote | `quote` |

### 🔧 Utility Commands
| Command | Description | Example |
|---------|-------------|---------|
| `qr <text>` | Generate QR code | `qr https://example.com` |
| `password <length>` | Generate password | `password 16` |
| `poll <question>? <options>` | Create poll | `poll Favorite color? Red, Blue` |
| `pick <options>` | Random selection | `pick Alice, Bob, Charlie` |

### ℹ️ General Commands
| Command | Description | Example |
|---------|-------------|---------|
| `help` | Complete help guide | `help` |
| `menu` | Interactive menu | `menu` |
| `hi` / `hello` | Welcome message | `hello` |

#### Step 1: Bot Framework Registration

The **Microsoft Bot Framework App ID and Password** are credentials that authenticate your bot with Microsoft's Bot Framework service. Here's how to get them:

1. **Create Azure Bot Resource**
   
   **Via Azure Portal:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "Create a resource" → Search for "Azure Bot"
   - Click "Create" and fill in:
     - **Bot handle**: `teams-productivity-bot` (must be globally unique)
     - **Subscription**: Select your Azure subscription
     - **Resource group**: Create new or use existing
     - **Pricing tier**: F0 (free) for development
     - **Microsoft App ID**: Select "Create new Microsoft App ID"
   - Click "Create"

   **Via Azure CLI:**
   ```bash
   # Create resource group
   az group create --name rg-teams-bot --location australiaeast
   
   # Create bot registration
   az bot create --resource-group rg-teams-bot \
     --name teams-productivity-bot \
     --kind registration \
     --sku F0 \
     --appid $(uuidgen) \
     --password $(openssl rand -base64 32)
   ```

2. **Get App ID and Create App Secret**
   
   **Get App ID:**
   - In Azure Portal, go to your Bot resource
   - Under "Settings" → "Configuration"
   - Copy the **Microsoft App ID** (GUID format: `12345678-1234-1234-1234-123456789012`)
   
   **Create App Secret:**
   - In the same Configuration page, click "Manage" next to Microsoft App ID
   - This opens Azure AD App Registration
   - Go to "Certificates & secrets" → "Client secrets"
   - Click "New client secret"
   - Add description: "Teams Bot Secret"
   - Set expiration (24 months recommended)
   - Click "Add" and **immediately copy the secret value** (you won't see it again!)

   **Add Microsoft Graph API Permissions (Required for Teams App Upload):**
   - In the same Azure AD App Registration, go to "API permissions"
   - Click "Add a permission" → "Microsoft Graph" → "Application permissions"
   - Search and select: `AppCatalog.ReadWrite.All`
   - Click "Add permissions"
   - Click "Grant admin consent for [Your Organization]" (requires admin rights)
   - Wait for status to show "Granted for [Your Organization]"

   > **⚠️ Important**: Without `AppCatalog.ReadWrite.All` permission, the Teams app upload will fail with "403 Forbidden" error.

3. **Configure Bot Endpoint**
   - Back in your Bot resource, under "Settings" → "Configuration"
   - Set **Messaging endpoint**: `https://your-app-name.azurewebsites.net/api/messages`
   - Replace `your-app-name` with your actual Azure App Service name
   - Click "Apply"

4. **Enable Teams Channel**
   - In Bot resource → Channels
   - Add Microsoft Teams channel
   - Configure and save

#### Step 2: Configure GitHub Repository

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/promisinganuj/teams-bot.git
   cd teams-bot
   ```

2. **Get Azure Publish Profile**
   ```bash
   # Download from Azure Portal or use CLI
   az webapp deployment list-publishing-profiles \
     --name teams-productivity-bot \
     --resource-group rg-teams-bot \
     --xml
   ```

3. **Configure GitHub Secrets**
   
   Go to GitHub Repository → Settings → Secrets and Variables → Actions
   
   **Required Secrets:**

   | Secret | Description | Example | Where to Find |
   |--------|-------------|---------|---------------|
   | `AZURE_WEBAPP_NAME` | Name of your Azure Web App | `teams-productivity-bot` | Azure Portal → App Service name |
   | `AZURE_WEBAPP_PUBLISH_PROFILE` | Azure publish profile XML | `<publishData>...</publishData>` | Azure Portal → App Service → Get publish profile |
   | `BOT_APP_ID` | Microsoft Bot Framework App ID | `12345678-1234-1234-1234-123456789012` | Azure Portal → Bot resource → Configuration |
   | `BOT_APP_PASSWORD` | Microsoft Bot Framework App Secret | `abc123XYZ_secret_value` | Azure AD → App registrations → Certificates & secrets |
   | `TENANT_ID` | Azure AD Tenant ID | `87654321-4321-4321-4321-210987654321` | Azure Portal → Azure Active Directory → Properties |
   | `GRAPH_CLIENT_ID` | Microsoft Graph App ID | `11111111-2222-3333-4444-555555555555` | Azure AD → App registrations (same as BOT_APP_ID) |
   | `GRAPH_CLIENT_SECRET` | Microsoft Graph App Secret | `def456ABC_graph_secret` | Azure AD → App registrations → Certificates & secrets |

#### Step 3: Enable Automated Deployment

1. **Trigger First Deployment**
   ```bash
   # Push to main branch triggers CI/CD pipeline
   git add .
   git commit -m "Enable CI/CD deployment"
   git push origin main
   ```

2. **Monitor Deployment**
   - Go to GitHub Repository → Actions
   - Watch the "Deploy Teams Bot to Azure" workflow
   - Verify each step: Test → Build → Deploy → Upload Manifest

#### Step 4: Verify Deployment

```bash
# Check health endpoint
curl https://your-app-name.azurewebsites.net/api/health

# Should return:
# {"status": "healthy", "service": "teams-productivity-bot", "version": "2.0.0"}
```

### 🔧 Alternative Deployment Methods

#### Using Terraform (Infrastructure as Code)

1. **Configure variables**
   ```bash
   cd infra
   cp terraform.tfvars.example terraform.tfvars
   # Edit with your values
   ```

2. **Deploy infrastructure**
   ```bash
   terraform init
   terraform plan
### 📱 Teams App Setup

After successful deployment, configure the Teams app:

#### Automatic Upload (via CI/CD)
The GitHub Actions workflow automatically uploads the Teams app manifest.

#### Manual Upload
```bash
python scripts/upload_manifest.py
```

#### Install in Teams
1. Go to Microsoft Teams
2. Apps → Manage Apps → Upload Custom App
3. Select the uploaded bot
4. Add to team or use personally

### 🧪 Testing Your Deployment

Test all bot features in Teams:
```
Hi                           # Welcome message
calc 2^3 + sqrt(16)         # Calculator: 12
weather Sydney              # Weather info
task add Buy groceries      # Task management
joke                        # Programming humor
password 16                 # Secure password
poll Lunch? Pizza, Burger   # Create poll
pick Alice, Bob, Charlie    # Random selection
help                        # Complete guide
```

### 🔧 Troubleshooting

#### Common Issues & Solutions

**❌ "Invalid value 'DISABLE_COLLECTSTATIC' for key '1'" Error**

This occurs when Azure Oryx build system receives invalid boolean values.

**Solution:**
```bash
# Update App Service configuration
az webapp config appsettings set --resource-group <your-rg> --name <your-app> \
  --settings DISABLE_COLLECTSTATIC=true

# Or via Azure Portal:
# App Service → Configuration → Application Settings
# Set DISABLE_COLLECTSTATIC = true (not 1 or DISABLE_COLLECTSTATIC)
```

**Root Cause:** Boolean environment variables must be exactly "true" or "false", not "1" or variable names.

**❌ "Basic Authentication is Disabled" Error**

**Solution:**
```bash
# Enable basic auth for deployment
az webapp config set --resource-group <your-rg> --name <your-app> --basic-auth-enabled true
az resource update --resource-group <your-rg> --name scm --namespace Microsoft.Web \
  --resource-type basicPublishingCredentialsPolicies --parent sites/<your-app> \
  --set properties.allow=true
```

**❌ "Missing role permissions: AppCatalog.ReadWrite.All" Error**

This occurs when trying to upload Teams app manifest without proper Graph API permissions.

**Solution:**
1. **Via Azure Portal**:
   - Go to Azure AD → App registrations → Your bot app
   - Navigate to "API permissions"
   - Click "Add a permission" → Microsoft Graph → Application permissions
   - Add `AppCatalog.ReadWrite.All`
   - Click "Grant admin consent" (requires admin privileges)

2. **Alternative: Manual Teams App Upload**:
   ```bash
   # If you can't get admin consent, upload manually to Teams
   # 1. Download the app package from GitHub Actions artifacts
   # 2. Go to Teams Admin Center → Teams apps → Manage apps
   # 3. Click "Upload new app" → Upload custom app
   ```

**❌ "Icon not found" Warning**

**Solution:**
```bash
# Icons are now included in the repository
# If missing, they'll be created automatically during deployment
```

**❌ GitHub Action Fails**
- Verify all GitHub secrets are correctly set
- Check Azure resource names match configuration
- Ensure publish profile is valid XML format

**❌ Bot Not Responding**
```bash
# Check Azure App Service logs
az webapp log tail --name teams-productivity-bot --resource-group rg-teams-bot

# Verify bot endpoint in Azure Bot resource
# Ensure MicrosoftAppId/Password are correct
```

**❌ Teams Manifest Upload Fails**
- Verify Microsoft Graph API permissions
- Check tenant ID and app registration
- Ensure manifest.json is valid JSON

**❌ Deployment Status Check**
```bash
# Health check
curl https://your-app-name.azurewebsites.net/api/health

# Check Azure logs
az webapp log tail --name your-app-name --resource-group your-rg
```

## 📁 Project Structure

```
teams-bot/
├── 📄 app.py                    # Main Flask application
├── 🤖 my_bot.py                 # Enhanced bot logic and handlers
├── 📦 requirements.txt          # Python dependencies
├── ⚙️  pyproject.toml            # Project configuration
├── 🚀 wsgi.py                   # Production WSGI server
├── 🌍 .env.template             # Environment variables template
├── 📋 .gitignore                # Git ignore rules
├── 📖 README.md                 # This file
├── � Makefile                  # Development commands
├── 🐳 Dockerfile.dev            # Development container
├── 🐳 docker-compose.yml        # Local development setup
├── �🔧 infra/                    # Terraform infrastructure
│   ├── main.tf                  # Main Terraform configuration
│   ├── variables.tf             # Variable definitions
│   ├── outputs.tf               # Output values
│   └── terraform.tfvars         # Variable values
├── 📱 teams_app/                # Teams app manifest
│   ├── manifest.json            # Teams app manifest
│   └── README.md                # Icons information
├── 🔄 .github/workflows/        # GitHub Actions
│   └── deploy.yml               # CI/CD pipeline
├── 📝 scripts/                  # Utility scripts
│   └── upload_manifest.py       # Teams app upload script
└── 🧪 tests/                    # Test suite
    ├── __init__.py
    └── test_bot.py              # Comprehensive bot tests
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
make install

# Run all tests
make test

# Run with coverage
make test-cov

# Format code
make format

# Lint code
make lint
```

## 🔧 Development

### Using Make Commands

```bash
# Setup development environment
make setup

# Run in development mode
make dev

# Run tests
make test

# Clean temporary files
make clean

# Docker development
make docker-run
```

### Manual Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run tests
python -m pytest tests/ -v

# Format code
black *.py tests/

# Lint code
flake8 *.py tests/
```

## 🔒 Security

- Bot credentials stored as Azure App Settings
- Secrets managed through GitHub Secrets
- HTTPS enforcement in production
- Input validation and sanitization
- Proper error handling without information disclosure
- Safe mathematical expression evaluation

## 📊 Monitoring

- **Health Check Endpoints**: `GET /` and `GET /api/health`
- **Application Insights**: Automatic logging and telemetry
- **Azure Monitor**: Performance and availability monitoring
- **Structured Logging**: Comprehensive application logs
- **Error Tracking**: Detailed error reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Bot not responding in Teams**
   - Check Azure App Service logs
   - Verify bot endpoint URL in Bot Framework registration
   - Ensure `MicrosoftAppId` and `MicrosoftAppPassword` are correct

2. **Calculator not working**
   - Check mathematical expression syntax
   - Verify function names (use `sqrt` not `square_root`)
   - Ensure proper parentheses in complex expressions

3. **Task management issues**
   - Tasks are stored in memory (use database for production)
   - Each user has separate task list
   - Task IDs are unique 8-character strings

4. **Weather data not showing**
   - Currently using mock data for demo
   - Integrate with OpenWeatherMap API for production
   - Check API key configuration

### Getting Help

- Create an issue in this repository
- Check Azure App Service diagnostics
- Review GitHub Actions workflow logs
- Consult Microsoft Teams developer documentation

## ❓ Frequently Asked Questions

### Q: Why is the "Deploy to Azure" button not working?

**A: Several reasons could cause this:**

1. **ARM Template Not Available**: The `azure-deploy.json` file must be committed to the `main` branch of the repository
   
   **Solution**: 
   ```bash
   # If you're a maintainer, commit the files:
   git add azure-deploy.json azure-deploy.parameters.json
   git commit -m "Add ARM template for one-click deployment"
   git push origin main
   ```

2. **Repository Access**: The repository might be private or the file path is incorrect
   
   **Solution**: Use the manual ARM template deployment (Option 1.5 above)

3. **URL Encoding Issues**: Sometimes the encoded URL in the button doesn't work correctly
   
   **Solution**: Copy the raw GitHub URL and paste it directly into Azure Portal:
   ```
   https://raw.githubusercontent.com/promisinganuj/teams-bot/main/azure-deploy.json
   ```

### Q: What does "Deploy to Azure" actually do?

**A: The button creates these Azure resources:**
- Azure App Service (Web App) with Python 3.11 runtime
- Azure App Service Plan (hosting plan)
- Application Insights (monitoring and logging)
- Automatic deployment from GitHub repository
- Configuration of all required environment variables

### Q: Can I customize the deployment?

**A: Yes! You have several options:**
1. Edit `azure-deploy.parameters.json` before deployment
2. Use the manual Azure CLI deployment with custom parameters
3. Use Terraform (in `/infra` directory) for full infrastructure control
4. Fork the repository and modify the ARM template

---

## 🎯 What's New in v2.0

### Major Features Added:
- ✅ **Advanced Calculator** - Full mathematical expression support
- ✅ **Weather Integration** - Current weather and forecasts
- ✅ **Task Management** - Complete task lifecycle
- ✅ **QR Code Generation** - URL and text QR codes
- ✅ **Password Generator** - Secure password creation
- ✅ **Team Utilities** - Polls and random selection
- ✅ **Fun Commands** - Jokes and inspirational quotes
- ✅ **Smart Parsing** - Natural language understanding
- ✅ **Interactive Menus** - Better user experience

### Technical Improvements:
- 🔧 **Enhanced Error Handling** - Graceful failure recovery
- 🔧 **Comprehensive Testing** - Full test coverage
- 🔧 **Better Documentation** - Complete usage guide
- 🔧 **Performance Optimization** - Faster response times

**Built with ❤️ using Python, Azure, and Microsoft Teams Platform**


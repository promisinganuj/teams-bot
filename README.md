# Teams Productivity Bot - AI-Powered Assistant 🤖

A comprehensive AI-powered Microsoft Teams bot that transforms your team's productivity. Built with Python Flask and the Bot Framework SDK, featuring advanced calculator, weather information, task management, and much more!

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fpromisinganuj%2Fteams-bot%2Fmain%2Fazure-deploy.json)
[![GitHub Actions](https://github.com/promisinganuj/teams-bot/workflows/Deploy%20Teams%20Bot%20to%20Azure/badge.svg)](https://github.com/promisinganuj/teams-bot/actions)

> **Note**: The Deploy to Azure button will work once the ARM template (`azure-deploy.json`) is committed to the main branch of this repository.

## 🚀 Quick Deploy Options

### Option 1: One-Click Azure Deployment

**🔄 Status**: Available after ARM template is pushed to repository

Once the Azure ARM template is available in the repository, you can use the one-click deployment:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fpromisinganuj%2Fteams-bot%2Fmain%2Fazure-deploy.json)

**What this does:**
- ✅ Creates Azure App Service with Python 3.11
- ✅ Deploys the bot code automatically
- ✅ Configures all necessary settings
- ✅ Sets up Application Insights monitoring

**You'll need:**
- Azure subscription
- Bot Framework App ID and Password
- 5 minutes of your time

### Option 1.5: Manual ARM Template Deployment

If the one-click button doesn't work, you can deploy manually:

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

### Option 2: GitHub Actions CI/CD
Use the automated pipeline for continuous deployment (see deployment guide below).

### Option 3: Manual Deployment
Use the helper script: `./scripts/deploy-azure.sh`

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

## ☁️ Azure Deployment

### Infrastructure Setup

1. **Configure Terraform variables**
   ```bash
   cd infra
   cp terraform.tfvars.example terraform.tfvars
   # Edit with your values
   ```

2. **Deploy infrastructure**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### CI/CD Setup

Configure GitHub Secrets:

| Secret | Description |
|--------|-------------|
| `AZURE_WEBAPP_NAME` | Name of your Azure Web App |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Azure publish profile |
| `BOT_APP_ID` | Microsoft Bot Framework App ID |
| `BOT_APP_PASSWORD` | Microsoft Bot Framework App Secret |
| `TENANT_ID` | Azure AD Tenant ID |
| `GRAPH_CLIENT_ID` | Microsoft Graph App ID |
| `GRAPH_CLIENT_SECRET` | Microsoft Graph App Secret |
| `AZURE_CREDENTIALS` | Azure service principal credentials |

### 🚀 Complete Deployment Guide

#### **Step 1: Azure Prerequisites**

1. **Create Azure Resources** (via Azure Portal or Terraform)
   ```bash
   # Option A: Use Terraform (Recommended)
   cd infra
   terraform init
   terraform apply -var="resource_group_name=rg-teams-bot" \
                   -var="bot_app_id=YOUR_BOT_APP_ID" \
                   -var="bot_app_password=YOUR_BOT_PASSWORD"
   
   # Option B: Use Azure CLI
   az group create --name rg-teams-bot --location australiaeast
   az appservice plan create --name plan-teams-bot --resource-group rg-teams-bot --sku B1 --is-linux
   az webapp create --name teams-productivity-bot --resource-group rg-teams-bot --plan plan-teams-bot --runtime "PYTHON:3.11"
   ```

2. **Get Publish Profile**
   ```bash
   # Download publish profile from Azure Portal or CLI
   az webapp deployment list-publishing-profiles --name teams-productivity-bot --resource-group rg-teams-bot --xml
   ```

#### **Step 2: Bot Framework Setup**

1. **Register Bot in Azure**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create "Azure Bot" resource
   - Note down `App ID` and create `App Secret`
   - Set Messaging Endpoint: `https://your-app-name.azurewebsites.net/api/messages`

2. **Enable Teams Channel**
   - In Bot resource → Channels
   - Add Microsoft Teams channel
   - Configure and save

#### **Step 3: GitHub Repository Setup**

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/promisinganuj/teams-bot.git
   cd teams-bot
   ```

2. **Configure GitHub Secrets**
   
   Go to GitHub Repository → Settings → Secrets and Variables → Actions
   
   **Required Secrets:**
   ```
   AZURE_WEBAPP_NAME=teams-productivity-bot
   AZURE_WEBAPP_PUBLISH_PROFILE=<paste-publish-profile-xml>
   BOT_APP_ID=12345678-1234-1234-1234-123456789012
   BOT_APP_PASSWORD=your-bot-app-secret
   TENANT_ID=your-azure-tenant-id
   GRAPH_CLIENT_ID=your-graph-app-id  
   GRAPH_CLIENT_SECRET=your-graph-app-secret
   ```

#### **Step 4: Deployment Process**

The deployment is **completely automated** via GitHub Actions:

1. **Trigger Deployment**
   ```bash
   # Push to main branch triggers deployment
   git add .
   git commit -m "Deploy enhanced bot"
   git push origin main
   ```

2. **Monitor Deployment**
   - Go to GitHub Repository → Actions
   - Watch the "Deploy Teams Bot to Azure" workflow
   - Check each step: Test → Build → Deploy → Upload Manifest

3. **Verify Deployment**
   ```bash
   # Check if app is running
   curl https://your-app-name.azurewebsites.net/
   
   # Should return:
   # {"status": "healthy", "service": "teams-productivity-bot", "version": "2.0.0"}
   ```

#### **Step 5: Teams App Setup**

1. **Upload to Teams**
   
   The GitHub Action automatically uploads the Teams app, or manually:
   ```bash
   python scripts/upload_manifest.py
   ```

2. **Install in Teams**
   - Go to Microsoft Teams
   - Apps → Manage Apps → Upload Custom App
   - Select the uploaded bot
   - Add to team or use personally

#### **Step 6: Testing**

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

### 🔧 **Troubleshooting Deployment**

#### **Common Issues & Solutions**

1. **❌ GitHub Action Fails**
   ```bash
   # Check secrets are correctly set
   # Verify Azure resource names match
   # Ensure publish profile is valid XML
   ```

2. **❌ Bot Not Responding**
   ```bash
   # Check Azure App Service logs
   az webapp log tail --name teams-productivity-bot --resource-group rg-teams-bot
   
   # Verify bot endpoint in Azure Bot resource
   # Ensure MicrosoftAppId/Password are correct
   ```

3. **❌ Teams Manifest Upload Fails**
   ```bash
   # Verify Microsoft Graph API permissions
   # Check tenant ID and app registration
   # Ensure manifest.json is valid
   ```

4. **❌ Dependencies Missing**
   ```bash
   # Check requirements.txt includes all packages
   # Verify Python version is 3.11
   # Check Azure build logs for errors
   ```

### 📊 **Deployment Status Check**

After deployment, verify everything works:

```bash
# 1. Health Check
curl https://your-app-name.azurewebsites.net/api/health

# 2. Test Bot Endpoint (requires proper headers)
curl -X POST https://your-app-name.azurewebsites.net/api/messages \
     -H "Content-Type: application/json" \
     -d '{"type":"message","text":"hello"}'

# 3. Check Azure Logs
az webapp log tail --name your-app-name --resource-group your-rg
```

### 🎯 **Production Considerations**

1. **Security**
   - Store secrets in Azure Key Vault
   - Enable HTTPS only
   - Configure CORS if needed

2. **Performance** 
   - Scale up App Service plan for production
   - Enable Application Insights monitoring
   - Set up alerts for failures

3. **Database**
   - Replace in-memory task storage with Azure SQL/CosmosDB
   - Implement proper data persistence
   - Add data backup strategies

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


# Teams Productivity Bot - AI-Powered Assistant 🤖

A comprehensive AI-powered Microsoft Teams bot that transforms your team's productivity. Built with Python Flask and the Bot Framework SDK, featuring advanced calculator, weather information, task management, and much more!

[![Deploy to Azure](https://github.com/yourusername/teams-bot/workflows/Deploy%20Teams%20Bot%20to%20Azure/badge.svg)](https://github.com/promisinganuj/teams-bot/actions)

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


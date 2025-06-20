#!/usr/bin/env python3
"""
Teams Bot Troubleshooting Script
Diagnoses common issues with Teams bot deployment and configuration
"""

import requests
import json
import os
import sys

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(check, status, details=""):
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {check}")
    if details:
        print(f"   → {details}")

def check_azure_deployment():
    """Check if the Azure deployment is working"""
    print_header("AZURE DEPLOYMENT STATUS")
    
    app_name = "teams-productivity-bot"  # Replace with your actual app name
    base_url = f"https://{app_name}.azurewebsites.net"
    
    # Test root endpoint
    try:
        response = requests.get(base_url, timeout=10)
        print_status("Root endpoint accessible", response.status_code == 200, 
                    f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
    except Exception as e:
        print_status("Root endpoint accessible", False, f"Error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print_status("Health endpoint accessible", response.status_code == 200,
                    f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Bot configured: {data.get('bot_configured', 'Unknown')}")
            print(f"   Environment: {data.get('environment', 'Unknown')}")
    except Exception as e:
        print_status("Health endpoint accessible", False, f"Error: {e}")
    
    # Test bot messages endpoint
    try:
        response = requests.get(f"{base_url}/api/messages", timeout=10)
        # Should return 405 Method Not Allowed for GET, which means endpoint exists
        print_status("Bot messages endpoint exists", response.status_code == 405,
                    f"Status: {response.status_code} (405 expected for GET)")
    except Exception as e:
        print_status("Bot messages endpoint exists", False, f"Error: {e}")

def check_environment_variables():
    """Check environment variable configuration"""
    print_header("ENVIRONMENT VARIABLES")
    
    # Read from GitHub secrets documentation
    required_vars = {
        "AZURE_WEBAPP_NAME": "Azure Web App name",
        "BOT_APP_ID": "Microsoft Bot Framework App ID", 
        "BOT_APP_PASSWORD": "Microsoft Bot Framework App Password",
        "TENANT_ID": "Azure AD Tenant ID"
    }
    
    print("Required GitHub Secrets (check in repo settings):")
    for var, desc in required_vars.items():
        print(f"  • {var}: {desc}")
    
    print("\nThese should be configured in:")
    print("  GitHub Repo → Settings → Secrets and Variables → Actions")

def check_bot_registration():
    """Check bot registration configuration"""
    print_header("BOT REGISTRATION CHECKLIST")
    
    print("✓ Verify in Azure Portal → Bot Services → Your Bot:")
    print("  1. Messaging endpoint is set to: https://your-app-name.azurewebsites.net/api/messages")
    print("  2. Microsoft Teams channel is enabled")
    print("  3. App ID and Password are correctly configured")
    print("  4. Bot is published and available")
    
    print("\n✓ Verify in Azure AD → App Registrations → Your Bot App:")
    print("  1. App ID matches the one in Bot Service")
    print("  2. Client secret is valid and not expired")
    print("  3. API permissions include necessary Graph permissions (if using)")

def check_teams_app():
    """Check Teams app configuration"""
    print_header("TEAMS APP CONFIGURATION")
    
    print("✓ Verify Teams App Manifest:")
    print("  1. Bot ID in manifest matches Azure Bot registration App ID")
    print("  2. App is uploaded to your Teams organization")
    print("  3. App permissions are granted")
    print("  4. App is installed in the team/chat where you're testing")
    
    print("\n✓ Test the bot:")
    print("  1. Try direct message to the bot: @YourBotName hello")
    print("  2. Try in a channel where bot is added: hello") 
    print("  3. Check if bot appears in Apps → Built for your org")

def suggest_fixes():
    """Suggest common fixes"""
    print_header("COMMON FIXES")
    
    print("🔧 If bot is not responding:")
    print("  1. Check Azure App Service logs:")
    print("     az webapp log tail --name your-app-name --resource-group your-rg")
    print("  2. Restart the Azure App Service")
    print("  3. Verify environment variables in Azure App Service Configuration")
    print("  4. Check if the bot endpoint URL is correct in Bot Service settings")
    
    print("\n🔧 If authentication fails:")
    print("  1. Regenerate bot password in Azure AD → App Registrations")
    print("  2. Update GitHub secrets with new password")
    print("  3. Redeploy the application")
    
    print("\n🔧 If Teams doesn't recognize the bot:")
    print("  1. Re-upload the Teams app package")
    print("  2. Check bot ID consistency across all configurations")
    print("  3. Wait 5-10 minutes for Teams to propagate changes")

def main():
    print("Teams Bot Troubleshooting Tool")
    print("This script helps diagnose common Teams bot issues")
    
    check_azure_deployment()
    check_environment_variables()
    check_bot_registration()
    check_teams_app()
    suggest_fixes()
    
    print_header("NEXT STEPS")
    print("1. Fix any ❌ issues identified above")
    print("2. Check Azure App Service logs for detailed error messages")
    print("3. Test bot responses after fixes")
    print("4. If issues persist, check the troubleshooting section in README.md")

if __name__ == "__main__":
    main()

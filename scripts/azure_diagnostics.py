#!/usr/bin/env python3
"""
Quick Azure diagnostics for Teams bot deployment
"""
import subprocess
import json
import sys

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def check_azure_login():
    """Check Azure login status"""
    print("🔐 Checking Azure login status...")
    account_info = run_command("az account show")
    if account_info:
        account = json.loads(account_info)
        print(f"✓ Logged in as: {account.get('user', {}).get('name')}")
        print(f"✓ Subscription: {account.get('name')}")
        return True
    else:
        print("❌ Not logged into Azure. Run: az login")
        return False

def list_app_services():
    """List App Services in subscription"""
    print("\n🔍 Finding App Services...")
    result = run_command("az webapp list --query '[].{name:name, resourceGroup:resourceGroup, state:state, defaultHostName:defaultHostName}' -o table")
    if result:
        print(result)
        return True
    return False

def check_specific_app_service(resource_group, app_name):
    """Check specific App Service details"""
    print(f"\n🔍 Checking App Service: {app_name}")
    
    # Get app settings
    print("\n📋 App Settings:")
    settings = run_command(f"az webapp config appsettings list -g {resource_group} -n {app_name} --query '[].{{name:name,value:value}}' -o table")
    if settings:
        print(settings)
    
    # Get recent logs
    print(f"\n📝 Recent logs for {app_name}:")
    print("(This will show recent application logs - press Ctrl+C to stop)")
    try:
        subprocess.run(f"az webapp log tail -g {resource_group} -n {app_name} --provider application", shell=True, timeout=10)
    except subprocess.TimeoutExpired:
        print("Log tail stopped after 10 seconds")
    except KeyboardInterrupt:
        print("\nLog monitoring stopped")

def main():
    print("🔧 Azure Teams Bot Diagnostics")
    print("=" * 50)
    
    if not check_azure_login():
        return
    
    if not list_app_services():
        print("No App Services found or error occurred")
        return
    
    # Ask user for App Service details
    print("\n" + "=" * 50)
    resource_group = input("Enter your Resource Group name (or press Enter to skip): ").strip()
    app_name = input("Enter your App Service name (or press Enter to skip): ").strip()
    
    if resource_group and app_name:
        check_specific_app_service(resource_group, app_name)
    else:
        print("Skipping detailed App Service check")
    
    print("\n✅ Diagnostics completed!")
    print("\nCommon issues to check:")
    print("1. MicrosoftAppId and MicrosoftAppPassword are set in App Settings")
    print("2. Python version is set correctly (3.9+)")
    print("3. All dependencies are installed (check deployment logs)")
    print("4. Bot endpoint URL matches what's configured in Azure Bot Service")

if __name__ == "__main__":
    main()

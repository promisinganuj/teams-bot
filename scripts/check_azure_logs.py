#!/usr/bin/env python3
"""
Script to check Azure App Service logs for the Teams bot
"""
import subprocess
import sys
import json
from datetime import datetime, timedelta

def run_az_command(command):
    """Run Azure CLI command and return output"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_azure_login():
    """Check if user is logged into Azure CLI"""
    result = run_az_command("az account show")
    if result:
        account = json.loads(result)
        print(f"✓ Logged into Azure as: {account.get('user', {}).get('name')}")
        print(f"✓ Subscription: {account.get('name')} ({account.get('id')})")
        return True
    else:
        print("❌ Not logged into Azure CLI. Please run: az login")
        return False

def get_app_service_logs(resource_group, app_name):
    """Get recent logs from App Service"""
    print(f"\n📋 Getting logs for App Service: {app_name}")
    
    # Get application logs
    print("\n=== Application Logs ===")
    app_logs = run_az_command(f"az webapp log tail --resource-group {resource_group} --name {app_name} --provider application")
    if app_logs:
        print(app_logs)
    else:
        print("No application logs found or error retrieving logs")
    
    # Get HTTP logs
    print("\n=== HTTP Logs ===")
    http_logs = run_az_command(f"az webapp log tail --resource-group {resource_group} --name {app_name} --provider http")
    if http_logs:
        print(http_logs)
    else:
        print("No HTTP logs found or error retrieving logs")

def get_app_service_config(resource_group, app_name):
    """Get App Service configuration"""
    print(f"\n⚙️ Getting configuration for App Service: {app_name}")
    
    # Get app settings
    settings = run_az_command(f"az webapp config appsettings list --resource-group {resource_group} --name {app_name}")
    if settings:
        settings_json = json.loads(settings)
        print("\n=== App Settings ===")
        for setting in settings_json:
            name = setting['name']
            value = setting['value']
            # Hide sensitive values
            if any(sensitive in name.lower() for sensitive in ['password', 'secret', 'key']):
                value = '***HIDDEN***'
            print(f"{name}: {value}")
    
    # Get general config
    print("\n=== General Configuration ===")
    config = run_az_command(f"az webapp config show --resource-group {resource_group} --name {app_name}")
    if config:
        config_json = json.loads(config)
        print(f"Python Version: {config_json.get('pythonVersion', 'Not set')}")
        print(f"Always On: {config_json.get('alwaysOn', False)}")
        print(f"HTTP20 Enabled: {config_json.get('http20Enabled', False)}")

def main():
    print("🔍 Azure App Service Diagnostics")
    print("=" * 50)
    
    if not check_azure_login():
        return
    
    # You'll need to replace these with your actual values
    resource_group = input("Enter your Resource Group name: ").strip()
    app_name = input("Enter your App Service name: ").strip()
    
    if not resource_group or not app_name:
        print("❌ Resource Group and App Service name are required")
        return
    
    try:
        # Get configuration
        get_app_service_config(resource_group, app_name)
        
        # Get logs
        print("\n" + "=" * 50)
        print("📋 Recent Logs (press Ctrl+C to stop)")
        get_app_service_logs(resource_group, app_name)
        
    except KeyboardInterrupt:
        print("\n\n✓ Log monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

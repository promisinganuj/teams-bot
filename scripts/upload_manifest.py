#!/usr/bin/env python3
"""
Microsoft Teams App Manifest Upload Script
Uploads a Teams app package to the Microsoft Teams App Catalog via Microsoft Graph API
"""

import requests
import os
import sys
import json
import zipfile
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_access_token():
    """Get access token from Microsoft Graph API"""
    tenant_id = os.environ.get("TENANT_ID")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    
    if not all([tenant_id, client_id, client_secret]):
        logger.error("Missing required environment variables: TENANT_ID, CLIENT_ID, CLIENT_SECRET")
        sys.exit(1)
    
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    
    try:
        logger.info("Acquiring access token...")
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to acquire access token: {e}")
        sys.exit(1)

def create_app_package():
    """Create Teams app package zip file"""
    logger.info("Creating Teams app package...")
    
    # Replace placeholders in manifest
    manifest_path = "teams_app/manifest.json"
    if not os.path.exists(manifest_path):
        logger.error(f"Manifest file not found: {manifest_path}")
        sys.exit(1)
        
    with open(manifest_path, 'r') as f:
        manifest_content = f.read()
    
    # Replace environment variables in manifest
    bot_app_id = os.environ.get("BOT_APP_ID", "")
    azure_domain = os.environ.get("AZURE_WEBAPP_DOMAIN", "")
    
    manifest_content = manifest_content.replace("{{BOT_APP_ID}}", bot_app_id)
    manifest_content = manifest_content.replace("{{AZURE_WEBAPP_DOMAIN}}", azure_domain)
    
    # Create temporary zip file
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add manifest
        zipf.writestr("manifest.json", manifest_content)
        
        # Add icons
        icon_files = ["color.png", "outline.png"]
        for icon_file in icon_files:
            icon_path = f"teams_app/{icon_file}"
            if os.path.exists(icon_path):
                zipf.write(icon_path, icon_file)
            else:
                logger.warning(f"Icon not found: {icon_path}")
    
    logger.info(f"Created app package: {temp_zip.name}")
    return temp_zip.name

def upload_app_package(token, package_path):
    """Upload the Teams app package with multiple fallback approaches"""
    
    # Try different upload approaches
    upload_approaches = [
        {
            "name": "Global App Catalog (Standard)",
            "url": "https://graph.microsoft.com/v1.0/appCatalogs/teamsApps",
            "headers": {"Authorization": f"Bearer {token}"}
        },
        {
            "name": "Beta API Endpoint", 
            "url": "https://graph.microsoft.com/beta/appCatalogs/teamsApps",
            "headers": {"Authorization": f"Bearer {token}"}
        }
    ]
    
    for approach in upload_approaches:
        logger.info(f"Trying upload approach: {approach['name']}")
        
        try:
            with open(package_path, "rb") as f:
                response = requests.post(
                    approach["url"],
                    headers=approach["headers"],
                    files={"file": ("teams-app.zip", f, "application/zip")}
                )
            
            if response.status_code == 201:
                logger.info("✅ Teams app uploaded successfully!")
                app_info = response.json()
                logger.info(f"App ID: {app_info.get('id', 'N/A')}")
                logger.info(f"Display Name: {app_info.get('displayName', 'N/A')}")
                logger.info(f"Version: {app_info.get('version', 'N/A')}")
                return True
            elif response.status_code == 409:
                logger.warning("⚠️  App already exists")
                logger.info(f"Response: {response.text}")
                return True
            elif response.status_code in [401, 403]:
                logger.warning(f"❌ {approach['name']} failed with {response.status_code}")
                logger.warning(f"Response: {response.text}")
                continue  # Try next approach
            else:
                logger.warning(f"❌ {approach['name']} failed with {response.status_code}: {response.text}")
                continue  # Try next approach
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"❌ {approach['name']} failed with exception: {e}")
            continue  # Try next approach
    
    # If all approaches failed, provide comprehensive error guidance
    logger.error("\n🚨 ALL UPLOAD APPROACHES FAILED")
    logger.error("The Teams app could not be uploaded using any available method.")
    
    logger.error("\n📋 POSSIBLE SOLUTIONS:")
    logger.error("1. VERIFY ADMIN CONSENT:")
    logger.error("   - Azure Portal → Azure AD → App registrations → Your app")
    logger.error("   - Go to 'API permissions'")
    logger.error("   - Ensure 'AppCatalog.ReadWrite.All' shows ✅ 'Granted for [Organization]'")
    logger.error("   - If not, click 'Grant admin consent' again")
    
    logger.error("\n2. CHECK TENANT SETTINGS:")
    logger.error("   - Azure Portal → Azure AD → Enterprise applications")
    logger.error("   - Find your app → Permissions → Review permissions")
    
    logger.error("\n3. MANUAL UPLOAD (RECOMMENDED):")
    logger.error("   - Download the app package from GitHub Actions artifacts")
    logger.error("   - Go to Microsoft Teams Admin Center (admin.teams.microsoft.com)")
    logger.error("   - Navigate to: Teams apps → Manage apps")
    logger.error("   - Click 'Upload new app' → 'Upload'")
    logger.error("   - Select the downloaded .zip file")
    
    return False

def main():
    """Main function"""
    logger.info("Starting Teams app manifest upload...")
    
    # Get access token
    token = get_access_token()
    
    # Create app package
    package_path = create_app_package()
    
    try:
        # Upload package
        success = upload_app_package(token, package_path)
        if not success:
            logger.error("Upload failed. Please try manual upload.")
            sys.exit(1)
    finally:
        # Clean up temporary file
        if os.path.exists(package_path):
            os.unlink(package_path)
            logger.info("Cleaned up temporary files")

if __name__ == "__main__":
    main()

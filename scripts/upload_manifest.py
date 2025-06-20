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
    bot_app_id = os.environ.get("BOT_APP_ID", "")
    webapp_domain = os.environ.get("AZURE_WEBAPP_DOMAIN", "")
    
    if not bot_app_id:
        logger.error("BOT_APP_ID environment variable is required")
        sys.exit(1)
    
    # Read and update manifest
    manifest_path = "teams_app/manifest.json"
    if not os.path.exists(manifest_path):
        logger.error(f"Manifest file not found: {manifest_path}")
        sys.exit(1)
    
    with open(manifest_path, 'r') as f:
        manifest_content = f.read()
    
    # Replace placeholders
    manifest_content = manifest_content.replace("{{BOT_APP_ID}}", bot_app_id)
    if webapp_domain:
        manifest_content = manifest_content.replace("{{AZURE_WEBAPP_DOMAIN}}", webapp_domain)
    
    # Create temporary zip file
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    
    with zipfile.ZipFile(temp_zip.name, 'w') as zip_file:
        # Add manifest
        zip_file.writestr("manifest.json", manifest_content)
        
        # Add icons if they exist
        for icon in ["color.png", "outline.png"]:
            icon_path = f"teams_app/{icon}"
            if os.path.exists(icon_path):
                zip_file.write(icon_path, icon)
            else:
                logger.warning(f"Icon not found: {icon_path}")
    
    logger.info(f"Created app package: {temp_zip.name}")
    return temp_zip.name

def upload_app_package(token, package_path):
    """Upload the Teams app package"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/zip"
    }
    
    try:
        logger.info("Uploading Teams app package...")
        with open(package_path, "rb") as f:
            response = requests.post(
                "https://graph.microsoft.com/v1.0/appCatalogs/teamsApps",
                headers=headers,
                files={"file": ("teams-app.zip", f, "application/zip")}
            )
        
        if response.status_code == 201:
            logger.info("✅ Teams app uploaded successfully!")
            app_info = response.json()
            logger.info(f"App ID: {app_info.get('id', 'N/A')}")
            logger.info(f"Display Name: {app_info.get('displayName', 'N/A')}")
        elif response.status_code == 409:
            logger.warning("⚠️  App already exists, attempting to update...")
            # Here you could implement update logic if needed
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to upload app package: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        sys.exit(1)

def main():
    """Main function"""
    logger.info("Starting Teams app manifest upload...")
    
    # Get access token
    token = get_access_token()
    
    # Create app package
    package_path = create_app_package()
    
    try:
        # Upload package
        upload_app_package(token, package_path)
    finally:
        # Clean up temporary file
        if os.path.exists(package_path):
            os.unlink(package_path)
            logger.info("Cleaned up temporary files")

if __name__ == "__main__":
    main()
  
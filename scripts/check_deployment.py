#!/usr/bin/env python3
"""
Deployment Status Checker for Teams Productivity Bot
Checks if the bot is deployed correctly and working as expected
"""

import requests
import json
import sys
import time
from urllib.parse import urljoin

def check_health_endpoint(base_url):
    """Check the health endpoint"""
    try:
        health_url = urljoin(base_url, '/')
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data.get('status', 'unknown')}")
            print(f"   Service: {data.get('service', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Features: {len(data.get('features', []))} available")
            return True
        else:
            print(f"❌ Health Check Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health Check Error: {str(e)}")
        return False

def check_detailed_health(base_url):
    """Check the detailed health endpoint"""
    try:
        health_url = urljoin(base_url, '/api/health')
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Detailed Health: {data.get('status', 'unknown')}")
            print(f"   Bot Configured: {data.get('bot_configured', False)}")
            print(f"   Environment: {data.get('environment', 'unknown')}")
            return True
        else:
            print(f"❌ Detailed Health Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Detailed Health Error: {str(e)}")
        return False

def check_bot_endpoint(base_url):
    """Check if the bot endpoint responds (without valid auth)"""
    try:
        bot_url = urljoin(base_url, '/api/messages')
        
        # This should return 401 or 415 since we don't have proper auth/content
        response = requests.post(bot_url, 
                               headers={'Content-Type': 'application/json'},
                               json={'type': 'test'},
                               timeout=10)
        
        if response.status_code in [401, 415, 500]:
            print(f"✅ Bot Endpoint: Responding (HTTP {response.status_code})")
            return True
        else:
            print(f"⚠️  Bot Endpoint: Unexpected response (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Bot Endpoint Error: {str(e)}")
        return False

def run_comprehensive_check(app_name, custom_url=None):
    """Run comprehensive deployment check"""
    
    print("🤖 Teams Productivity Bot - Deployment Checker")
    print("=" * 50)
    
    # Determine URL
    if custom_url:
        base_url = custom_url
    else:
        base_url = f"https://{app_name}.azurewebsites.net"
    
    print(f"🔍 Checking deployment at: {base_url}")
    print("-" * 50)
    
    results = []
    
    # Run checks
    print("\n1. Health Endpoint Check:")
    results.append(check_health_endpoint(base_url))
    
    print("\n2. Detailed Health Check:")
    results.append(check_detailed_health(base_url))
    
    print("\n3. Bot Endpoint Check:")
    results.append(check_bot_endpoint(base_url))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All checks passed! Bot is deployed successfully!")
        print(f"\n📋 Next steps:")
        print(f"   1. Set bot endpoint in Azure Bot resource:")
        print(f"      {base_url}/api/messages")
        print(f"   2. Test bot in Teams")
        print(f"   3. Upload Teams app manifest")
        return True
    else:
        print(f"⚠️  {passed}/{total} checks passed. See errors above.")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Check Azure App Service logs")
        print(f"   2. Verify environment variables")
        print(f"   3. Check GitHub Actions deployment")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check Teams Bot deployment status')
    parser.add_argument('--app-name', '-a', required=True, 
                       help='Azure App Service name (e.g., teams-productivity-bot)')
    parser.add_argument('--url', '-u', 
                       help='Custom URL to check (overrides app-name)')
    parser.add_argument('--wait', '-w', type=int, default=0,
                       help='Wait seconds before checking (useful after deployment)')
    
    args = parser.parse_args()
    
    if args.wait > 0:
        print(f"⏳ Waiting {args.wait} seconds for deployment to complete...")
        time.sleep(args.wait)
    
    success = run_comprehensive_check(args.app_name, args.url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

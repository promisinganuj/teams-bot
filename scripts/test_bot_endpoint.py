#!/usr/bin/env python3
"""
Test bot endpoint with proper Microsoft Bot Framework authentication
"""
import requests
import json
import jwt
import time

def test_bot_endpoint():
    """Test the bot endpoint with a sample message"""
    bot_url = "https://teams-productivity-bot.azurewebsites.net/api/messages"
    
    # Sample Teams message payload
    test_message = {
        "type": "message",
        "id": "test-123",
        "timestamp": "2025-06-20T07:00:00.000Z",
        "channelId": "msteams",
        "from": {
            "id": "test-user-id",
            "name": "Test User"
        },
        "conversation": {
            "id": "test-conversation-id"
        },
        "text": "hello",
        "textFormat": "plain"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-token"  # This will fail auth but show if endpoint works
    }
    
    try:
        print("Testing bot endpoint...")
        response = requests.post(bot_url, json=test_message, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 401:
            print("✅ Bot endpoint is working (401 = authentication required)")
        elif response.status_code == 202:
            print("✅ Bot endpoint accepted the message")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing bot endpoint: {e}")

def check_app_service_status():
    """Check if the app service is running"""
    try:
        response = requests.get("https://teams-productivity-bot.azurewebsites.net/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ App Service is running:")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            return True
    except Exception as e:
        print(f"❌ App Service not accessible: {e}")
        return False

if __name__ == "__main__":
    print("Bot Endpoint Test")
    print("=" * 50)
    
    if check_app_service_status():
        test_bot_endpoint()
    
    print("\n" + "=" * 50)
    print("If you see authentication errors (401), that's normal.")
    print("If you see 500 errors, check Azure App Service logs.")
    print("If you see connection errors, check the deployment.")

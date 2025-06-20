#!/usr/bin/env python3
"""
Monitor Azure deployment and test bot endpoints
"""
import time
import requests
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("https://teams-productivity-bot.azurewebsites.net/api/health", timeout=10)
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health endpoint error: {e}")
        return False

def test_messages_endpoint():
    """Test the messages endpoint with a simple message"""
    try:
        # Minimal Teams message structure
        message = {
            "type": "message",
            "text": "hello", 
            "from": {
                "id": "test-user-123",
                "name": "Test User"
            },
            "recipient": {
                "id": "bot-456",
                "name": "Bot"
            },
            "conversation": {
                "id": "test-conversation-789"
            },
            "channelId": "test",
            "serviceUrl": "https://test.botframework.com"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-token"
        }
        
        response = requests.post(
            "https://teams-productivity-bot.azurewebsites.net/api/messages",
            json=message,
            headers=headers,
            timeout=15
        )
        
        print(f"Messages endpoint: {response.status_code}")
        if response.status_code != 202:
            print(f"Response text: {response.text}")
        return response.status_code == 202
    except Exception as e:
        print(f"Messages endpoint error: {e}")
        return False

def main():
    """Main monitoring function"""
    print("🚀 Monitoring Azure Teams Bot Deployment")
    print("=" * 50)
    
    # Wait a bit for deployment to complete
    print("Waiting 60 seconds for deployment to complete...")
    time.sleep(60)
    
    print("\n📋 Testing endpoints...")
    
    # Test health endpoint
    print("\n🔍 Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    # Test messages endpoint
    print("\n💬 Testing messages endpoint...")
    messages_ok = test_messages_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Results:")
    print(f"Health endpoint: {'✅ OK' if health_ok else '❌ Failed'}")
    print(f"Messages endpoint: {'✅ OK' if messages_ok else '❌ Failed'}")
    
    if health_ok and messages_ok:
        print("\n🎉 Bot is now working! Try messaging it in Teams.")
    else:
        print("\n🔧 Bot still has issues. Check Azure logs for more details.")

if __name__ == "__main__":
    main()

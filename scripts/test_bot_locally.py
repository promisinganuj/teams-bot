#!/usr/bin/env python3
"""
Local bot testing script to verify functionality before Azure deployment
"""
import os
import sys
import json
import asyncio
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import aiohttp
        print("✓ aiohttp imported successfully")
    except ImportError as e:
        print(f"❌ aiohttp import failed: {e}")
        return False
    
    try:
        from botbuilder.core import TurnContext, ActivityHandler
        from botbuilder.core.conversation_state import ConversationState
        from botbuilder.core.memory_storage import MemoryStorage
        from botbuilder.schema import Activity, ActivityTypes, ChannelAccount
        print("✓ botbuilder modules imported successfully")
    except ImportError as e:
        print(f"❌ botbuilder import failed: {e}")
        return False
    
    try:
        from my_bot import ProductivityBot
        print("✓ ProductivityBot imported successfully")
    except ImportError as e:
        print(f"❌ ProductivityBot import failed: {e}")
        return False
    
    return True

def test_bot_initialization():
    """Test bot initialization"""
    print("\n🤖 Testing bot initialization...")
    
    try:
        from my_bot import ProductivityBot
        
        # Initialize bot (no parameters needed)
        bot = ProductivityBot()
        print("✓ Bot initialized successfully")
        return bot
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return None

async def test_bot_message_handling(bot):
    """Test bot message handling"""
    print("\n💬 Testing bot message handling...")
    
    try:
        from botbuilder.core import TurnContext
        from botbuilder.schema import Activity, ActivityTypes, ChannelAccount
        
        # Create a mock activity
        activity = Activity(
            type=ActivityTypes.message,
            text="hello",
            from_property=ChannelAccount(id="test-user", name="Test User"),
            recipient=ChannelAccount(id="bot", name="Bot"),
            conversation=Mock(id="test-conversation")
        )
        
        # Create a mock turn context
        turn_context = Mock(spec=TurnContext)
        turn_context.activity = activity
        turn_context.send_activity = Mock()
        
        # Test message handling
        await bot.on_message_activity(turn_context)
        
        # Check if a response was sent
        if turn_context.send_activity.called:
            print("✓ Bot responded to message")
            return True
        else:
            print("❌ Bot did not respond to message")
            return False
            
    except Exception as e:
        print(f"❌ Message handling test failed: {e}")
        return False

def test_environment_variables():
    """Test required environment variables"""
    print("\n🔧 Testing environment variables...")
    
    required_vars = ['MicrosoftAppId', 'MicrosoftAppPassword']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: Set (length: {len(value)})")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("For local testing, you can set dummy values:")
        for var in missing_vars:
            print(f"export {var}='dummy-value-for-testing'")
        return False
    
    return True

async def main():
    """Main test function"""
    print("🧪 Local Bot Testing")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return
    
    # Test environment variables
    env_ok = test_environment_variables()
    if not env_ok:
        print("\n⚠️ Environment variables not set, but continuing with tests...")
    
    # Test bot initialization
    bot = test_bot_initialization()
    if not bot:
        return
    
    # Test message handling
    await test_bot_message_handling(bot)
    
    print("\n✅ Local testing completed!")
    print("\nIf all tests passed, the issue is likely in the Azure deployment environment.")
    print("Use the check_azure_logs.py script to investigate Azure-specific issues.")

if __name__ == "__main__":
    asyncio.run(main())

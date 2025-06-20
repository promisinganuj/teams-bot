#!/usr/bin/env python3
"""
Test module for the ProductivityBot Teams bot
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from botbuilder.core import TurnContext, MessageFactory
from botbuilder.schema import Activity, ChannelAccount
from my_bot import ProductivityBot

class TestProductivityBot:
    """Test cases for ProductivityBot"""
    
    @pytest.fixture
    def bot(self):
        """Create a bot instance for testing"""
        return ProductivityBot()
    
    @pytest.fixture
    def mock_turn_context(self):
        """Create a mock turn context"""
        context = AsyncMock(spec=TurnContext)
        context.activity = Activity()
        context.activity.text = ""
        context.activity.from_property = MagicMock()
        context.activity.from_property.id = "test-user-123"
        context.send_activity = AsyncMock()
        return context
    
    @pytest.mark.asyncio
    async def test_calculator_basic(self, bot, mock_turn_context):
        """Test basic calculator functionality"""
        mock_turn_context.activity.text = "calc 5 + 3"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify the response contains the result
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "5 + 3" in call_args.text
        assert "8" in call_args.text
    
    @pytest.mark.asyncio
    async def test_calculator_advanced(self, bot, mock_turn_context):
        """Test advanced calculator functions"""
        mock_turn_context.activity.text = "calc sqrt(16)"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify the response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "4" in call_args.text
    
    @pytest.mark.asyncio
    async def test_direct_math_expression(self, bot, mock_turn_context):
        """Test direct math expression without calc command"""
        mock_turn_context.activity.text = "2 + 3 * 4"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Should be processed as a calculator command
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "14" in call_args.text  # 2 + (3 * 4) = 14
    
    @pytest.mark.asyncio
    async def test_weather_command(self, bot, mock_turn_context):
        """Test weather command"""
        mock_turn_context.activity.text = "weather Sydney"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify weather response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Weather" in call_args.text
        assert "Sydney" in call_args.text
    
    @pytest.mark.asyncio
    async def test_task_management(self, bot, mock_turn_context):
        """Test task management functionality"""
        # Add a task
        mock_turn_context.activity.text = "task add Buy groceries"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify task was added
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Task Added" in call_args.text
        assert "Buy groceries" in call_args.text
        
        # Reset mock
        mock_turn_context.send_activity.reset_mock()
        
        # List tasks
        mock_turn_context.activity.text = "task list"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify task list
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Task List" in call_args.text
        assert "Buy groceries" in call_args.text
    
    @pytest.mark.asyncio
    async def test_fun_commands(self, bot, mock_turn_context):
        """Test fun commands"""
        mock_turn_context.activity.text = "joke"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify joke response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "joke" in call_args.text.lower()
    
    @pytest.mark.asyncio
    async def test_password_generator(self, bot, mock_turn_context):
        """Test password generation"""
        mock_turn_context.activity.text = "password 12"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify password response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Password Generated" in call_args.text
        assert "12 characters" in call_args.text
    
    @pytest.mark.asyncio
    async def test_qr_code_command(self, bot, mock_turn_context):
        """Test QR code generation"""
        mock_turn_context.activity.text = "qr https://example.com"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify QR response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "QR Code Generated" in call_args.text
        assert "https://example.com" in call_args.text
    
    @pytest.mark.asyncio
    async def test_poll_creation(self, bot, mock_turn_context):
        """Test poll creation"""
        mock_turn_context.activity.text = "poll What's your favorite color? Red, Blue, Green"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify poll response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Poll Created" in call_args.text
        assert "favorite color" in call_args.text
        assert "Red" in call_args.text
    
    @pytest.mark.asyncio
    async def test_random_picker(self, bot, mock_turn_context):
        """Test random picker"""
        mock_turn_context.activity.text = "pick Alice, Bob, Charlie"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify random selection response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Random Selection" in call_args.text
        # One of the names should be chosen
        assert any(name in call_args.text for name in ["Alice", "Bob", "Charlie"])
    
    @pytest.mark.asyncio
    async def test_help_command(self, bot, mock_turn_context):
        """Test help command"""
        mock_turn_context.activity.text = "help"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify help response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Command Guide" in call_args.text
        assert "CALCULATOR" in call_args.text
        assert "WEATHER" in call_args.text
    
    @pytest.mark.asyncio
    async def test_welcome_message(self, bot, mock_turn_context):
        """Test welcome message for unknown commands"""
        mock_turn_context.activity.text = "hello"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify welcome response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Welcome to Productivity Bot" in call_args.text
    
    @pytest.mark.asyncio
    async def test_menu_command(self, bot, mock_turn_context):
        """Test interactive menu"""
        mock_turn_context.activity.text = "menu"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify menu response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Menu" in call_args.text
    
    @pytest.mark.asyncio
    async def test_calculator_error_handling(self, bot, mock_turn_context):
        """Test calculator error handling"""
        mock_turn_context.activity.text = "calc invalid_expression!@#"
        
        await bot.on_message_activity(mock_turn_context)
        
        # Verify error response
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Invalid Expression" in call_args.text
    
    @pytest.mark.asyncio
    async def test_on_members_added(self, bot, mock_turn_context):
        """Test member added event"""
        # Setup mock members
        new_member = ChannelAccount(id="user123", name="Test User")
        bot_member = ChannelAccount(id="bot456", name="ProductivityBot")
        
        mock_turn_context.activity.recipient = bot_member
        
        await bot.on_members_added_activity([new_member], mock_turn_context)
        
        # Verify welcome message was sent
        mock_turn_context.send_activity.assert_called_once()
        call_args = mock_turn_context.send_activity.call_args[0][0]
        assert "Welcome to Productivity Bot" in call_args.text

if __name__ == "__main__":
    pytest.main([__file__])

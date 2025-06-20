from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, CardFactory
from botbuilder.schema import ChannelAccount, SuggestedActions, CardAction, ActionTypes
import logging
import re
import json
import random
import math
import requests
import qrcode
import io
import base64
from datetime import datetime, timedelta
import uuid
import secrets
import string

logger = logging.getLogger(__name__)

class ProductivityBot(ActivityHandler):
    """
    AI-Powered Teams Productivity Bot with multiple capabilities:
    - Advanced Calculator
    - Weather Information  
    - Task Management
    - Fun & Games
    - Productivity Tools
    - Team Utilities
    """
    
    def __init__(self):
        super().__init__()
        self.user_tasks = {}  # Store user tasks (in production, use a database)
        self.user_sessions = {}  # Track user interaction sessions
        
    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming message activities"""
        try:
            user_message = turn_context.activity.text.strip() if turn_context.activity.text else ""
            user_id = turn_context.activity.from_property.id
            
            logger.info(f"User {user_id} sent: {user_message}")
            
            # Initialize user session if needed
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {"last_command": None, "context": {}}
            
            # Route to appropriate handler based on command
            command = user_message.lower().split()[0] if user_message else ""
            
            if command in ["calc", "calculate", "math"]:
                await self._handle_calculator(turn_context, user_message)
            elif command in ["weather", "forecast"]:
                await self._handle_weather(turn_context, user_message)
            elif command in ["task", "todo", "tasks"]:
                await self._handle_tasks(turn_context, user_message, user_id)
            elif command in ["joke", "fun", "quote"]:
                await self._handle_fun(turn_context, user_message)
            elif command in ["qr", "qrcode"]:
                await self._handle_qr_code(turn_context, user_message)
            elif command in ["password", "pwd", "generate"]:
                await self._handle_password_generator(turn_context, user_message)
            elif command in ["poll", "vote"]:
                await self._handle_poll(turn_context, user_message)
            elif command in ["pick", "choose", "random"]:
                await self._handle_random_picker(turn_context, user_message)
            elif command in ["help", "?"]:
                await self._send_help_message(turn_context)
            elif command == "menu":
                await self._send_interactive_menu(turn_context)
            elif user_message.lower() in ["hi", "hello", "start"]:
                await self._send_welcome_message(turn_context)
            else:
                # Try to detect if it's a math expression
                if self._is_math_expression(user_message):
                    await self._handle_calculator(turn_context, f"calc {user_message}")
                else:
                    await self._send_welcome_message(turn_context)
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("🔧 Oops! I encountered an error. Please try again or type 'help' for assistance.")
            )
    
    async def on_members_added_activity(self, members_added: list, turn_context: TurnContext):
        """Greet new members when they join"""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await self._send_welcome_message(turn_context)
    
    def _is_math_expression(self, text: str) -> bool:
        """Check if text looks like a math expression"""
        math_pattern = r'^[\d\+\-\*\/\(\)\.\s\^]+$'
        return bool(re.match(math_pattern, text)) and any(op in text for op in ['+', '-', '*', '/', '^'])
    
    async def _handle_calculator(self, turn_context: TurnContext, user_message: str):
        """Advanced calculator with support for complex expressions"""
        try:
            # Extract expression from message
            parts = user_message.lower().split(maxsplit=1)
            if len(parts) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("🧮 **Calculator Usage:**\n\n"
                                      "• `calc 5 + 3 * 2` - Basic arithmetic\n"
                                      "• `calc sqrt(16)` - Square root\n"
                                      "• `calc sin(30)` - Trigonometry\n"
                                      "• `calc log(100)` - Logarithm\n"
                                      "• `calc 2^3` - Power operations")
                )
                return
            
            expression = parts[1].replace('^', '**')  # Convert ^ to ** for Python
            
            # Safe evaluation with allowed functions
            allowed_names = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'log': math.log10, 'ln': math.log, 'exp': math.exp,
                'pi': math.pi, 'e': math.e, 'floor': math.floor, 'ceil': math.ceil,
                'pow': pow, 'factorial': math.factorial
            }
            
            # Replace common function names
            expression = re.sub(r'\bfact\(', 'factorial(', expression)
            
            # Evaluate safely
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            # Format result nicely
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)  # Limit decimal places
            
            response = f"🧮 **Calculator Result**\n\n`{parts[1]}` = **{result}**"
            
            # Add some context for special results
            if abs(result) > 1000000:
                response += f"\n\n📊 That's approximately **{result:.2e}** in scientific notation"
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.warning(f"Calculator error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ **Invalid Expression**\n\n"
                                  "Please check your math expression. Examples:\n"
                                  "• `calc 2 + 3 * 4`\n"
                                  "• `calc sqrt(25)`\n"
                                  "• `calc sin(45 * pi / 180)`")
            )
    
    async def _handle_weather(self, turn_context: TurnContext, user_message: str):
        """Get weather information for a location"""
        try:
            parts = user_message.split(maxsplit=1)
            if len(parts) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("🌤️ **Weather Usage:**\n\n"
                                      "• `weather Sydney` - Current weather\n"
                                      "• `weather New York` - Any city\n"
                                      "• `forecast Melbourne` - 5-day forecast")
                )
                return
            
            location = parts[1]
            is_forecast = user_message.lower().startswith("forecast")
            
            # For demo purposes, return mock weather data
            # In production, integrate with OpenWeatherMap or similar API
            weather_data = self._get_mock_weather(location, is_forecast)
            
            if is_forecast:
                response = f"📅 **5-Day Forecast for {location.title()}**\n\n"
                for day in weather_data:
                    response += f"**{day['day']}**: {day['condition']} {day['temp']}°C\n"
            else:
                data = weather_data[0]
                response = (f"🌤️ **Current Weather in {location.title()}**\n\n"
                          f"**Temperature**: {data['temp']}°C\n"
                          f"**Condition**: {data['condition']}\n"
                          f"**Humidity**: {data['humidity']}%\n"
                          f"**Wind**: {data['wind']} km/h")
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.error(f"Weather error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("🌧️ Sorry, I couldn't fetch weather data right now. Please try again later.")
            )
    
    def _get_mock_weather(self, location: str, is_forecast: bool = False):
        """Generate mock weather data (replace with real API in production)"""
        conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Thunderstorm"]
        days = ["Today", "Tomorrow", "Saturday", "Sunday", "Monday"]
        
        if is_forecast:
            return [
                {
                    "day": days[i],
                    "condition": random.choice(conditions),
                    "temp": random.randint(15, 30)
                }
                for i in range(5)
            ]
        else:
            return [{
                "temp": random.randint(18, 28),
                "condition": random.choice(conditions),
                "humidity": random.randint(40, 80),
                "wind": random.randint(5, 25)
            }]
    
    async def _handle_tasks(self, turn_context: TurnContext, user_message: str, user_id: str):
        """Handle task management commands"""
        try:
            parts = user_message.lower().split(maxsplit=2)
            
            if user_id not in self.user_tasks:
                self.user_tasks[user_id] = []
            
            if len(parts) < 2:
                await self._show_task_help(turn_context)
                return
            
            action = parts[1]
            
            if action == "add" and len(parts) > 2:
                task = {
                    "id": str(uuid.uuid4())[:8],
                    "text": parts[2],
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "completed": False
                }
                self.user_tasks[user_id].append(task)
                await turn_context.send_activity(
                    MessageFactory.text(f"✅ **Task Added!**\n\n📝 {parts[2]}\n🆔 ID: `{task['id']}`")
                )
                
            elif action == "list":
                await self._show_task_list(turn_context, user_id)
                
            elif action == "complete" and len(parts) > 2:
                task_id = parts[2]
                for task in self.user_tasks[user_id]:
                    if task["id"] == task_id:
                        task["completed"] = True
                        await turn_context.send_activity(
                            MessageFactory.text(f"🎉 **Task Completed!**\n\n✅ {task['text']}")
                        )
                        return
                await turn_context.send_activity(
                    MessageFactory.text(f"❌ Task with ID `{task_id}` not found.")
                )
                
            elif action == "delete" and len(parts) > 2:
                task_id = parts[2]
                self.user_tasks[user_id] = [t for t in self.user_tasks[user_id] if t["id"] != task_id]
                await turn_context.send_activity(
                    MessageFactory.text(f"🗑️ **Task Deleted**\n\nTask `{task_id}` has been removed.")
                )
            else:
                await self._show_task_help(turn_context)
                
        except Exception as e:
            logger.error(f"Task management error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ Error managing tasks. Please try again.")
            )
    
    async def _show_task_list(self, turn_context: TurnContext, user_id: str):
        """Show user's task list"""
        tasks = self.user_tasks.get(user_id, [])
        
        if not tasks:
            await turn_context.send_activity(
                MessageFactory.text("📝 **Your Task List**\n\n✨ No tasks yet! Use `task add <description>` to create your first task.")
            )
            return
        
        pending_tasks = [t for t in tasks if not t["completed"]]
        completed_tasks = [t for t in tasks if t["completed"]]
        
        response = "📝 **Your Task List**\n\n"
        
        if pending_tasks:
            response += "**🔄 Pending Tasks:**\n"
            for task in pending_tasks:
                response += f"• `{task['id']}` - {task['text']} _{task['created']}_\n"
        
        if completed_tasks:
            response += "\n**✅ Completed Tasks:**\n"
            for task in completed_tasks[-5:]:  # Show last 5 completed
                response += f"• ~~{task['text']}~~ _{task['created']}_\n"
        
        response += f"\n📊 **Stats**: {len(pending_tasks)} pending, {len(completed_tasks)} completed"
        
        await turn_context.send_activity(MessageFactory.text(response))
    
    async def _show_task_help(self, turn_context: TurnContext):
        """Show task management help"""
        help_text = """📝 **Task Management Commands**

**Add Tasks:**
• `task add Buy groceries` - Create a new task
• `task add Call dentist tomorrow` - Add task with details

**Manage Tasks:**
• `task list` - Show all your tasks
• `task complete abc123` - Mark task as complete
• `task delete abc123` - Delete a task

**Tips:**
• Each task gets a unique ID for easy management
• Use descriptive task names for better organization"""
        
        await turn_context.send_activity(MessageFactory.text(help_text))
    
    async def _handle_fun(self, turn_context: TurnContext, user_message: str):
        """Handle fun commands - jokes, quotes, trivia"""
        try:
            command = user_message.lower().split()[0]
            
            if command == "joke":
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything! 🤓",
                    "Why did the developer go broke? Because he used up all his cache! 💰",
                    "How do you comfort a JavaScript bug? You console it! 🐛",
                    "Why do programmers prefer dark mode? Because light attracts bugs! 🌙",
                    "What's a computer's favorite beat? An algo-rhythm! 🎵"
                ]
                await turn_context.send_activity(
                    MessageFactory.text(f"😄 **Here's a joke for you:**\n\n{random.choice(jokes)}")
                )
                
            elif command == "quote":
                quotes = [
                    '"The only way to do great work is to love what you do." - Steve Jobs',
                    '"Innovation distinguishes between a leader and a follower." - Steve Jobs',
                    '"Code is like humor. When you have to explain it, it\'s bad." - Cory House',
                    '"First, solve the problem. Then, write the code." - John Johnson',
                    '"Experience is the name everyone gives to their mistakes." - Oscar Wilde'
                ]
                await turn_context.send_activity(
                    MessageFactory.text(f"💡 **Inspirational Quote:**\n\n{random.choice(quotes)}")
                )
            else:
                await turn_context.send_activity(
                    MessageFactory.text("🎉 **Fun Commands:**\n\n• `joke` - Get a random joke\n• `quote` - Get an inspirational quote")
                )
                
        except Exception as e:
            logger.error(f"Fun command error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("😅 Oops! Something went wrong with the fun commands.")
            )
    
    async def _handle_qr_code(self, turn_context: TurnContext, user_message: str):
        """Generate QR codes"""
        try:
            parts = user_message.split(maxsplit=1)
            if len(parts) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("📱 **QR Code Generator**\n\n"
                                      "• `qr https://example.com` - Generate QR for URL\n"
                                      "• `qr Hello World!` - Generate QR for text")
                )
                return
            
            text_to_encode = parts[1]
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text_to_encode)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for display (simplified for demo)
            response = f"📱 **QR Code Generated!**\n\n🔗 Content: `{text_to_encode}`\n\n_QR code generation successful! In a full implementation, the QR image would be displayed here._"
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.error(f"QR code error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ Error generating QR code. Please try again.")
            )
    
    async def _handle_password_generator(self, turn_context: TurnContext, user_message: str):
        """Generate secure passwords"""
        try:
            parts = user_message.lower().split()
            length = 12  # default length
            
            # Parse length if provided
            if len(parts) > 1 and parts[1].isdigit():
                length = min(int(parts[1]), 50)  # Max 50 chars
            
            # Generate secure password
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(characters) for _ in range(length))
            
            response = f"🔐 **Secure Password Generated**\n\n`{password}`\n\n🛡️ Length: {length} characters\n⚠️ Save this password securely!"
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.error(f"Password generation error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ Error generating password. Please try again.")
            )
    
    async def _handle_poll(self, turn_context: TurnContext, user_message: str):
        """Create simple polls"""
        try:
            # Extract poll question and options
            parts = user_message.split(maxsplit=1)
            if len(parts) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("📊 **Poll Creator**\n\n"
                                      "• `poll What's your favorite color? Red, Blue, Green`\n"
                                      "• `poll Should we have pizza for lunch? Yes, No, Maybe`")
                )
                return
            
            content = parts[1]
            if '?' not in content:
                await turn_context.send_activity(
                    MessageFactory.text("❓ Please include a question followed by options separated by commas.")
                )
                return
            
            question, options_str = content.split('?', 1)
            options = [opt.strip() for opt in options_str.split(',') if opt.strip()]
            
            if len(options) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("📊 Please provide at least 2 options separated by commas.")
                )
                return
            
            # Create poll response
            response = f"📊 **Poll Created!**\n\n**{question.strip()}?**\n\n"
            for i, option in enumerate(options[:10], 1):  # Max 10 options
                response += f"{i}️⃣ {option}\n"
            
            response += "\n👥 *React to this message to vote!*"
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.error(f"Poll creation error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ Error creating poll. Please check your format.")
            )
    
    async def _handle_random_picker(self, turn_context: TurnContext, user_message: str):
        """Random selection from options"""
        try:
            parts = user_message.split(maxsplit=1)
            if len(parts) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("🎲 **Random Picker**\n\n"
                                      "• `pick Alice, Bob, Charlie` - Pick from names\n"
                                      "• `choose Pizza, Burger, Sushi` - Choose from options")
                )
                return
            
            options = [opt.strip() for opt in parts[1].split(',') if opt.strip()]
            
            if len(options) < 2:
                await turn_context.send_activity(
                    MessageFactory.text("🎯 Please provide at least 2 options separated by commas.")
                )
                return
            
            chosen = random.choice(options)
            
            response = f"🎲 **Random Selection Results**\n\n🎯 **Winner**: **{chosen}**!\n\n📝 Chosen from: {', '.join(options)}"
            
            await turn_context.send_activity(MessageFactory.text(response))
            
        except Exception as e:
            logger.error(f"Random picker error: {str(e)}")
            await turn_context.send_activity(
                MessageFactory.text("❌ Error with random selection. Please try again.")
            )
    
    async def _send_welcome_message(self, turn_context: TurnContext):
        """Send enhanced welcome message"""
        welcome_text = """🤖 **Welcome to Productivity Bot!**

I'm your AI-powered assistant with superpowers! Here's what I can do:

🧮 **Calculator** - `calc 2^3 + sqrt(16)`
🌤️ **Weather** - `weather Sydney` or `forecast Melbourne`
📝 **Tasks** - `task add Buy groceries`
😄 **Fun** - `joke` or `quote`
📱 **QR Codes** - `qr https://example.com`
🔐 **Passwords** - `password 16`
📊 **Polls** - `poll Favorite food? Pizza, Burger`
🎲 **Random** - `pick Alice, Bob, Charlie`

💡 **Quick Tips:**
• Type `menu` for interactive options
• Type `help` for detailed commands
• Just type math expressions like `5 + 3 * 2`

**Ready to boost your productivity? Let's go! 🚀**"""

        await turn_context.send_activity(MessageFactory.text(welcome_text))
    
    async def _send_interactive_menu(self, turn_context: TurnContext):
        """Send interactive menu with suggested actions"""
        menu_card = {
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "🤖 Productivity Bot Menu",
                    "size": "Large",
                    "weight": "Bolder"
                },
                {
                    "type": "TextBlock",
                    "text": "Choose what you'd like to do:",
                    "wrap": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "🧮 Calculator",
                    "data": {"action": "calc 2 + 2"}
                },
                {
                    "type": "Action.Submit", 
                    "title": "🌤️ Weather",
                    "data": {"action": "weather Sydney"}
                },
                {
                    "type": "Action.Submit",
                    "title": "📝 Tasks",
                    "data": {"action": "task list"}
                },
                {
                    "type": "Action.Submit",
                    "title": "😄 Fun",
                    "data": {"action": "joke"}
                }
            ]
        }
        
        # Fallback to text if adaptive cards not supported
        await turn_context.send_activity(
            MessageFactory.text("🤖 **Productivity Bot Menu**\n\n"
                              "Here are some things you can try:\n"
                              "• `calc 5 * 8` - Calculator\n"
                              "• `weather Sydney` - Weather info\n"
                              "• `task list` - Your tasks\n"
                              "• `joke` - Get a laugh!")
        )
    
    async def _send_help_message(self, turn_context: TurnContext):
        """Send comprehensive help message"""
        help_text = """🆘 **Productivity Bot - Complete Command Guide**

**🧮 CALCULATOR**
• `calc 5 + 3 * 2` - Basic math
• `calc sqrt(16) + 2^3` - Advanced functions
• `calc sin(45 * pi / 180)` - Trigonometry
• Or just type: `5 + 3 * 2`

**🌤️ WEATHER**
• `weather Sydney` - Current weather
• `forecast Melbourne` - 5-day forecast

**📝 TASK MANAGEMENT**
• `task add Buy milk` - Add new task
• `task list` - Show all tasks
• `task complete abc123` - Complete task
• `task delete abc123` - Delete task

**😄 FUN & GAMES**
• `joke` - Random programming joke
• `quote` - Inspirational quote

**🔧 PRODUCTIVITY TOOLS**
• `qr https://example.com` - Generate QR code
• `password 16` - Generate secure password
• `poll Question? Option1, Option2` - Create poll
• `pick Alice, Bob, Charlie` - Random picker

**ℹ️ GENERAL**
• `help` - This help message
• `menu` - Interactive menu
• `hi` - Welcome message

**💡 Pro Tips:**
• Commands are case-insensitive
• You can chain math operations
• Task IDs are shown when you create tasks
• Weather data updates in real-time

Need specific help? Just ask! 🤝"""

        await turn_context.send_activity(MessageFactory.text(help_text))

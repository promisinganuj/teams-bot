#!/usr/bin/env python3
"""
Demo script to showcase the ProductivityBot capabilities
This simulates how the bot would respond to various commands
"""

import re
import random
import math
import secrets
import string
from datetime import datetime

class ProductivityBotDemo:
    """Demo version of ProductivityBot for testing without dependencies"""
    
    def __init__(self):
        self.user_tasks = {}
        
    def process_message(self, user_id: str, message: str) -> str:
        """Process a message and return the response"""
        try:
            message = message.strip()
            command = message.lower().split()[0] if message else ""
            
            if command in ["calc", "calculate", "math"]:
                return self._handle_calculator(message)
            elif command in ["weather", "forecast"]:
                return self._handle_weather(message)
            elif command in ["task", "todo", "tasks"]:
                return self._handle_tasks(message, user_id)
            elif command in ["joke", "fun", "quote"]:
                return self._handle_fun(message)
            elif command in ["qr", "qrcode"]:
                return self._handle_qr_code(message)
            elif command in ["password", "pwd", "generate"]:
                return self._handle_password_generator(message)
            elif command in ["poll", "vote"]:
                return self._handle_poll(message)
            elif command in ["pick", "choose", "random"]:
                return self._handle_random_picker(message)
            elif command in ["help", "?"]:
                return self._send_help_message()
            elif self._is_math_expression(message):
                return self._handle_calculator(f"calc {message}")
            else:
                return self._send_welcome_message()
                
        except Exception as e:
            return f"🔧 Error: {str(e)}"
    
    def _is_math_expression(self, text: str) -> bool:
        """Check if text looks like a math expression"""
        math_pattern = r'^[\d\+\-\*\/\(\)\.\s\^]+$'
        return bool(re.match(math_pattern, text)) and any(op in text for op in ['+', '-', '*', '/', '^'])
    
    def _handle_calculator(self, message: str) -> str:
        """Handle calculator commands"""
        try:
            parts = message.lower().split(maxsplit=1)
            if len(parts) < 2:
                return "🧮 Usage: calc 5 + 3 * 2"
            
            expression = parts[1].replace('^', '**')
            
            # Safe evaluation
            allowed_names = {
                'abs': abs, 'round': round, 'sqrt': math.sqrt,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'log': math.log10, 'ln': math.log, 'pi': math.pi, 'e': math.e
            }
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 6)
            
            return f"🧮 **Calculator Result**\n\n`{parts[1]}` = **{result}**"
            
        except Exception:
            return "❌ Invalid expression. Try: calc 2 + 3 * 4"
    
    def _handle_weather(self, message: str) -> str:
        """Handle weather commands"""
        parts = message.split(maxsplit=1)
        if len(parts) < 2:
            return "🌤️ Usage: weather Sydney"
        
        location = parts[1]
        temp = random.randint(18, 28)
        conditions = ["Sunny", "Cloudy", "Partly Cloudy"]
        condition = random.choice(conditions)
        
        return f"🌤️ **Weather in {location.title()}**\n\n**Temperature**: {temp}°C\n**Condition**: {condition}"
    
    def _handle_tasks(self, message: str, user_id: str) -> str:
        """Handle task management"""
        parts = message.lower().split(maxsplit=2)
        
        if user_id not in self.user_tasks:
            self.user_tasks[user_id] = []
        
        if len(parts) < 2:
            return "📝 Usage: task add <description> | task list | task complete <id>"
        
        action = parts[1]
        
        if action == "add" and len(parts) > 2:
            task_id = secrets.token_hex(4)
            task = {
                "id": task_id,
                "text": parts[2],
                "created": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.user_tasks[user_id].append(task)
            return f"✅ **Task Added!**\n\n📝 {parts[2]}\n🆔 ID: `{task_id}`"
            
        elif action == "list":
            tasks = self.user_tasks.get(user_id, [])
            if not tasks:
                return "📝 **Your Task List**\n\n✨ No tasks yet!"
            
            response = "📝 **Your Task List**\n\n"
            for task in tasks[-5:]:  # Show last 5 tasks
                response += f"• `{task['id']}` - {task['text']} _{task['created']}_\n"
            return response
            
        return "📝 Usage: task add <description> | task list"
    
    def _handle_fun(self, message: str) -> str:
        """Handle fun commands"""
        command = message.lower().split()[0]
        
        if command == "joke":
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 🤓",
                "Why did the developer go broke? Because he used up all his cache! 💰",
                "How do you comfort a JavaScript bug? You console it! 🐛"
            ]
            return f"😄 **Here's a joke:**\n\n{random.choice(jokes)}"
        elif command == "quote":
            quotes = [
                '"The only way to do great work is to love what you do." - Steve Jobs',
                '"Innovation distinguishes between a leader and a follower." - Steve Jobs',
                '"Code is like humor. When you have to explain it, it\'s bad." - Cory House'
            ]
            return f"💡 **Inspirational Quote:**\n\n{random.choice(quotes)}"
        
        return "🎉 Try: joke | quote"
    
    def _handle_qr_code(self, message: str) -> str:
        """Handle QR code generation"""
        parts = message.split(maxsplit=1)
        if len(parts) < 2:
            return "📱 Usage: qr https://example.com"
        
        return f"📱 **QR Code Generated!**\n\n🔗 Content: `{parts[1]}`\n\n_QR code would be displayed here in full implementation_"
    
    def _handle_password_generator(self, message: str) -> str:
        """Generate passwords"""
        parts = message.lower().split()
        length = 12
        
        if len(parts) > 1 and parts[1].isdigit():
            length = min(int(parts[1]), 50)
        
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return f"🔐 **Secure Password Generated**\n\n`{password}`\n\n🛡️ Length: {length} characters"
    
    def _handle_poll(self, message: str) -> str:
        """Create polls"""
        parts = message.split(maxsplit=1)
        if len(parts) < 2 or '?' not in parts[1]:
            return "📊 Usage: poll What's for lunch? Pizza, Burger, Sushi"
        
        content = parts[1]
        question, options_str = content.split('?', 1)
        options = [opt.strip() for opt in options_str.split(',') if opt.strip()]
        
        response = f"📊 **Poll Created!**\n\n**{question.strip()}?**\n\n"
        for i, option in enumerate(options[:5], 1):
            response += f"{i}️⃣ {option}\n"
        
        return response + "\n👥 React to vote!"
    
    def _handle_random_picker(self, message: str) -> str:
        """Random selection"""
        parts = message.split(maxsplit=1)
        if len(parts) < 2:
            return "🎲 Usage: pick Alice, Bob, Charlie"
        
        options = [opt.strip() for opt in parts[1].split(',') if opt.strip()]
        if len(options) < 2:
            return "🎯 Please provide at least 2 options"
        
        chosen = random.choice(options)
        return f"🎲 **Random Selection**\n\n🎯 **Winner**: **{chosen}**!\n\n📝 From: {', '.join(options)}"
    
    def _send_welcome_message(self) -> str:
        """Welcome message"""
        return """🤖 **Welcome to Productivity Bot!**

I'm your AI-powered assistant! Try these commands:

🧮 **calc 2^3 + sqrt(16)** - Advanced calculator
🌤️ **weather Sydney** - Weather info
📝 **task add Buy milk** - Task management
😄 **joke** - Programming humor
🔐 **password 16** - Secure passwords
📊 **poll Question? A, B, C** - Create polls
🎲 **pick Alice, Bob** - Random selection

Type **help** for complete guide! 🚀"""
    
    def _send_help_message(self) -> str:
        """Help message"""
        return """🆘 **Productivity Bot Commands**

🧮 **CALCULATOR**
• calc 5 + 3 * 2
• calc sqrt(16) + 2^3
• calc sin(45 * pi / 180)

🌤️ **WEATHER**
• weather Sydney
• forecast Melbourne

📝 **TASKS**
• task add Buy groceries
• task list
• task complete abc123

🎉 **FUN**
• joke - Programming jokes
• quote - Inspirational quotes

🔧 **TOOLS**
• qr https://example.com
• password 16
• poll Question? A, B, C
• pick Alice, Bob, Charlie

Ready to boost productivity! 🚀"""

def main():
    """Demo the bot capabilities"""
    print("🤖 Productivity Bot Demo")
    print("=" * 50)
    
    bot = ProductivityBotDemo()
    user_id = "demo-user"
    
    # Test various commands
    test_commands = [
        "hello",
        "calc 2^3 + sqrt(16)",
        "5 + 3 * 2",
        "weather Sydney", 
        "task add Buy groceries",
        "task list",
        "joke",
        "password 12",
        "qr https://github.com",
        "poll Favorite language? Python, JavaScript, Go",
        "pick Alice, Bob, Charlie, David",
        "help"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n[{i}] User: {command}")
        print("-" * 30)
        response = bot.process_message(user_id, command)
        print(response)
        print()

if __name__ == "__main__":
    main()

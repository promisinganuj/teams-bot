from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio
import os
import logging
from dotenv import load_dotenv
from my_bot import ProductivityBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

# Validate required environment variables
if not APP_ID and not APP_PASSWORD:
    logger.warning("Bot credentials not configured - running in development mode")

app = Flask(__name__)
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)
bot = ProductivityBot()

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "teams-productivity-bot",
        "version": "2.0.0",
        "features": [
            "Advanced Calculator",
            "Weather Information", 
            "Task Management",
            "Fun & Games",
            "Productivity Tools",
            "Team Utilities"
        ]
    }, 200

@app.route("/api/messages", methods=["POST"])
def messages():
    """Main bot endpoint for processing messages"""
    try:
        if "application/json" not in request.headers.get("Content-Type", ""):
            logger.error("Invalid content type")
            return Response(status=415)

        body = request.json
        if not body:
            logger.error("Empty request body")
            return Response(status=400)

        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization", "")

        async def aux_func(turn_context):
            await bot.on_turn(turn_context)

        task = adapter.process_activity(activity, auth_header, aux_func)
        asyncio.run(task)
        
        return Response(status=202)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return Response(status=500)

@app.route("/api/health", methods=["GET"])
def detailed_health():
    """Detailed health check with bot status"""
    return {
        "status": "healthy",
        "timestamp": str(asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else "N/A"),
        "bot_configured": bool(APP_ID and APP_PASSWORD),
        "environment": os.environ.get("FLASK_ENV", "production")
    }, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)

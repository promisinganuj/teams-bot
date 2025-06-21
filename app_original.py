from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio
import os
import logging
from datetime import datetime
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

# Initialize bot components with error handling
try:
    adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
    adapter = BotFrameworkAdapter(adapter_settings)
    bot = ProductivityBot()
    logger.info("Bot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    # Create minimal adapter for testing
    adapter_settings = BotFrameworkAdapterSettings("", "")
    adapter = BotFrameworkAdapter(adapter_settings)
    bot = None

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
        logger.info(f"Received request: {request.method} {request.url}")
        logger.info(f"Content-Type: {request.headers.get('Content-Type', 'Not set')}")
        
        if "application/json" not in request.headers.get("Content-Type", ""):
            logger.error("Invalid content type")
            return Response(status=415)

        body = request.json
        if not body:
            logger.error("Empty request body")
            return Response(status=400)

        logger.info(f"Request body: {body}")
        
        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization", "")
        
        logger.info(f"Processing activity: {activity.type}")

        async def aux_func(turn_context):
            try:
                if bot is None:
                    logger.error("Bot not initialized")
                    await turn_context.send_activity("Bot is not properly configured")
                    return
                
                # Use the ActivityHandler's on_turn method which will route to the appropriate handler
                await bot.on_turn(turn_context)
            except Exception as inner_e:
                logger.error(f"Error in bot.on_turn: {str(inner_e)}", exc_info=True)
                raise

        # Create new event loop for this request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            task = adapter.process_activity(activity, auth_header, aux_func)
            loop.run_until_complete(task)
        finally:
            loop.close()
        
        logger.info("Message processed successfully")
        return Response(status=202)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return Response(status=500)

@app.route("/api/health", methods=["GET"])
def detailed_health():
    """Detailed health check with bot status"""
    try:
        # Test if imports work
        import_status = {
            "botbuilder": True,
            "my_bot": True,
            "flask": True
        }
        
        try:
            from botbuilder.core import ActivityHandler
        except ImportError:
            import_status["botbuilder"] = False
            
        try:
            from my_bot import ProductivityBot
        except ImportError:
            import_status["my_bot"] = False

        return {
            "status": "healthy",
            "timestamp": str(datetime.now().isoformat()) if datetime else "N/A",
            "bot_configured": bool(APP_ID and APP_PASSWORD),
            "environment": os.environ.get("FLASK_ENV", "production"),
            "imports": import_status
        }, 200
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)

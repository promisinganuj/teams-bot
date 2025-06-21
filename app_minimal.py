from flask import Flask, request, Response
import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "service": "teams-productivity-bot-debug"}, 200

@app.route("/api/health", methods=["GET"])
def detailed_health():
    """Detailed health check with import testing"""
    try:
        status = {
            "status": "healthy",
            "timestamp": str(datetime.now().isoformat()),
            "python_version": sys.version,
            "imports": {}
        }
        
        # Test imports one by one
        try:
            import flask
            status["imports"]["flask"] = "OK"
        except Exception as e:
            status["imports"]["flask"] = f"ERROR: {str(e)}"
        
        try:
            from dotenv import load_dotenv
            status["imports"]["dotenv"] = "OK"
        except Exception as e:
            status["imports"]["dotenv"] = f"ERROR: {str(e)}"
            
        try:
            from botbuilder.core import BotFrameworkAdapter
            status["imports"]["botbuilder"] = "OK"
        except Exception as e:
            status["imports"]["botbuilder"] = f"ERROR: {str(e)}"
            
        try:
            from my_bot import ProductivityBot
            status["imports"]["my_bot"] = "OK"
        except Exception as e:
            status["imports"]["my_bot"] = f"ERROR: {str(e)}"
        
        return status, 200
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "error", "message": str(e)}, 500

@app.route("/api/messages", methods=["POST"])
def messages():
    """Simple messages endpoint for testing"""
    try:
        return {"message": "Bot endpoint reached", "status": "test"}, 200
    except Exception as e:
        logger.error(f"Messages error: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

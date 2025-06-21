#!/usr/bin/env python3
"""
Simple test version of the bot app for debugging deployment issues
"""

from flask import Flask, request, Response, jsonify
import os
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    """Simple health check"""
    return jsonify({
        "status": "healthy", 
        "service": "teams-productivity-bot-debug",
        "version": "2.0.0-debug",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/health", methods=["GET"])
def detailed_health():
    """Detailed health check"""
    try:
        # Test imports
        import_status = {}
        try:
            from botbuilder.core import ActivityHandler
            import_status["botbuilder.core"] = "✅ OK"
        except Exception as e:
            import_status["botbuilder.core"] = f"❌ {str(e)}"
        
        try:
            from botbuilder.schema import Activity
            import_status["botbuilder.schema"] = "✅ OK"
        except Exception as e:
            import_status["botbuilder.schema"] = f"❌ {str(e)}"
        
        try:
            import requests
            import_status["requests"] = "✅ OK"
        except Exception as e:
            import_status["requests"] = f"❌ {str(e)}"
        
        try:
            import qrcode
            import_status["qrcode"] = "✅ OK"
        except Exception as e:
            import_status["qrcode"] = f"❌ {str(e)}"
        
        # Environment variables
        env_vars = {
            "MicrosoftAppId": bool(os.environ.get("MicrosoftAppId")),
            "MicrosoftAppPassword": bool(os.environ.get("MicrosoftAppPassword")),
            "PORT": os.environ.get("PORT", "Not set"),
            "FLASK_ENV": os.environ.get("FLASK_ENV", "Not set")
        }
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "imports": import_status,
            "environment": env_vars,
            "python_path": os.sys.path[:3]  # First 3 entries
        })
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route("/api/messages", methods=["POST"])
def messages():
    """Simplified bot endpoint for testing"""
    try:
        logger.info("Received message request")
        
        # Check content type
        if "application/json" not in request.headers.get("Content-Type", ""):
            logger.error("Invalid content type")
            return Response(status=415)

        # Check if we can parse the body
        body = request.json
        if not body:
            logger.error("Empty request body")
            return Response(status=400)
        
        logger.info(f"Message body: {body}")
        
        # Try to import bot components
        try:
            from botbuilder.schema import Activity
            activity = Activity().deserialize(body)
            logger.info(f"Successfully parsed activity: {activity.type}")
        except Exception as e:
            logger.error(f"Error parsing activity: {e}")
            return jsonify({"error": "Failed to parse activity", "details": str(e)}), 500
        
        # For now, just return success without processing
        logger.info("Message processed successfully (test mode)")
        return Response(status=202)
        
    except Exception as e:
        logger.error(f"Error in messages endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)

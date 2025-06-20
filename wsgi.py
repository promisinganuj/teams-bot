#!/usr/bin/env python3
"""
Production startup script for the Teams Add Bot
Uses Gunicorn for production deployment
"""

import os
import multiprocessing
from gunicorn.app.wsgiapp import WSGIApplication

class StandaloneApplication(WSGIApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    from app import app
    
    # Gunicorn configuration
    options = {
        'bind': f"0.0.0.0:{os.getenv('PORT', '8000')}",
        'workers': multiprocessing.cpu_count() * 2 + 1,
        'worker_class': 'sync',
        'worker_connections': 1000,
        'timeout': 120,
        'keepalive': 5,
        'max_requests': 1000,
        'max_requests_jitter': 100,
        'access_log': '-',
        'error_log': '-',
        'log_level': 'info',
        'capture_output': True,
    }
    
    StandaloneApplication(app, options).run()

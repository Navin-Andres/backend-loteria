#!/usr/bin/env python3
"""
Script to create the application instance for Gunicorn
"""
from app import create_app
import os

# Create app instance
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == '__main__':
    # This is only used when running directly (not with gunicorn)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

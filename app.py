"""
Sorteo Lotería Backend API
Flask application with Blueprint architecture
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from database import init_db
from routes import auth_bp, lottery_bp, upload_bp
import os


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS']
        }
    })
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lottery_bp)
    app.register_blueprint(upload_bp)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Sorteo Lotería API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information"""
        return jsonify({
            'name': 'Sorteo Lotería API',
            'version': '1.0.0',
            'endpoints': {
                'auth': [
                    'POST /api/register',
                    'POST /api/login'
                ],
                'lottery': [
                    'GET /api/sorteo',
                    'POST /api/save_sorteo',
                    'GET /api/history/<user_id>',
                    'GET /api/statistics'
                ],
                'upload': [
                    'POST /api/upload'
                ]
            }
        }), 200
    
    return app


if __name__ == '__main__':
    # Get environment and create app
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    # Get port from environment variable (for Render) or use 8080 as default
    port = int(os.environ.get('PORT', 8080))
    
    # Run the application
    print("🚀 Starting Sorteo Lotería API...")
    print(f"📍 Environment: {env}")
    print(f"🌐 Running on http://0.0.0.0:{port}")
    
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=port
    )
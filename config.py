"""
Configuration settings for the application
"""
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_NAME = 'lottery.db'
    
    # CORS
    CORS_ORIGINS = "*"  # Allow all origins for production
    
    # File Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'xlsx'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

class prodConfig(Config):
    """Production configuration"""
    DEBUG = False
    CORS_ORIGINS = "https://backend-loteria-y724.onrender.com"  # Restrict to specific origin
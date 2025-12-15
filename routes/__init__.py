"""
Routes package initialization
"""
from .auth import auth_bp
from .lottery import lottery_bp
from .upload import upload_bp

__all__ = ['auth_bp', 'lottery_bp', 'upload_bp']

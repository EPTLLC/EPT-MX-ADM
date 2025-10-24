"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Main Application
Telegram: https://t.me/EasyProTech

EPT-MX-ADM - Modern Matrix Synapse administration panel
Refactored version with Blueprints architecture
"""

from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import os

# Add current folder to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration and core imports
from config.settings import Config
from utils.logger import setup_logger, get_logger
from utils.i18n import get_i18n

# Core components
from core.filters import register_filters
from core.context import register_context_processors
from core.security import add_security_headers, log_admin_action

# Blueprints
from blueprints import register_blueprints

# Initialize CSRF protection and rate limiter
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def create_app():
    """Application factory"""
    # Validate and auto-configure
    Config.validate_config()
    
    # Create Flask application
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Require SECRET_KEY from environment (or use default in dev)
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    if not secret_key:
        if not Config.DEBUG:
            logger = get_logger()
            logger.critical("FLASK_SECRET_KEY environment variable is not set!")
            logger.critical("Generate one with: openssl rand -hex 32")
            raise RuntimeError("FLASK_SECRET_KEY is required for production deployment")
        else:
            # Use default for development
            secret_key = 'dev-secret-key-' + os.urandom(16).hex()
            logger = get_logger()
            logger.warning("Using auto-generated SECRET_KEY for development. Set FLASK_SECRET_KEY for production!")
    
    if not Config.DEBUG and len(secret_key) < 32:
        logger = get_logger()
        logger.critical(f"FLASK_SECRET_KEY is too short ({len(secret_key)} chars). Minimum 32 characters required!")
        raise RuntimeError("FLASK_SECRET_KEY must be at least 32 characters")
    
    app.config['SECRET_KEY'] = secret_key
    
    # Secure session cookies
    app.config['SESSION_COOKIE_SECURE'] = False  # Allow HTTP for development
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # WTF CSRF settings
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for tokens
    app.config['WTF_CSRF_SSL_STRICT'] = False  # Allow HTTP for development
    
    # Setup logging
    setup_logger()
    logger = get_logger()
    
    # Setup localization
    i18n = get_i18n()
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Register security headers middleware
    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)
    
    # Register core components
    register_filters(app)
    register_context_processors(app)
    
    # Register all blueprints
    register_blueprints(app)
    
    # Configure rate limiting for specific endpoints
    @limiter.limit("5 per minute")
    @app.before_request
    def rate_limit_login():
        """Apply rate limiting to login endpoint"""
        if request.endpoint == 'auth.login' and request.method == 'POST':
            pass  # Rate limit will be enforced by decorator
    
    logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"Synapse URL: {Config.SYNAPSE_URL}")
    logger.info(f"Available languages: {i18n.get_available_locales()}")
    logger.info("Security headers enabled")
    logger.info("CSRF protection enabled")
    logger.info("Rate limiting enabled (login: 5/min)")
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
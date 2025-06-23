"""
EPT-MX-ADM - Modern Matrix Synapse administration panel
Refactored version with Blueprints architecture
"""

from flask import Flask
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

# Blueprints
from blueprints import register_blueprints


def create_app():
    """Application factory"""
    # Validate and auto-configure
    Config.validate_config()
    
    # Create Flask application
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logging
    setup_logger()
    logger = get_logger()
    
    # Setup localization
    i18n = get_i18n()
    
    # Register core components
    register_filters(app)
    register_context_processors(app)
    
    # Register all blueprints
    register_blueprints(app)
    
    logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"Synapse URL: {Config.SYNAPSE_URL}")
    logger.info(f"Available languages: {i18n.get_available_locales()}")
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
"""
Blueprints package for EPT-MX-ADM
"""

from .auth import auth_bp
from .dashboard import dashboard_bp
from .users import users_bp
from .rooms import rooms_bp
from .spaces import spaces_bp
from .media import media_bp
from .api import api_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(spaces_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(api_bp) 
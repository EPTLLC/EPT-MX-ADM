"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Context Processors
Telegram: https://t.me/EasyProTech

Context processors for EPT-MX-ADM templates
"""

from flask import session
from config.settings import Config
from utils.i18n import get_i18n, t
from modules.auth import AuthManager


def inject_globals():
    """Global variables for all templates"""
    auth_manager = AuthManager()
    i18n = get_i18n()
    
    return {
        'app_name': Config.APP_NAME,
        'app_version': Config.APP_VERSION,
        'current_user': auth_manager.get_current_user() if auth_manager.is_authenticated() else None,
        'colors': Config.COLORS,
        't': t,  # Localization function
        'i18n': i18n,  # Localization object for templates
        'current_locale': i18n.get_locale(),
        'available_locales': i18n.get_available_locales(),
        'config': Config,  # Add Config to templates
        'session': session  # Add session to templates
    }


def register_context_processors(app):
    """Register all context processors with the Flask app"""
    app.context_processor(inject_globals) 
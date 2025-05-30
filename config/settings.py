"""
EPT-MX-ADM Configuration
"""
import os

class Config:
    """Main application configuration"""
    
    # Application info
    APP_NAME = "EPT-MX-ADM"
    APP_VERSION = "v0.0.1-beta"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ept-mx-admin-secret-key-2025')
    DEBUG = True
    
    # Domain and server settings
    DOMAIN = os.environ.get('DOMAIN', 'matrix.easypro.tech')
    SYNAPSE_URL = os.environ.get('SYNAPSE_URL', f'https://{os.environ.get("DOMAIN", "matrix.easypro.tech")}')
    SYNAPSE_ADMIN_API = "/_synapse/admin"
    SYNAPSE_CLIENT_API = "/_matrix/client"
    
    # UI settings
    ITEMS_PER_PAGE = 50
    
    # Localization settings
    DEFAULT_LOCALE = "en"  # Default English
    SUPPORTED_LOCALES = [
        "en",  # English
        "ru",  # Russian
        "de",  # German
        "fr",  # French
        "it",  # Italian
        "es",  # Spanish
        "tr",  # Turkish
        "zh",  # Chinese
        "ja",  # Japanese
        "ar",  # Arabic
        "he"   # Hebrew
    ]
    
    # Color scheme
    COLORS = {
        'primary': '#4e73df',
        'success': '#1cc88a', 
        'warning': '#f6c23e',
        'danger': '#e74a3b',
        'info': '#36b9cc',
        'dark': '#5a5c69'
    }
    
    # Paths (configurable)
    BASE_DIR = '/var/matrix/admin.matrix.easypro.tech'
    BASE_PATH = os.environ.get('BASE_PATH', BASE_DIR)
    LOG_FILE = os.path.join(BASE_PATH, 'debug.log')
    LOCALES_DIR = os.path.join(BASE_PATH, 'locales')
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    # API limits
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    
    @staticmethod
    def get_full_synapse_url():
        """Full URL for Synapse API"""
        return f"{Config.SYNAPSE_URL}{Config.SYNAPSE_ADMIN_API}"
    
    @staticmethod 
    def get_client_api_url():
        """URL for Client API"""
        return f"{Config.SYNAPSE_URL}{Config.SYNAPSE_CLIENT_API}"
    
    @staticmethod
    def get_domain():
        """Get configured domain"""
        return Config.DOMAIN
    
    @staticmethod
    def get_user_domain_suffix():
        """Get domain suffix for user IDs"""
        return f":{Config.DOMAIN}" 
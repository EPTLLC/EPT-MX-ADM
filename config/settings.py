"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Configuration Settings
Telegram: https://t.me/EasyProTech

EPT-MX-ADM Configuration
Ultra-simple setup: just edit config.json with your Matrix server!
"""
import os
import json
from urllib.parse import urlparse

class Config:
    """Auto-configuring Matrix Admin Panel - reads from config.json"""
    
    # Application info
    APP_NAME = "EPT-MX-ADM"
    APP_VERSION = "v1.0.1"
    
    # Load configuration from config.json
    @staticmethod
    def _load_config():
        """Load configuration from config.json"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file not found: {config_path}")
            print("   Creating default config.json...")
            default_config = {
                "matrix_server": "https://matrix.example.com",
                "debug": True,
                "language": "en"
            }
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config.json: {e}")
            return {"matrix_server": "https://matrix.example.com", "debug": True, "language": "en"}
    
    # Load config once
    _config = _load_config()
    
    # =======================================================================
    # 🎯 SIMPLE CONFIGURATION (from config.json)
    # =======================================================================
    
    # Matrix server from config.json
    SYNAPSE_URL = _config.get('matrix_server', 'https://matrix.example.com')
    DEBUG = _config.get('debug', True)
    DEFAULT_LOCALE = _config.get('language', 'en')
    
    # API endpoints (automatically configured)
    SYNAPSE_ADMIN_API = "/_synapse/admin"
    SYNAPSE_CLIENT_API = "/_matrix/client"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ept-mx-admin-secret-key-2025')
    
    # =======================================================================
    # 🔧 AUTO-CONFIGURATION (computed from config.json)
    # =======================================================================
    
    @staticmethod
    def get_domain():
        """Auto-extract domain from matrix_server"""
        try:
            parsed = urlparse(Config.SYNAPSE_URL)
            return parsed.netloc
        except:
            return 'matrix.example.com'
    
    @staticmethod
    def get_base_path():
        """Auto-detect application base path"""
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Auto-configured properties (will be set in validate_config)
    DOMAIN = None
    BASE_DIR = None
    BASE_PATH = None
    LOG_FILE = None
    LOCALES_DIR = None
    
    # UI settings
    ITEMS_PER_PAGE = 50
    
    # Supported languages
    SUPPORTED_LOCALES = [
        "en", "ru", "de", "fr", "it", "es", "tr", "zh", "ja", "ar", "he"
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
    
    # Logging
    LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    # API limits
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # =======================================================================
    # 🚀 HELPER METHODS
    # =======================================================================
    
    @staticmethod
    def get_full_synapse_url():
        """Full URL for Synapse Admin API"""
        return f"{Config.SYNAPSE_URL}{Config.SYNAPSE_ADMIN_API}"
    
    @staticmethod 
    def get_client_api_url():
        """URL for Client API"""
        return f"{Config.SYNAPSE_URL}{Config.SYNAPSE_CLIENT_API}"
    
    @staticmethod
    def get_user_domain_suffix():
        """Get domain suffix for user IDs"""
        return f":{Config.get_domain()}"
    
    @staticmethod
    def validate_config():
        """Validate configuration and show setup info"""
        # Set auto-configured properties
        Config.DOMAIN = Config.get_domain()
        Config.BASE_DIR = Config.get_base_path()
        Config.BASE_PATH = Config.get_base_path()
        Config.LOG_FILE = os.path.join(Config.get_base_path(), 'debug.log')
        Config.LOCALES_DIR = os.path.join(Config.get_base_path(), 'locales')
        
        print(f"📁 Working directory: {Config.BASE_PATH}")
        print(f"📄 Config file: {os.path.join(Config.BASE_PATH, 'config.json')}")
        
        if Config.SYNAPSE_URL == 'https://matrix.example.com':
            print("⚠️  Please edit config.json and set your matrix_server!")
            print("   Example: \"matrix_server\": \"https://matrix.yourdomain.com\"")
            return False
        
        print(f"✅ Matrix server: {Config.SYNAPSE_URL}")
        print(f"✅ Auto-detected domain: {Config.DOMAIN}")
        print(f"✅ Language: {Config.DEFAULT_LOCALE}")
        print(f"✅ Debug mode: {Config.DEBUG}")
        return True
    
    @staticmethod
    def reload_config():
        """Reload configuration from config.json"""
        Config._config = Config._load_config()
        Config.SYNAPSE_URL = Config._config.get('matrix_server', 'https://matrix.example.com')
        Config.DEBUG = Config._config.get('debug', True)
        Config.DEFAULT_LOCALE = Config._config.get('language', 'en')
        Config.DOMAIN = Config.get_domain()
        return True 
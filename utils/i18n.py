"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Internationalization System
Telegram: https://t.me/EasyProTech

Internationalization system for EPT-MX-ADM
"""
import json
import os
from flask import session, request
from utils.logger import get_logger
from config.settings import Config

class I18n:
    """Internationalization manager"""
    
    def __init__(self):
        self.locales_dir = None
        self.default_locale = Config.DEFAULT_LOCALE
        self.logger = get_logger()
        self._translations = {}
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure translations are loaded"""
        if not self._initialized:
            self.locales_dir = Config.LOCALES_DIR or os.path.join(Config.get_base_path(), 'locales')
            self._load_translations()
            self._initialized = True
    
    def _load_translations(self):
        """Load all translations"""
        try:
            if not self.locales_dir or not os.path.exists(self.locales_dir):
                self.logger.error(f"Locales directory not found: {self.locales_dir}")
                return
                
            for filename in os.listdir(self.locales_dir):
                if filename.endswith('.json'):
                    locale = filename[:-5]  # remove .json
                    filepath = os.path.join(self.locales_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self._translations[locale] = json.load(f)
                    
                    self.logger.info(f"Loaded translation for locale: {locale}")
        
        except Exception as e:
            self.logger.error(f"Error loading translations: {str(e)}")
    
    def get_locale(self):
        """Get current locale"""
        # Check session
        if 'locale' in session:
            return session['locale']
        
        # Always return default language (English) for new users
        # User can change language via the switcher
        return self.default_locale
    
    def set_locale(self, locale):
        """Set locale"""
        if locale in self._translations:
            session['locale'] = locale
            self.logger.info(f"Locale set: {locale}")
            return True
        return False
    
    def get_available_locales(self):
        """Get available locales"""
        self._ensure_initialized()
        return list(self._translations.keys())
    
    def t(self, key, **kwargs):
        """Get translation by key"""
        self._ensure_initialized()
        
        locale = self.get_locale()
        translations = self._translations.get(locale, self._translations.get(self.default_locale, {}))
        
        # Split key by dots for nested structure navigation
        keys = key.split('.')
        value = translations
        
        try:
            for k in keys:
                value = value[k]
            
            # Substitute parameters if present
            if kwargs and isinstance(value, str):
                value = value.format(**kwargs)
            
            return value
        
        except (KeyError, TypeError):
            self.logger.warning(f"Translation not found for key '{key}' in locale '{locale}'")
            return key  # return the key itself if translation not found
    
    def get_locale_info(self, locale=None):
        """Get locale info"""
        if locale is None:
            locale = self.get_locale()
        
        info = {
            'code': locale,
            'name': '',
            'native_name': '',
            'flag': ''
        }
        
        if locale == 'en':
            info.update({
                'name': 'English',
                'native_name': 'English',
                'flag': '🇺🇸'
            })
        elif locale == 'ru':
            info.update({
                'name': 'Russian',
                'native_name': 'Русский',
                'flag': '🇷🇺'
            })
        elif locale == 'de':
            info.update({
                'name': 'German',
                'native_name': 'Deutsch',
                'flag': '🇩🇪'
            })
        elif locale == 'fr':
            info.update({
                'name': 'French',
                'native_name': 'Français',
                'flag': '🇫🇷'
            })
        elif locale == 'it':
            info.update({
                'name': 'Italian',
                'native_name': 'Italiano',
                'flag': '🇮🇹'
            })
        elif locale == 'es':
            info.update({
                'name': 'Spanish',
                'native_name': 'Español',
                'flag': '🇪🇸'
            })
        elif locale == 'tr':
            info.update({
                'name': 'Turkish',
                'native_name': 'Türkçe',
                'flag': '🇹🇷'
            })
        elif locale == 'zh':
            info.update({
                'name': 'Chinese',
                'native_name': '中文',
                'flag': '🇨🇳'
            })
        elif locale == 'ja':
            info.update({
                'name': 'Japanese',
                'native_name': '日本語',
                'flag': '🇯🇵'
            })
        elif locale == 'ar':
            info.update({
                'name': 'Arabic',
                'native_name': 'العربية',
                'flag': '🇦🇪'
            })
        elif locale == 'he':
            info.update({
                'name': 'Hebrew',
                'native_name': 'עברית',
                'flag': '🇮🇱'
            })
        
        return info

# Create global instance
i18n = I18n()

def get_i18n():
    """Get i18n instance"""
    return i18n

def t(key, **kwargs):
    """Short translation function"""
    return i18n.t(key, **kwargs) 
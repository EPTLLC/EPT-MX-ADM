import pytest
from unittest.mock import Mock, patch
from utils.i18n import i18n, t
from utils.logger import setup_logger


class TestI18n:
    """Internationalization tests"""
    
    def test_get_locale_default(self):
        """Test getting default locale"""
        with patch('flask.session', {}):
            locale = i18n.get_locale()
            assert locale == 'en'
    
    def test_get_locale_from_session(self):
        """Test getting locale from session"""
        with patch('flask.session', {'locale': 'ru'}):
            locale = i18n.get_locale()
            assert locale == 'ru'
    
    def test_translate_existing_key(self):
        """Test translation of existing key"""
        with patch.object(i18n, 'get_locale', return_value='en'):
            # Mock translation loading
            mock_translations = {
                'en': {'login': {'title': 'Login'}}
            }
            with patch.object(i18n, '_translations', mock_translations):
                result = t('login.title')
                assert result == 'Login'
    
    def test_translate_missing_key(self):
        """Test translation of missing key"""
        with patch.object(i18n, 'get_locale', return_value='en'):
            with patch.object(i18n, '_translations', {'en': {}}):
                result = t('missing.key')
                assert result == 'missing.key'


class TestLogger:
    """Logger tests"""
    
    def test_setup_logger(self):
        """Test logger setup"""
        logger = setup_logger('test_logger')
        assert logger.name == 'test_logger'
        assert len(logger.handlers) > 0
    
    def test_logger_levels(self):
        """Test logger levels"""
        logger = setup_logger('test_levels')
        
        # Check that logger can handle different levels
        logger.debug('Debug message')
        logger.info('Info message')
        logger.warning('Warning message')
        logger.error('Error message')
        
        # If we got here without exceptions, test passed
        assert True 
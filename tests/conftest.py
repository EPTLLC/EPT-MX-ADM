import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config.settings import Config


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SYNAPSE_URL = "https://test.matrix.local"
    SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    """Create test Flask application"""
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create test Flask client"""
    return app.test_client()


@pytest.fixture
def mock_matrix_api():
    """Mock Matrix API client"""
    with patch('utils.api_client.MatrixAPIClient') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        
        # Configure basic responses
        mock_instance.login.return_value = {
            'access_token': 'test_token',
            'user_id': '@admin:test.local'
        }
        mock_instance.get_users.return_value = {
            'users': [],
            'total': 0
        }
        mock_instance.get_rooms.return_value = {
            'rooms': [],
            'total_rooms': 0
        }
        
        yield mock_instance


@pytest.fixture
def authenticated_session(client, mock_matrix_api):
    """Create authenticated session"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'
        sess['user_id'] = '@admin:test.local'
        sess['is_admin'] = True
    return client 
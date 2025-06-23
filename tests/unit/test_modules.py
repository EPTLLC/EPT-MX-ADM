import pytest
from unittest.mock import Mock, patch
from modules.users import UserManager
from modules.rooms import RoomManager
from modules.auth import AuthManager


class TestUserManager:
    """User management module tests"""
    
    @pytest.fixture
    def user_manager(self):
        """Create UserManager instance with mocked API"""
        with patch('modules.users.MatrixAPIClient') as mock_api:
            mock_instance = Mock()
            mock_api.return_value = mock_instance
            return UserManager(mock_instance)
    
    def test_get_users_list(self, user_manager):
        """Test getting users list"""
        # Configure mock
        user_manager.api_client.get_users.return_value = {
            'users': [
                {'name': '@user1:test.local', 'admin': False},
                {'name': '@user2:test.local', 'admin': True}
            ],
            'total': 2
        }
        
        result = user_manager.get_users()
        
        assert 'users' in result
        assert len(result['users']) == 2
        assert result['total'] == 2
    
    def test_create_user_success(self, user_manager):
        """Test successful user creation"""
        user_manager.api_client.create_user.return_value = {
            'name': '@newuser:test.local'
        }
        
        result = user_manager.create_user('newuser', 'password123')
        
        assert result is not None
        user_manager.api_client.create_user.assert_called_once()
    
    def test_deactivate_user(self, user_manager):
        """Test user deactivation"""
        user_manager.api_client.deactivate_user.return_value = {'success': True}
        
        result = user_manager.deactivate_user('@user:test.local')
        
        assert result['success'] is True
        user_manager.api_client.deactivate_user.assert_called_once_with('@user:test.local')


class TestRoomManager:
    """Room management module tests"""
    
    @pytest.fixture
    def room_manager(self):
        """Create RoomManager instance with mocked API"""
        with patch('modules.rooms.MatrixAPIClient') as mock_api:
            mock_instance = Mock()
            mock_api.return_value = mock_instance
            return RoomManager(mock_instance)
    
    def test_get_rooms_list(self, room_manager):
        """Test getting rooms list"""
        room_manager.api_client.get_rooms.return_value = {
            'rooms': [
                {'room_id': '!room1:test.local', 'name': 'Test Room 1'},
                {'room_id': '!room2:test.local', 'name': 'Test Room 2'}
            ],
            'total_rooms': 2
        }
        
        result = room_manager.get_rooms()
        
        assert 'rooms' in result
        assert len(result['rooms']) == 2
    
    def test_delete_room(self, room_manager):
        """Test room deletion"""
        room_manager.api_client.delete_room.return_value = {'success': True}
        
        result = room_manager.delete_room('!room:test.local')
        
        assert result['success'] is True
        room_manager.api_client.delete_room.assert_called_once_with('!room:test.local')


class TestAuthManager:
    """Authentication module tests"""
    
    @pytest.fixture
    def auth_manager(self):
        """Create AuthManager instance"""
        return AuthManager()
    
    def test_validate_matrix_id_valid(self, auth_manager):
        """Test validation of valid Matrix ID"""
        valid_ids = [
            '@user:matrix.org',
            '@admin:test.local',
            '@test123:example.com'
        ]
        
        for matrix_id in valid_ids:
            assert auth_manager.validate_matrix_id(matrix_id) is True
    
    def test_validate_matrix_id_invalid(self, auth_manager):
        """Test validation of invalid Matrix ID"""
        invalid_ids = [
            'user:matrix.org',  # without @
            '@user',            # without domain
            '@:matrix.org',     # empty name
            'invalid'           # completely wrong format
        ]
        
        for matrix_id in invalid_ids:
            assert auth_manager.validate_matrix_id(matrix_id) is False
    
    def test_extract_username(self, auth_manager):
        """Test extracting username from Matrix ID"""
        matrix_id = '@testuser:matrix.org'
        username = auth_manager.extract_username(matrix_id)
        assert username == 'testuser'
    
    def test_extract_domain(self, auth_manager):
        """Test extracting domain from Matrix ID"""
        matrix_id = '@testuser:matrix.org'
        domain = auth_manager.extract_domain(matrix_id)
        assert domain == 'matrix.org' 
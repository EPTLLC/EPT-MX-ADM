"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Users Management Module
Telegram: https://t.me/EasyProTech

Users management module for EPT-MX-ADM
Compact user management functionality
"""

from utils.logger import get_logger
import json

logger = get_logger()


class UserManager:
    """Compact user management class"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_users_list(self, from_token=None, limit=10, search_term=None, guests=None, deactivated=None):
        """Get users list with filters"""
        try:
            params = {'limit': limit}
            
            if from_token:
                params['from'] = from_token
            if search_term:
                params['name'] = search_term
            if guests is not None:
                params['guests'] = 'true' if guests else 'false'
            if deactivated is not None:
                params['deactivated'] = 'true' if deactivated else 'false'
            
            response = self.api_client.get('/v2/users', params=params)
            
            if response and response.status_code == 200:
                data = response.json()
                # Патчим дату создания, если её нет
                for user in data.get('users', []):
                    if 'creation_ts' not in user or not user['creation_ts']:
                        user['creation_ts'] = user.get('creation_ts') or None
                logger.debug(f"Retrieved users count: {len(data.get('users', []))}")
                return data
            else:
                logger.error(f"Failed to get users: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            return None
    
    def get_user_details(self, user_id):
        """Get detailed user information"""
        try:
            response = self.api_client.get(f'/v2/users/{user_id}')
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user details: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user details: {str(e)}")
            return None
    
    def create_user(self, user_data):
        """Create new user"""
        try:
            user_id = user_data.get('user_id')
            response = self.api_client.put(f'/v2/users/{user_id}', data=user_data)
            
            if response and response.status_code in [200, 201]:
                logger.info(f"User {user_id} created successfully")
                return True
            else:
                logger.error(f"Failed to create user: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return False
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        try:
            response = self.api_client.put(f'/v2/users/{user_id}', data=user_data)
            
            if response and response.status_code == 200:
                logger.info(f"User {user_id} updated successfully")
                return True
            else:
                logger.error(f"Failed to update user: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return False
    
    def deactivate_user(self, user_id, erase=False):
        """Deactivate user"""
        try:
            data = {'deactivated': True}
            if erase:
                data['erase'] = True
            
            response = self.api_client.put(f'/v2/users/{user_id}', data=data)
            
            if response and response.status_code == 200:
                logger.info(f"User {user_id} deactivated successfully")
                return True
            else:
                logger.error(f"Failed to deactivate user: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            return False
    
    def get_user_sessions(self, user_id):
        """Get user session information (whois)"""
        try:
            response = self.api_client.get(f'/v1/whois/{user_id}')
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user sessions: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user sessions: {str(e)}")
            return None
    
    def get_user_devices(self, user_id):
        """Get user devices"""
        try:
            response = self.api_client.get(f'/v2/users/{user_id}/devices')
            
            if response and response.status_code == 200:
                return response.json().get('devices', [])
            else:
                logger.error(f"Failed to get user devices: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user devices: {str(e)}")
            return None
    
    def delete_user_device(self, user_id, device_id):
        """Delete user device"""
        try:
            response = self.api_client.delete(f'/v2/users/{user_id}/devices/{device_id}')
            
            if response and response.status_code == 200:
                logger.info(f"Device {device_id} deleted for user {user_id}")
                return True
            else:
                logger.error(f"Failed to delete device: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting device: {str(e)}")
            return False
    
    def delete_user(self, user_id):
        """Permanently delete user (using deactivate with erase)"""
        try:
            # Synapse doesn't support direct DELETE, use deactivate with erase instead
            data = {
                'deactivated': True,
                'erase': True  # This will delete user data
            }
            response = self.api_client.put(f'/v2/users/{user_id}', data=data)
            
            if response and response.status_code == 200:
                logger.info(f"User {user_id} deleted successfully (deactivated with erase)")
                return True
            else:
                logger.error(f"Failed to delete user: {response.status_code if response else 'No response'}")
                if response:
                    logger.error(f"API Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return False
    
    def reset_user_password(self, user_id, new_password):
        """Reset user password"""
        try:
            data = {'new_password': new_password}
            response = self.api_client.post(f'/v1/users/{user_id}/password', data=data)
            
            if response and response.status_code == 200:
                logger.info(f"Password reset for user {user_id}")
                return True
            else:
                logger.error(f"Failed to reset password: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error resetting password: {str(e)}")
            return False
    
    def get_user_rooms(self, user_id):
        """Get user rooms"""
        try:
            response = self.api_client.get(f'/v1/users/{user_id}/rooms')
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user rooms: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user rooms: {str(e)}")
            return None
    
    def get_user_media(self, user_id, from_token=None, limit=10):
        """Get user media"""
        try:
            params = {'limit': limit}
            if from_token:
                params['from'] = from_token
            
            response = self.api_client.get(f'/v1/users/{user_id}/media', params=params)
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user media: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user media: {str(e)}")
            return None
    
    def delete_user_media(self, user_id, media_id=None):
        """Delete user media (all or specific)"""
        try:
            if media_id:
                endpoint = f'/v1/users/{user_id}/media/{media_id}'
            else:
                endpoint = f'/v1/users/{user_id}/media'
            
            response = self.api_client.delete(endpoint)
            
            if response and response.status_code == 200:
                logger.info(f"Media deleted for user {user_id}")
                return True
            else:
                logger.error(f"Failed to delete media: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting media: {str(e)}")
            return False
    
    def get_user_account_data(self, user_id):
        """Get user account data"""
        try:
            response = self.api_client.get(f'/v1/users/{user_id}/account_data')
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get account data: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting account data: {str(e)}")
            return None
    
    def login_as_user(self, user_id):
        """Get access token on behalf of user"""
        try:
            response = self.api_client.post(f'/v1/users/{user_id}/login')
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to login as user: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error logging as user: {str(e)}")
            return None
    
    def override_rate_limit(self, user_id, messages_per_second=None, burst_count=None):
        """Configure rate limits for user"""
        try:
            data = {}
            if messages_per_second is not None:
                data['messages_per_second'] = messages_per_second
            if burst_count is not None:
                data['burst_count'] = burst_count
            
            response = self.api_client.post(f'/v1/users/{user_id}/override_ratelimit', data=data)
            
            if response and response.status_code == 200:
                logger.info(f"Rate limit configured for user {user_id}")
                return True
            else:
                logger.error(f"Failed to configure rate limit: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error configuring rate limit: {str(e)}")
            return False
    
    def reactivate_user(self, user_id):
        """Reactivate user"""
        try:
            response = self.api_client.post(f'/v1/users/{user_id}/reactivate')
            
            if response and response.status_code == 200:
                logger.info(f"User {user_id} reactivated successfully")
                return True
            else:
                logger.error(f"Failed to reactivate user: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error reactivating user: {str(e)}")
            return False
    
    def export_users_csv(self, filters=None):
        """Export users to CSV format"""
        try:
            # Get all users with filters
            users_data = self.get_users_list(
                limit=1000,  # Large limit for export
                search_term=filters.get('search') if filters else None,
                guests=filters.get('guests') if filters else None,
                deactivated=filters.get('deactivated') if filters else None
            )
            
            if not users_data or not users_data.get('users'):
                return None
            
            # Create CSV content
            csv_lines = ['User ID,Display Name,Admin,Guest,Deactivated,Creation Time']
            
            for user in users_data['users']:
                line = f"{user.get('name', '')},{user.get('displayname', '')},{user.get('admin', False)},{user.get('user_type') == 'guest'},{user.get('deactivated', False)},{user.get('creation_ts', '')}"
                csv_lines.append(line)
            
            return '\n'.join(csv_lines)
            
        except Exception as e:
            logger.error(f"Error exporting users CSV: {str(e)}")
            return None 
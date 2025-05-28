"""
Rooms management module for EPT-MX-ADM
Basic room management functionality
"""

from utils.logger import get_logger

logger = get_logger()


class RoomManager:
    """Basic room management class"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_rooms_list(self, from_token=None, limit=10, search_term=None):
        """Get rooms list - basic implementation"""
        try:
            params = {'limit': limit}
            if from_token:
                params['from'] = from_token
            if search_term:
                params['search_term'] = search_term
            
            response = self.api_client.get('/v1/rooms', params=params)
            
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get rooms: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting rooms: {str(e)}")
            return None 

    def get_room_details(self, room_id):
        """Get details for a specific room"""
        try:
            response = self.api_client.get(f'/v1/rooms/{room_id}')
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get room details: {response.status_code if response else 'No response'}")
                return None
        except Exception as e:
            logger.error(f"Error getting room details: {str(e)}")
            return None 
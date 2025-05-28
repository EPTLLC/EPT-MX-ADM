"""
Spaces management module for EPT-MX-ADM
Basic spaces management functionality
"""

from utils.logger import get_logger

logger = get_logger()


class SpaceManager:
    """Basic space management class"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_spaces_list(self):
        """Get spaces list - basic implementation"""
        try:
            response = self.api_client.get('/v1/rooms')
            
            if response and response.status_code == 200:
                data = response.json()
                # Filter only spaces
                spaces = [room for room in data.get('rooms', []) if room.get('room_type') == 'm.space']
                return {'spaces': spaces}
            else:
                logger.error(f"Failed to get spaces: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting spaces: {str(e)}")
            return None 
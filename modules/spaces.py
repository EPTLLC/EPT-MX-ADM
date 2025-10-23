"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Spaces Management Module
Telegram: https://t.me/EasyProTech

Spaces management module for EPT-MX-ADM
Basic spaces management functionality
"""

from utils.logger import get_logger

logger = get_logger()


class SpaceManager:
    """Basic space management class"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_spaces_list(self, from_token=None, limit=25, search_term=None):
        """Get spaces list with pagination and search"""
        try:
            # First, get ALL spaces to know the total count
            all_params = {'limit': 1000}  # Get all rooms
            if search_term:
                all_params['search_term'] = search_term
            
            all_response = self.api_client.get('/v1/rooms', params=all_params)
            
            if all_response and all_response.status_code == 200:
                all_data = all_response.json()
                all_rooms = all_data.get('rooms', [])
                
                # Filter only spaces from ALL rooms
                all_spaces = [room for room in all_rooms if room.get('room_type') == 'm.space']
                
                # Apply search filter if provided
                if search_term:
                    search_lower = search_term.lower()
                    all_spaces = [s for s in all_spaces if 
                                 search_lower in (s.get('name') or '').lower() or
                                 search_lower in (s.get('canonical_alias') or '').lower() or
                                 search_lower in (s.get('room_id') or '').lower()]
                
                # Calculate total
                total_spaces = len(all_spaces)
                
                # Apply pagination manually
                from_offset = int(from_token) if from_token else 0
                spaces_page = all_spaces[from_offset:from_offset + limit]
                
                return {
                    'rooms': spaces_page,
                    'total_spaces': total_spaces,
                    'total': total_spaces,
                    'next_token': str(from_offset + limit) if (from_offset + limit) < total_spaces else None
                }
            else:
                logger.error(f"Failed to get spaces: {all_response.status_code if all_response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting spaces: {str(e)}")
            return None 
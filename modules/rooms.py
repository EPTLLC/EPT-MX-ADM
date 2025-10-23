"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Rooms Management Module
Telegram: https://t.me/EasyProTech

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

    def get_room_members(self, room_id):
        """Get room members list"""
        try:
            response = self.api_client.get(f'/v1/rooms/{room_id}/members')
            if response and response.status_code == 200:
                data = response.json()
                # Handle both response formats
                if isinstance(data, dict) and 'members' in data:
                    return data['members']
                elif isinstance(data, list):
                    return data
                else:
                    return data
            else:
                logger.error(f"Failed to get room members: {response.status_code if response else 'No response'}")
                return []
        except Exception as e:
            logger.error(f"Error getting room members: {str(e)}")
            return []

    def get_room_state_events(self, room_id):
        """Get room state events"""
        try:
            response = self.api_client.get(f'/v1/rooms/{room_id}/state')
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get room state: {response.status_code if response else 'No response'}")
                return []
        except Exception as e:
            logger.error(f"Error getting room state: {str(e)}")
            return []

    def block_room(self, room_id, block=True):
        """Block or unblock room"""
        try:
            data = {"block": block}
            response = self.api_client.put(f'/v1/rooms/{room_id}/block', json=data)
            if response and response.status_code == 200:
                logger.info(f"Room {room_id} {'blocked' if block else 'unblocked'} successfully")
                return True
            else:
                logger.error(f"Failed to block/unblock room: {response.status_code if response else 'No response'}")
                return False
        except Exception as e:
            logger.error(f"Error blocking/unblocking room: {str(e)}")
            return False

    def unblock_room(self, room_id):
        """Unblock room (convenience method)"""
        return self.block_room(room_id, block=False)

    def make_room_admin(self, room_id, user_id):
        """Make user admin of the room"""
        try:
            data = {"user_id": user_id}
            response = self.api_client.post(f'/v1/rooms/{room_id}/make_room_admin', json=data)
            if response and response.status_code == 200:
                logger.info(f"User {user_id} made admin of room {room_id}")
                return True
            else:
                logger.error(f"Failed to make room admin: {response.status_code if response else 'No response'}")
                return False
        except Exception as e:
            logger.error(f"Error making room admin: {str(e)}")
            return False



    def delete_room(self, room_id, purge=True, message=None):
        """Delete room completely (removes all users)
        
        Args:
            room_id: Room ID to delete
            purge: Whether to purge all events (should be True for deletion)
            message: Message to show to users
        """
        try:
            data = {
                "block": True,
                "purge": purge,
                "message": message or "Room has been deleted by administrator"
            }
            
            response = self.api_client.delete(f'/v1/rooms/{room_id}', json=data)
            
            if response and response.status_code == 200:
                logger.info(f"Room {room_id} deleted successfully")
                return True
            elif response and response.status_code == 404:
                logger.error(f"Room {room_id} not found for deletion")
                return False
            else:
                logger.error(f"Failed to delete room: {response.status_code if response else 'No response'}")
                if response:
                    logger.error(f"Response text: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error deleting room: {str(e)}")
            return False

    def export_rooms_csv(self, filters=None):
        """Export rooms to CSV format"""
        try:
            # Get all rooms with filters
            search_term = filters.get('search') if filters else None
            rooms_data = self.get_rooms_list(limit=1000, search_term=search_term)
            
            if not rooms_data or not rooms_data.get('rooms'):
                return None
            
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Headers
            writer.writerow([
                'Room ID', 'Name', 'Canonical Alias', 'Members', 'Local Members',
                'Creator', 'Encrypted', 'Federated', 'Version', 'State Events',
                'In Directory', 'Public', 'Join Rules', 'Guest Access'
            ])
            
            # Data rows
            for room in rooms_data['rooms']:
                writer.writerow([
                    room.get('room_id', ''),
                    room.get('name', ''),
                    room.get('canonical_alias', ''),
                    room.get('joined_members', 0),
                    room.get('joined_local_members', 0),
                    room.get('creator', ''),
                    'Yes' if room.get('encryption') else 'No',
                    'Yes' if room.get('federatable', True) else 'No',
                    room.get('version', '1'),
                    room.get('state_events', 0),
                    'Yes' if room.get('public', False) else 'No',
                    'Yes' if room.get('public', False) else 'No',
                    room.get('join_rules', 'Unknown'),
                    room.get('guest_access', 'Unknown')
                ])
            
            return output.getvalue()
        
        except Exception as e:
            logger.error(f"Error exporting rooms CSV: {str(e)}")
            return None 
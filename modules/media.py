"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Media Management Module
Telegram: https://t.me/EasyProTech

Media management module for EPT-MX-ADM
Complete media management functionality
"""

from utils.logger import get_logger
import json

logger = get_logger()


class MediaManager:
    """Complete media management class"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_users_media_list(self, from_token=None, limit=25, search_term=None, page=1):
        """Get list of users with their media statistics"""
        try:
            # Use the fast media statistics endpoint
            media_response = self.api_client.get('/v1/statistics/users/media')
            
            if not media_response or media_response.status_code != 200:
                logger.error(f"Failed to get media statistics: {media_response.status_code if media_response else 'No response'}")
                return {'users': [], 'total': 0}
            
            media_data = media_response.json()
            all_users_media = media_data.get('users', [])
            
            # Filter users with media > 0
            users_with_media = [u for u in all_users_media if u.get('media_count', 0) > 0]
            
            # Apply search filter if provided
            if search_term:
                search_lower = search_term.lower()
                users_with_media = [
                    u for u in users_with_media 
                    if search_lower in (u.get('user_id', '') or '').lower()
                ]
            
            # Sort by media count (descending)
            users_with_media.sort(key=lambda x: x.get('media_count', 0), reverse=True)
            
            # Apply pagination (client-side)
            from_offset = (page - 1) * limit
            start_idx = from_offset
            end_idx = start_idx + limit
            paginated_users = users_with_media[start_idx:end_idx]
            
            # Format data for template
            formatted_users = []
            for user in paginated_users:
                formatted_users.append({
                    'user_id': user.get('user_id', ''),
                    'display_name': '',  # API doesn't provide displayname
                    'media_count': user.get('media_count', 0),
                    'media_length': user.get('media_length', 0),
                    'media_length_formatted': self._format_file_size(user.get('media_length', 0))
                })
            
            return {
                'users': formatted_users,
                'total': len(users_with_media)
            }
            
        except Exception as e:
            logger.error(f"Error getting users media list: {str(e)}")
            return {'users': [], 'total': 0}
    
    def get_media_statistics(self):
        """Get overall media statistics"""
        try:
            # Use the fast media statistics endpoint
            media_response = self.api_client.get('/v1/statistics/users/media')
            
            if not media_response or media_response.status_code != 200:
                logger.error(f"Failed to get media statistics: {media_response.status_code if media_response else 'No response'}")
                return {
                    'total_media_files': 0,
                    'total_media_size': 0,
                    'total_media_size_formatted': '0 B',
                    'users_with_media': 0
                }
            
            media_data = media_response.json()
            users_media_list = media_data.get('users', [])
            
            # Calculate totals
            total_files = sum(user.get('media_count', 0) for user in users_media_list)
            total_size = sum(user.get('media_length', 0) for user in users_media_list)
            users_with_media = sum(1 for user in users_media_list if user.get('media_count', 0) > 0)
            
            return {
                'total_media_files': total_files,
                'total_media_size': total_size,
                'total_media_size_formatted': self._format_file_size(total_size),
                'users_with_media': users_with_media
            }
            
        except Exception as e:
            logger.error(f"Error getting media statistics: {str(e)}")
            return {
                'total_media_files': 0,
                'total_media_size': 0,
                'total_media_size_formatted': '0 B',
                'users_with_media': 0
            }
    
    def get_user_media(self, user_id, from_token=None, limit=10):
        """Get user media list"""
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
    
    def get_user_media_detailed(self, user_id, limit=25):
        """Get detailed user media information"""
        try:
            params = {'limit': limit}
            response = self.api_client.get(f'/v1/users/{user_id}/media', params=params)
            
            if response and response.status_code == 200:
                data = response.json()
                
                # Process media files to add additional info
                media_files = data.get('media', [])
                processed_media = []
                total_size = 0
                
                for media in media_files:
                    # Add file type based on content type
                    content_type = media.get('media_type', '')
                    if content_type.startswith('image/'):
                        file_type = 'image'
                    elif content_type.startswith('video/'):
                        file_type = 'video'
                    elif content_type.startswith('audio/'):
                        file_type = 'audio'
                    elif content_type.startswith('text/') or 'document' in content_type:
                        file_type = 'document'
                    else:
                        file_type = 'other'
                    
                    media['file_type'] = file_type
                    
                    # Add quarantine status
                    media['is_quarantined'] = media.get('quarantined_by') is not None
                    media['is_safe_from_quarantine'] = media.get('safe_from_quarantine', False)
                    
                    # Add formatted file size
                    file_size = media.get('media_length', 0)
                    media['file_size_formatted'] = self._format_file_size(file_size)
                    total_size += file_size
                    
                    processed_media.append(media)
                
                return {
                    'media': processed_media,
                    'total_count': data.get('total', len(processed_media)),  # Use API total
                    'total_size': total_size,
                    'total_size_formatted': self._format_file_size(total_size),
                    'next_token': data.get('next_token')
                }
            else:
                logger.error(f"Failed to get user media: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting detailed user media: {str(e)}")
            return None
    
    def export_users_media_csv(self, filters=None):
        """Export users media statistics to CSV"""
        try:
            # Get users with media
            users_data = self.get_users_media_list(limit=10000)
            
            if not users_data or not users_data.get('users'):
                return None
            
            # Create CSV content
            csv_lines = ['User ID,Media Count,Total Size (Bytes),Total Size (Formatted)']
            
            for user in users_data['users']:
                line = f"{user.get('user_id', '')},{user.get('media_count', 0)},{user.get('media_length', 0)},{user.get('media_length_formatted', '0 B')}"
                csv_lines.append(line)
            
            return '\n'.join(csv_lines)
            
        except Exception as e:
            logger.error(f"Error exporting users media CSV: {str(e)}")
            return None
    
    def export_user_media_csv(self, user_id):
        """Export specific user's media files to CSV"""
        try:
            media_data = self.get_user_media_detailed(user_id, limit=1000)
            
            if not media_data or not media_data.get('media'):
                return None
            
            # Create CSV content
            csv_lines = ['Media ID,File Name,File Type,Size (Bytes),Size (Formatted),Created,Last Access,Quarantined']
            
            for media in media_data['media']:
                line = f"{media.get('media_id', '')},{media.get('upload_name', '')},{media.get('file_type', '')},{media.get('media_length', 0)},{media.get('file_size_formatted', '0 B')},{media.get('created_ts', '')},{media.get('last_access_ts', '')},{media.get('is_quarantined', False)}"
                csv_lines.append(line)
            
            return '\n'.join(csv_lines)
            
        except Exception as e:
            logger.error(f"Error exporting user media CSV: {str(e)}")
            return None
    
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        try:
            size_bytes = int(size_bytes) if size_bytes else 0
        except:
            return "0 B"
        
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size_float = float(size_bytes)
        while size_float >= 1024 and i < len(size_names) - 1:
            size_float /= 1024.0
            i += 1
        
        return f"{size_float:.1f} {size_names[i]}"

"""
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
                    
                    # Add quarantine status (placeholder - would need actual API)
                    media['is_quarantined'] = media.get('quarantined_by') is not None
                    media['is_safe_from_quarantine'] = media.get('safe_from_quarantine', False)
                    
                    # Add formatted file size
                    file_size = media.get('media_length', 0)
                    media['file_size_formatted'] = self._format_file_size(file_size)
                    total_size += file_size
                    
                    processed_media.append(media)
                
                return {
                    'media': processed_media,
                    'total_count': len(processed_media),
                    'total_size': total_size,
                    'total_size_formatted': self._format_file_size(total_size)
                }
            else:
                logger.error(f"Failed to get user media: {response.status_code if response else 'No response'}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting detailed user media: {str(e)}")
            return None
    
    def get_users_media_list(self, from_token=None, limit=25, search_term=None, page=1):
        """Get list of users with their media statistics"""
        try:
            # First get all users
            user_params = {'limit': 1000}  # Get many users to calculate media stats
            if search_term:
                user_params['name'] = search_term
            
            users_response = self.api_client.get('/v2/users', params=user_params)
            
            if not users_response or users_response.status_code != 200:
                logger.error(f"Failed to get users: {users_response.status_code if users_response else 'No response'}")
                return None
            
            users_data = users_response.json()
            all_users = users_data.get('users', [])
            
            # Get media statistics for each user
            users_with_media = []
            
            for user in all_users:
                user_id = user.get('name')
                if not user_id:
                    continue
                
                try:
                    # Get user media count
                    media_response = self.api_client.get(f'/v1/users/{user_id}/media', params={'limit': 1})
                    
                    if media_response and media_response.status_code == 200:
                        media_data = media_response.json()
                        media_count = len(media_data.get('media', []))
                        
                        # Calculate total media size (would need to get all media for accurate count)
                        total_size = 0
                        for media in media_data.get('media', []):
                            total_size += media.get('media_length', 0)
                        
                        if media_count > 0:  # Only include users with media
                            users_with_media.append({
                                'user_id': user_id,
                                'display_name': user.get('displayname', ''),
                                'media_count': media_count,
                                'media_length': total_size,
                                'media_length_formatted': self._format_file_size(total_size)
                            })
                    
                except Exception as e:
                    logger.debug(f"Error getting media for user {user_id}: {str(e)}")
                    continue
            
            # Sort by media count (descending)
            users_with_media.sort(key=lambda x: x.get('media_count', 0), reverse=True)
            
            # Apply pagination
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_users = users_with_media[start_idx:end_idx]
            
            return {
                'users': paginated_users,
                'total': len(users_with_media)
            }
            
        except Exception as e:
            logger.error(f"Error getting users media list: {str(e)}")
            return None
    
    def get_media_statistics(self):
        """Get overall media statistics"""
        try:
            # This would ideally use a dedicated API endpoint
            # For now, we'll return basic stats
            stats = {
                'total_media_files': 0,
                'total_media_size': 0,
                'total_media_size_formatted': '0 B',
                'users_with_media': 0
            }
            
            # Try to get some basic stats from users
            try:
                users_response = self.api_client.get('/v2/users', params={'limit': 100})
                if users_response and users_response.status_code == 200:
                    users_data = users_response.json()
                    users = users_data.get('users', [])
                    
                    total_files = 0
                    total_size = 0
                    users_with_media = 0
                    
                    for user in users[:10]:  # Sample first 10 users to avoid timeout
                        user_id = user.get('name')
                        if user_id:
                            try:
                                media_response = self.api_client.get(f'/v1/users/{user_id}/media', params={'limit': 100})
                                if media_response and media_response.status_code == 200:
                                    media_data = media_response.json()
                                    media_files = media_data.get('media', [])
                                    
                                    if media_files:
                                        users_with_media += 1
                                        total_files += len(media_files)
                                        
                                        for media in media_files:
                                            total_size += media.get('media_length', 0)
                            except:
                                continue
                    
                    stats['total_media_files'] = total_files
                    stats['total_media_size'] = total_size
                    stats['total_media_size_formatted'] = self._format_file_size(total_size)
                    stats['users_with_media'] = users_with_media
            
            except Exception as e:
                logger.debug(f"Error calculating media statistics: {str(e)}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting media statistics: {str(e)}")
            return {
                'total_media_files': 0,
                'total_media_size': 0,
                'total_media_size_formatted': '0 B',
                'users_with_media': 0
            }
    
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
    
    def quarantine_media(self, server_name, media_id):
        """Quarantine specific media file"""
        try:
            response = self.api_client.post(f'/v1/quarantine_media/{server_name}/{media_id}')
            
            if response and response.status_code == 200:
                logger.info(f"Media {media_id} quarantined")
                return True
            else:
                logger.error(f"Failed to quarantine media: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error quarantining media: {str(e)}")
            return False
    
    def protect_media(self, server_name, media_id):
        """Protect media from quarantine"""
        try:
            response = self.api_client.post(f'/v1/protect_media/{server_name}/{media_id}')
            
            if response and response.status_code == 200:
                logger.info(f"Media {media_id} protected")
                return True
            else:
                logger.error(f"Failed to protect media: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error protecting media: {str(e)}")
            return False
    
    def delete_media_file(self, server_name, media_id):
        """Delete specific media file"""
        try:
            response = self.api_client.delete(f'/v1/media/{server_name}/{media_id}')
            
            if response and response.status_code == 200:
                logger.info(f"Media file {media_id} deleted")
                return True
            else:
                logger.error(f"Failed to delete media file: {response.status_code if response else 'No response'}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting media file: {str(e)}")
            return False
    
    def export_users_media_csv(self, filters=None):
        """Export users media statistics to CSV"""
        try:
            # Get users with media
            users_data = self.get_users_media_list(limit=1000)
            
            if not users_data or not users_data.get('users'):
                return None
            
            # Create CSV content
            csv_lines = ['User ID,Display Name,Media Count,Total Size (Bytes),Total Size (Formatted)']
            
            for user in users_data['users']:
                line = f"{user.get('user_id', '')},{user.get('display_name', '')},{user.get('media_count', 0)},{user.get('media_length', 0)},{user.get('media_length_formatted', '0 B')}"
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
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}" 
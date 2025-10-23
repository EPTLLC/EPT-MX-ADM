"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Analytics Module
Telegram: https://t.me/EasyProTech

Analytics module for EPT-MX-ADM
Complete analytics functionality with Matrix health monitoring
"""

from utils.logger import get_logger
import time
import requests

logger = get_logger()


class AnalyticsManager:
    """Complete analytics manager with health monitoring"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_dashboard_stats(self):
        """Get comprehensive dashboard statistics"""
        try:
            stats = {
                'total_users': 0,
                'active_users': 0,
                'deactivated_users': 0,
                'total_rooms': 0,
                'local_rooms': 0,
                'remote_rooms': 0,
                'server_version': 'Unknown',
                'domain': 'Unknown',
                'python_version': 'Unknown',
                'media_count': 0,
                'media_size': 0,
                'media_size_human': 'N/A'
            }
            
            # Get users statistics
            try:
                # Get ALL users including deactivated (no filter = only active, deactivated=true = all)
                # Synapse API quirk: need to request with deactivated=true to get both active and deactivated
                all_response = self.api_client.get('/v2/users', params={'limit': 10000, 'deactivated': 'true'})
                if all_response and all_response.status_code == 200:
                    all_data = all_response.json()
                    all_users = all_data.get('users', [])
                    
                    # Use API total if available, otherwise count manually
                    stats['total_users'] = all_data.get('total', len(all_users))
                    
                    # Count active (not deactivated)
                    stats['active_users'] = sum(1 for u in all_users if not u.get('deactivated', False))
                    
                    # Count deactivated
                    stats['deactivated_users'] = sum(1 for u in all_users if u.get('deactivated', False))
                    
                    logger.info(f"Users stats - Total: {stats['total_users']}, Active: {stats['active_users']}, Deactivated: {stats['deactivated_users']}")
                else:
                    logger.error(f"Failed to get users: {all_response.status_code if all_response else 'No response'}")
                    
            except Exception as e:
                logger.error(f"Error getting user stats: {str(e)}")
            
            # Get rooms statistics
            try:
                rooms_response = self.api_client.get('/v1/rooms', params={'limit': 1})
                if rooms_response and rooms_response.status_code == 200:
                    rooms_data = rooms_response.json()
                    stats['total_rooms'] = rooms_data.get('total_rooms', 0)
                    
                    # Count local vs remote rooms
                    if 'rooms' in rooms_data:
                        local_count = 0
                        remote_count = 0
                        for room in rooms_data['rooms']:
                            if room.get('federatable', True):
                                remote_count += 1
                            else:
                                local_count += 1
                        stats['local_rooms'] = local_count
                        stats['remote_rooms'] = remote_count
            except Exception as e:
                logger.error(f"Error getting room stats: {str(e)}")
            
            # Get media statistics (total storage used by all users)
            try:
                media_response = self.api_client.get('/v1/statistics/users/media')
                if media_response and media_response.status_code == 200:
                    media_data = media_response.json()
                    users_media = media_data.get('users', [])
                    
                    # Sum all users' media sizes
                    total_size = sum(user.get('media_length', 0) for user in users_media)
                    total_count = sum(user.get('media_count', 0) for user in users_media)
                    
                    stats['media_count'] = total_count
                    stats['media_size'] = total_size
                    stats['media_size_human'] = self._format_bytes(total_size)
                    
                    logger.info(f"Media stats - Total files: {total_count}, Total size: {stats['media_size_human']}")
            except Exception as e:
                logger.debug(f"Media stats not available: {str(e)}")
            
            # Get server version
            try:
                version_response = self.api_client.get('/v1/server_version')
                if version_response and version_response.status_code == 200:
                    version_data = version_response.json()
                    stats['server_version'] = version_data.get('server_version', 'Unknown')
            except Exception as e:
                logger.error(f"Error getting server version: {str(e)}")
            
            # Extract domain from API client
            if hasattr(self.api_client, 'base_url'):
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(self.api_client.base_url)
                    stats['domain'] = parsed.netloc
                except:
                    pass
            
            # Get Python version
            try:
                import sys
                python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                stats['python_version'] = python_version
            except Exception as e:
                logger.error(f"Error getting Python version: {str(e)}")
                stats['python_version'] = 'Unknown'
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {str(e)}")
            return {}
    
    def _format_bytes(self, bytes_size):
        """Format bytes to human readable format"""
        try:
            bytes_size = int(bytes_size)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_size < 1024.0:
                    return f"{bytes_size:.1f} {unit}"
                bytes_size /= 1024.0
            return f"{bytes_size:.1f} PB"
        except:
            return 'N/A'
    
    def get_server_performance(self):
        """Get server performance metrics"""
        try:
            performance = {
                'api_response_time': 0,
                'status': 'unknown'
            }
            
            # Measure API response time
            start_time = time.time()
            try:
                response = self.api_client.get('/v1/server_version')
                end_time = time.time()
                
                if response and response.status_code == 200:
                    response_time = round((end_time - start_time) * 1000, 2)  # ms
                    performance['api_response_time'] = response_time
                    performance['status'] = 'online'
                    
                    # Categorize performance
                    if response_time < 100:
                        performance['performance_level'] = 'excellent'
                    elif response_time < 300:
                        performance['performance_level'] = 'good'
                    elif response_time < 1000:
                        performance['performance_level'] = 'fair'
                    else:
                        performance['performance_level'] = 'poor'
                else:
                    performance['status'] = 'offline'
                    performance['performance_level'] = 'poor'
                    
            except Exception as e:
                logger.error(f"Error measuring API response time: {str(e)}")
                performance['status'] = 'offline'
                performance['performance_level'] = 'poor'
            
            return performance
            
        except Exception as e:
            logger.error(f"Error getting server performance: {str(e)}")
            return {}
    
    def get_system_health(self):
        """Get comprehensive system health status"""
        try:
            health = {
                'matrix_api': {'status': 'unknown', 'message': 'Checking...'},
                'users_api': {'status': 'unknown', 'message': 'Checking...'},
                'rooms_api': {'status': 'unknown', 'message': 'Checking...'},
                'overall_status': 'unknown'
            }
            
            healthy_services = 0
            total_services = 3
            
            # Check Matrix Core API
            try:
                response = self.api_client.get('/v1/server_version')
                if response and response.status_code == 200:
                    health['matrix_api'] = {'status': 'healthy', 'message': 'Core API accessible'}
                    healthy_services += 1
                else:
                    health['matrix_api'] = {'status': 'unhealthy', 'message': f'HTTP {response.status_code if response else "No response"}'}
            except Exception as e:
                health['matrix_api'] = {'status': 'unhealthy', 'message': f'Error: {str(e)[:50]}'}
            
            # Check Users API
            try:
                response = self.api_client.get('/v2/users', params={'limit': 1})
                if response and response.status_code == 200:
                    health['users_api'] = {'status': 'healthy', 'message': 'User management accessible'}
                    healthy_services += 1
                else:
                    health['users_api'] = {'status': 'unhealthy', 'message': f'HTTP {response.status_code if response else "No response"}'}
            except Exception as e:
                health['users_api'] = {'status': 'unhealthy', 'message': f'Error: {str(e)[:50]}'}
            
            # Check Rooms API
            try:
                response = self.api_client.get('/v1/rooms', params={'limit': 1})
                if response and response.status_code == 200:
                    health['rooms_api'] = {'status': 'healthy', 'message': 'Room management accessible'}
                    healthy_services += 1
                else:
                    health['rooms_api'] = {'status': 'unhealthy', 'message': f'HTTP {response.status_code if response else "No response"}'}
            except Exception as e:
                health['rooms_api'] = {'status': 'unhealthy', 'message': f'Error: {str(e)[:50]}'}
            
            # Determine overall health
            if healthy_services == total_services:
                health['overall_status'] = 'healthy'
            elif healthy_services >= total_services * 0.7:  # 70% or more
                health['overall_status'] = 'degraded'
            else:
                health['overall_status'] = 'unhealthy'
            
            health['healthy_services'] = healthy_services
            health['total_services'] = total_services
            
            # Добавляем совместимость для шаблона
            health['api_available'] = health['matrix_api']['status'] == 'healthy'
            health['users_api_available'] = health['users_api']['status'] == 'healthy'
            health['rooms_api_available'] = health['rooms_api']['status'] == 'healthy'

            return health
            
        except Exception as e:
            logger.error(f"Error getting system health: {str(e)}")
            return {
                'matrix_api': {'status': 'unhealthy', 'message': 'Health check failed'},
                'users_api': {'status': 'unhealthy', 'message': 'Health check failed'},
                'rooms_api': {'status': 'unhealthy', 'message': 'Health check failed'},
                'overall_status': 'unhealthy',
                'healthy_services': 0,
                'total_services': 3
            }
    
    def get_user_statistics(self):
        """Get detailed user statistics"""
        try:
            stats = {
                'total_users': 0,
                'active_users': 0,
                'deactivated_users': 0,
                'admin_users': 0,
                'guest_users': 0
            }
            
            # Get all users
            response = self.api_client.get('/v2/users', params={'limit': 1000})
            if response and response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                
                stats['total_users'] = len(users)
                
                for user in users:
                    if user.get('deactivated'):
                        stats['deactivated_users'] += 1
                    else:
                        stats['active_users'] += 1
                    
                    if user.get('admin'):
                        stats['admin_users'] += 1
                    
                    if user.get('user_type') == 'guest':
                        stats['guest_users'] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user statistics: {str(e)}")
            return {}
    
    def get_room_statistics(self):
        """Get detailed room statistics"""
        try:
            stats = {
                'total_rooms': 0,
                'public_rooms': 0,
                'encrypted_rooms': 0,
                'federated_rooms': 0,
                'local_rooms': 0
            }
            
            # Get all rooms
            response = self.api_client.get('/v1/rooms', params={'limit': 1000})
            if response and response.status_code == 200:
                data = response.json()
                rooms = data.get('rooms', [])
                
                stats['total_rooms'] = len(rooms)
                
                for room in rooms:
                    if room.get('public'):
                        stats['public_rooms'] += 1
                    
                    if room.get('encrypted'):
                        stats['encrypted_rooms'] += 1
                    
                    if room.get('federatable'):
                        stats['federated_rooms'] += 1
                    else:
                        stats['local_rooms'] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting room statistics: {str(e)}")
            return {} 
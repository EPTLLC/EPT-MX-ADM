"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Media Management Blueprint
Telegram: https://t.me/EasyProTech

Media Management Blueprint for EPT-MX-ADM
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from modules.auth import AuthManager, admin_required
from modules.media import MediaManager
from modules.users import UserManager
from utils.logger import get_logger
from utils.i18n import t
import datetime

media_bp = Blueprint('media', __name__)

# Create managers
auth_manager = AuthManager()
logger = get_logger()


@media_bp.route('/users-media')
@admin_required
def users_media():
    """Users media list with statistics"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        # Search and pagination parameters
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 25))
        
        # Get users with media statistics
        users_data = media_manager.get_users_media_list(
            page=page,
            limit=limit,
            search_term=search if search else None
        )
        
        if not users_data:
            users_data = {'users': [], 'total': 0}
        
        # Get overall media statistics
        media_stats = media_manager.get_media_statistics()
        
        # Calculate pagination info
        total_users = users_data.get('total', 0)
        total_pages = (total_users + limit - 1) // limit if limit > 0 else 1
        
        return render_template('users_media.html', 
                             users=users_data.get('users', []),
                             media_stats=media_stats,
                             search=search,
                             current_page=page,
                             total_pages=total_pages,
                             limit=limit,
                             total=total_users)
    
    except Exception as e:
        logger.error(f"Users media loading error: {str(e)}")
        flash(t('media.error_load'), 'danger')
        return render_template('users_media.html', 
                             users=[],
                             media_stats={'total_media_files': 0, 'total_media_size_formatted': '0 B', 'users_with_media': 0},
                             current_page=1,
                             total_pages=1,
                             limit=25,
                             total=0,
                             search='')


@media_bp.route('/users/<user_id>/media')
@admin_required
def user_media(user_id):
    """Detailed media files for specific user"""
    try:
        logger.info(f"=== user_media called for {user_id} ===")
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        user_manager = UserManager(api_client)
        
        # Get user details
        logger.info(f"Getting user details...")
        user_details = user_manager.get_user_details(user_id)
        if not user_details:
            logger.error(f"User not found: {user_id}")
            flash(t('users.user_not_found'), 'danger')
            return redirect(url_for('media.users_media'))
        
        logger.info(f"User found: {user_details.get('name')}")
        
        # Get TOTAL media stats for this user from statistics API
        logger.info(f"Getting total media statistics...")
        total_media_count = 0
        total_media_size = 0
        total_media_size_formatted = '0 B'
        
        try:
            stats_response = api_client.get('/v1/statistics/users/media')
            if stats_response and stats_response.status_code == 200:
                stats_data = stats_response.json()
                users_media = stats_data.get('users', [])
                # Find this specific user
                for user_stats in users_media:
                    if user_stats.get('user_id') == user_id:
                        total_media_count = user_stats.get('media_count', 0)
                        total_media_size = user_stats.get('media_length', 0)
                        # Format size
                        total_media_size_formatted = media_manager._format_file_size(total_media_size)
                        break
                logger.info(f"Total stats: {total_media_count} files, {total_media_size_formatted}")
        except Exception as e:
            logger.error(f"Could not get total stats: {str(e)}")
        
        # Pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 25))
        logger.info(f"Pagination: page={page}, limit={limit}")
        
        # Get user media files for current page
        logger.info(f"Getting media files...")
        media_data = media_manager.get_user_media_detailed(user_id, limit=limit)
        logger.info(f"Media data: {media_data is not None}")
        
        if not media_data:
            logger.warning(f"No media data returned, using empty dict")
            media_data = {'media': [], 'total_count': 0, 'total_size': 0}
        
        # Override with correct total from statistics API
        media_data['total_count'] = total_media_count
        media_data['total_size'] = total_media_size
        media_data['total_size_formatted'] = total_media_size_formatted
        
        # Calculate size and count for current page
        page_files = media_data.get('media', [])
        page_count = len(page_files)
        page_size = sum(media.get('media_length', 0) for media in page_files)
        page_size_formatted = media_manager._format_file_size(page_size)
        
        media_data['files_on_page'] = page_count
        media_data['size_on_page'] = page_size
        media_data['size_on_page_formatted'] = page_size_formatted
        
        # Calculate pagination using correct total
        total = total_media_count
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        logger.info(f"Pagination calc: total={total}, total_pages={total_pages}")
        
        logger.info(f"Rendering template with current_page={page}")
        return render_template('user_media.html',
                             user_id=user_id,
                             user_display_name=user_details.get('displayname', ''),
                             media_data=media_data,
                             current_page=page,
                             total_pages=total_pages,
                             total=total,
                             limit=limit)
    
    except Exception as e:
        logger.error(f"User media error: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        flash(t('media.error_load'), 'danger')
        return redirect(url_for('media.users_media'))


@media_bp.route('/users-media/export')
@admin_required
def export_users_media():
    """Export users media statistics to CSV"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        # Get filter parameters from request
        filters = {
            'search': request.args.get('search', '')
        }
        
        csv_content = media_manager.export_users_media_csv(filters)
        
        if csv_content:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'users_media_export_{timestamp}.csv'
            
            return Response(
                csv_content,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
        else:
            flash(t('media.error_load'), 'danger')
            return redirect(url_for('media.users_media'))
    
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        flash(t('media.error_export'), 'danger')
        return redirect(url_for('media.users_media'))


@media_bp.route('/users/<user_id>/media/export')
@admin_required
def export_user_media(user_id):
    """Export specific user's media files to CSV"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        csv_content = media_manager.export_user_media_csv(user_id)
        
        if csv_content:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'user_{user_id}_media_export_{timestamp}.csv'
            
            return Response(
                csv_content,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
        else:
            flash(t('media.error_load'), 'danger')
            return redirect(url_for('media.user_media', user_id=user_id))
    
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        flash(t('media.error_export'), 'danger')
        return redirect(url_for('media.user_media', user_id=user_id))

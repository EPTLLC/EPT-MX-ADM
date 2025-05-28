"""
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
        from_token = request.args.get('from', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 25))
        
        # Get users with media statistics
        users_data = media_manager.get_users_media_list(
            from_token=from_token if from_token else None,
            limit=limit,
            search_term=search if search else None,
            page=page
        )
        
        if not users_data:
            users_data = {'users': [], 'total': 0}
        
        # Get overall media statistics
        media_stats = media_manager.get_media_statistics()
        
        # Calculate pagination info
        total_users = users_data.get('total', 0)
        total_pages = (total_users + limit - 1) // limit if limit > 0 else 1
        
        return render_template('users_media.html', 
                             users_data=users_data,
                             media_stats=media_stats,
                             search=search,
                             from_token=from_token,
                             current_page=page,
                             total_pages=total_pages,
                             limit=limit,
                             total=total_users,
                             total_users=len([u for u in users_data.get('users', []) if u.get('media_count', 0) > 0]))
    
    except Exception as e:
        logger.error(f"Users media loading error: {str(e)}")
        flash(t('media.error_load'), 'danger')
        return render_template('users_media.html', 
                             users_data={'users': [], 'total': 0},
                             media_stats={'total_media_files': 0, 'total_media_size_formatted': '0 B'},
                             current_page=1,
                             total_pages=1,
                             limit=25,
                             total=0,
                             search=search,
                             total_users=0)


@media_bp.route('/users/<user_id>/media')
@admin_required
def user_media(user_id):
    """Detailed media files for specific user"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        user_manager = UserManager(api_client)
        
        # Get user details
        user_details = user_manager.get_user_details(user_id)
        if not user_details:
            flash(t('users.user_not_found'), 'danger')
            return redirect(url_for('media.users_media'))
        
        # Pagination and filter parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 25))
        file_type = request.args.get('file_type', '')
        quarantine_status = request.args.get('quarantine', '')
        
        # Get user media files
        media_data = media_manager.get_user_media_detailed(
            user_id, 
            limit=limit
        )
        
        if not media_data:
            media_data = {'media': [], 'total_count': 0, 'total_size': 0}
        
        # Apply filters if specified
        if file_type or quarantine_status:
            filtered_media = []
            for media in media_data.get('media', []):
                # File type filter
                if file_type and media.get('file_type') != file_type:
                    continue
                
                # Quarantine filter
                if quarantine_status == 'quarantined' and not media.get('is_quarantined'):
                    continue
                elif quarantine_status == 'safe' and not media.get('is_safe_from_quarantine'):
                    continue
                elif quarantine_status == 'normal' and (media.get('is_quarantined') or media.get('is_safe_from_quarantine')):
                    continue
                
                filtered_media.append(media)
            
            media_data['media'] = filtered_media
        
        return render_template('user_media.html',
                             user_id=user_id,
                             user_display_name=user_details.get('displayname'),
                             media_data=media_data,
                             current_page=page,
                             limit=limit,
                             file_type=file_type,
                             quarantine_status=quarantine_status)
    
    except Exception as e:
        logger.error(f"User media loading error: {str(e)}")
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
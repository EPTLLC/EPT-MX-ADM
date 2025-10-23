"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Users Management Blueprint
Telegram: https://t.me/EasyProTech

Users Management Blueprint for EPT-MX-ADM
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from modules.auth import AuthManager, admin_required
from modules.users import UserManager
from utils.logger import get_logger
from utils.i18n import t
import datetime
from config.settings import Config

users_bp = Blueprint('users', __name__)

# Create managers
auth_manager = AuthManager()
logger = get_logger()


def _format_bytes(bytes_size):
    """Format bytes to human readable format"""
    try:
        bytes_size = int(bytes_size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"
    except:
        return '0 B'


def _protect_main_admin(user_id):
    main_admin_id = f"@admin:{Config.DOMAIN}"
    current_user_id = session.get('user_id')
    if user_id == main_admin_id and current_user_id != main_admin_id:
        flash(t('users.error_update') + ': Only the main admin can perform this action.', 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/users')
@admin_required
def users():
    """Users list with enhanced filtering and pagination"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        # Search and pagination parameters
        search = request.args.get('search', '')
        limit = request.args.get('limit', 10, type=int)  # Items per page
        page = request.args.get('page', 1, type=int)
        
        # Filter parameters
        show_guests = request.args.get('guests') == 'true'
        show_deactivated = request.args.get('deactivated') == 'true'
        
        # Calculate offset for Matrix API pagination (from token)
        # Matrix API uses 'from' as offset: page 1 = from 0, page 2 = from limit, page 3 = from limit*2, etc.
        from_offset = (page - 1) * limit
        
        # Get users list
        users_data = user_manager.get_users_list(
            from_token=str(from_offset) if from_offset > 0 else None,
            limit=limit,
            search_term=search if search else None,
            guests=show_guests if request.args.get('guests') else None,
            deactivated=show_deactivated if request.args.get('deactivated') else None
        )
        
        if not users_data:
            users_data = {'users': [], 'total': 0}
        
        # Скрываем главного админа для всех, кроме него самого
        main_admin_id = f"@admin:{Config.DOMAIN}"
        current_user_id = session.get('user_id')
        original_total = users_data.get('total', 0)  # Save original total BEFORE filtering
        
        if current_user_id != main_admin_id:
            # Filter out main admin from the current page
            users_data['users'] = [u for u in users_data['users'] if u.get('name') != main_admin_id]
            # Decrease total by 1 if main admin exists in the system
            if original_total > 0:
                users_data['total'] = original_total - 1
        
        # Get media statistics for all users
        users_media_map = {}
        try:
            media_response = api_client.get('/v1/statistics/users/media')
            if media_response and media_response.status_code == 200:
                media_data = media_response.json()
                users_media_list = media_data.get('users', [])
                # Create a map of user_id -> media stats
                for user_media in users_media_list:
                    user_id = user_media.get('user_id')
                    users_media_map[user_id] = {
                        'media_count': user_media.get('media_count', 0),
                        'media_length': user_media.get('media_length', 0)
                    }
        except Exception as e:
            logger.debug(f"Could not fetch media stats: {str(e)}")
        
        # Attach media info to each user
        for user in users_data.get('users', []):
            user_id = user.get('name')
            if user_id in users_media_map:
                user['media_count'] = users_media_map[user_id]['media_count']
                user['media_size'] = users_media_map[user_id]['media_length']
                user['media_size_human'] = _format_bytes(users_media_map[user_id]['media_length'])
            else:
                user['media_count'] = 0
                user['media_size'] = 0
                user['media_size_human'] = '0 B'
        
        # Calculate pagination info
        total_users = users_data.get('total', 0)
        total_pages = (total_users + limit - 1) // limit if limit > 0 else 1
        
        return render_template('users.html', 
                             users=users_data.get('users', []) if users_data else [],
                             total=total_users,
                             current_page=page,
                             total_pages=total_pages,
                             limit=limit,
                             next_token=users_data.get('next_token') if users_data else None,
                             search=search,
                             show_guests=show_guests,
                             show_deactivated=show_deactivated)
    
    except Exception as e:
        logger.error(f"Users loading error: {str(e)}")
        flash(t('users.error_load'), 'danger')
        return render_template('users.html', 
                             users=[], 
                             total=0, 
                             current_page=1,
                             total_pages=1,
                             limit=10,
                             next_token=None,
                             search='',
                             show_guests=False,
                             show_deactivated=False)


@users_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        try:
            api_client = auth_manager.get_api_client()
            user_manager = UserManager(api_client)
            
            # Get username from form and create proper user_id
            username = request.form.get('username')
            if not username or not username.strip():
                flash(t('users.error_create') + ': Username is required', 'danger')
                return render_template('create_user.html')
            username = username.strip()

            # Получаем домен из настроек
            domain = Config.get_domain()
            if not username.startswith('@'):
                user_id = f"@{username}:{domain}"
            else:
                # Если пользователь ввёл @user, но без домена
                if ':' not in username:
                    user_id = f"{username}:{domain}"
                else:
                    user_id = username
            # Проверка формата user_id
            if not user_id.startswith('@') or ':' not in user_id:
                flash(t('users.error_create') + ': Invalid user_id format', 'danger')
                return render_template('create_user.html')
            
            # Collect user data
            user_data = {
                'user_id': user_id,
                'password': request.form.get('password'),
                'displayname': request.form.get('displayname', ''),
                'admin': 'admin' in request.form,
                'created_by': session.get('username'),
                'creation_ts': int(datetime.datetime.now().timestamp() * 1000)
            }
            
            # Add email if specified
            email = request.form.get('email')
            if email:
                user_data['threepids'] = [{'medium': 'email', 'address': email}]
            
            # Create user
            result = user_manager.create_user(user_data)
            
            if result:
                flash(t('users.create_success', user_id=user_data["user_id"]), 'success')
                return redirect(url_for('users.users'))
            else:
                flash(t('users.error_create'), 'danger')
        
        except Exception as e:
            logger.error(f"User creation error: {str(e)}")
            flash(t('users.error_server'), 'danger')
    
    return render_template('create_user.html')


@users_bp.route('/users/<user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if request.method == 'POST':
            # Update user data
            user_data = {
                'updated_by': session.get('username')
            }
            
            # Add only changeable fields
            if request.form.get('password'):
                user_data['password'] = request.form.get('password')
            
            if request.form.get('displayname') is not None:
                user_data['displayname'] = request.form.get('displayname')
            
            user_data['admin'] = 'admin' in request.form
            
            # Update user
            result = user_manager.update_user(user_id, user_data)
            
            if result:
                flash(t('users.update_success', user_id=user_id), 'success')
                return redirect(url_for('users.users'))
            else:
                flash(t('users.error_update'), 'danger')
        
        # Get current user data
        user_details = user_manager.get_user_details(user_id)
        
        if not user_details:
            flash(t('users.user_not_found'), 'danger')
            return redirect(url_for('users.users'))
        
        return render_template('edit_user.html', user=user_details)
    
    except Exception as e:
        logger.error(f"User editing error: {str(e)}")
        flash(t('users.error_server'), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        erase = 'erase' in request.form
        
        if user_manager.deactivate_user(user_id, erase):
            action = t('users.deactivated_and_deleted') if erase else t('users.deactivated')
            flash(t('users.deactivate_success', user_id=user_id, action=action), 'success')
        else:
            flash(t('users.error_update'), 'danger')
    
    except Exception as e:
        logger.error(f"User deactivation error: {str(e)}")
        flash(t('users.error_server'), 'danger')
    
    return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Permanently delete user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.delete_user(user_id):
            flash(t('users.delete_success', user_id=user_id), 'success')
        else:
            flash(t('users.error_delete'), 'danger')
    
    except Exception as e:
        logger.error(f"User deletion error: {str(e)}")
        flash(t('users.error_server'), 'danger')
    
    return redirect(url_for('users.users'))


@users_bp.route('/users/export')
@admin_required
def export_users():
    """Export users to CSV"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        # Get filter parameters from request
        filters = {
            'search': request.args.get('search', ''),
            'guests': request.args.get('guests') == 'true' if request.args.get('guests') else None,
            'deactivated': request.args.get('deactivated') == 'true' if request.args.get('deactivated') else None
        }
        
        csv_content = user_manager.export_users_csv(filters)
        
        if csv_content:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'users_export_{timestamp}.csv'
            
            return Response(
                csv_content,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
        else:
            flash(t('users.error_load'), 'danger')
            return redirect(url_for('users.users'))
    
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        flash(t('users.error_server'), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/users/import', methods=['POST'])
@admin_required
def import_users():
    """Import users from CSV"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        # Check if file was uploaded
        if 'csv_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('users.users'))
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('users.users'))
        
        if not file.filename or not file.filename.lower().endswith('.csv'):
            flash('Please upload a CSV file', 'danger')
            return redirect(url_for('users.users'))
        
        # Process CSV import (implementation would be in UserManager)
        # result = user_manager.import_users_csv(file)
        
        flash('CSV import functionality needs implementation', 'info')
        return redirect(url_for('users.users'))
    
    except Exception as e:
        logger.error(f"CSV import error: {str(e)}")
        flash(t('users.error_server'), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/reactivate', methods=['POST'])
@admin_required
def reactivate_user(user_id):
    """Reactivate user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.reactivate_user(user_id):
            flash(f'User {user_id} reactivated successfully', 'success')
        else:
            flash('Failed to reactivate user', 'danger')
    
    except Exception as e:
        logger.error(f"User reactivation error: {str(e)}")
        flash('Server error during reactivation', 'danger')
    
    return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/reset_password', methods=['POST'])
@admin_required
def reset_password(user_id):
    """Reset user password"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        new_password = request.form.get('new_password')
        if not new_password:
            flash('New password is required', 'danger')
            return redirect(url_for('users.users'))
        
        if user_manager.reset_user_password(user_id, new_password):
            flash(f'Password reset for user {user_id}', 'success')
        else:
            flash('Failed to reset password', 'danger')
    
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        flash('Server error during password reset', 'danger')
    
    return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/rate_limit', methods=['POST'])
@admin_required
def configure_rate_limit(user_id):
    """Configure rate limits for user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        messages_per_second = request.form.get('messages_per_second', type=int)
        burst_count = request.form.get('burst_count', type=int)
        
        if user_manager.override_rate_limit(user_id, messages_per_second, burst_count):
            flash(f'Rate limit configured for user {user_id}', 'success')
        else:
            flash('Failed to configure rate limit', 'danger')
    
    except Exception as e:
        logger.error(f"Rate limit configuration error: {str(e)}")
        flash('Server error during rate limit configuration', 'danger')
    
    return redirect(url_for('users.users'))


@users_bp.route('/users/<user_id>/details')
@admin_required
def user_details(user_id):
    """Show detailed user information"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        # Get user details
        user_info = user_manager.get_user_details(user_id)
        if not user_info:
            flash('User not found', 'danger')
            return redirect(url_for('users.users'))
        
        # Get additional information
        user_sessions = user_manager.get_user_sessions(user_id)
        user_devices = user_manager.get_user_devices(user_id)
        user_rooms = user_manager.get_user_rooms(user_id)
        user_media = user_manager.get_user_media(user_id, limit=20)
        
        return render_template('user_details.html',
                             user=user_info,
                             sessions=user_sessions,
                             devices=user_devices,
                             rooms=user_rooms,
                             media=user_media)
    
    except Exception as e:
        logger.error(f"User details error: {str(e)}")
        flash('Error loading user details', 'danger')
        return redirect(url_for('users.users'))


# Route moved to media.py to avoid conflicts
# @users_bp.route('/users/<user_id>/media')


@users_bp.route('/users/<user_id>/media/<media_id>/delete', methods=['POST'])
@admin_required
def delete_user_media_item(user_id, media_id):
    """Delete specific user media item"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.delete_user_media(user_id, media_id):
            flash(f'Media item deleted for user {user_id}', 'success')
        else:
            flash('Failed to delete media item', 'danger')
    
    except Exception as e:
        logger.error(f"Media deletion error: {str(e)}")
        flash('Server error during media deletion', 'danger')
    
    return redirect(url_for('users.user_media', user_id=user_id))


@users_bp.route('/users/<user_id>/media/delete_all', methods=['POST'])
@admin_required
def delete_all_user_media(user_id):
    """Delete all user media"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.delete_user_media(user_id):
            flash(f'All media deleted for user {user_id}', 'success')
        else:
            flash('Failed to delete user media', 'danger')
    
    except Exception as e:
        logger.error(f"Media deletion error: {str(e)}")
        flash('Server error during media deletion', 'danger')
    
    return redirect(url_for('users.user_media', user_id=user_id))


@users_bp.route('/users/<user_id>/login_as', methods=['POST'])
@admin_required
def login_as_user(user_id):
    """Get access token on behalf of user"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        token_data = user_manager.login_as_user(user_id)
        
        if token_data:
            # Show token in a modal or separate page
            flash(f'Access token generated for user {user_id}', 'success')
            # You might want to render a template with the token
            return render_template('user_token.html', user_id=user_id, token_data=token_data)
        else:
            flash('Failed to generate access token', 'danger')
    
    except Exception as e:
        logger.error(f"Login as user error: {str(e)}")
        flash('Server error during token generation', 'danger')
    
    return redirect(url_for('users.users'))


# AJAX API endpoints for modal operations
@users_bp.route('/api/users/<user_id>/media')
@admin_required
def api_user_media(user_id):
    """API endpoint for user media (for modal)"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        limit = request.args.get('limit', 10, type=int)
        media_data = user_manager.get_user_media(user_id, limit=limit)
        
        if not media_data:
            media_data = {'media': [], 'total': 0}
        
        return {
            'success': True,
            'media_data': media_data
        }
    
    except Exception as e:
        logger.error(f"API user media error: {str(e)}")
        return {'success': False, 'error': str(e)}


@users_bp.route('/api/users/<user_id>/reset_password', methods=['POST'])
@admin_required
def api_reset_password(user_id):
    """API endpoint for password reset (for modal)"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        new_password = request.form.get('new_password')
        if not new_password:
            return {'success': False, 'error': 'New password is required'}
        
        if user_manager.reset_user_password(user_id, new_password):
            return {'success': True, 'message': f'Password reset for user {user_id}'}
        else:
            return {'success': False, 'error': 'Failed to reset password'}
    
    except Exception as e:
        logger.error(f"API password reset error: {str(e)}")
        return {'success': False, 'error': str(e)}


@users_bp.route('/api/users/<user_id>/rate_limit', methods=['POST'])
@admin_required
def api_configure_rate_limit(user_id):
    """API endpoint for rate limit configuration (for modal)"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        messages_per_second = request.form.get('messages_per_second', type=int)
        burst_count = request.form.get('burst_count', type=int)
        
        if user_manager.override_rate_limit(user_id, messages_per_second, burst_count):
            return {'success': True, 'message': f'Rate limit configured for user {user_id}'}
        else:
            return {'success': False, 'error': 'Failed to configure rate limit'}
    
    except Exception as e:
        logger.error(f"API rate limit configuration error: {str(e)}")
        return {'success': False, 'error': str(e)}


@users_bp.route('/api/users/<user_id>/login_as', methods=['POST'])
@admin_required
def api_login_as_user(user_id):
    """API endpoint for login as user (for modal)"""
    protect = _protect_main_admin(user_id)
    if protect: return protect
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        token_data = user_manager.login_as_user(user_id)
        
        if token_data:
            return {'success': True, 'token_data': token_data, 'message': f'Access token generated for user {user_id}'}
        else:
            return {'success': False, 'error': 'Failed to generate access token'}
    
    except Exception as e:
        logger.error(f"API login as user error: {str(e)}")
        return {'success': False, 'error': str(e)} 
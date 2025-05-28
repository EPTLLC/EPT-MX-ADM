"""
API Blueprint for EPT-MX-ADM
All JSON API endpoints (no system metrics)
"""

from flask import Blueprint, jsonify, request
from modules.auth import AuthManager, admin_required
from modules.users import UserManager
from modules.rooms import RoomManager
from modules.spaces import SpaceManager
from modules.media import MediaManager
from utils.logger import get_logger
from utils.i18n import t

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Create managers
auth_manager = AuthManager()
logger = get_logger()


# ==================== USER API ====================

@api_bp.route('/users/<user_id>/whois')
@admin_required
def api_user_whois(user_id):
    """API for getting user activity details (whois)"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        whois_data = user_manager.get_user_sessions(user_id)
        
        if whois_data:
            return jsonify({'success': True, 'whois': whois_data})
        else:
            return jsonify({'success': False, 'error': t('users.error_load')})
    
    except Exception as e:
        logger.error(f"User whois error: {str(e)}")
        return jsonify({'success': False, 'error': t('users.error_server')})


@api_bp.route('/users/<user_id>/devices')
@admin_required
def api_user_devices(user_id):
    """API for getting user devices"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        devices_data = user_manager.get_user_devices(user_id)
        
        if devices_data:
            return jsonify({'success': True, 'devices': devices_data})
        else:
            return jsonify({'success': False, 'error': t('users.error_load')})
    
    except Exception as e:
        logger.error(f"User devices error: {str(e)}")
        return jsonify({'success': False, 'error': t('users.error_server')})


@api_bp.route('/users/<user_id>/devices/<device_id>', methods=['DELETE'])
@admin_required
def api_delete_user_device(user_id, device_id):
    """API for deleting user device"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.delete_user_device(user_id, device_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('users.error_update')})
    
    except Exception as e:
        logger.error(f"Device deletion error: {str(e)}")
        return jsonify({'success': False, 'error': t('users.error_server')})


@api_bp.route('/users/<user_id>/delete', methods=['POST'])
@admin_required
def api_delete_user(user_id):
    """API for permanently deleting user"""
    try:
        api_client = auth_manager.get_api_client()
        user_manager = UserManager(api_client)
        
        if user_manager.delete_user(user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('users.error_delete')})
    
    except Exception as e:
        logger.error(f"User deletion error: {str(e)}")
        return jsonify({'success': False, 'error': t('users.error_server')})


# ==================== ROOM API ====================

@api_bp.route('/rooms/<room_id>/details')
@admin_required
def api_room_details(room_id):
    """API for getting room details"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        room_data = room_manager.get_room_details(room_id)
        
        if room_data:
            return jsonify({'success': True, 'room': room_data})
        else:
            return jsonify({'success': False, 'error': 'Room not found'})
    
    except Exception as e:
        logger.error(f"Room details error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error loading room details'})


@api_bp.route('/rooms/<room_id>/members')
@admin_required
def api_room_members(room_id):
    """API for getting room members"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        members = room_manager.get_room_members(room_id)
        
        return jsonify({'success': True, 'members': members})
    
    except Exception as e:
        logger.error(f"Room members error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error loading room members'})


@api_bp.route('/rooms/<room_id>/state_events')
@admin_required
def api_room_state_events(room_id):
    """API for getting room state events"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        events = room_manager.get_room_state_events(room_id)
        
        return jsonify({'success': True, 'events': events})
    
    except Exception as e:
        logger.error(f"Room state events error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error loading state events'})


@api_bp.route('/rooms/<room_id>/block', methods=['POST'])
@admin_required
def api_block_room(room_id):
    """API for blocking room"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        if room_manager.block_room(room_id, True):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('errors.error_room_block')})
    
    except Exception as e:
        logger.error(f"Room blocking error: {str(e)}")
        return jsonify({'success': False, 'error': t('errors.error_room_block')})


@api_bp.route('/rooms/<room_id>/delete', methods=['POST'])
@admin_required
def api_delete_room(room_id):
    """API for deleting room"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        data = request.get_json() or {}
        purge = data.get('purge', False)
        
        result = room_manager.delete_room(room_id, purge=purge)
        
        if result:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('errors.error_room_delete')})
    
    except Exception as e:
        logger.error(f"Room deletion error: {str(e)}")
        return jsonify({'success': False, 'error': t('errors.error_room_delete')})


# ==================== SPACE API ====================

@api_bp.route('/spaces/<space_id>/details')
@admin_required
def api_space_details(space_id):
    """API for getting space details"""
    try:
        api_client = auth_manager.get_api_client()
        space_manager = SpaceManager(api_client)
        
        space_data = space_manager.get_space_details(space_id)
        
        if space_data:
            return jsonify({'success': True, 'space': space_data})
        else:
            return jsonify({'success': False, 'error': t('errors.space_not_found')})
    
    except Exception as e:
        logger.error(f"Space details error: {str(e)}")
        return jsonify({'success': False, 'error': t('errors.error_space_details')})


@api_bp.route('/spaces/<space_id>/hierarchy')
@admin_required
def api_space_hierarchy(space_id):
    """API for getting space hierarchy"""
    try:
        api_client = auth_manager.get_api_client()
        space_manager = SpaceManager(api_client)
        
        hierarchy = space_manager.get_space_hierarchy(space_id)
        
        if hierarchy:
            return jsonify({'success': True, 'hierarchy': hierarchy})
        else:
            return jsonify({'success': False, 'error': t('errors.error_space_hierarchy')})
    
    except Exception as e:
        logger.error(f"Space hierarchy error: {str(e)}")
        return jsonify({'success': False, 'error': t('errors.error_space_hierarchy')})


# ==================== MEDIA API ====================

@api_bp.route('/users/<user_id>/media/<media_id>/quarantine', methods=['POST'])
@admin_required
def api_quarantine_media(user_id, media_id):
    """API for quarantining media file"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        if media_manager.quarantine_media(media_id, user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('media.error_quarantine')})
    
    except Exception as e:
        logger.error(f"Media quarantine error: {str(e)}")
        return jsonify({'success': False, 'error': t('media.error_quarantine')})


@api_bp.route('/users/<user_id>/media/<media_id>/unquarantine', methods=['POST'])
@admin_required
def api_unquarantine_media(user_id, media_id):
    """API for marking media as safe from quarantine"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        if media_manager.unquarantine_media(media_id, user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('media.error_unquarantine')})
    
    except Exception as e:
        logger.error(f"Media unquarantine error: {str(e)}")
        return jsonify({'success': False, 'error': t('media.error_unquarantine')})


@api_bp.route('/users/<user_id>/media/<media_id>', methods=['DELETE'])
@admin_required
def api_delete_media(user_id, media_id):
    """API for deleting media file"""
    try:
        api_client = auth_manager.get_api_client()
        media_manager = MediaManager(api_client)
        
        result = media_manager.delete_media(media_id, user_id)
        
        if result:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': t('media.error_delete_media')})
    
    except Exception as e:
        logger.error(f"Media deletion error: {str(e)}")
        return jsonify({'success': False, 'error': t('media.error_delete_media')}) 
"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Rooms Management Blueprint
Telegram: https://t.me/EasyProTech

Rooms Management Blueprint for EPT-MX-ADM
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from modules.auth import AuthManager, admin_required
from modules.rooms import RoomManager
from utils.logger import get_logger
from utils.i18n import t
from config.settings import Config
import datetime

rooms_bp = Blueprint('rooms', __name__)

# Create managers
auth_manager = AuthManager()
logger = get_logger()


@rooms_bp.route('/rooms')
@admin_required
def rooms():
    """Rooms list with filtering and pagination"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        # Search and pagination parameters
        search = request.args.get('search', '')
        limit = request.args.get('limit', 25, type=int)
        page = request.args.get('page', 1, type=int)
        
        # Calculate offset for Matrix API pagination
        from_offset = (page - 1) * limit
        
        # Get rooms list
        rooms_data = room_manager.get_rooms_list(
            from_token=str(from_offset) if from_offset > 0 else None,
            limit=limit,
            search_term=search if search else None
        )
        
        if not rooms_data:
            rooms_data = {'rooms': [], 'total_rooms': 0}
        
        total = rooms_data.get('total_rooms') or rooms_data.get('total') or 0
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return render_template('rooms.html', 
                             rooms_data=rooms_data,
                             search=search,
                             current_page=page,
                             limit=limit,
                             total=total,
                             total_pages=total_pages)
    
    except Exception as e:
        logger.error(f"Rooms loading error: {str(e)}")
        flash(t('rooms.error_load'), 'danger')
        return render_template('rooms.html', 
                             rooms_data={'rooms': [], 'total_rooms': 0},
                             total_pages=1,
                             current_page=1,
                             total=0)


@rooms_bp.route('/rooms/export')
@admin_required
def export_rooms():
    """Export rooms to CSV"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        filters = {
            'search': request.args.get('search', '')
        }
        
        csv_content = room_manager.export_rooms_csv(filters)
        
        if csv_content:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'rooms_export_{timestamp}.csv'
            
            return Response(
                csv_content,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
        else:
            flash(t('rooms.error_load'), 'danger')
            return redirect(url_for('rooms.rooms'))
    
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        flash(t('rooms.error_export'), 'danger')
        return redirect(url_for('rooms.rooms'))


@rooms_bp.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_room(room_id):
    """Edit room settings"""
    try:
        api_client = auth_manager.get_api_client()
        room_manager = RoomManager(api_client)
        
        if request.method == 'POST':
            # Handle room updates
            room_data = {
                'name': request.form.get('name'),
                'topic': request.form.get('topic'),
                'public': 'public' in request.form,
                'encrypted': 'encrypted' in request.form
            }
            
            # Update room via API (this would need implementation in RoomManager)
            # For now, just redirect back
            flash(t('rooms.update_success'), 'success')
            return redirect(url_for('rooms.rooms'))
        
        # Get room details for editing
        room_details = room_manager.get_room_details(room_id)
        
        if not room_details:
            flash(t('errors.room_not_found'), 'danger')
            return redirect(url_for('rooms.rooms'))
        
        return render_template('edit_room.html', room=room_details)
    
    except Exception as e:
        logger.error(f"Room editing error: {str(e)}")
        flash(t('errors.error_room_details'), 'danger')
        return redirect(url_for('rooms.rooms')) 
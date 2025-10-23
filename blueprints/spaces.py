"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Spaces Management Blueprint
Telegram: https://t.me/EasyProTech

Spaces Management Blueprint for EPT-MX-ADM
"""

from flask import Blueprint, render_template, request, flash
from modules.auth import AuthManager, admin_required
from modules.spaces import SpaceManager
from utils.logger import get_logger
from utils.i18n import t

spaces_bp = Blueprint('spaces', __name__)

# Create managers
auth_manager = AuthManager()
logger = get_logger()


@spaces_bp.route('/spaces')
@admin_required
def spaces():
    """Spaces list with pagination"""
    try:
        api_client = auth_manager.get_api_client()
        space_manager = SpaceManager(api_client)
        
        # Search and pagination parameters
        search = request.args.get('search', '')
        limit = request.args.get('limit', 25, type=int)
        page = request.args.get('page', 1, type=int)
        
        # Calculate offset for Matrix API pagination
        from_offset = (page - 1) * limit
        
        # Get spaces list
        spaces_data = space_manager.get_spaces_list(
            from_token=str(from_offset) if from_offset > 0 else None,
            limit=limit,
            search_term=search if search else None
        )
        
        if not spaces_data:
            spaces_data = {'rooms': [], 'total_spaces': 0}
        
        # Ensure 'rooms' and 'total_spaces' for template compatibility
        rooms = spaces_data.get('rooms') or spaces_data.get('spaces') or []
        total_spaces = spaces_data.get('total_spaces') or spaces_data.get('total') or len(rooms)
        spaces_data['rooms'] = rooms
        spaces_data['total_spaces'] = total_spaces
        
        # Calculate pagination info
        total = total_spaces
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return render_template('spaces.html', 
                             spaces_data=spaces_data,
                             search=search,
                             current_page=page,
                             limit=limit,
                             total=total,
                             total_pages=total_pages)
    
    except Exception as e:
        logger.error(f"Spaces loading error: {str(e)}")
        flash(t('spaces.error_load'), 'danger')
        return render_template('spaces.html', 
                             spaces_data={'rooms': [], 'total_spaces': 0},
                             search='',
                             current_page=1,
                             limit=25,
                             total=0,
                             total_pages=1) 
"""
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
    """Spaces list"""
    try:
        api_client = auth_manager.get_api_client()
        space_manager = SpaceManager(api_client)
        
        # Search and pagination parameters
        search = request.args.get('search', '')
        from_token = request.args.get('from', '')
        
        # Get spaces list
        spaces_data = space_manager.get_spaces_list()
        
        if not spaces_data:
            spaces_data = {'rooms': [], 'total_spaces': 0}
        # --- PATCH: provide 'rooms' and 'total_spaces' for template compatibility ---
        rooms = spaces_data.get('rooms') or spaces_data.get('spaces') or []
        total_spaces = spaces_data.get('total_spaces') or len(rooms)
        spaces_data['rooms'] = rooms
        spaces_data['total_spaces'] = total_spaces
        
        return render_template('spaces.html', 
                             spaces_data=spaces_data,
                             search=search,
                             from_token=from_token)
    
    except Exception as e:
        logger.error(f"Spaces loading error: {str(e)}")
        flash(t('spaces.error_load'), 'danger')
        return render_template('spaces.html', spaces_data={'rooms': [], 'total_spaces': 0}) 
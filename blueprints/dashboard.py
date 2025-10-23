"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Dashboard Blueprint
Telegram: https://t.me/EasyProTech

Dashboard Blueprint for EPT-MX-ADM
Only Matrix-specific metrics, no system metrics
"""

from flask import Blueprint, render_template, jsonify, flash
from modules.auth import AuthManager, login_required
from modules.analytics import AnalyticsManager
from utils.logger import get_logger
from utils.i18n import t

dashboard_bp = Blueprint('dashboard', __name__)

# Create managers
auth_manager = AuthManager()
logger = get_logger()


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Main panel with Matrix statistics only"""
    try:
        # Get API client
        api_client = auth_manager.get_api_client()
        
        # Create analytics manager
        analytics = AnalyticsManager(api_client)
        
        # Get Matrix statistics only
        stats = analytics.get_dashboard_stats()
        performance = analytics.get_server_performance()
        health = analytics.get_system_health()
        
        return render_template('dashboard.html', 
                             stats=stats,
                             performance=performance,
                             health=health)
    
    except Exception as e:
        logger.error(f"Dashboard loading error: {str(e)}")
        flash(t('dashboard.error_loading'), 'danger')
        return render_template('dashboard.html', 
                             stats={}, performance={}, health={})


@dashboard_bp.route('/api/dashboard/refresh')
@login_required
def api_dashboard_refresh():
    """API for dashboard statistics refresh - Matrix only"""
    try:
        api_client = auth_manager.get_api_client()
        analytics = AnalyticsManager(api_client)
        
        stats = analytics.get_dashboard_stats()
        performance = analytics.get_server_performance()
        health = analytics.get_system_health()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'performance': performance,
            'health': health
        })
    
    except Exception as e:
        logger.error(f"Dashboard refresh error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
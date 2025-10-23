"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Authentication Blueprint
Telegram: https://t.me/EasyProTech

Authentication Blueprint for EPT-MX-ADM
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.auth import AuthManager
from utils.i18n import get_i18n, t

auth_bp = Blueprint('auth', __name__)

# Create authorization manager
auth_manager = AuthManager()
i18n = get_i18n()


@auth_bp.route('/')
def index():
    """Main page - redirect to dashboard or login"""
    if auth_manager.is_authenticated():
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authorization page"""
    if auth_manager.is_authenticated():
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        matrix_server = request.form.get('matrix_server')
        
        if auth_manager.login_user(username, password, matrix_server):
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard.dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Logout"""
    auth_manager.logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/set_locale/<locale>')
def set_locale(locale):
    """Set language"""
    if i18n.set_locale(locale):
        flash(t('settings.language_changed'), 'success')
    else:
        flash(t('messages.error'), 'danger')
    
    # Return to previous page, or login if not authenticated
    if auth_manager.is_authenticated():
        return redirect(request.referrer or url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('auth.login')) 
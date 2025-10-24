"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Authentication Module
Telegram: https://t.me/EasyProTech

Authentication module for EPT-MX-ADM
Compact and modular authentication system
"""

from flask import session, request, redirect, url_for, flash
from functools import wraps
import requests
import json
import os
from config.settings import Config
from utils.logger import get_logger
from utils.i18n import t

# SSL verification control
# Set EPT_DISABLE_SSL_VERIFY=true ONLY for development with self-signed certificates
# NEVER disable in production!
SSL_VERIFY = os.environ.get('EPT_DISABLE_SSL_VERIFY', 'false').lower() != 'true'
CA_BUNDLE = os.environ.get('EPT_CA_BUNDLE', None)

if CA_BUNDLE:
    SSL_VERIFY = CA_BUNDLE
    
if not SSL_VERIFY:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger()

if not SSL_VERIFY:
    logger.warning("⚠️  SSL VERIFICATION DISABLED - This is insecure and should only be used in development!")
    logger.warning("⚠️  Set EPT_DISABLE_SSL_VERIFY=false or provide EPT_CA_BUNDLE for production")


class AuthManager:
    """Compact authentication manager"""
    
    def __init__(self):
        self.api_client = None
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return 'access_token' in session and 'username' in session
    
    def get_current_user(self):
        """Get current user info"""
        if self.is_authenticated():
            return {
                'username': session.get('username'),
                'is_admin': session.get('is_admin', False),
                'user_id': session.get('user_id')
            }
        return None
    
    def login_user(self, username, password, matrix_server=None):
        """Login user with username and password"""
        try:
            # Use provided server or default from config
            server_input = matrix_server or Config.SYNAPSE_URL
            
            # Smart server URL formatting
            # If no protocol specified, add https://
            if not server_input.startswith(('http://', 'https://')):
                server_url = f'https://{server_input}'
            else:
                server_url = server_input
            
            # Remove trailing slash if present
            server_url = server_url.rstrip('/')
            
            # Smart username formatting
            # If username doesn't contain @, format it as @username:domain
            if not username.startswith('@'):
                # Extract domain from server URL
                from urllib.parse import urlparse
                parsed = urlparse(server_url)
                domain = parsed.netloc
                user_id = f'@{username}:{domain}'
            else:
                user_id = username
            
            # Prepare login data
            login_data = {
                'type': 'm.login.password',
                'user': user_id,
                'password': password
            }
            
            # Make login request with SSL verification
            response = requests.post(
                f"{server_url}/_matrix/client/r0/login",
                json=login_data,
                timeout=10,
                verify=SSL_VERIFY
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Store session data including the server URL
                session['access_token'] = data.get('access_token')
                session['username'] = username
                session['user_id'] = data.get('user_id')
                session['device_id'] = data.get('device_id')
                session['matrix_server'] = server_url  # Save server URL
                
                # Check admin status
                self._check_admin_status(user_id, server_url)
                
                logger.info(f"User {user_id} logged in successfully to {server_url}")
                return True
            else:
                logger.warning(f"Login failed for {user_id}: {response.status_code}")
                flash(t('auth.invalid_credentials'), 'danger')
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash(f'Connection error: {str(e)}', 'danger')
            return False
    
    def logout_user(self):
        """Logout current user"""
        username = session.get('username')
        session.clear()
        if username:
            logger.info(f"User {username} logged out")
    
    def _check_admin_status(self, username, server_url=None):
        """Check if user is admin via Matrix API"""
        try:
            user_id = session.get('user_id')
            access_token = session.get('access_token')
            server = server_url or session.get('matrix_server') or Config.SYNAPSE_URL
            
            if not user_id or not access_token:
                session['is_admin'] = False
                return
            
            # Check admin status via Matrix API
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f"{server}/_synapse/admin/v1/users/{user_id}/admin",
                headers=headers,
                timeout=10,
                verify=SSL_VERIFY  # Disable SSL verification
            )
            
            if response.status_code == 200:
                admin_data = response.json()
                session['is_admin'] = admin_data.get('admin', False)
                logger.info(f"User {username} admin status: {session['is_admin']}")
            else:
                logger.warning(f"Failed to check admin status for {username}: {response.status_code}")
                session['is_admin'] = False
                
        except Exception as e:
            logger.error(f"Admin check error: {str(e)}")
            session['is_admin'] = False
    
    def get_api_client(self):
        """Get API client for authenticated requests"""
        if not self.is_authenticated():
            return None
        
        if not self.api_client:
            self.api_client = SynapseAPIClient(session.get('access_token'))
        
        return self.api_client


class SynapseAPIClient:
    """Simple Synapse API client"""
    
    def __init__(self, access_token, server_url=None):
        self.access_token = access_token
        self.base_url = server_url or session.get('matrix_server') or Config.SYNAPSE_URL
        self.admin_url = f"{self.base_url}/_synapse/admin"
    
    def get(self, endpoint, params=None):
        """Make GET request to Synapse API"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=SSL_VERIFY)
            return response
        except Exception as e:
            logger.error(f"API GET error: {str(e)}")
            return None
    
    def post(self, endpoint, data=None):
        """Make POST request to Synapse API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10, verify=SSL_VERIFY)
            return response
        except Exception as e:
            logger.error(f"API POST error: {str(e)}")
            return None
    
    def put(self, endpoint, data=None):
        """Make PUT request to Synapse API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.put(url, headers=headers, json=data, timeout=10, verify=SSL_VERIFY)
            return response
        except Exception as e:
            logger.error(f"API PUT error: {str(e)}")
            return None
    
    def delete(self, endpoint, json=None, **kwargs):
        """Make DELETE request to Synapse API"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        if json:
            headers['Content-Type'] = 'application/json'
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.delete(url, headers=headers, json=json, timeout=10, verify=SSL_VERIFY, **kwargs)
            return response
        except Exception as e:
            logger.error(f"API DELETE error: {str(e)}")
            return None


def login_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_manager = AuthManager()
        if not auth_manager.is_authenticated():
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator for routes that require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_manager = AuthManager()
        if not auth_manager.is_authenticated():
            return redirect(url_for('auth.login', next=request.url))
        
        current_user = auth_manager.get_current_user()
        if not current_user or not current_user.get('is_admin'):
            flash(t('auth.admin_required'), 'danger')
            return redirect(url_for('dashboard.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function 
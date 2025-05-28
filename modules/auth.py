"""
Authentication module for EPT-MX-ADM
Compact and modular authentication system
"""

from flask import session, request, redirect, url_for, flash
from functools import wraps
import requests
import json
from config.settings import Config
from utils.logger import get_logger
from utils.i18n import t

logger = get_logger()


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
    
    def login_user(self, username, password):
        """Login user with username and password"""
        try:
            # Prepare login data
            login_data = {
                'type': 'm.login.password',
                'user': username,
                'password': password
            }
            
            # Make login request
            response = requests.post(
                f"{Config.SYNAPSE_URL}/_matrix/client/r0/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Store session data
                session['access_token'] = data.get('access_token')
                session['username'] = username
                session['user_id'] = data.get('user_id')
                session['device_id'] = data.get('device_id')
                
                # Check admin status
                self._check_admin_status(username)
                
                logger.info(f"User {username} logged in successfully")
                return True
            else:
                logger.warning(f"Login failed for {username}: {response.status_code}")
                flash(t('auth.invalid_credentials'), 'danger')
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash(t('auth.login_error'), 'danger')
            return False
    
    def logout_user(self):
        """Logout current user"""
        username = session.get('username')
        session.clear()
        if username:
            logger.info(f"User {username} logged out")
    
    def _check_admin_status(self, username):
        """Check if user is admin"""
        try:
            # Simple admin check - you can enhance this
            session['is_admin'] = username in Config.ADMIN_USERS if hasattr(Config, 'ADMIN_USERS') else True
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
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = Config.SYNAPSE_URL
        self.admin_url = f"{self.base_url}/_synapse/admin"
    
    def get(self, endpoint, params=None):
        """Make GET request to Synapse API"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
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
            response = requests.post(url, headers=headers, json=data, timeout=10)
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
            response = requests.put(url, headers=headers, json=data, timeout=10)
            return response
        except Exception as e:
            logger.error(f"API PUT error: {str(e)}")
            return None
    
    def delete(self, endpoint):
        """Make DELETE request to Synapse API"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.admin_url}{endpoint}"
        
        try:
            response = requests.delete(url, headers=headers, timeout=10)
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
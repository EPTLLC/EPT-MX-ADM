"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Matrix API Client
Telegram: https://t.me/EasyProTech

API client for working with Matrix Synapse
"""
import requests
import time
from config.settings import Config
from utils.logger import get_logger, log_api_request

class MatrixAPIClient:
    """Client for working with Matrix Synapse API"""
    
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.user_id = None
        self.session = requests.Session()
        self.logger = get_logger()
        
        # Configure session
        self.session.timeout = Config.API_TIMEOUT
        
    def _make_request(self, method, endpoint, **kwargs):
        """Base method for making API requests"""
        
        url = f"{Config.get_full_synapse_url()}{endpoint}"
        
        # Add authorization if token is present
        if self.access_token:
            headers = kwargs.get('headers', {})
            headers['Authorization'] = f'Bearer {self.access_token}'
            kwargs['headers'] = headers
        
        start_time = time.time()
        
        try:
            # Make the request
            response = self.session.request(method, url, **kwargs)
            response_time = time.time() - start_time
            
            # Log the request
            log_api_request(method, endpoint, response.status_code, response_time)
            
            # Check status
            if response.status_code >= 400:
                self.logger.error(f"API Error {response.status_code}: {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            self.logger.error(f"API Request failed: {str(e)}")
            log_api_request(method, endpoint, 'ERROR', response_time)
            raise
    
    def get(self, endpoint, **kwargs):
        """GET request"""
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        """POST request"""
        return self._make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint, **kwargs):
        """PUT request"""
        return self._make_request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """DELETE request"""
        return self._make_request('DELETE', endpoint, **kwargs)
    
    def login(self, username, password):
        """Login via Matrix Client API"""
        
        login_url = f"{Config.get_client_api_url()}/v3/login"
        
        data = {
            "type": "m.login.password",
            "user": username,
            "password": password
        }
        
        response = requests.post(login_url, json=data, timeout=Config.API_TIMEOUT)
        
        if response.status_code == 200:
            login_data = response.json()
            self.access_token = login_data['access_token']
            self.user_id = login_data.get('user_id', username)
            self.logger.info(f"Successful login for user {username}")
            return login_data
        else:
            self.logger.error(f"Login error for {username}: {response.status_code}")
            return None
    
    def check_admin_rights(self, user_id):
        """Check admin rights"""
        
        response = self.get(f"/v1/users/{user_id}/admin")
        
        if response.status_code == 200:
            return response.json().get('admin', False)
        
        return False
    
    def get_server_version(self):
        """Get server version"""
        
        response = self.get("/v1/server_version")
        
        if response.status_code == 200:
            return response.json()
        
        return None 
    
    def is_admin(self):
        """Check if current user is admin"""
        if not self.user_id:
            return False
        return self.check_admin_rights(self.user_id) 
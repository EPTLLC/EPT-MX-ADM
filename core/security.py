# Project: EPT-MX-ADM
# Company: EasyProTech LLC (www.easypro.tech)
# Dev: Brabus
# Date: Fri 24 Oct 2025 UTC
# Status: Created
# Telegram: https://t.me/EasyProTech

"""
Security middleware for EPT-MX-ADM
Handles security headers, CSRF protection (basic), and request validation
"""

from functools import wraps
from flask import request, session, abort

# Note: Logger will be initialized when first called to avoid circular imports
_logger = None


def get_logger():
    """Lazy logger initialization"""
    global _logger
    if _logger is None:
        from utils.logger import get_logger as _get_logger
        _logger = _get_logger()
    return _logger


def require_auth(f):
    """
    Decorator to require authentication for routes
    Usage: @require_auth
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or 'access_token' not in session:
            get_logger().warning(f"Unauthorized access attempt to {request.endpoint}")
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """
    Decorator to require admin privileges
    Usage: @require_admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or 'access_token' not in session:
            get_logger().warning(f"Unauthorized access attempt to {request.endpoint}")
            abort(401)
        
        # Check if user has admin flag
        if not session.get('is_admin', False):
            get_logger().warning(
                f"Non-admin user {session.get('user')} attempted to access {request.endpoint}"
            )
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def add_security_headers(response):
    """
    Add security headers to all responses
    Called automatically by Flask after_request hook
    """
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS filter in browser
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Strict Transport Security (only if HTTPS)
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response


def sanitize_input(data):
    """
    Basic input sanitization
    Prevents XSS by escaping HTML characters
    """
    if isinstance(data, str):
        # Replace dangerous characters in correct order
        data = data.replace('&', '&amp;')  # Must be first!
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace('"', '&quot;')
        data = data.replace("'", '&#x27;')
    return data


def validate_matrix_id(matrix_id):
    """
    Validate Matrix ID format
    Must be @username:domain
    """
    if not isinstance(matrix_id, str):
        return False
    
    if not matrix_id.startswith('@'):
        return False
    
    if ':' not in matrix_id:
        return False
    
    parts = matrix_id.split(':')
    if len(parts) != 2:
        return False
    
    username = parts[0][1:]  # Remove @
    domain = parts[1]
    
    if not username or not domain:
        return False
    
    # Basic validation
    if len(username) < 1 or len(username) > 255:
        return False
    
    if len(domain) < 1 or len(domain) > 255:
        return False
    
    return True


def log_admin_action(action, user, details=None):
    """
    Log administrative actions for audit trail
    """
    log_entry = {
        'action': action,
        'user': user,
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string,
        'timestamp': None,  # Will be added by logger
    }
    
    if details:
        log_entry['details'] = details
    
    get_logger().info(f"ADMIN_ACTION: {log_entry}")


def rate_limit_check(key, max_requests=10, window=60):
    """
    Basic rate limiting check
    
    Args:
        key: Identifier for rate limit (e.g., IP address, user ID)
        max_requests: Maximum requests allowed
        window: Time window in seconds
    
    Returns:
        bool: True if within rate limit, False if exceeded
    
    Note: This is a basic implementation. For production, use Redis or similar.
    """
    # TODO: Implement with Redis for production
    # For now, always return True (no rate limiting)
    return True


def check_csrf_token():
    """
    Basic CSRF protection
    
    Note: This is a simplified implementation.
    For production, use Flask-WTF or similar library.
    """
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        session_token = session.get('csrf_token')
        
        if not token or not session_token or token != session_token:
            get_logger().warning(f"CSRF token mismatch from {request.remote_addr}")
            # For now, just log warning - don't block
            # TODO: Enable blocking in v1.1.0
            pass
    
    return True


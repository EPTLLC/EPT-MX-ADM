"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Logging System
Telegram: https://t.me/EasyProTech

Logging system for EPT-MX-ADM
"""
import logging
import sys
from config.settings import Config

def setup_logger():
    """Configure logger for the application"""
    
    # Create logger
    logger = logging.getLogger('ept_mx_adm')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Clear old handlers
    logger.handlers = []
    
    # Formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger():
    """Get configured logger"""
    return logging.getLogger('ept_mx_adm')

def log_api_request(method, url, status_code=None, response_time=None):
    """Log API requests"""
    logger = get_logger()
    
    message = f"API {method} {url}"
    if status_code:
        message += f" - Status: {status_code}"
    if response_time:
        message += f" - Time: {response_time:.2f}s"
        
    logger.info(message)

def log_user_action(username, action, details=None):
    """Log user actions"""
    logger = get_logger()
    
    message = f"User '{username}' - {action}"
    if details:
        message += f" - {details}"
        
    logger.info(message) 
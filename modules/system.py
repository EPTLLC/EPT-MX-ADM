"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: System Monitoring Module
Telegram: https://t.me/EasyProTech

System monitoring module for EPT-MX-ADM
Basic system monitoring functionality
"""

from utils.logger import get_logger

logger = get_logger()


class SystemMonitor:
    """Basic system monitor"""
    
    def __init__(self):
        pass
    
    def get_all_metrics(self):
        """Get basic system metrics"""
        return {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0
        }
    
    def get_top_processes(self, limit=15):
        """Get top processes"""
        return [] 
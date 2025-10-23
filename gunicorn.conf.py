"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Gunicorn Configuration
Telegram: https://t.me/EasyProTech
"""

# Gunicorn Configuration for EPT-MX-ADM
# Production-ready settings for Matrix admin panel

import os

# Get base path from environment variable
BASE_PATH = os.environ.get('BASE_PATH', os.getcwd())

# Server socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# Restart workers after this many requests, with up to 50% jitter
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this many seconds
max_worker_memory = 200  # MB

# Process naming
proc_name = "ept-mx-adm"

# Server mechanics
daemon = False
pidfile = f"{BASE_PATH}/logs/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = f"{BASE_PATH}/logs/gunicorn_access.log"
errorlog = f"{BASE_PATH}/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process limits
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL (if needed in future)
# keyfile = None
# certfile = None

# Environment variables
raw_env = [
    'FLASK_ENV=production',
    'EPT_MX_ADM_CONFIG=production'
]

# Preload app for better performance
preload_app = True

# Enable stats
enable_stdio_inheritance = True

# Security
forwarded_allow_ips = "*"
secure_headers = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block'
}

# Worker lifecycle hooks
def on_starting(server):
    server.log.info("EPT-MX-ADM starting up...")

def on_reload(server):
    server.log.info("EPT-MX-ADM reloading...")

def when_ready(server):
    server.log.info("EPT-MX-ADM ready to serve requests")

def on_exit(server):
    server.log.info("EPT-MX-ADM shutting down...")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    worker.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    worker.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal") 
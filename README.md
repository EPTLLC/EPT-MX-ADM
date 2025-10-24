# EPT-MX-ADM v1.0.1

[![PyPI version](https://badge.fury.io/py/ept-mx-adm.svg)](https://badge.fury.io/py/ept-mx-adm)
[![Python](https://img.shields.io/pypi/pyversions/ept-mx-adm.svg)](https://pypi.org/project/ept-mx-adm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/ept-mx-adm)](https://pepy.tech/project/ept-mx-adm)

```
  _____ ____ _____     __  ____   __      _    ____  __  __ 
 | ____|  _ \_   _|   |  \/  \ \ / /     / \  |  _ \|  \/  |
 |  _| | |_) || |_____|  |\/  |\ \  /____/ _ \ | | | | |\/| |
 | |___|  __/ | |_____|  |  | |/ /  \___/ ___ \| |_| | |  | |
 |_____|_|    |_|     |__|  |_/_/\_\  /_/   \_\____/|_|  |_|
```

**Web-Based Administration Panel for Matrix Synapse Server**

Universal admin tool that works with ANY Matrix server - local, remote, cloud, or self-hosted. Just admin credentials needed.

![Login Page with Security Features](screenshots/login_security.png)

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Localization](#localization)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## Features

### Universal Compatibility
- Works with ANY Matrix server (local, remote, cloud, self-hosted)
- Supports self-signed SSL certificates
- No complex configuration needed
- Multi-server support in one installation

### Dashboard
- Real-time server statistics
- User analytics (active, deactivated, total)
- Room statistics and analytics
- Media storage monitoring
- API health status
- Synapse version information
- Python version display

### User Management
- View all users with pagination
- Create new users
- Edit user profiles and settings
- Deactivate/reactivate users
- Reset user passwords
- View user devices and sessions
- Media storage per user
- Filter by guests and deactivated users
- CSV export/import
- Advanced search functionality

### Room Management
- List all rooms with detailed information
- View room details and statistics
- Edit room settings
- Delete rooms
- Unblock rooms
- Assign room administrators
- Column visibility toggles
- Advanced filtering and search
- CSV export
- Pagination with customizable rows per page

### Space Management
- List all Matrix spaces
- View space hierarchies
- Manage space settings
- Consistent pagination
- Modern card-based UI

### Media Management
- Overall media statistics dashboard
- Users with media list
- Detailed user media files view
- File type filtering (Images, Videos, Audio, Documents, Other)
- Quarantine system for suspicious files
- Media file deletion
- CSV export
- Human-readable file sizes
- Status filtering (Normal, Quarantined)

### Authentication & Security
- Simplified login form
- Server auto-detection
- Username auto-formatting
- Real Matrix admin rights verification
- Session management
- SSL certificate support
- Secure API integration

### Localization
- Multi-language support: English, Russian, German, French, Italian, Spanish, Turkish, Arabic, Hebrew, Japanese, Chinese
- Easy language switching
- Full interface translation
- RTL support ready

### Modern UI/UX
- Responsive design for all devices
- Dark/Light theme toggle
- Bootstrap 5 framework
- Bootstrap Icons
- Chart.js for analytics
- Smooth animations
- Modal dialogs
- Toast notifications

---

## Requirements

### System Requirements
- **Python**: 3.8 or higher
- **pip**: Latest version recommended
- **Operating System**: Linux, macOS (Windows with WSL or manual setup)

### Matrix Server Requirements
- **Matrix Synapse**: Any version with Admin API enabled
- **Admin Account**: User with admin privileges on the Matrix server
- **Network Access**: HTTP/HTTPS access to Matrix server

### Python Dependencies
All dependencies are listed in `requirements.txt`:
- Flask >= 2.3.0
- requests >= 2.31.0
- Jinja2 >= 3.1.0
- MarkupSafe >= 2.1.0
- werkzeug >= 2.3.0

---

## Installation

### Quick Start (PyPI - Recommended)

```bash
# Install from PyPI
pip install ept-mx-adm

# Download static assets
cd $(pip show ept-mx-adm | grep Location | cut -d' ' -f2)/ept-mx-adm
chmod +x install_assets.sh
./install_assets.sh

# Run the application
python -m ept-mx-adm
# or
ept-mx-adm
```

### Installation from Source

#### Option 1: Simple Installation
```bash
# Clone the repository
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Install dependencies
pip install -r requirements.txt

# Download static assets
chmod +x install_assets.sh
./install_assets.sh

# Run the application
python app.py
```

#### Option 2: Using Helper Script
```bash
# Clone the repository
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Make script executable
chmod +x run.sh

# Run (auto-installs dependencies and starts app)
./run.sh
```

#### Option 3: With Virtual Environment
```bash
# Clone the repository
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download static assets
chmod +x install_assets.sh
./install_assets.sh

# Run the application
python app.py
```

#### Option 4: With pipx (Isolated)
```bash
# Install pipx if not already installed
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Clone and setup
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Install dependencies (pipx manages isolation)
pip install -r requirements.txt

# Download static assets
chmod +x install_assets.sh
./install_assets.sh

# Run
python app.py
```

#### Option 5: Windows (Manual Setup)
```cmd
# Clone the repository
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download static assets manually or use WSL:
# - Download Bootstrap 5, Bootstrap Icons, Chart.js
# - Place in static/vendor/ folders
# - See install_assets.sh for URLs

# Run the application
python app.py
```

**Note for Windows users:**
- Shell scripts (.sh files) require WSL (Windows Subsystem for Linux) or Git Bash
- Alternatively, manually download static assets from CDN links in `install_assets.sh`
- Python application itself runs natively on Windows

---

## Configuration

### config.json

The main configuration file is `config.json` in the project root.

**Default Configuration:**
```json
{
  "matrix_server": "https://matrix.example.com",
  "app": {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": true
  },
  "session": {
    "secret_key": "your-secret-key-here-change-this"
  }
}
```

**Configuration Options:**

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `matrix_server` | Your Matrix Synapse server URL (can be changed at login) | `https://matrix.example.com` | No |
| `app.host` | Application host | `127.0.0.1` | Yes |
| `app.port` | Application port | `5000` | Yes |
| `app.debug` | Debug mode (disable in production) | `true` | Yes |
| `session.secret_key` | Flask session secret key (change in production) | Generated | Yes |

### Important Notes

1. **Matrix Server**: The `matrix_server` in config.json is optional - you can specify any server at login
2. **Secret Key**: Change `session.secret_key` in production to a random string
3. **Debug Mode**: Set `app.debug` to `false` in production
4. **SSL Certificates**: Self-signed certificates are automatically supported

---

## Running the Application

### Development Mode

```bash
# Activate virtual environment if using one
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python app.py
```

The application will start on `http://127.0.0.1:5000` (or the host/port specified in config.json).

### Production Mode (Gunicorn)

```bash
# Activate virtual environment if using one
source venv/bin/activate

# Run with Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

### Systemd Service (Linux)

Create `/etc/systemd/system/ept-mx-adm.service`:

```ini
[Unit]
Description=EPT-MX-ADM Matrix Admin Panel
After=network.target

[Service]
Type=notify
User=your-user
Group=your-group
WorkingDirectory=/path/to/EPT-MX-ADM
Environment="PATH=/path/to/EPT-MX-ADM/venv/bin"
ExecStart=/path/to/EPT-MX-ADM/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ept-mx-adm
sudo systemctl start ept-mx-adm
sudo systemctl status ept-mx-adm
```

---

## Usage

### First Login

1. Open your browser and navigate to `http://localhost:5000` (or your configured host:port)

2. **Login Form:**
   - **Matrix Server**: Enter your server domain (e.g., `matrix.example.com` or `localhost`)
     - No need for `https://` - it's added automatically
     - Works with local servers, remote servers, and self-signed certificates
   
   - **Username**: Enter your admin username (e.g., `admin`)
     - No need for `@` or domain - it's formatted automatically
   
   - **Password**: Enter your Matrix admin password

3. Click "Login"

The application will:
- Automatically format the server URL (add `https://` if needed)
- Automatically format the username into Matrix ID (add `@` and domain)
- Verify admin privileges via Matrix API
- Create a session for your admin user

### Managing Users

**View Users:**
- Navigate to "Users" tab
- See all users with pagination
- Filter by guests and deactivated users
- View media storage per user

**Create User:**
- Click "Create User" button
- Fill in username, password, and optional display name
- Choose if user should be admin
- Click "Create"

**Edit User:**
- Click on user card dropdown menu
- Select "Edit"
- Modify user settings
- Save changes

**Deactivate User:**
- Click on user dropdown menu
- Select "Deactivate"
- Confirm action

### Managing Rooms

**View Rooms:**
- Navigate to "Rooms" tab
- See all rooms with statistics
- Toggle column visibility
- Use search to find specific rooms

**View Room Details:**
- Click "View" button on room card
- See detailed information in modal
- View members, settings, and statistics

**Edit Room:**
- Click dropdown menu on room card
- Select "Edit"
- Modify room settings
- Save changes

**Delete Room:**
- Click dropdown menu
- Select "Delete"
- Confirm action (room will be permanently deleted)

### Managing Media

**View Media Statistics:**
- Navigate to "Media" tab
- See overall statistics dashboard
- View total files, storage, and users with media

**View User Media:**
- Click on user in media list
- See all media files for that user
- Filter by file type (Images, Videos, Audio, Documents, Other)
- Filter by status (Normal, Quarantined)

**Quarantine Media:**
- In user media view, click dropdown on file
- Select "Quarantine"
- File will be marked as quarantined

**Delete Media:**
- Click dropdown on file
- Select "Delete"
- Confirm action

### Managing Spaces

**View Spaces:**
- Navigate to "Spaces" tab
- See all Matrix spaces
- View space hierarchies
- Manage space settings

---

## Localization

EPT-MX-ADM supports multiple languages out of the box.

### Available Languages
- English (en)
- Russian (ru)
- German (de)
- French (fr)
- Italian (it)
- Spanish (es)
- Turkish (tr)
- Arabic (ar)
- Hebrew (he)
- Japanese (ja)
- Chinese (zh)

### Changing Language

**In Application:**
1. Click on language selector in top navigation
2. Choose your preferred language
3. Interface will update immediately
4. Language preference is saved in session

**Adding New Language:**
1. Copy `locales/en/messages.json` to `locales/[language_code]/messages.json`
2. Translate all strings in the new file
3. Language will be automatically detected and available

---

## Production Deployment

### Security Checklist

- [ ] Change `session.secret_key` in config.json to a random string
- [ ] Set `app.debug` to `false` in config.json
- [ ] Use strong passwords for admin accounts
- [ ] Enable HTTPS (use nginx or Apache as reverse proxy)
- [ ] Restrict access to the application (firewall, VPN)
- [ ] Keep Python and dependencies up to date
- [ ] Regular backups of config.json
- [ ] Monitor logs for suspicious activity

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name admin.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name admin.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName admin.yourdomain.com
    Redirect permanent / https://admin.yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName admin.yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
    
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "https"
</VirtualHost>
```

---

## Troubleshooting

### Common Issues

#### "Connection refused" or "Cannot connect to Matrix server"
**Solution:**
- Verify Matrix server URL is correct
- Check if Matrix server is running
- Ensure network connectivity
- For local servers, try `localhost` or `127.0.0.1`
- Check firewall rules

#### "SSL: CERTIFICATE_VERIFY_FAILED" error
**Solution:**
- EPT-MX-ADM automatically handles self-signed certificates
- If error persists, verify server URL starts with `https://`
- Check if Matrix server certificate is properly configured

#### "Invalid credentials" or "Not an admin"
**Solution:**
- Verify username and password are correct
- Ensure user has admin privileges on Matrix server
- Check if user is deactivated
- Try logging in via Matrix client first to verify credentials

#### Login form only shows username/password (no server field)
**Solution:**
- This is normal - server field is optional
- Enter server domain at login or use default from config.json
- Server field will be shown after first failed attempt

#### Dashboard shows "N/A" or "0" for statistics
**Solution:**
- Verify admin API is enabled on Matrix server
- Check if user has proper admin rights
- Wait a few seconds for data to load
- Check browser console for errors
- Verify Matrix server API endpoints are accessible

#### Pagination not working (users/rooms/spaces)
**Solution:**
- Clear browser cache and reload
- Check browser console for JavaScript errors
- Verify API responses in Network tab
- Ensure using latest version of EPT-MX-ADM

#### Media page shows "Error loading media data"
**Solution:**
- Verify `/v1/statistics/users/media` endpoint is available on Matrix server
- Check if user has admin rights
- Clear browser cache
- Check server logs for errors

---

## Security

### Best Practices

1. **Passwords**: Use strong, unique passwords for admin accounts
2. **Session Secret**: Change `session.secret_key` to a random string
3. **Debug Mode**: Disable debug mode in production
4. **HTTPS**: Always use HTTPS in production (via reverse proxy)
5. **Access Control**: Restrict access to the application via firewall or VPN
6. **Updates**: Keep Python, Flask, and all dependencies up to date
7. **Logs**: Monitor application and server logs regularly
8. **Backups**: Regular backups of configuration and data

### SSL/TLS Support

EPT-MX-ADM automatically:
- Supports self-signed SSL certificates
- Disables SSL verification for local/development servers
- Adds `https://` to server URLs if not present
- Suppresses SSL warnings in logs

For production, always use valid SSL certificates via reverse proxy.

---

## Contributing

We welcome contributions to EPT-MX-ADM!

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments and docstrings
- Update documentation for new features
- Test your changes thoroughly
- Update CHANGELOG.md

### Reporting Issues

Found a bug or have a feature request?

1. Check if issue already exists
2. Create new issue with detailed description
3. Include steps to reproduce (for bugs)
4. Provide environment details (OS, Python version, Matrix Synapse version)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License allows you to:
- Use the software for any purpose
- Modify the source code
- Distribute copies
- Include in proprietary software

With the following conditions:
- Include the original license and copyright notice
- Provide attribution to original authors

---

## Support

### Support Policy

**No Support Provided**: This project is released as-is without support, consultation, or assistance.

**Community Contributions**: Development contributions are welcome but not obligated.

### Resources

- **Documentation**: [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md)
- **Issues**: [GitHub Issues](https://github.com/EPTLLC/EPT-MX-ADM/issues) - for bug reports only
- **Community**: [@EasyProTech](https://t.me/EasyProTech)

---

## Project Information

- **Project Name**: EPT-MX-ADM
- **Version**: 1.0.0
- **Status**: Production Ready
- **PyPI**: [pypi.org/project/ept-mx-adm](https://pypi.org/project/ept-mx-adm/)
- **Company**: EasyProTech LLC
- **Website**: [www.easypro.tech](https://www.easypro.tech)
- **Developer**: Brabus
- **Repository**: [github.com/EPTLLC/EPT-MX-ADM](https://github.com/EPTLLC/EPT-MX-ADM)
- **License**: MIT
- **Python**: 3.8+
- **Supported Languages**: EN, RU, DE, FR, IT, ES, TR, AR, HE, JA, ZH

---

## Acknowledgments

- **Matrix Foundation** for the Matrix protocol
- **Synapse Team** for the Matrix Synapse server
- **Flask Team** for the amazing web framework
- **Bootstrap Team** for the UI framework
- **Chart.js Team** for visualization library
- **Community Contributors** for feedback and contributions

---

## Changelog

For detailed history of changes, see [CHANGELOG.md](CHANGELOG.md).

---

**Created with care by EasyProTech LLC**

Visit us: [www.easypro.tech](https://www.easypro.tech) | Telegram: [@EasyProTech](https://t.me/EasyProTech)

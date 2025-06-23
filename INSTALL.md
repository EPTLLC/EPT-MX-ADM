# 🚀 EPT-MX-ADM Installation

**Ultra-simple Matrix admin panel setup!**

## ⚡ Quick Install

### 1. Download & Setup
```bash
# Download or clone EPT-MX-ADM
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Install dependencies
pip3 install -r requirements.txt

# Download static assets
./install_assets.sh
```

### 2. Configure (Only 1 file!)
Edit `config.json`:
```json
{
  "matrix_server": "https://your-matrix-server.com",
  "debug": false,
  "language": "en"
}
```

That's it! No domains, no paths, no complex configuration!

### 3. Run
```bash
# Development
python3 app.py

# Production (with Gunicorn)
gunicorn --config gunicorn.conf.py app:app
```

## 🌐 Access

- **URL**: Any domain you want (http://localhost:5000, https://admin.yoursite.com, etc.)
- **Login**: Your Matrix admin user (@admin:your-matrix-server.com)
- **Password**: Your Matrix password

## 🔧 Configuration Options

### config.json
```json
{
  "matrix_server": "https://matrix.example.com",  // Your Matrix server URL
  "debug": true,                                  // Enable debug mode
  "language": "en"                               // Default language (en/ru/de/fr/it/es/tr/zh/ja/ar/he)
}
```

### Environment Variables (optional)
```bash
export SECRET_KEY="your-secret-key"  # Flask secret key (auto-generated if not set)
```

## 🎯 Why This is Better

- ✅ **One config file** - just `config.json`
- ✅ **No hardcoded domains** - works on any domain
- ✅ **Auto-detection** - paths, domains, everything automatic
- ✅ **Portable** - move anywhere, still works
- ✅ **Simple** - edit 1 line, you're done!

## 🔄 Reload Configuration

If you change `config.json`, just restart the application:
```bash
# Kill and restart
pkill -f "python3 app.py"
python3 app.py

# Or with systemd
systemctl restart your-admin-service
```

## 🌍 Multi-Domain Setup

You can run the same admin panel on multiple domains:
- `https://admin.company.com` 
- `https://matrix-admin.internal.net`
- `http://localhost:5000`

All point to the same Matrix server configured in `config.json`!

## 🛠️ Systemd Service Example

```ini
[Unit]
Description=EPT-MX-ADM Matrix Admin Panel
After=network.target

[Service]
Type=exec
User=matrix
WorkingDirectory=/path/to/EPT-MX-ADM
ExecStart=/usr/bin/python3 -m gunicorn --config gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## ❓ Troubleshooting

**Can't login?**
- Check `matrix_server` URL in `config.json`
- Verify your user has admin rights in Matrix
- Use full Matrix ID: `@username:domain.com`

**Wrong domain detected?**
- Check `matrix_server` format: `https://matrix.domain.com` (with https://)

**Want to change language?**
- Edit `language` in `config.json` and restart 
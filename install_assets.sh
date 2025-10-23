#!/bin/bash
#
# Project: EPT-MX-ADM
# Company: EasyProTech LLC (www.easypro.tech)
# Dev: Brabus
# Date: Thu 23 Oct 2025 22:56:11 UTC
# Status: Assets Installer
# Telegram: https://t.me/EasyProTech
#

# EPT-MX-ADM Assets Installer
# Downloads all required static assets automatically

echo "🚀 Installing EPT-MX-ADM static assets..."

# Create directories
mkdir -p static/vendor/{bootstrap/{css,js},bootstrap-icons/fonts,chartjs}

echo "📦 Downloading Bootstrap CSS & JS..."
curl -o static/vendor/bootstrap/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
curl -o static/vendor/bootstrap/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

echo "🎨 Downloading Bootstrap Icons..."
curl -o static/vendor/bootstrap-icons/bootstrap-icons.css https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css
curl -o static/vendor/bootstrap-icons/fonts/bootstrap-icons.woff https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff
curl -o static/vendor/bootstrap-icons/fonts/bootstrap-icons.woff2 https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff2

echo "📊 Downloading Chart.js..."
curl -o static/vendor/chartjs/chart.min.js https://cdn.jsdelivr.net/npm/chart.js

echo "🔧 Fixing font paths..."
sed -i 's|https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/|../bootstrap-icons/fonts/|g' static/vendor/bootstrap-icons/bootstrap-icons.css

echo "✅ All assets installed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Edit config.json with your Matrix server"
echo "2. Run: python3 app.py"
echo "" 
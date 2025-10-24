#!/bin/bash
#
# Project: EPT-MX-ADM
# Company: EasyProTech LLC (www.easypro.tech)
# Dev: Brabus
# Date: Thu 23 Oct 2025 22:56:11 UTC
# Status: PyPI Publish Script
# Telegram: https://t.me/EasyProTech
#

echo "Publishing EPT-MX-ADM to PyPI"
echo "================================"

# Check for .pypirc file
if [ ! -f ~/.pypirc ] && [ ! -f .pypirc ]; then
    echo "ERROR: .pypirc not found!"
    echo "Create .pypirc from .pypirc.example template"
    echo "See: https://packaging.python.org/en/latest/specifications/pypirc/"
    exit 1
fi
echo "✓ PyPI credentials found"
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

# Install build tools
echo "Installing build tools..."
pip install --upgrade pip setuptools wheel twine

# Build distribution
echo "Building distribution packages..."
python setup.py sdist bdist_wheel

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/* --config-file .pypirc

echo ""
echo "Done! Package published to PyPI"
echo "Install with: pip install ept-mx-adm"


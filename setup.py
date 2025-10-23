"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: PyPI Setup Configuration
Telegram: https://t.me/EasyProTech
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ept-mx-adm",
    version="1.0.0",
    author="Brabus (EasyProTech LLC)",
    author_email="support@easypro.tech",
    description="Web-Based Administration Panel for Matrix Synapse Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EPTLLC/EPT-MX-ADM",
    project_urls={
        "Bug Reports": "https://github.com/EPTLLC/EPT-MX-ADM/issues",
        "Source": "https://github.com/EPTLLC/EPT-MX-ADM",
        "Documentation": "https://github.com/EPTLLC/EPT-MX-ADM/blob/main/README.md",
        "Changelog": "https://github.com/EPTLLC/EPT-MX-ADM/blob/main/CHANGELOG.md",
        "Telegram": "https://t.me/EasyProTech",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Systems Administration",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Natural Language :: German",
        "Natural Language :: French",
        "Natural Language :: Italian",
        "Natural Language :: Spanish",
        "Natural Language :: Turkish",
    ],
    keywords=[
        "matrix",
        "synapse",
        "admin",
        "administration",
        "panel",
        "web",
        "flask",
        "matrix-synapse",
        "admin-panel",
        "chat",
        "communication",
        "server-management",
        "user-management",
        "room-management",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
            "locales/**/*.json",
            "config.json",
        ],
    },
    entry_points={
        "console_scripts": [
            "ept-mx-adm=app:main",
        ],
    },
    zip_safe=False,
)


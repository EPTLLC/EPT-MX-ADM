# EPT-MX-ADM Changelog

All notable changes to this project will be documented in this file.

---

## [1.0.0] - 2025-10-23

### Major Release - Production Ready

This release marks the transition from beta to stable production version with comprehensive improvements across all components.

### Login & Authentication
- Simplified login form with user-friendly inputs
- Matrix Server field now accepts domain only (e.g., matrix.example.com) without https://
- Username field accepts simple username (e.g., admin) without @ or domain
- Automatic formatting of server URL and Matrix ID from simplified inputs
- Added support for self-signed SSL certificates
- Disabled SSL verification for local/self-signed certificate servers
- Dynamic server selection - works with any Matrix server (local or remote)
- Stored matrix_server in Flask session for multi-server support

### Dashboard Improvements
- Redesigned dashboard layout with larger, more prominent cards
- Fixed deactivated user count calculation
- Added media storage statistics to dashboard
- New cards: Total Users, Total Rooms, API Response, Synapse Version, System Status
- User Details card with Active/Deactivated/Total counts
- Storage Info card with media storage, total rooms, and Python version
- Improved data accuracy with proper API queries

### Users Management
- Fixed pagination - now correctly switches between pages
- Added media storage information to each user card (space consumed and file count)
- Implemented full pagination controls (first, previous, page numbers, next, last)
- Moved pagination controls to the right for consistency
- Added JavaScript-based pagination navigation
- Fixed user count calculation after filtering main admin
- Media statistics fetched from /v1/statistics/users/media endpoint
- Formatted file sizes displayed in human-readable format (B, KB, MB, GB, TB)

### Rooms Management
- Fixed pagination functionality
- Added full pagination controls matching Users page
- Moved pagination to the right side
- Implemented proper offset calculation for Matrix API
- JavaScript pagination functions for smooth navigation
- "Showing X-Y of Z entries" text display

### Spaces Management
- Fixed pagination issues - arrows no longer disappear
- Unified styling with Users and Rooms pages using Bootstrap cards
- Consistent pagination layout and behavior
- Fixed text overflow in space cards with text-truncate
- Removed API limitation notice
- Proper pagination calculation and display

### Media Management
- Complete recreation of /users-media page from scratch
- Fixed "Error loading media data" issue
- Proper use of /v1/statistics/users/media endpoint
- Client-side pagination and search filtering
- Sorted users by media count (descending)
- Fixed "View Media" button functionality

### User Media Details Page
- Recreation of user media detail page with consistent styling
- Fixed display of total media files and storage
- Separate display for overall totals and current page stats
- Shows: Total storage, Total files, On this page (files/size)
- Restored and improved file type and status filters
- Compact filter card layout
- Filters: File type (Images, Videos, Audio, Documents, Other)
- Filters: Status (Normal, Quarantined)
- Filters: Rows per page (25, 50, 100)
- Combined user info and filters in single card
- Fixed pagination to match other pages

### Configuration & Documentation
- Updated README.md to emphasize universal admin panel concept
- Added "Works Anywhere, Any Server" section
- Three installation options: simple pip, pipx, venv
- Simplified quick start instructions
- Updated common issues section for better troubleshooting
- Created run.sh helper script for quick setup
- Improved INSTALL.md with venv setup instructions
- Removed forced venv requirement - user choice

### Code Quality
- Added project headers to all source files (Python, HTML, JS, CSS, Shell)
- Consistent header format with project info, company, developer, date, status
- Headers added to 36+ files across the entire project
- Improved code organization and documentation
- Removed route conflicts (users_bp vs media_bp for /users/<user_id>/media)
- Fixed Jinja2/JavaScript linter errors in templates
- Proper error handling and logging throughout

### Technical Improvements
- Fixed from_offset calculation for Matrix API pagination
- Proper use of /v1/statistics/users/media for efficient queries
- Client-side pagination for media users list
- Format helper functions for file sizes
- Session management for matrix_server
- Context processors updated with Config and session objects
- Disabled SSL warnings with urllib3
- Smart username and server URL formatting in auth module

### Version Updates
- Updated version from v0.0.1-beta to v1.0.0 in all files
- Updated config/settings.py
- Updated project.json
- Removed beta warnings and notices

---

## [0.0.1-beta] - Previous Beta Releases

### Configuration & Localization Fix
- Revolutionary config.json configuration system
- One file setup - only edit matrix_server in config.json
- Auto-path detection for working directory, locales, logs
- Portable installation - works in any folder, any domain, any Matrix server
- Fixed localization system with lazy initialization
- Zero hardcoding - removed all hardcoded domains
- Simple install process: Download, Edit 1 line, Run
- Dynamic configuration computed at runtime
- Backward compatibility maintained
- Created INSTALL.md with setup instructions

### Critical API & Authentication Fixes
- Fixed Matrix Admin API access via nginx configuration
- Real admin rights verification via Matrix API
- Fixed API health status indicators on dashboard
- CORS headers optimization for admin endpoints
- Secure authentication flow - only real Matrix admins
- Fixed Matrix API, Users API, and Rooms API connectivity
- Enhanced security - removed fallback admin access
- Automatic configuration - no manual paths needed
- Real-time admin check on every login
- Performance improvement in API client initialization

### Room Management Fixes & Improvements
- Fixed room deletion with corrected SynapseAPIClient.delete() method
- Simplified room actions - removed confusing "Clear Room" functionality
- Single action interface for clarity
- API testing and validation on real Matrix rooms
- Code cleanup - removed unused functions
- Endpoint cleanup - deleted non-functional endpoints
- Translation updates for EN/RU locales
- Improved error handling in JavaScript
- Room unblocking functionality
- Room admin assignment feature
- Enhanced room menu with additional actions
- Security focus - removed message reading to maintain privacy
- New API endpoints: /api/rooms/unblock and /api/rooms/make_admin
- Complete translations for new features

### User Media Management
- Full-featured media content viewing and management
- Dashboard with overall statistics
- Users with media list with avatars and progress bars
- Detailed user media view with file tables
- Powerful filtering by file types and quarantine status
- Quarantine system for suspicious files
- Media file deletion with confirmation
- CSV media export for users and files
- Colored file type badges
- Media search with input delay
- Customizable pagination (10-1000 records)
- Responsive design for all devices
- Full localization for 7 languages
- Modal dialogs with animations
- Filter persistence in localStorage

### Room Management
- Column visibility toggles for table customization
- Column settings persistence in localStorage
- Separate "VIEW" column for better navigation
- Shortened column names for optimized headers
- New header design with blue styling
- Date and time separation in columns
- CSV room export with 15 data fields
- Advanced pagination with first/last page navigation
- Powerful real-time room search
- Fixed creation date retrieval from m.room.create event
- Full localization for 7 languages
- Colored status badges and sticky headers
- Modern responsive design
- Performance optimization for API requests

### User Functionality
- Beautiful movie-style user profiles with avatars
- Whois system for IP addresses, devices, login times
- Clickable room creators for quick navigation
- Improved user menu with better positioning
- Device management API for viewing and deleting devices
- Extended information: device types, account statuses, dates
- New modal design in profile card style
- 7 new API endpoints for extended functionality
- Dark/Light theme toggle with auto-save
- Extended multilingual support: Spanish and Turkish (7 languages total)
- Powerful user filters for guests and deactivated users
- CSV export/import for bulk user operations
- Advanced pagination (10-1000 rows per page)
- Optimized UI with dynamic filters and smart tooltips

### Multilingual Support & UI/UX
- Project renamed to "EPT-MX-ADM" (EasyProTech Matrix Admin)
- Multilingual support: English and Russian
- UI/UX improvements: redesigned login page, gradients
- Bug fixes: authorization, localization, footer
- Full template localization for two languages

### Initial Release
- Basic admin panel functionality
- User management
- Room viewing
- Simple dashboard
- Authorization via Matrix API

---

## Navigation
- [Main README](README.md) - project description and installation
- [Changelog](CHANGELOG.md) - detailed history of all changes (this file)

Created by EasyProTech LLC (www.easypro.tech)

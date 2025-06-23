# 📅 EPT-MX-ADM Changelog

## 🚧 Beta Version Notice

**This project is in BETA stage and will remain in beta until it becomes perfect!** 

🔥 We're constantly improving and adding features. All changes listed below are part of the ongoing beta development process.

---

## 🌍 Ultra-Simple Configuration & Localization Fix (June 23, 2025)
- **🎯 REVOLUTIONARY: config.json Configuration**: Replaced all hardcoded domains with single config.json file
- **📁 One File Setup**: Only need to edit `matrix_server` in config.json - everything else auto-configured
- **🔧 Auto-Path Detection**: Automatic detection of working directory, locales, logs - no manual paths needed
- **🌐 Portable Installation**: Admin panel works in any folder, on any domain, with any Matrix server
- **🌍 Localization System Fixed**: Fixed lazy initialization of translation system to work with dynamic config
- **🚀 Zero Hardcoding**: Removed ALL hardcoded domains from codebase - truly universal setup
- **📝 Simple Install Process**: Download → Edit 1 line in config.json → Run - that's it!
- **🔄 Dynamic Configuration**: Config properties computed at runtime, not at import time
- **🛠️ Backward Compatibility**: All existing functionality preserved while simplifying setup
- **📚 Installation Documentation**: Created INSTALL.md with ultra-simple setup instructions

## 🔧 Critical API & Authentication Fixes (June 23, 2025)
- **🚨 MAJOR FIX: Matrix Admin API Access**: Fixed nginx configuration to properly route `/_synapse/admin` endpoints
- **🔐 Real Admin Rights Verification**: Replaced broken `Config.ADMIN_USERS` check with actual Matrix API verification via `/_synapse/admin/v1/users/{user_id}/admin`
- **✅ API Health Status Fixed**: All dashboard API status indicators now show correct green/red states instead of permanent errors
- **🌐 CORS Headers Optimization**: Updated nginx regex from `/_synapse/client` to `/_synapse` to include all admin endpoints
- **🔒 Secure Authentication Flow**: Only users with actual Matrix admin privileges can now access the admin panel
- **📊 Dashboard API Connectivity**: Fixed Matrix API, Users API, and Rooms API connectivity issues
- **🛡️ Enhanced Security**: Removed fallback admin access - only real Matrix admins can use the panel
- **⚡ Automatic Configuration**: No manual path configuration needed - everything works out of the box
- **🔍 Real-time Admin Check**: Admin status verified on every login via live Matrix API call
- **📈 Performance Improvement**: Streamlined API client initialization and error handling

## 🏠 Room Management Fixes & Improvements (Latest Beta)
- **🔧 Fixed Room Deletion**: Corrected SynapseAPIClient.delete() method to properly accept JSON parameters
- **🚮 Simplified Room Actions**: Removed confusing "Clear Room" functionality that didn't work as expected
- **🎯 Single Action Interface**: Streamlined to only "Delete Room" action for clarity and reliability
- **🔍 API Testing & Validation**: Tested room deletion on real Matrix rooms (purge: false/true both delete completely)
- **🧹 Code Cleanup**: Removed unused functions: clearRoom(), clearRoomAction(), clearRoomConfirm()
- **🗑️ Endpoint Cleanup**: Deleted non-functional /api/rooms/clear endpoint and purge_room_history() method
- **🌍 Translation Updates**: Added missing 'time_of_send' translations for EN/RU locales
- **⚠️ Error Handling**: Improved JavaScript error handling with Content-Type validation
- **🏷️ Template Cleanup**: Removed clearRoomModal and associated UI elements
- **✅ Bug Resolution**: Fixed "MatrixError: [404] Not a known room" by removing problematic rooms
- **📝 Translation Cleanup**: Removed unused translation keys related to room clearing functionality
- **🔓 Room Unblocking**: Added ability to unblock previously blocked rooms
- **👑 Room Admin Assignment**: New functionality to assign room administrator privileges to users
- **🎨 Enhanced Room Menu**: Expanded dropdown with additional safe administrative actions
- **🔐 Security Focus**: Removed message reading functionality to maintain Matrix privacy principles
- **📡 New API Endpoints**: Added /api/rooms/unblock and /api/rooms/make_admin endpoints
- **🌍 Complete Translations**: Updated EN/RU locale files with new action labels

## 📁 Professional User Media Management (Beta)
- **📁 User Media Management**: Full-featured system for viewing and managing media content
- **📊 Media Statistics**: Dashboard with overall stats - file count, total size, users with media
- **👥 Users with Media List**: Professional table with avatars, file counts, media sizes, progress bars
- **🗂️ Detailed User Media View**: Complete file table with IDs, dates, sizes, types, filenames
- **🔍 Powerful Media Filtering**: By file types (images, videos, audio, documents, other) and quarantine status
- **⚠️ Quarantine System**: Place suspicious files in quarantine and mark as safe
- **🗑️ Media File Deletion**: Safe removal of unwanted content with confirmation
- **📊 CSV Media Export**: Export user media lists and detailed files for specific users
- **🎨 Colored File Types**: Different colored badges for visual file type distinction
- **🔍 Media Search**: Instant user search with input delay
- **📑 Media Pagination**: Customizable records per page (10-1000)
- **📱 Responsive Design**: Adaptive interface for all devices
- **🌍 Full Localization**: Translations for all 7 languages in media management interface
- **⚡ Modal Dialogs**: Beautiful confirmations for all actions with animations
- **💾 Filter Persistence**: Filter states saved in localStorage

## 🏠 Professional Room Management (Beta)
- **🔧 Column Visibility Toggles**: Compact filters for showing/hiding columns (encrypted, members, local members, state events, version, federation, directory)
- **💾 Column Settings Persistence**: Toggle states saved in localStorage
- **👁️ Separate "VIEW" Column**: Room view button moved to separate column for better navigation
- **🎯 Shortened Column Names**: Optimized table headers (NAME, LOCAL, EVENTS, DIRECTORY, VIEW)
- **🎨 New Header Design**: Blue table headers (#4e73df) matching button style
- **📅 Date and Time Separation**: Separate columns for room creation date and time
- **📊 CSV Room Export**: Export rooms with complete information (15 data fields)
- **📑 Advanced Pagination**: Choose 10-1000 rows, navigation with first/last page
- **🔍 Powerful Search**: Real-time room name search
- **📅 Fixed Creation Date**: Correct time retrieval from m.room.create event
- **🌍 Full Localization**: Updated translations for all 7 languages (EN, RU, DE, FR, IT, ES, TR)
- **🎨 Improved Interface**: Colored status badges, sticky table headers, modern responsive design
- **⚡ Performance Optimization**: Improved Matrix API requests, efficient data processing

## 👥 Extended User Functionality (Beta)
- **🎬 Beautiful User Profiles**: Movie-style profiles with avatars and detailed information
- **📱 Whois System**: View IP addresses, devices and user login times
- **🔗 Clickable Room Creators**: Quick navigation to room creator profiles
- **⚙️ Improved User Menu**: More options, better positioning, screen edge protection
- **🔧 Device Management**: API for viewing and deleting user devices
- **📊 Extended Information**: Device types, account statuses, creation dates
- **🎨 New Modal Design**: Modern UI in profile card style
- **🔌 New API Endpoints**: 7 new endpoints for extended functionality
- **🌙 Dark/Light Theme Toggle**: Full dark theme support with auto-save
- **🌍 Extended Multilingual**: Added Spanish 🇪🇸 and Turkish 🇹🇷 languages (now 7 languages)
- **🔍 Powerful User Filters**: Show guests, deactivated users with instant switching
- **📊 CSV Export/Import**: Bulk user export and import with data validation
- **📑 Advanced Pagination**: Choose 10-1000 rows per page, beautiful arrow navigation
- **⚡ Optimized UI**: Dynamic filters, smart tooltips, colored status badges

## 🌍 Multilingual Support & UI/UX (Beta)
- **🏷️ Project Rename**: **"EPT-MX-ADM"** (EasyProTech Matrix Admin)
- **🌍 Multilingual Support**: English and Russian languages
- **🎨 UI/UX Improvements**: Redesigned login page, added gradients
- **🔧 Bug Fixes**: Authorization, localization, footer
- **📄 Full Localization**: All templates translated to two languages

## 🎉 Initial Release (Beta)
- 🎉 Basic admin panel functionality
- 👥 User management
- 🏠 Room viewing
- 📊 Simple dashboard
- 🔐 Authorization via Matrix API

---

## 🚀 Beta Development Status

**🔥 EPT-MX-ADM will remain in BETA until it becomes perfect!**

We're continuously adding features, fixing bugs, and improving the user experience. The beta phase allows us to:

- 🔧 **Test all functionality** in real environments
- 🐛 **Fix bugs** as they're discovered  
- ✨ **Add new features** based on user feedback
- 🎨 **Polish the interface** to perfection
- 🌍 **Complete translations** for all languages
- ⚡ **Optimize performance** for large Matrix servers

**Current focus**: Making EPT-MX-ADM the **perfect Matrix admin panel** that administrators will love to use! 😎

---

## 🔗 Navigation
- **[Main README](README.md)** - project description and installation
- **[Changelog](CHANGELOG.md)** - detailed history of all changes (this file)

**Created with ❤️ by EasyProTech team** 
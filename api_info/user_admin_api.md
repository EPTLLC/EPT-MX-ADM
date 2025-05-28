# Synapse Admin API Endpoints for EPT-MX-ADM

## IMPORTANT: Using paths in code
In our project, the API client (`utils/api_client.py`) automatically adds the `/_synapse/admin` prefix to all requests.
Therefore **shortened paths should be used in code**, for example:
- In documentation: `GET /_synapse/admin/v2/users`
- In code: `self.api_client.get("/v2/users")`

## User Management (User Admin API)
```
GET /v2/users                           # List all users with pagination and filters
GET /v2/users/{user_id}                 # User information
PUT /v2/users/{user_id}                 # Create or update user
DELETE /v2/users/{user_id}              # Delete user
POST /v1/users/{user_id}/login          # Get access_token on behalf of user
GET /v1/whois/{user_id}                 # User activity details
POST /v1/users/{user_id}/override_ratelimit # Configure rate limits
GET /v1/users/{user_id}/media           # List user media
DELETE /v1/users/{user_id}/media        # Delete user media
GET /v1/users/{user_id}/account_data    # User account data
GET /v1/devices/{user_id}               # List user devices
DELETE /v1/devices/{user_id}/{device_id} # Delete device
POST /v1/users/{user_id}/password       # Reset user password
GET /v1/users/{user_id}/rooms           # List user rooms
POST /v1/users/{user_id}/deactivate     # Deactivate account
POST /v1/users/{user_id}/reactivate     # Reactivate account
```

## Room Management (Room Admin API)
```
GET /v1/rooms                           # List all rooms with pagination and filters
GET /v1/rooms/{room_id}                 # Room information
DELETE /v1/rooms/{room_id}              # Delete/clear room (MAIN ENDPOINT)
PUT /v1/rooms/{room_id}/block           # Block/unblock room
GET /v1/rooms/{room_id}/members         # List room members
GET /v1/rooms/{room_id}/state           # Room state
POST /v1/rooms/{room_id}/make_room_admin # Assign room admin
GET /v1/rooms/{room_id}/messages        # Room messages
GET /v1/rooms/{room_id}/forward_extremities # Forward extremities
DELETE /v1/rooms/{room_id}/forward_extremities # Delete forward extremities
```

### Parameters for DELETE /v1/rooms/{room_id}:
```json
{
    "message": "Message for users",
    "block": true,                      # Block room
    "purge": false                      # false = clear, true = complete deletion
}
```

**Usage examples in code:**
```python
# Clear room (removes users but preserves data)
data = {"block": True, "purge": False, "message": "Room cleared"}
response = self.api_client.delete(f"/v1/rooms/{room_id}", json=data)

# Complete room deletion
data = {"block": True, "purge": True, "message": "Room deleted"}
response = self.api_client.delete(f"/v1/rooms/{room_id}", json=data)
```

## Media Management (Media Admin API)
```
GET /v1/media                           # List all media files
DELETE /v1/media/{server_name}/{media_id} # Delete specific media
POST /v1/quarantine_media/{room_id}     # Quarantine room media
POST /v1/quarantine_media/user/{user_id} # Quarantine user media
POST /v1/protect_media/{server_name}/{media_id} # Protect media
POST /v1/purge_media_cache              # Clear media cache
POST /v1/purge_remote_media             # Delete remote media
GET /v1/media/{server_name}/{media_id}  # Media information
```

## Cleanup and Maintenance
```
POST /v1/purge_history/{room_id}        # Clear room history
```

### DEPRECATED ENDPOINTS (DO NOT USE):
```
❌ POST /v1/shutdown_room/{room_id}     # REMOVED in Synapse 1.130.0
❌ POST /v1/purge_room/{room_id}        # REMOVED in Synapse 1.130.0
```

## Federation and Server
```
GET /v1/federation/destinations         # List federation servers
GET /v1/server_version                  # Synapse version
POST /v1/federation/destination/{dest}/reset_connection # Reset connection
```

## Moderation and Reports
```
GET /v1/event_reports                   # List event reports
GET /v1/event_reports/{report_id}       # Report information
POST /v1/event_reports/{report_id}/resolve # Resolve report
```

## Statistics and Analytics
```
GET /v1/statistics/users                # User statistics
GET /v1/statistics/rooms                # Room statistics
GET /v1/statistics/events               # Event statistics
```

## Registration and Tokens
```
GET /v1/registration_tokens             # List registration tokens
POST /v1/registration_tokens/new        # Create token
PUT /v1/registration_tokens/{token}     # Update token
DELETE /v1/registration_tokens/{token}  # Delete token
```

## Support and Information
```
GET /.well-known/matrix/support         # Administrator contacts
GET /.well-known/matrix/server          # Server information
GET /.well-known/matrix/client          # Client information
```

## Examples of correct usage in EPT-MX-ADM:

### 1. Getting room list:
```python
response = self.api_client.get("/v1/rooms", params={"limit": 100})
```

### 2. Clearing room:
```python
data = {"block": True, "purge": False, "message": "Room cleared"}
response = self.api_client.delete(f"/v1/rooms/{room_id}", json=data)
```

### 3. Deleting room:
```python
data = {"block": True, "purge": True, "message": "Room deleted"}
response = self.api_client.delete(f"/v1/rooms/{room_id}", json=data)
```

### 4. Getting user information:
```python
response = self.api_client.get(f"/v2/users/{user_id}")
```
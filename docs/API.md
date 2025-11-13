# 📡 API Documentation

## Base URL
- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

## Authentication

JWT token-based authentication. Include token in headers:
```
Authorization: Bearer <your_access_token>
```

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "newuser",
    "role": "PUBLIC_USER"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1Q...",
    "refresh": "eyJ0eXAiOiJKV1Q..."
  }
}
```

### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
```

## Locations

### List All Locations
```http
GET /api/locations/
```

**Query Parameters:**
- `type`: Filter by type (BARANGAY, LANDMARK, SITIO)
- `search`: Search by name
- `ordering`: Sort by field (name, -name)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Basey Municipal Hall",
    "type": "LANDMARK",
    "latitude": 11.27893,
    "longitude": 125.07054,
    "address": "Basey Center"
  }
]
```

### Get Location Detail
```http
GET /api/locations/{id}/
```

### Create Location (Admin only)
```http
POST /api/locations/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "New Location",
  "type": "LANDMARK",
  "latitude": 11.2800,
  "longitude": 125.0700,
  "address": "Address here"
}
```

## Routes

### Calculate Fare
```http
POST /api/routes/calculate/
Content-Type: application/json

{
  "origin": [11.27893, 125.07054],
  "destination": [11.2768363, 125.0114879],
  "passenger_type": "REGULAR"
}
```

**Passenger Types:**
- `REGULAR`: Standard fare
- `SENIOR`: 20% discount
- `PWD`: 20% discount
- `STUDENT`: 20% discount

**Response:**
```json
{
  "distance_km": 5.42,
  "base_fare": 15.00,
  "additional_fare": 7.50,
  "subtotal": 22.50,
  "discount": 0.00,
  "total_fare": 22.50,
  "passenger_type": "REGULAR",
  "origin": {
    "latitude": 11.27893,
    "longitude": 125.07054
  },
  "destination": {
    "latitude": 11.2768363,
    "longitude": 125.0114879
  }
}
```

### Get Route History (Authenticated)
```http
GET /api/routes/history/
Authorization: Bearer <access_token>
```

## Fares

### List All Fares
```http
GET /api/fares/
```

**Response:**
```json
[
  {
    "id": 1,
    "route": {
      "id": 1,
      "name": "Basey Center to Barangay 1"
    },
    "base_fare": 15.00,
    "per_km_rate": 3.00,
    "passenger_type": "REGULAR"
  }
]
```

## User Profile

### Get Current User
```http
GET /api/users/me/
Authorization: Bearer <access_token>
```

### Update Profile
```http
PATCH /api/users/me/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

## Admin Endpoints

### User Management
```http
GET /api/users/              # List all users
GET /api/users/{id}/         # Get user detail
PATCH /api/users/{id}/       # Update user
DELETE /api/users/{id}/      # Delete user
```

**Requires:** Admin role

## Error Responses

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

## Rate Limiting

- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Admin: Unlimited

## Example Usage

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'admin',
    'password': 'your_password'
})
token = response.json()['tokens']['access']

# Calculate fare
response = requests.post('http://localhost:8000/api/routes/calculate/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'origin': [11.27893, 125.07054],
        'destination': [11.2768363, 125.0114879],
        'passenger_type': 'REGULAR'
    }
)
print(response.json())
```

### JavaScript
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'your_password'
  })
});
const { tokens } = await response.json();

// Calculate fare
const fareResponse = await fetch('http://localhost:8000/api/routes/calculate/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${tokens.access}`
  },
  body: JSON.stringify({
    origin: [11.27893, 125.07054],
    destination: [11.2768363, 125.0114879],
    passenger_type: 'REGULAR'
  })
});
const fare = await fareResponse.json();
```

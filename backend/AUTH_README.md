# Authentication System

This backend now includes a complete JWT-based authentication system with the following features:

## Features

- ✅ User registration (signup)
- ✅ User login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Protected routes with JWT authentication
- ✅ User roles (admin/regular users)
- ✅ Authenticated chat endpoints
- ✅ User-specific chat history

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/login` | Login user | No |
| POST | `/auth/token` | OAuth2 compatible login | No |
| GET | `/auth/me` | Get current user info | Yes |
| GET | `/auth/users` | List all users | Yes (Admin) |
| GET | `/auth/users/{user_id}` | Get user by ID | Yes (Admin) |

### Chat Routes (New Authenticated Endpoints)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/chat/authenticated` | Chat with authenticated user | Yes |
| GET | `/history/me` | Get my chat history | Yes |
| DELETE | `/history/me` | Delete my chat history | Yes |

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "securepassword123",
       "full_name": "Test User"
     }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "securepassword123"
     }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Protected Endpoints

```bash
# Get current user info
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Authenticated chat
curl -X POST "http://localhost:8000/chat/authenticated" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [
         {"role": "user", "content": "Hello, I am authenticated!"}
       ]
     }'
```

## Environment Variables

Add these to your `.env` file:

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Collections

The authentication system creates a `users` collection in MongoDB with the following structure:

```javascript
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "hashed_password": "$2b$12$...", // bcrypt hash
  "is_active": true,
  "is_admin": false,
  "created_at": ISODate("2025-09-21T..."),
  "updated_at": ISODate("2025-09-21T...")
}
```

## Creating an Admin User

Run the admin creation script:

```bash
poetry run python scripts/create_admin.py
```

This creates an admin user with:
- Username: `admin`
- Email: `admin@campus.edu`
- Password: `admin123` (⚠️ Change this in production!)

## Security Features

1. **Password Hashing**: Uses bcrypt with salt rounds
2. **JWT Tokens**: Secure token-based authentication
3. **Token Expiration**: Configurable token lifetime
4. **Role-Based Access**: Admin vs regular user permissions
5. **Input Validation**: Pydantic models validate all inputs
6. **CORS Support**: Configured for frontend integration

## Dependencies Added

The following packages were added to `pyproject.toml`:

```toml
python-jose = { version = "^3.3.0", extras = ["cryptography"] }
passlib = { version = "^1.7.4", extras = ["bcrypt"] }
python-multipart = "^0.0.9"
```

## Next Steps for Frontend

1. Create login/signup forms
2. Store JWT tokens (localStorage/sessionStorage)
3. Add Authorization headers to API calls
4. Handle token expiration and refresh
5. Implement role-based UI features

## File Structure

```
backend/
├── models/
│   └── user.py              # User data models
├── routers/
│   └── auth.py              # Authentication routes
├── services/
│   ├── auth.py              # JWT and password utilities
│   └── users.py             # User database operations
├── scripts/
│   └── create_admin.py      # Admin user creation
└── schemas.py               # Updated with auth schemas
```

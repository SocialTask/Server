
# API Documentation

## Authentication Endpoints

### Register a New User

- **URL**: `/register`
- **Method**: `POST`
- **Request Body**:
  - `username`: String (required) - Username of the user.
  - `email`: String (required) - Email address of the user.
  - `password`: String (required) - Password for the user account.

#### Request Example:

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 400

##### Success Response Body:

```json
{
  "message": "User registered successfully and logged in",
  "token": "<JWT_TOKEN>"
}
```

##### Error Response Body:

```json
{
  "error": "User registration failed",
  "message": "Reason for failure"
}
```

### User Login

- **URL**: `/login`
- **Method**: `POST`
- **Request Body**:
  - `email`: String (required) - Email address of the user.
  - `password`: String (required) - Password for the user account.

#### Request Example:

```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 401 (Unauthorized), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "Login successful",
  "token": "<JWT_TOKEN>"
}
```

##### Error Response Body:

```json
{
  "error": "Invalid credentials",
  "message": "Reason for failure"
}
```

```json
{
  "error": "Login failed",
  "message": "Reason for failure"
}
```


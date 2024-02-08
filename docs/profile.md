# API Documentation

## Profile Endpoints

### Upload Picture

- **URL**: `/upload-picture`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Request Body:
- `file`: File - Image file to be uploaded.
- `file_type`: String - Type of the file (either 'profile_picture' or 'cover_photo').

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 400 (Bad Request), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "file_url": "<image_url>"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to upload file",
  "message": "Reason for failure"
}
```

### Profile

- **URL**: `/profile`
- **Methods**: `GET`, `PUT`
- **Authorization**: Bearer Token Required

#### GET Request:
- Retrieves the profile information of the authenticated user.

#### PUT Request:
- Updates the profile information of the authenticated user.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 404 (Not Found), 500 (Internal Server Error)

##### Success Response Body (GET):

```json
{
  "id": <user_id>,
  "username": "<username>",
  "email": "<email>",
  "profile_pic_url": "<profile_pic_url>",
  "privacy_setting": "<privacy_setting>",
  "made_tasks": <made_tasks>,
  "points": <points>,
  "verified": <verified>,
  "description": "<description>",
  "cover_photo_url": "<cover_photo_url>",
  "followers_count": <followers_count>,
  "following_count": <following_count>
}
```

##### Success Response Body (PUT):

```json
{
  "message": "Profile updated successfully"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to fetch/update user profile",
  "message": "Reason for failure"
}
```
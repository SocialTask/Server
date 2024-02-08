# API Documentation

## Follow Endpoints

### Follow a User

- **URL**: `/follow/<int:user_id_to_follow>`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Request Parameters:
- `user_id_to_follow`: Integer (required) - ID of the user to follow.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "You are now following this user"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to follow user",
  "message": "Reason for failure"
}
```

### Unfollow a User

- **URL**: `/unfollow/<int:user_id_to_unfollow>`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Request Parameters:
- `user_id_to_unfollow`: Integer (required) - ID of the user to unfollow.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "You have unfollowed this user"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to unfollow user",
  "message": "Reason for failure"
}
```

### Check Follow Status

- **URL**: `/followStatus/<int:user_id_to_check>`
- **Method**: `GET`
- **Authorization**: Bearer Token Required

#### Request Parameters:
- `user_id_to_check`: Integer (required) - ID of the user to check the follow status for.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "isFollowing": true
}
```

- `isFollowing`: Boolean - Indicates whether the current user is following the specified user.

##### Error Response Body:

```json
{
  "error": "Failed to check follow status",
  "message": "Reason for failure"
}
```

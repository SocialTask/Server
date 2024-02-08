# API Documentation

## Posts Endpoints

### Create a Post

- **URL**: `/post`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Request Body:
- `text`: String - Text content of the post.
- `media`: File - Media file (image or video) to be attached to the post.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "Post created successfully",
  "post_id": <post_id>
}
```

##### Error Response Body:

```json
{
  "error": "Failed to create post",
  "message": "Reason for failure"
}
```

### Get Posts

- **URL**: `/posts`
- **Method**: `GET`
- **Authorization**: Bearer Token Required

#### Query Parameters:
- `page`: Integer (optional) - Page number of the posts.
- `per_page`: Integer (optional) - Number of posts per page.

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 500 (Internal Server Error)

##### Success Response Body:

```json
[
  {
    "id": <post_id>,
    "user_id": <user_id>,
    "img_raw": <raw_image_url>,
    "img_compressed": <compressed_image_url>,
    "video_url": <video_url>,
    "video_thumbnail": <video_thumbnail_url>,
    "text": "Post content",
    "created_at": "2024-02-05T12:00:00Z",
    "upvotes": 10,
    "downvotes": 5
  },
  { ... }
]
```

##### Error Response Body:

```json
{
  "error": "Error retrieving posts",
  "message": "Reason for failure"
}
```

### Get User Posts

- **URL**: `/user/<username>/posts`
- **Method**: `GET`
- **Authorization**: Bearer Token Required

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 404 (Not Found), 500 (Internal Server Error)

##### Success Response Body:

```json
[
  {
    "id": <post_id>,
    "user_id": <user_id>,
    "img_raw": <raw_image_url>,
    "img_compressed": <compressed_image_url>,
    "video_url": <video_url>,
    "video_thumbnail": <video_thumbnail_url>,
    "text": "Post content",
    "created_at": "2024-02-05T12:00:00Z",
    "upvotes": 10,
    "downvotes": 5
  },
  { ... }
]
```

##### Error Response Body:

```json
{
  "error": "Failed to retrieve user posts",
  "message": "Reason for failure"
}
```

### Delete a Post

- **URL**: `/post/<post_id>`
- **Method**: `DELETE`
- **Authorization**: Bearer Token Required

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 404 (Not Found), 403 (Forbidden), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "Post deleted successfully"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to delete post",
  "message": "Reason for failure"
}
```

### Upvote a Post

- **URL**: `/post/<post_id>/upvote`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 401 (Unauthorized), 400 (Bad Request), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "Upvote added successfully"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to add upvote",
  "message": "Reason for failure"
}
```

### Downvote a Post

- **URL**: `/post/<post_id>/downvote`
- **Method**: `POST`
- **Authorization**: Bearer Token Required

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 401 (Unauthorized), 400 (Bad Request), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "message": "Downvote added successfully"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to add downvote",
  "message": "Reason for failure"
}
```
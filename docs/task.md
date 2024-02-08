## Task Endpoints

### Get Selected Task

- **URL**: `/task`
- **Method**: `GET`
- **Authorization**: Bearer Token Required

#### Response:
- **Success Response Code**: 200
- **Error Response Code**: 404 (Not Found), 500 (Internal Server Error)

##### Success Response Body:

```json
{
  "TaskID": "<task_id>",
  "Name": "<task_name>",
  "Description": "<task_description>",
  "Category": "<task_category>",
  "Explanation": "<task_explanation>",
  "Feature1": "<task_feature1>",
  "Feature2": "<task_feature2>",
  "Feature3": "<task_feature3>"
}
```

##### Error Response Body:

```json
{
  "error": "Failed to retrieve task details",
  "message": "Reason for failure"
}
```
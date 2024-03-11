# Notification API documentation

--------------------------------------------------------------------------------

## `/notification/user/`

### Send a notification to a list of users

<details>
 <summary><code>POST</code> <code><b>/notification/user/</b></code></summary>

### Request

#### Body

> | name                     | type      | description        | requirement |
> |--------------------------|-----------|--------------------|-------------|
> | `title`                  | String    | Notification title | Required    |
> | `type`                   | String    | Notification type  | Required    |
> | `user_list`              | list[int] | User ids           | Required    |
> | `data`                   | string    | Notification data  | Optional    |

[Allowed types (see `ALLOWED_USER_TYPES` variable)](../src/notification/settings.py)

### Response

#### Status code

> | status code | content-type       | response                             |
> |-------------|--------------------|--------------------------------------|
> | `201`       | `application/json` | {"message": "Notification created"}  |
> | `400`       | `application/json` | {"errors": [...]}                    |
> | `500`       | `application/json` | {"errors": [...]}                    |

</details>

--------------------------------------------------------------------------------

## `/notification/user/{notification_id}/`

### Delete a notification

<details>
 <summary><code>DELETE</code> <code><b>/notification/user/{notification_id}/</b></code></summary>

### Request

#### Body

None

### Response

#### Status code

> | status code | content-type       | response                            |
> |-------------|--------------------|-------------------------------------|
> | `201`       | `application/json` | {"message": "Notification deleted"} |
> | `400`       | `application/json` | {"errors": [...]}                   |
> | `500`       | `application/json` | {"errors": [...]}                   |

</details>

--------------------------------------------------------------------------------

## `/notification/friend/add/`

### Send status of two new friends

<details>
 <summary><code>POST</code> <code><b>/notification/friend/add/</b></code></summary>

Sends a `friend_status` notification with the status of the new friend

### Request

#### Headers

> | name             | type   | description   | requirement |
> |------------------|--------|---------------|-------------|
> | `Authorization`  | String | Service token | Required    |

#### Body

> | name               | type        | description          | requirement |
> |--------------------|-------------|----------------------|-------------|
> | `new_relationship` | `list[int]` | New friends' user_id | Required    |

### Response

#### Status code

> | status code | content-type       | response                         |
> |-------------|--------------------|----------------------------------|
> | `200`       | `application/json` | {"message": "Notification sent"} |
> | `400`       | `application/json` | {"errors": [...]}                |
> | `500`       | `application/json` | {"errors": [...]}                |

</details>

--------------------------------------------------------------------------------

## `/notification/friend/delete/`

### Send a notification to delete a friend

<details>
 <summary><code>POST</code> <code><b>/notification/friend/delete/</b></code></summary>

Sends a `friend_status` notification with status `deleted`.

### Request

#### Headers

> | name             | type   | description   | requirement |
> |------------------|--------|---------------|-------------|
> | `Authorization`  | String | Service token | Required    |

#### Body

> | name                   | type        | description              | requirement |
> |------------------------|-------------|--------------------------|-------------|
> | `deleted_relationship` | `list[int]` | Deleted friends' user_id | Required    |

### Response

#### Status code

> | status code | content-type       | response                         |
> |-------------|--------------------|----------------------------------|
> | `200`       | `application/json` | {"message": "Notification sent"} |
> | `400`       | `application/json` | {"errors": [...]}                |
> | `500`       | `application/json` | {"errors": [...]}                |

</details>

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

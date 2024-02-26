# User Management

--------------------------------------------------------------------------------

## `/user/signup/`

### Account creation

will send an email to the user with a link to confirm the account

<details>
 <summary><code>POST</code><code><b>/user/signup/</b></code></summary>

### Parameters

#### Body
all fields are mandatory
- Username must be unique and between 1 and 20 characters long
- Email must be unique and between 1 and 50 characters long
- Password must be between 8 and 50 characters long and contain at least one uppercase letter, one digit and one special character
> ``` javascript
> {
>     "username": "Aurel",
>     "email": "alevra@student.42lyon.fr",
>     "password": "Validpass42*"
> }
> ```

#### Responses

> | http code | content-type       | response                                                  |
> |-----------|--------------------|-----------------------------------------------------------|
> | `201`     | `application/json` | `{"message": "Account created, Verification email sent"}` |
> | `401`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`                       |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}`      |

</details>

## `user/verify-email/<id>/<token>`

### Verify the email of the user (and so the account)

will return 200 if successful

<details>
 <summary><code>POST</code><code><b>/user/verify-email/</b></code></summary>


#### Responses

> | http code | content-type       | response                                                                      |
> |-----------|--------------------|-------------------------------------------------------------------------------|
> | `200`     | `application/json` | `{'message': 'user verified', 'refresh_token': refresh_token}`                |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                                         |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}`                          |

</details>


## `/user/signin/`

### User connection

will return a refresh token when successful

<details>
 <summary><code>POST</code> <code><b>/user/signin/</b></code></summary>

### Parameters

#### Body

mandatory fields :
- login (username or email) 
- password

optional fields :
- 2fa_code : if the user has 2FA enabled, this field is mandatory

> ``` javascript
> {
>     "login": "Aurel",
>     "password": "Validpass21*",
>     "2fa_code": "123456"
> }
> ```

#### Responses

> | http code | content-type               | response                                             |
> |-----------|----------------------------|------------------------------------------------------|
> | `201`     | `application/json`         | `{"refresh_token": "eyJhbGci.."}`                    |
> | `401`     | `application/json`         | `{"errors": [ "AAA","BBB", "..."], '2fa': true}`     |
> | `500`     | `application/json`         | `{"errors": ['An unexpected error occurred : ...']}` |

</details>


## `/user/username-exist/`

### Check if username is already taken

will return a boolean

<details>
 <summary><code>POST</code> <code><b>/user/username-exist/</b></code></summary>

### Parameters

#### Body

> ``` javascript
> {
>     "username": "Aurel"
> }
> ```

#### Responses

> | http code | content-type             | response                                             |
> |-----------|--------------------------|------------------------------------------------------|
> | `200`     | `application/json`       | `{"is_taken": false}`                                |
> | `200`     | `application/json`       | `{"is_taken": true}`              n                  |
> | `401`     | `application/json`       | `{"errors": [ "AAA","BBB", "..."]}`                  |
> | `500`     | `application/json`       | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/email-exist/`

### Check if email is already taken

will return a boolean

<details>
 <summary><code>POST</code> <code><b>/user/email-exist/</b></code></summary>

### Parameters

#### Body

> ``` javascript
> {
>     "email": "..."
> }
> ```

#### Responses

> | http code | content-type             | response                                             |
> |-----------|--------------------------|------------------------------------------------------|
> | `200`     | `application/json`       | `{"is_taken": false}`                                |
> | `200`     | `application/json`       | `{"is_taken": true}`                                 |
> | `401`     | `application/json`       | `{"errors": [ "AAA","BBB", "..."]}`                  |
> | `500`     | `application/json`       | `{"errors": ['An unexpected error occurred : ...']}` |

</details>


## `/user/refresh-access-jwt/`

### Trade a valid refresh token for an access token

will return an access token when successful

<details>
 <summary><code>POST</code><code><b>/user/refresh-access-jwt/</b></code></summary>

### Parameters

#### Body
all fields are mandatory
> ``` javascript
> {
>     "refresh_token": "234235sfs3r2.."
> }
> ```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"access_token": "eyJhbGci.."}`                     |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`                  |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>


## `/user/forgot-password/send-code/`

### Send a code to the user's email

will return 200 if successful and send a 6 alphanum code to the user's email

<details>
 <summary><code>POST</code><code><b>/user/forgot-password/send-code/</b></code></summary>

### Parameters

#### Body
all fields are mandatory
> ``` javascript
> {
>     "email": "..."
> }
> ```

#### Responses

> | http code | content-type       | response                                                                                          |
> |-----------|--------------------|---------------------------------------------------------------------------------------------------|
> | `200`     | `application/json` | `{"ok": "Email sent","email": "************ra@gmail.com", "expires": "2024-01-10T11:20:43.253"}}` |
> | `400`     | `application/json` | `{"errors": "AAA"}`                                                                               |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}`                                              |


</details>

## `/user/forgot-password/check-code/`

### Verify the code sent by email

will return 200 if successful

<details>
 <summary><code>POST</code><code><b>/user/forgot-password/check-code/</b></code></summary>

### Parameters

#### Body
all fields are mandatory
> ``` javascript
> {
>     "email": "...",
>     "code": "..."
> }
> ```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"ok": "ok"}`                                       |
> | `400`     | `application/json` | `{"errors": "AAA", errors details : "aaa" }`         |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |


</details>


## `/user/forgot-password/change-password/`

### Change the password of the user with the given code

will return 200 if successful,
change the user password,
revoke the code given by email

<details>
 <summary><code>POST</code><code><b>/user/forgot-password/change-password/</b></code></summary>

### Parameters

#### Body
all fields are mandatory
> ``` javascript
> {
>     "email": "...",
>     "code": "..."
>     "new_password": "..."
> }
> ```

</details>


## `/user/id/{user-id}/`
### Get user non-sensitive information

will return public user information

<details>
 <summary><code>GET</code><code><b>/user/{user_id}/</b></code></summary>

### Headers

Authorization: {access_token}

#### In the URL (mandatory)
 {user_id}
> 
> NB : user_id must be an integer
> 
#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"id": "1", "username": "tdameros"}`                |
> | `400`     | `application/json` | `{"errors": "AAA", errors details : "aaa" }`         |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |


</details>

## `/user/id-list/`

### Get a list of user ids

will return a list of user ids

<details>
 <summary><code>POST</code><code><b>/user/id_list/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

> ``` javascript
> 
> {
>     "id_list": [1, 2, 3]
> }

> NB : id_list could be a list of integers or strings (ex : ["1", "2", "3"])
>
> if a user is not found, it will not be in the response

#### Responses

200 :
```javascript

[
    {
        "2": "Aurel1243",
        "3": "Aurel121233"
    }
]
```

If you want to retrieve a username, you should do something like :
```py
result.json().get(str(id))
```
nb :I cannot respond with id as int because keys are converted to strings in the json response

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `...`                                                |
> | `400`     | `application/json` | `{"errors": ["AAA"]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/{username}/`
### Get user non-sensitive information

will return public user information

<details>
 <summary><code>GET</code><code><b>/user/{username}/</b></code></summary>

### Headers

Authorization: {access_token}

#### In the URL (mandatory)
{username}
>
> NB : username must be a string
>
#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"id": "1", "username": "tdameros"}`                |
> | `400`     | `application/json` | `{"errors": "AAA", errors details : "aaa" }`         |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |


</details>

## `/user/search-username/`

### Search for a username

will return a list of usernames that contains the searched username

<details>
 <summary><code>POST</code><code><b>/user/search-username/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

> ``` javascript
>   
> {
>    "username": "Aurel"
> }
> ```
> 
> NB : An empty username will return an error "Username not found"

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"usernames": ["Aurel", "Aurel2", "Aurel3"]}`       |
> | `400`     | `application/json` | `{"errors": ["AAA"]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>


## `/user/oauth/{oauth-service}/`
### Initiate OAuth authentication for the specified service

This endpoint initiates the OAuth authentication process for the specified authentication service.
It returns a redirection URL to the OAuth service's authorization endpoint.
<details>
 <summary><code>GET</code><code><b>/user/oauth/{auth_service}/?source=https://example.com</b></code></summary>

### Parameters

#### In the URL (mandatory)
 {auth_service}
 and as a query parameter :
- `source`: The URL to which the OAuth service will redirect the user after authentication
> 
> NB: `auth_service` must be one of the following values: 'github', '42api'
> and `source` must be a valid URL wich does not begin with www but with http or https
> 
#### Responses

> | http code | content-type       | response                                                                                                               |
> |-----------|--------------------|------------------------------------------------------------------------------------------------------------------------|
> | `200`     | `application/json` | `{"redirection_url": "https://oauth-service.com/authorize?client_id=XXX&redirect_uri=YYY&state=ZZZ&scope=user:email"}` |
> | `400`     | `application/json` | `{"errors": ["Unknown auth service"]}`                                                                                 |

NB : if the user cancel oauth2, it will be redirect to the source URI specified, with an error message in the query parameters 
and no refresh token will be created

</details>

## `/user/oauth/callback/{auth-service}/`
### OAuth Callback for the specified service

This endpoint handles the callback after successful OAuth authentication and retrieves the user's information.

<details>
 <summary><code>GET</code><code><b>/user/oauth/callback/{auth_service}/</b></code></summary>

### Parameters

#### In the URL (mandatory)
 {auth_service}
> 
> NB: `auth_service` must be one of the following values: 'github', '42api'
> 
#### In the Query Parameters (mandatory)
- `code`: Authorization code obtained from the OAuth service
- `state`: State parameter to prevent CSRF attacks

#### Responses

> | http code | content-type       | response                                                                        |
> |-----------|--------------------|---------------------------------------------------------------------------------|
> | `201`     | `application/json` | `redirect to source, putting the refresh token in a cookie named refresh_token` |
> | `400`     | `application/json` | `{"errors": ["Failed to retrieve access token"]}`                               |
> | `400`     | `application/json` | `{"errors": ["Invalid state"]}`                                                 |
> | `400`     | `application/json` | `{"errors": ["Failed to create or get user"]}`                                  |
> | `400`     | `application/json` | `{"errors": ["An unexpected error occurred : ..."]}`                            |
> | `500`     | `application/json` | `{"errors": ['Failed to create or get user']}`                                  |

</details>

## `/user/update-infos/`


### Update user's information

will return 200 if successful

<details>
 <summary><code>POST</code><code><b>/user/update-infos/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

mandatory field : change_list, access_token
all other fields are optional and depend on the change_list

> ``` javascript
> {
>   "change_list": ["username", "email", "password"]
>    "username": "NewUsername",
>    "email": "newemail@asdf.fr",
>   "password": "NewPassword42*"
> }
> NB : change_list must contain at least one of the following values : "username", "email", "password"
> ```


#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"ok": "ok"}`                                       |
> | `400`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`                  |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |


</details>

## `/user/2fa/enable`
### Enable Two-Factor Authentication

This endpoint enables Two-Factor Authentication for the user.

<details>
 <summary><code>POST</code><code><b>/user/2fa/enable</b></code></summary>

### Headers

Authorization: {access_token}

#### Responses


> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `image/png`        | `png of the QR code the user needs to scan`          |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |
</details>

## `/user/2fa/disable`

### Disable Two-Factor Authentication

This endpoint disables Two-Factor Authentication for the user.

<details>
 <summary><code>POST</code><code><b>/user/2fa/disable</b></code></summary>

### Headers

Authorization: {access_token}

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "2fa disabled"}`                        |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |
If the user already have 2FA disabled, the response will be :
400 `{"errors": ["2FA is already disabled"]}`
else
200 `{'message': '2fa disabled'}`

</details>

## `/user/2fa/verify`


### Verify Two-Factor Authentication

This endpoint verifies the user's Two-Factor Authentication code.

<details>
 <summary><code>POST</code><code><b>/user/2fa/verify</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

All fields mandatory:

> ``` javascript
> {
>    "code": "123456"
> }
> ```
#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "2fa verified"}`                        |
> | `400`     | `application/json` | `{"errors": ["...]}`                                 |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |
****
</details>

## `/user/friends/`

### Get user's friends

This endpoint retrieves the user's friend list.

<details>
 <summary><code>GET</code><code><b>/user/friends/</b></code></summary>

### Headers

Authorization: {access_token}

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"friends": [{"id": 1, "status": accepted}, ...]}`  |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

### Delete a friend

This endpoint delete a friend of the user

<details>
 <summary><code>DELETE</code><code><b>/user/friends/</b></code></summary>

### Headers

Authorization: {access_token}

#### Query

> | name        | data type | description | type      |
> |-------------|-----------|-------------|-----------|
> | `friend_id` | int       | Friend's id | Required  |

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "friend deleted"}`                      |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/friends/request/`

### Send a friend request

This endpoint send a friend request

<details>
 <summary><code>POST</code><code><b>/user/friends/request/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

All fields mandatory:

> ```json
> {
>    "friend_id": 1
> }
> ```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "friend request sent"}`                 |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/friends/accept/`

### Accept a friend request

This endpoint is used to accept a friend request

<details>
 <summary><code>POST</code><code><b>/user/friends/accept/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

All fields mandatory:

> ```json
> {
>    "friend_id": 1
> }
> ```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "friend request accepted"}`             |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/friends/decline/`

### Decline a friend request

This endpoint is used to decline a friend request

<details>
 <summary><code>POST</code><code><b>/user/friends/decline/</b></code></summary>

### Headers

Authorization: {access_token}

#### Body

All fields mandatory:

> ```json
> {
>    "friend_id": 1
> }
> ```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "friend request declined"}`             |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/delete-account/`

### Anonymize user's account

This endpoint anonymizes the user's account.

<details>
 <summary><code>DELETE</code><code><b>/user/delete-account/</b></code></summary>

### Headers

Authorization: {access_token}

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "account deleted"}`                     |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

## `/user/avatar/`

This endpoint allows the user to get and update his avatar.

### Get user's avatar

<details>
 <summary><code>GET</code><code><b>/user/avatar/</b></code></summary>

### Parameters


#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `image/png`        | `png of the user's avatar`                           |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>


### Update user's avatar

<details>
 <summary><code>POST</code><code><b>/user/avatar/</b></code></summary>

### Parameters

Authorization: {access_token}

#### Body

all fields are mandatory

```json
{
    "avatar": "base64 of the new avatar"
}
```

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "avatar updated"}`                      |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

### Delete user's avatar

<details>
 <summary><code>DELETE</code><code><b>/user/avatar/</b></code></summary>

### Parameters

Authorization: {access_token}

#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"message": "avatar deleted"}`                      |
> | `400`     | `application/json` | `{"errors": ["..."]}`                                |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

</details>

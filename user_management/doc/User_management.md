# User Management

--------------------------------------------------------------------------------

## `/user/signup/`

### Account creation

will return a refresh token when successful

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

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `201`     | `application/json` | `{"refresh_token": "eyJhbGci.."}`                    |
> | `401`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}`                  |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

>errors can be combined

> errors can be :
> - Username empty
> - Username already taken
> - Username length {len(username)} > 20
> - Username must be alphanumeric

> - Email {email} already taken
> - Email empty
> - Email length {len(email)} > 50
> - Email missing @
> - Email missing "." character
> - Email contains more than one @ character

> - Password empty
> - Password length {len(password)} < 8
> - Password missing uppercase character
> - Password missing digit
> - Password missing special character

> - Invalid JSON format in the request body
> - An unexpected error occurred
</details>


## `/user/signin/`

### User connection

will return a refresh token when successful

<details>
 <summary><code>POST</code> <code><b>/user/signin/</b></code></summary>

### Parameters

#### Body

all fields are mandatory

> ``` javascript
> {
>     "username": "Aurel",
>     "password": "Validpass21*"
> }
> ```

#### Responses

> | http code | content-type               | response                                             |
> |-----------|----------------------------|------------------------------------------------------|
> | `201`     | `application/json`         | `{"refresh_token": "eyJhbGci.."}`                    |
> | `401`     | `application/json`         | `{"errors": [ "AAA","BBB", "..."]}`                  |
> | `500`     | `application/json`         | `{"errors": ['An unexpected error occurred : ...']}` |
> 
> errors can be combined

> errors can be :
> - Username empty
> - Password empty
> - Username not found
> - Invalid password
> - Invalid JSON format in the request body
> - An unexpected error occurred

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

> 
> errors can be combined

> errors can be :
> - Invalid JSON format in the request body
> - An unexpected error occurred
> 
> NB : An empty username is considered as not taken

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

> 
> errors can be combined

> errors can be :
> - Empty email
> - Invalid JSON format in the request body
> - An unexpected error occurred

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

>errors can be combined

> errors can be :
> - Refresh token not found
> - Signature verification failed
> - No expiration date found
> - Signature has expired
> - No user_id in payload
> - User does not exist
> - Invalid JSON format in the request body
> - An unexpected error occurred
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


> errors can be :
> - No email provided
> - Email can not be empty
> - Username not found
> - Invalid JSON format in the request body : decode error
> - An unexpected error occurred

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

> errors details are optional

> errors can be :
> - Mandatory value missing : 'email'
> - Mandatory value missing : 'code'
> - Email empty
> - Code empty
> - Username not found
> - Invalid code
> - Code expired

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


## `/user/{user-id}/`
### Get user non-sensitive information

will return a user object when successful
Might be extended to return more information in the future, if needed

<details>
 <summary><code>GET</code><code><b>/user/{user_id}/</b></code></summary>

### Parameters

#### In the URL (mandatory)
 {user_id}
> 
> NB : user_id must be an integer
> 
#### Responses

> | http code | content-type       | response                                             |
> |-----------|--------------------|------------------------------------------------------|
> | `200`     | `application/json` | `{"ok": "ok"}`                                       |
> | `400`     | `application/json` | `{"errors": "AAA", errors details : "aaa" }`         |
> | `500`     | `application/json` | `{"errors": ['An unexpected error occurred : ...']}` |

> errors details are optional

> errors can be :
> - Mandatory value missing : 'username'
> - Mandatory value missing : 'code'
> - Mandatory value missing : 'password'
> - Email empty
> - Code empty
> - Username not found
> - Invalid code
> - Code expired
> - (all the errors from the is_valid_password function in the sign_up route)


</details>

## `/user/search-username/`

### Search for a username

will return a list of usernames that contains the searched username

<details>
 <summary><code>POST</code><code><b>/user/search-username/</b></code></summary>

### Parameters

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

> 
> errors can be :
> - Invalid JSON format in the request body
> - An unexpected error occurred
> - No username found
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
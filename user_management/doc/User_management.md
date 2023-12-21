# User Management

--------------------------------------------------------------------------------

## `signup`

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

> | http code | content-type       | response                            |
> |-----------|--------------------|-------------------------------------|
> | `201`     | `application/json` | `{"refresh_token": "eyJhbGci.."}`   |
> | `401`     | `application/json` | `{"errors": ["AAA", "BBB", "..."]}` |

>errors can be combined

> errors can be :
> - Username empty
> - Username already taken
> - Username length {len(username)} > 20

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


## `signin`

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

> | http code | content-type               | response                            |
> |-----------|----------------------------|-------------------------------------|
> | `201`     | `application/json`         | `{"refresh_token": "eyJhbGci.."}`   |
> | `401`     | `application/json`         | `{"errors": [ "AAA","BBB", "..."]}` |
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


## `username-exist`

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

> | http code | content-type               | response                            |
> |-----------|----------------------------|-------------------------------------|
> | `200`     | `application/json`         | `{"is_taken": false}`               |
> | `200`     | `application/json`         | `{"is_taken": true}`                |
> | `401`     | `application/json`         | `{"errors": [ "AAA","BBB", "..."]}` |
> 
> errors can be combined

> errors can be :
> - Invalid JSON format in the request body
> - An unexpected error occurred
> 
> NB : An empty username is considered as not taken

</details>
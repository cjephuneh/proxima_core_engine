Usage
=====


# Authentication

### Params
* `context` 

### Notes
* Enable all users to signin 

### Example
#### Request
```
/api/auth/signin
```

#### Response
```
{
    "email": "employee@mail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwiZXhwIjoxNjg1ODcyMjU2fQ.aEZSq4gq5_eV2uDFwpEBvm1562aaeMUAFPqOuNw-qfY",
    "user_type": "employee"
}
```

### Params
* `context` 

### Notes
* Register organization admin user

### Example
#### Request
```
/api/auth/admin
```

#### Response
```
{
    "username": "testadmin",
    "email": "testadmin@mail.com",
    "first_name": "test",
    "last_name": "admin",
    "phonenumber": "0790001947",
    "gender": "Male",
    "DOB": null,
    "user_type": "admin",
    "tenant_id": 1
}

```

### Params
* `context` 

### Notes
* Register anonymous user

### Example
#### Request
```
/api/auth/anonymoususer
```

#### Response
```

```

### Params
* `context` 

### Notes
* Register users who will seek assistance from organizations 

### Example
#### Request
```
/api/auth/client
```

#### Response
```
{
    "username": "testclient2",
    "email": "testclient2@mail.com",
    "first_name": "testclient",
    "last_name": "test",
    "phonenumber": "07936818408",
    "gender": "Male",
    "DOB": "1999-09-01",
    "user_type": "client"
}
```

### Params
* `context` 

### Notes
* Register organization employee

### Example
#### Request
```
/api/auth/employee
```

#### Response
```
{
    "username": "employee",
    "email": "employee@mail.com",
    "first_name": "employee",
    "last_name": "employee",
    "phonenumber": "079368184099",
    "gender": "Male",
    "DOB": null,
    "user_type": "employee",
    "tenant_id": 1
}
```

### Params
* `context` 

### Notes
* Enable any user to change password 

### Example
#### Request
```
/api/auth/changepassword
```

#### Response
```

```

### Params
* `context` 

### Notes
* Enable user to say they forgot their password 

### Example
#### Request
```
/api/auth/forgotpassword
```

#### Response
```

```

### Params
* `context` 

### Notes
* Activate a user after they have signed up 

### Example
#### Request
```
/api/auth/activate_user/<str:uid>/<str:token>/<str:activation_key>/$
```

#### Response
```

```

### Params
* `context` 

### Notes
* Resend invitation link to user incase they did not get one

### Example
#### Request
```
/api/auth/resendactivationlink
```

#### Response
```

```

### Params
* `context` 

### Notes
* Enable a useer to reset their password

### Example
#### Request
```
/api/auth/reset_password/<str:uid>/<str:token>/$
```

#### Response
```

```



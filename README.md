# EmployeeEventsManagement

## Configurations to run the server

When running the server take into account that you should create a .env file with the following parameters:

- For Django its required a secret key. It should go in DJANGO_SECRET_KEY parameter and it can be obtained using the following command.

```shell
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

- In order to set the configuration of the email there should the following parameters. An example is presented with the values required for an outlook account.

```python
DJANGO_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DJANGO_EMAIL_PORT = 587
DJANGO_EMAIL_USE_TLS = True
DJANGO_EMAIL_HOST = 'smtp-mail.outlook.com'
DJANGO_EMAIL_HOST_USER = '***@outlook.com'
DJANGO_EMAIL_HOST_PASSWORD = '***'
DJANGO_EMAIL_USE_SSL = False
```

- Related to the email as well is the daily report subscriber list that for the moment is configured in .env
```python
EMAIL_DAILY_REPORT_SUBSCRIBERS = ['***']
```

- To enable the holiday API request it is required to set the abstract's Public Holidays API key 
```python
HOLIDAY_API_KEY="***"
```

To store the holidays api responses there is a data base cache configured so in order to use it the following line must de run

```shell
python manage.py createcachetable
```


### Authentication

To have access to the API the header of the calls must include "Authorization: Token {{token}}"

This token can be obtained using the /api-token-auth endpoint and sending in the body, in json format, username and password. These are from Users that must be created using Django admin. A token can be generated as well using drf_create_token

```shell
python manage.py drf_create_token <<username>>
```

### Endpoints
Complete examples of the endpoints are included in EmployeeEventManagement.postman_collection.json inside collections folder.

The collection list is 
- Get authentication token
    POST - returns the token required for authentication and receives the username and password of a User
- Create employee
    POST - tasked with the creation of new employees.
- Delete employee logically
    DELETE - deletes a specific employee by setting it as not active.
- Update employee
    PUT - updates (first_name", "last_name", "email" and "is_active") to the employee with the requested id
- Update employee fields
    PATCH - updates (first_name", "last_name", "email" or "is_active") to the employee with the requested id
- List active employees
    GET - lists all employees set as active
- List all employees
    GET - lists all employees 
- Get employee by id
    GET - gets the employee with the requested id
- Search employee
    GET - lists all employees in accordance with the filters (first_name", "last_name", "email" or "is_active")
- Following events
    POST - returns the events that are registered for the next 3 days



## Events Daily Report

To activate the 8 AM events daily report use the following command
```python
python manage.py crontab add
```

To deactivate it use the following command
```python
python manage.py crontab remove
```

## Testing
There are tests for the endpoints developed in api_v1. There are three files dedicated to the employee, to the following events and for the following holiday endpoints. There are tests of ok results, of bad requests and of no authorization.
```python
manage.py test api_v1 
```

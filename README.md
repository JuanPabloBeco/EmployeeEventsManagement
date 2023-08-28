# EmployeeEventsManagement

## Authentication

To have access to the API the header of the calls must include "Authorization: Token {{token}}"

This token can be obtained using the /api-token-auth endpoint and sending in the body, in json format, username and password


## Events Daily Report

To activate the 8 AM events daily report use the following command
```python
python manage.py crontab add
```

To deactivate it use the following command
```python
python manage.py crontab remove
```

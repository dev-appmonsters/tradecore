# Tradecore-Test-task
## Prerequisites

 - Python:3.8.5
 - Redis

## Setup

Setup project environment with `virtualenv` and `pip`.

```bash
$ virtualenv venv
$ source venv/bin/activate
```

After activating the environment, run below command where    `requirements.txt` is present, to install the dependencies.

``` (venv)$ pip install -r requirements.txt ```

Run below commands inside the root directory(where `manage.py` is present) of the project.
For migrations, `python manage.py migrate`
To start server, `python manage.py runserver`
Navigate to `http://127.0.0.1:8000/`

Before starting celery workers for asynchronous tasks for user data enrichment, we need to export below `ENVIRONMENT VARIABLES`

    HOLIDAYS_API_KEY
    IP_GEOLOCATION_API_KEY
Both the above ones can be obtained from [abstractapi](https://www.abstractapi.com/)'s(third Party integration used for user data enrichment task) dashboard, after successfully signing up on it.

After setting up the `ENVIRONMENT VARIABLES`, run below command to start the celery workers.

    celery -A project worker -l info

##  API Endpoints

#####  /signup/
Method: `POST`
Required Params:
```
{
    "email": "",
    "first_name": "",
    "last_name": "",
    "password": "",
    "confirm_password": ""
}
```

#####    /token/obtain/
Method: `POST`
Required Params:
```
{
    "email": "",
    "password": ""
}
```

#####    /token/refresh/
Method: `POST`
Required Params:
```
{
    "refresh": ""
}
```

#####    /user/{id}/
Method: `GET`

#####    /posts/
Method: `GET`

#####    /posts/
Authentication Required
Method: `POST`
```
{
    "title": "",
    "content": ""
}
```

#####    /posts/{id}/
Authentication Required
Method: `GET`

#####    /posts/{id}/
Authentication Required
Method: `DELETE`

#####    /posts/{id}/
Authentication Required
Method: `PUT`

#####    /posts/{id}/like
Authentication Required
Method: `GET`

#####    /posts/{id}/unlike
Authentication Required
Method: `GET`


## Running Tests
```
CELERY_ALWAYS_EAGER=True IP_GEOLOCATION_API_KEY=XXXX HOLIDAYS_API_KEY=XXXX python manage.py test
```
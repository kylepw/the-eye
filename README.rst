=======
The Eye
=======
Event data aggregator in Django REST framework.

Requirements
------------
- Python
- Docker

Setup
-----
- Clone, configure virtual environment, run: ::

    git clone git@github.com:kylepw/the-eye.git && \
    cd the-eye && python3 -m venv venv && source venv/bin/activate && pip3 install -U pip -r requirements.txt && \
    echo SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env && \
    docker-compose up --build

- Stop app and start again: ::

    ^C
    docker-compose up

Usage
-----
- List events: ::

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/

- Check specific event: ::

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/3/

- Send event: ::

    curl -X POST http://127.0.0.1:8000/events/ \
        -H 'Content-Type: application/json'    \
        -d @- << EOF
    {
        "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
        "category": "click",
        "name": "pageview",
        "data": {
            "host": "www.consumeraffairs.com",
            "path": "/"
        },
        "timestamp": "2021-01-01 09:15:29.243860"
    }
    EOF

- Query a session, category, or timestamp range: ::

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/?session_id=e2085be5-9137-4e4e-80b5-f1ffddc25423

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/?category=form%20interaction

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/?timestamp_before=2021-05-20

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/?timestamp_after=2021-06-01

- Run tests (from top of repo after running *docker-compose up --build*): ::

    docker-compose exec web /code/manage.py test

Conclusions
-----------
I decided to use one **model** as opposed to multiple (ex. Event, Session, etc.) because relationships and joins seemed overkill
given the standardized structure of the event payloads and query requirements.

I utilized Celery/Redis to **run a pseudo task asynchronously** on event retrieve and create requests to the API to tackle the
*~100 events/second* and *make sure to not leave them hanging* constraints.

The **specific time range query** was interesting. To do this, I employed *django-filter* to allow range queries on the 
*timestamp* field. I chose an ISO8601 format over a more general date/time format given the examples and the fact that requests
could be coming from places in different timezones.

I assumed that although events could share a timestamp or session_id value, there shouldn't be multiple events with ALL the same
values, so I tackled this with a *unique_together* property set to all fields in the model.
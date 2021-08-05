=======
The Eye
=======
Event data aggregator in Django REST framework.

Setup
-----
- Clone, configure virtual environment, migrate, run: ::

    git clone git@github.com:kylepw/the-eye.git && \
    cd the-eye && python3 -m venv venv && source venv/bin/activate && pip3 install -U pip -r requirements.txt && \
    echo SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env && \
    python3 manage.py migrate && python3 manage.py loaddata db.json && \
    python3 manage.py runserver

Usage
-----
- List events: ::

    curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/events/

- Check specific event: ::

    curl -L http://127.0.0.1:8000/events/1

- Send event: ::

    curl -X POST http://127.0.0.1:8000/events/   \
         -H 'Content-Type: application/json' \
         -d '{"session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423", "category": "page interaction", "name": "pageview", "data": {"host": "www.consumeraffairs.com", "path": "/"}, "timestamp": "2021-01-01 09:15:27.243860"}'

- Run tests (from top of repo): ::

    python3 manage.py test

- Test coverage (from top of repo): ::
  
    coverage run manage.py test && coverage report

Conclusions
-----------
*Explain what conclusions you've made from the entities, constraints, requirements and use cases of this test.*
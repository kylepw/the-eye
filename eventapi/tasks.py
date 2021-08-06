import time

from celery import shared_task


@shared_task
def process_event(e):
    """Pseudo-processing of event to demonstrate asynchronous task queue with Celery.

    Why:
    - "The Eye" will be receiving, in average, ~100 events/second, so consider
      not processing events in real time.
    - When Applications talk to "The Eye", make sure to not leave them hanging.

    """
    time.sleep(5)
    print(f'{e} PROCESSED!!')

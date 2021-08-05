"""eventapi helper functions."""
from rest_framework import status
from rest_framework.views import exception_handler, Response


def custom_exception_handler(exc, context):
    """Add status code to error response payload."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response
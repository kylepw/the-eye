from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import Event, EventFilter
from .serializers import EventSerializer
from .tasks import process_event


class EventViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter

    # Define create and retrieve methods to add asynchronous tasks.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Process event in background.
        process_event.delay(serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Process event in background.
        process_event.delay(serializer.data)

        return Response(serializer.data)

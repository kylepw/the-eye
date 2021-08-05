from rest_framework import mixins, viewsets

from .models import Event, EventFilter
from .serializers import EventSerializer


class EventViewSet(
    mixins.CreateModelMixin, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
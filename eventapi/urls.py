"""eventapi URL Configuration"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet


router = DefaultRouter()
router.register(r'', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
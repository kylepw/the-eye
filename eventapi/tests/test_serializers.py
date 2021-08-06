from django.test import TestCase

from .factories import EventFactory
from ..models import Event
from ..serializers import EventSerializer


class EventSerializerTestCase(TestCase):
    def setUp(self):
        self.expected_fields = set(
            ['id', 'session_id', 'category', 'name', 'data', 'timestamp']
        )
        self.event = EventFactory.create()
        self.serializer = EventSerializer(self.event)

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.serializer.data.keys()), self.expected_fields)

    def test_create_serializer_with_only_name_field(self):
        s = EventSerializer(data={'name': 'howdy'})
        self.assertFalse(s.is_valid())
        self.assertTrue(
            all([True if k in ('session_id', 'category') else False for k in s.errors])
        )

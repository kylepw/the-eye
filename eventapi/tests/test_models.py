from django.test import TestCase

from ..models import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            session_id='g5085gc5-8888-4e4e-79b5-f1ffddc12345',
            category='page interaction',
            name='pageview',
            data={'host': 'www.instagram.com', 'path': '/'},
        )

    def test_type_property(self):
        self.assertEqual(
            self.event.type,
            '_'.join(self.event.category.split() + self.event.name.split()),
        )

    def test_str(self):
        self.assertEqual(
            str(self.event), f'{self.event.session_id} ({self.event.type})'
        )

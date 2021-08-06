from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from .factories import EventFactory
from ..models import Event


class EventViewSetTestCase(APITestCase):
    def setUp(self):
        EventFactory.create_batch(4)
        self.default_event_kwargs = {
            'session_id': 'd4305gc5-7777-4e4e-79b5-f1ffddc0986',
            'category': 'form interaction',
            'name': 'submit',
            'data': {'host': 'www.netflix.com', 'path': '/'},
        }
        self.default_event = Event.objects.create(**self.default_event_kwargs)

    def test_list_count(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(response_json['count'], 5)
        self.assertEqual(len(response_json['results']), 5)

    def test_list_pagination_works(self):
        PAGE_SIZE = int(settings.REST_FRAMEWORK['PAGE_SIZE'])
        EventFactory.create_batch(PAGE_SIZE * 2)

        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        # Should be as many results as PAGE_SIZE, but more in total count
        self.assertEqual(len(response_json['results']), PAGE_SIZE)
        self.assertGreater(response_json['count'], PAGE_SIZE)

    def test_list_new_event_in_results(self):
        new_event = Event(
            session_id='g5085gc5-8888-4e4e-79b5-f1ffddc12345',
            category='form interaction',
            name='submit',
            data={'host': 'www.consumerreports.com', 'path': '/'},
        )
        url = reverse('event-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertNotIn(new_event.session_id, [r['session_id'] for r in results])

        new_event.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertIn(new_event.session_id, [r['session_id'] for r in results])

    def test_post_invalid_event(self):
        url = reverse('event-list')

        response = self.client.post(url, {'name': 'Jimmy Beam'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field is required.', response_json['session_id'])
        self.assertIn('This field is required.', response_json['category'])

    def test_post_valid_event(self):
        # Change it up a little to prevent duplication
        data = self.default_event_kwargs.copy()
        data['session_id'] = 'z4305gc5-7777-4e4e-8888-f1ffdd1111'

        url = reverse('event-list')
        response = self.client.post(url, data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json['session_id'], data['session_id'])
        self.assertTrue(Event.objects.filter(session_id=data['session_id']).exists())

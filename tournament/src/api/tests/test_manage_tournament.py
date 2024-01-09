import json

from django.test import TestCase
from django.urls import reverse

from api.models import Tournament


class DeleteTournamentTest(TestCase):
    def setUp(self):
        Tournament.objects.create(id=1, name='Test1', admin_id=1)
        Tournament.objects.create(id=2, name='Test2', admin_id=2)

    def test_delete_tournament(self):
        url = reverse('manage-tournament', args=[1])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(body['message'], 'tournament `Test1` successfully deleted')

    def test_delete_tournament_not_found(self):
        url = reverse('manage-tournament', args=[3])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tournament.objects.count(), 2)
        self.assertEqual(body['error'], 'tournament with id `3` does not exist')

    def test_delete_tournament_not_owner(self):
        url = reverse('manage-tournament', args=[2])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tournament.objects.count(), 2)
        self.assertEqual(body['error'], 'you cannot delete `Test2` because you are not the owner of the tournament')

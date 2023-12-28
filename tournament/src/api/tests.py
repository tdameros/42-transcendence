from django.test import TestCase
from django.urls import reverse

from tournament.src.api.models import Tournament


# Create your tests here.
class TournamentBasicTest:
    def test_basic(self):
        data_tournamenent = {
            "name": "World Championship",
            "max-players": 16,
            "registration-deadline": "2025-02-17T10:53",
            "is-private": true
        }
        url = reverse('tournament')
        response = self.client.post(url, data_tournamenent, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(Tournament.objects.get().name, 'World Championship')
        self.assertEqual(Tournament.objects.get().max_players, 16)
        self.assertEqual(Tournament.objects.get().registration_deadline, '2025-02-17T10:53')
        self.assertEqual(Tournament.objects.get().is_private, true)



import unittest
from time import time

from src.matchmaking import Matchmaking
from src.player import Player


class TestSearchOpponent(unittest.TestCase):
    matchmaking = Matchmaking(None)

    def setUp(self):
        self.player_1 = Player(None, 1, 1000)
        self.player_2 = Player(None, 1, 2000)

    def tearDown(self):
        self.matchmaking.queue.clear()

    def test_single_player(self):
        self.matchmaking.queue.append(self.player_1)
        opponent = self.matchmaking.search_opponent(self.player_1, 0)
        self.assertEqual(opponent, None)

    def test_two_players(self):
        self.matchmaking.queue.append(self.player_1)
        self.matchmaking.queue.append(self.player_2)
        opponent = self.matchmaking.search_opponent(self.player_1, 0)
        self.assertEqual(opponent, None)

    def test_invalid_elo_threshold(self):
        self.player_1.elo = 5000
        self.matchmaking.queue.append(self.player_1)
        self.matchmaking.queue.append(self.player_2)
        opponent = self.matchmaking.search_opponent(self.player_1, 0)
        self.assertEqual(opponent, None)

    def test_valid_elo_threshold(self):
        self.player_1.timestamp -= 60
        self.matchmaking.queue.append(self.player_1)
        self.matchmaking.queue.append(self.player_2)
        opponent = self.matchmaking.search_opponent(self.player_1, 0)
        self.assertEqual(opponent, self.player_2)

    def test_valid_high_elo_threshold(self):
        self.player_1.elo = 5000
        self.player_1.timestamp -= 240
        self.matchmaking.queue.append(self.player_1)
        self.matchmaking.queue.append(self.player_2)
        opponent = self.matchmaking.search_opponent(self.player_1, 0)
        self.assertEqual(opponent, self.player_2)


if __name__ == '__main__':
    unittest.main()

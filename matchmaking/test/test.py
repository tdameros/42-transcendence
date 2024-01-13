import unittest
from time import time

from src.matchmaking import Matchmaking


class TestSearchOpponent(unittest.TestCase):
    matchmaking = Matchmaking()
    player1 = {
        'elo': 1000,
        'timestamp': time(),
    }
    player2 = {
        'elo': 1000,
        'timestamp': time(),
    }

    def setUp(self):
        self.player1['elo'] = 1000
        self.player2['elo'] = 2000
        self.player1['timestamp'] = time()
        self.player2['timestamp'] = time()

    def tearDown(self):
        self.matchmaking.queue.clear()

    def test_single_player(self):
        self.matchmaking.queue.append(self.player1)
        opponent = self.matchmaking.search_opponent(self.player1)
        self.assertEqual(opponent, None)

    def test_two_players(self):
        self.matchmaking.queue.append(self.player1)
        self.matchmaking.queue.append(self.player2)
        opponent = self.matchmaking.search_opponent(self.player1)
        self.assertEqual(opponent, None)

    def test_invalid_elo_threshold(self):
        self.player1['elo'] = 5000
        self.matchmaking.queue.append(self.player1)
        self.matchmaking.queue.append(self.player2)
        opponent = self.matchmaking.search_opponent(self.player1)
        self.assertEqual(opponent, None)

    def test_valid_elo_threshold(self):
        self.player1['timestamp'] -= 10
        self.matchmaking.queue.append(self.player1)
        self.matchmaking.queue.append(self.player2)
        opponent = self.matchmaking.search_opponent(self.player1)
        self.assertEqual(opponent, self.player2)

    def test_valid_high_elo_threshold(self):
        self.player1['elo'] = 9000
        self.player1['timestamp'] -= 50
        self.matchmaking.queue.append(self.player1)
        self.matchmaking.queue.append(self.player2)
        opponent = self.matchmaking.search_opponent(self.player1)
        self.assertEqual(opponent, self.player2)


if __name__ == '__main__':
    unittest.main()

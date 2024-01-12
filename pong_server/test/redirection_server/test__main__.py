import unittest

import src.redirection_server.__main__ as main
from src.redirection_server.Game import Game


class TestGetGameIdFunction(unittest.TestCase):
    def test_game_id_is_not_present_in_query_string(self):
        with self.assertRaises(Exception) as context:
            main.get_game_id({})
        self.assertEqual(str(context.exception),
                         'game_id was not found in query string')

    def test_game_id_is_not_a_string(self):
        with self.assertRaises(Exception) as context:
            main.get_game_id({'game_id': 4})
        self.assertEqual(str(context.exception),
                         'game_id must be a string')

    def test_game_id_is_an_empty_string(self):
        with self.assertRaises(Exception) as context:
            main.get_game_id({'game_id': ''})
        self.assertEqual(str(context.exception),
                         'game_id must not be empty')

    def test_with_correct_arguments(self):
        game_id = 'game_1'
        self.assertEqual(main.get_game_id({'game_id': f'{game_id}'}),
                         game_id)


class TestGetGameFunction(unittest.TestCase):
    def test_game_does_not_exist(self):
        main.games = {}

        game_id = 'game_id'
        with self.assertRaises(Exception) as context:
            main.get_game(game_id, 'user_id')
        self.assertEqual(str(context.exception),
                         f'Game {game_id} does not exist')

    def test_user_is_not_part_of_requested_game(self):
        game_id = 'game_id'
        bad_user_id = 'bad_user_id'

        main.games = {game_id: Game(['good_user_id'])}
        with self.assertRaises(Exception) as context:
            main.get_game(game_id, bad_user_id)
        self.assertEqual(str(context.exception),
                         f'User {bad_user_id} is not part of game {game_id}')

    def test_with_correct_arguments(self):
        game_id = 'game_id'
        user_id = 'user_id'
        game = Game([user_id])

        main.games = {game_id: game}
        self.assertIs(main.get_game(game_id, user_id),
                      game)


class TestCreateGameServerIfNeededFunction(unittest.TestCase):
    class FakeGame(object):
        def __init__(self, is_started: bool):
            self._is_started = is_started
            self.create_server_function_was_called = False

        def was_server_created(self):
            return self._is_started

        def create_server(self):
            self.create_server_function_was_called = True

    def test_server_is_not_started(self):
        game = self.FakeGame(is_started=False)
        main.create_game_server_if_needed(game)
        self.assertEqual(game.create_server_function_was_called,
                         True)

    def test_server_is_started(self):
        game = self.FakeGame(is_started=True)
        main.create_game_server_if_needed(game)
        self.assertEqual(game.create_server_function_was_called,
                         False)


#  TODO make new test, I disabled them for now because this changes all the time
# class TestConnectEvent(unittest.TestCase):
#     def test_good_input(self):
#         main.sio = FakeSio()
#         user_id = 'user_1'
#         game_id = 'game_id'
#         main.games = {game_id: Game([user_id, 'user_2'])}
#
#         sid = 'sid'
#         jwt = {'user_id': user_id}
#
#         query_string = json.dumps({'json_web_token': jwt, 'game_id': game_id})
#
#         asyncio.run(main.connect(sid, {'QUERY_STRING': query_string}, 'auth'))
#         self.assertEqual(main.sio.emitted_events[0].event,
#                          'game_server_uri')
#
#     def test_bad_input(self):
#         main.sio = FakeSio()
#         user_id = 'user_1'
#         game_id = 'game_id'
#         main.games = {game_id: Game([user_id, 'user_2'])}
#
#         sid = 'sid'
#         jwt = {'user_id': user_id}
#
#         query_string = json.dumps({'json_wb_token': jwt, 'game_id': game_id})
#
#         asyncio.run(main.connect(sid, {'QUERY_STRING': query_string}, 'auth'))
#         self.assertEqual(main.sio.emitted_events[0],
#                          EmittedEvent('error',
#                                       sid,
#                                       'json_web_token was not found in query string'))


if __name__ == '__main__':
    unittest.main()

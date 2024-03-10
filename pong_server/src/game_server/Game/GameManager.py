from typing import Optional

import settings
from ClientManager import ClientManager
from Clock import Clock
from EventEmitter import EventEmitter
from Game.Match import Match
from Game.MatchLocation import MatchLocation
from Game.Player.Player import Player
from Game.PlayerLocation import PlayerLocation
from PostSender.PostSender import PostSender
from Server import Server
from vector_to_dict import vector_to_dict


class GameManager(object):
    GAME_ID: int

    _has_game_started: bool = False
    _is_game_over: bool = False

    _loosers: list[Player] = []
    _matches: list[Match] = []
    #             dict[MatchLocation, Match]
    _match_table: dict[MatchLocation, Match] = {}
    #            dict[player_id, Player]
    _player_map: dict[int, Player] = {}
    _matches_middle_x: float
    _matches_middle_y: float

    @staticmethod
    async def init(game_id: int, players: list[Optional[int]]):
        GameManager.GAME_ID = game_id

        for i in range(0, len(players), 2):
            match_index = i // 2
            if players[i] is None:
                GameManager._create_player(
                    players[i + 1],
                    PlayerLocation(1, match_index // 2, match_index % 2))
            elif players[i + 1] is None:
                GameManager._create_player(
                    players[i],
                    PlayerLocation(1, match_index // 2, match_index % 2))
            else:
                GameManager._create_player(
                    players[i],
                    PlayerLocation(0, match_index, 0))
                GameManager._create_player(
                    players[i + 1],
                    PlayerLocation(0, match_index, 1))
        GameManager._set_matches_bounding_box(len(players) // 2)
        await GameManager._start_first_round()

    @staticmethod
    async def _start_first_round():
        for match in GameManager._matches:
            player_1: Player = match.get_player(0)
            player_2: Player = match.get_player(1)
            if player_1 is not None and player_2 is not None:
                await PostSender.post_start_match(GameManager.GAME_ID,
                                                  player_1.PLAYER_ID,
                                                  player_2.PLAYER_ID)
            else:
                match.set_is_animating(True)

    @staticmethod
    def get_scene() -> dict:
        return {
            'matches': [match.to_json() for match in GameManager._matches],
            'loosers': [player.to_json() for player in GameManager._loosers],
            'matches_middle': {
                'x': GameManager._matches_middle_x,
                'y': GameManager._matches_middle_y,
            },
            'match_half_width': settings.MATCH_SIZE[0] * 0.5,
            'match_half_height': settings.MATCH_SIZE[1] * 0.5,
            'matches_x_offset': settings.MATCHES_X_OFFSET,
            'matches_y_offset': settings.MATCHES_Y_OFFSET,
            'points_to_win_match': settings.POINTS_TO_WIN_MATCH,
            'paddle_height': settings.PADDLE_SIZE[1],
            'board_size': vector_to_dict(settings.BOARD_SIZE),
        }

    @staticmethod
    async def start_game():
        GameManager._has_game_started = True
        for match in GameManager._matches:
            if match.get_player(0) is not None and match.get_player(1) is not None:
                await match.start_match()

        await GameManager.game_loop()

    @staticmethod
    async def game_loop():
        clock = Clock()
        while True:
            current_time, time_delta = clock.get_time()
            finished_matches: list[Match] = []

            for match in GameManager._matches:
                match_is_animating = match.is_animating()
                await match.update(current_time, time_delta)
                if match_is_animating and not match.is_animating():
                    await match.start_match()
                elif match.is_over():
                    finished_matches.append(match)

            for match in finished_matches:
                await GameManager.match_was_won(match, current_time)

            await Server.sio.sleep(0.01)
            if GameManager._is_game_over:
                return

    @staticmethod
    async def match_was_won(match: Match, current_time: float):
        winner_index = match.get_winner_index()
        looser_index = 1 - winner_index
        await PostSender.post_end_match(
            GameManager.GAME_ID,
            match.get_player(winner_index).PLAYER_ID,
            match.get_player_score(winner_index),
            match.get_player(looser_index).PLAYER_ID,
            match.get_player_score(looser_index)
        )
        ClientManager.unregister_player(match.get_player(looser_index).PLAYER_ID)

        if len(GameManager._matches) == 1:
            GameManager._is_game_over = True
            await EventEmitter.game_over(match.get_winner_index())
            return

        await GameManager.move_players_after_match_over(
            match, winner_index, looser_index, current_time,
        )

    @staticmethod
    async def move_players_after_match_over(match: Match,
                                            winner_index: int,
                                            looser_index: int,
                                            current_time: float):
        GameManager._handle_match_looser(match, looser_index)

        new_match: Match = GameManager._get_or_create_match(MatchLocation(
            match.LOCATION.game_round + 1, match.LOCATION.match // 2
        ), should_animate=True)

        GameManager._handle_match_winner(match, winner_index, new_match, current_time)

        await EventEmitter.player_won_match(
            match.LOCATION, winner_index, new_match.to_json(should_include_players=False),
            current_time
        )
        if new_match.is_full():
            await PostSender.post_start_match(
                GameManager.GAME_ID,
                new_match.get_player(0).PLAYER_ID,
                new_match.get_player(1).PLAYER_ID
            )

        GameManager._delete_match(match)

    @staticmethod
    def _handle_match_looser(match: Match, looser_index: int):
        looser: Player = match.get_player(looser_index)
        # Adding the match position to the looser position to make the position global
        # instead of relative to the match
        looser.set_position(looser.get_position() + match.get_position())
        looser.set_location(PlayerLocation(-1, -1, len(GameManager._loosers), True))
        looser.set_index_when_lost_match(looser_index)
        GameManager._loosers.append(looser)

    @staticmethod
    def _handle_match_winner(match: Match,
                             winner_index: int,
                             new_match: Match,
                             current_time: float):
        winner: Player = match.get_player(winner_index)
        player_new_index: int = match.LOCATION.match % 2

        winner.start_animation(current_time, player_new_index != winner_index,
                               match, new_match)

        winner.set_location(PlayerLocation(
            new_match.LOCATION.game_round, new_match.LOCATION.match, player_new_index
        ))

        new_match.set_player(winner.get_location().player_index, winner)

    @staticmethod
    def has_game_started() -> bool:
        return GameManager._has_game_started

    @staticmethod
    def get_match(match_location: MatchLocation) -> Optional[Match]:
        return GameManager._match_table.get(match_location)

    @staticmethod
    def get_player(player_id: int) -> Player:
        return GameManager._player_map.get(player_id)

    @staticmethod
    def is_game_over() -> bool:
        return GameManager._is_game_over

    @staticmethod
    def _create_player(player_id: int, player_location: PlayerLocation):
        match = GameManager._get_or_create_match(player_location.match_location)

        player = Player(player_id, player_location, bool(player_location.player_index))
        GameManager._player_map[player_id] = player
        match.set_player(player_location.player_index, player)

    @staticmethod
    def _get_or_create_match(match_location: MatchLocation,
                             should_animate: bool = False) -> Match:
        match = GameManager.get_match(match_location)
        if not match:
            match = Match(GameManager.GAME_ID, match_location, should_animate)
            GameManager._matches.append(match)
            GameManager._match_table[match_location] = match
        return match

    @staticmethod
    def _delete_match(match: Match):
        GameManager._matches.remove(match)
        del GameManager._match_table[match.LOCATION]
        del match

    @staticmethod
    def _set_matches_bounding_box(nb_of_matches: int):
        matches_size: float = settings.MATCH_SIZE[0] * nb_of_matches
        offsets_size: float = settings.MATCHES_X_OFFSET * (nb_of_matches - 1)
        total_len: float = (settings.BASE_OFFSET * 2.
                            + matches_size
                            + offsets_size)
        GameManager._matches_middle_x = total_len * .5

        matches_size: float = settings.MATCH_SIZE[1] * nb_of_matches
        offsets_size: float = settings.MATCHES_Y_OFFSET * (nb_of_matches - 1)
        total_len: float = (settings.BASE_OFFSET * 2.
                            + matches_size
                            + offsets_size)
        GameManager._matches_middle_y = total_len * .5

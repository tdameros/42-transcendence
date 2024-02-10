from typing import Optional

from ClientManager import ClientManager
from Clock import Clock
from EventEmitter import EventEmitter
from Game.Match import Match
from Game.MatchLocation import MatchLocation
from Game.Player.Player import Player
from Game.PlayerLocation import PlayerLocation
from Server import Server


class GameManager(object):
    _has_game_started: bool = False

    _loosers: list[Player] = []
    _matches: list[Match] = []
    #             dict[MatchLocation, Match]
    _match_table: dict[MatchLocation, Match] = {}
    #            dict[player_id, Player]
    _player_map: dict[int, Player] = {}

    @staticmethod
    def init(players: list[Optional[int]]):
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

    @staticmethod
    def get_scene() -> dict:
        return {
            'matches': [match.to_json() for match in GameManager._matches],
            'loosers': [player.to_json() for player in GameManager._loosers]
        }

    @staticmethod
    async def start_game():
        for match in GameManager._matches:
            await match.start_match()

        scene = GameManager.get_scene()
        for client_id in ClientManager.CLIENTS_IDS:
            client_sid = ClientManager.get_user_sid(client_id)
            player_location = GameManager._player_map[client_id].get_location()
            if client_sid is not None:
                await EventEmitter.scene(client_sid, player_location, scene)
        GameManager._has_game_started = True

        await GameManager.game_loop()

    @staticmethod
    async def game_loop():
        clock = Clock()
        while True:
            current_time, time_delta = clock.get_time()

            for match in GameManager._matches:
                await match.update(current_time, time_delta)
                if match.is_over():
                    await GameManager.match_was_won(match)
            await Server.sio.sleep(0.01)

            if False:  # TODO: Check if the game is over
                return

    @staticmethod
    async def match_was_won(match: Match):
        # TODO check if it was the final match

        winner_index: int = match.get_winner_index()

        GameManager._handle_match_looser(match, 1 - winner_index)

        new_match: Match = GameManager._get_or_create_match(MatchLocation(
            match.LOCATION.game_round + 1, match.LOCATION.match // 2
        ))

        GameManager._handle_match_winner(match, winner_index, new_match)

        await EventEmitter.player_won_match(match.LOCATION, winner_index, new_match.to_json())
        if new_match.is_full():
            await new_match.start_match()

        GameManager._delete_match(match)

    @staticmethod
    def _handle_match_looser(match: Match, looser_index: int):
        looser: Player = match.get_player(looser_index)
        # Adding the match position to the looser position to make the position global
        # instead of relative to the match
        looser.set_position(looser.get_position() + match.get_position())
        looser.set_location(PlayerLocation(-1, -1, len(GameManager._loosers), True))
        GameManager._loosers.append(looser)

    @staticmethod
    def _handle_match_winner(match: Match,
                             winner_index: int,
                             new_match: Match):
        winner: Player = match.get_player(winner_index)
        winner.set_location(PlayerLocation(
            new_match.LOCATION.game_round, new_match.LOCATION.match, match.LOCATION.match % 2
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
    def _create_player(player_id: int, player_location: PlayerLocation):
        match = GameManager._get_or_create_match(player_location.match_location)

        player = Player(player_id, player_location, bool(player_location.player_index))
        GameManager._player_map[player_id] = player
        match.set_player(player_location.player_index, player)

    @staticmethod
    def _get_or_create_match(match_location: MatchLocation) -> Match:
        match = GameManager.get_match(match_location)
        if not match:
            match = Match(match_location)
            GameManager._matches.append(match)
            GameManager._match_table[match_location] = match
        return match

    @staticmethod
    def _delete_match(match: Match):
        GameManager._matches.remove(match)
        del GameManager._match_table[match.LOCATION]
        del match
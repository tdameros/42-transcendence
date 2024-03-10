import time
from typing import Optional

import numpy

import rooms
import settings
from Game.MatchLocation import MatchLocation
from Game.PlayerLocation import PlayerLocation
from Server import Server
from vector_to_dict import vector_to_dict


class EventEmitter(object):
    @staticmethod
    async def time_sync(sid, time1: any):
        await Server.emit('time_sync', sid, {
            'time1': time1,
            'time2': time.time()
        })

    @staticmethod
    async def scene(sid: str,
                    player_location: PlayerLocation,
                    scene: dict,
                    game_has_started: bool):
        await Server.emit('scene', sid, {
            'scene': scene,
            'player_location': player_location.to_json(),
            'game_has_started': game_has_started,
        })

    @staticmethod
    async def update_paddle(player_location: PlayerLocation,
                            direction: str,
                            paddle_y_position: float,
                            skip_sid: Optional[str]):
        await Server.emit('update_paddle', rooms.ALL_PLAYERS, {
            'player_location': player_location.to_json(),
            'direction': direction,
            'y_position': paddle_y_position
        }, skip_sid)

    @staticmethod
    async def prepare_ball_for_match(match_location: MatchLocation,
                                     ball_movement: numpy.ndarray,
                                     ball_start_time: float):
        await Server.emit('prepare_ball_for_match', rooms.ALL_PLAYERS, {
            'match_location': match_location.to_json(),
            'ball_movement': vector_to_dict(ball_movement),
            'ball_start_time': ball_start_time,
        })

    @staticmethod
    async def update_ball(match_location: MatchLocation,
                          position: numpy.ndarray,
                          movement: numpy.ndarray):
        await Server.emit('update_ball', rooms.ALL_PLAYERS, {
            'match_location': match_location.to_json(),
            'position': vector_to_dict(position),
            'movement': vector_to_dict(movement),
            'time_at_update': time.time(),
        })

    @staticmethod
    async def player_won_match(finished_match_location: MatchLocation,
                               winner_index: int,
                               new_match_json: dict,
                               current_time: float):
        await Server.emit('player_won_match', rooms.ALL_PLAYERS, {
            'finished_match_location': finished_match_location.to_json(),
            'winner_index': winner_index,
            'new_match_json': new_match_json,
            'animation_start_time': current_time,
            'animation_end_time': current_time + settings.ANIMATION_DURATION,
        })

    @staticmethod
    async def game_over(winner_index: int):
        await Server.emit('game_over', rooms.ALL_PLAYERS, winner_index)

    @staticmethod
    async def fatal_error(error: str):
        await Server.emit('fatal_error', rooms.ALL_PLAYERS, {
            'error_message': error,
        })

    @staticmethod
    async def player_scored_a_point(player_location: PlayerLocation):
        await Server.emit('player_scored_a_point', rooms.ALL_PLAYERS, {
            'player_location': player_location.to_json()
        })

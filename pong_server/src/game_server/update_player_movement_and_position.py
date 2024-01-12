import numpy

from src.game_server.Game import Game
from src.game_server.settings import AUTHORIZED_DELAY


def is_bad_movement_event_call(game: Game, client_player_position: any):
    if not game.has_started:
        return True
    if not isinstance(client_player_position, list):
        return True
    if not len(client_player_position) == 3:
        return True
    return not (isinstance(client_player_position[0], (float, int))
                and isinstance(client_player_position[1], (float, int))
                and isinstance(client_player_position[2], (float, int)))


def get_fixed_player_position(game: Game,
                              player_index: int,
                              client_player_position):
    position_on_server = game.get_scene().get_player_position(player_index)
    player_movement = game.get_scene().get_player_movement(player_index)
    max_player_position = position_on_server + player_movement * AUTHORIZED_DELAY
    if player_movement > 0:
        if client_player_position[1] > max_player_position[1]:
            return position_on_server
    elif client_player_position[1] < max_player_position[1]:
        return position_on_server
    return client_player_position


async def update_player_movement_and_position(sio,
                                              sid: str,
                                              game: Game,
                                              client_player_position,
                                              movement: str):
    if is_bad_movement_event_call(game, client_player_position):
        return
    client_player_position = numpy.array(client_player_position)
    player_index = game.get_player_index(sid)
    fixed_player_position = get_fixed_player_position(game,
                                                      player_index,
                                                      client_player_position)

    if fixed_player_position is not None:
        await game.set_player_movement_and_position(sio,
                                                    None,
                                                    player_index,
                                                    movement,
                                                    fixed_player_position)
    else:
        await game.set_player_movement_and_position(sio,
                                                    sid,
                                                    player_index,
                                                    movement,
                                                    client_player_position)

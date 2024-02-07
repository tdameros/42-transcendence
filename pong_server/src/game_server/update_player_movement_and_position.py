import numpy

from Game import Game
from Scene.PlayerFinder.PlayerLocation import PlayerLocation
from settings import AUTHORIZED_DELAY


def is_bad_movement_event_call(game: Game,
                               client_player_position: list[float]):
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
                              player_location: PlayerLocation,
                              client_player_position: numpy.ndarray
                              ) -> numpy.ndarray | None:
    position_on_server = game.get_scene().get_player_paddle_position(player_location)
    player_movement = game.get_scene().get_player_paddle_movement(player_location)
    max_player_position = position_on_server + player_movement * AUTHORIZED_DELAY
    if player_movement[1] > 0.:
        if client_player_position[1] > max_player_position[1]:
            return position_on_server
    elif client_player_position[1] < max_player_position[1]:
        return position_on_server
    return None


async def update_player_direction_and_position(sio,
                                               sid: str,
                                               game: Game,
                                               client_player_position_list: list[float],
                                               direction: str):
    if is_bad_movement_event_call(game, client_player_position_list):
        return
    client_player_position: numpy.ndarray = numpy.array(client_player_position_list,
                                                        dtype=float)
    player_location: PlayerLocation = game.get_player_location(sid)
    fixed_player_position = get_fixed_player_position(game,
                                                      player_location,
                                                      client_player_position)

    should_update_position_on_client_side = fixed_player_position is not None

    if should_update_position_on_client_side:
        skip_sid = None
        true_player_position = fixed_player_position
    else:
        skip_sid = sid
        true_player_position = client_player_position
    await game.set_player_movement_and_position(sio,
                                                player_location,
                                                direction,
                                                true_player_position,
                                                skip_sid)

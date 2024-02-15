from typing import Optional

import numpy

import settings
from EventEmitter import EventEmitter
from Game.Player.Paddle import Paddle
from Game.Player.Player import Player


class AntiCheat(object):
    @staticmethod
    async def update_paddle_position_and_direction(client_paddle_position: float,
                                                   direction: str,
                                                   player: Player,
                                                   sid: str):
        paddle: Paddle = player.get_paddle()

        fixed_paddle_position: Optional[float] \
            = (AntiCheat._get_fixed_paddle_position(client_paddle_position, paddle))

        cheat_or_high_latency: bool = fixed_paddle_position is not None

        paddle_position: numpy.ndarray = paddle.get_position()
        if cheat_or_high_latency:
            # Send the fixed paddle position to the client
            skip_sid = None
        else:
            # No need to send the paddle position to the client
            skip_sid = sid

            # Update the paddle position on server side
            paddle_position[1] = client_paddle_position
        paddle.set_direction(direction)

        await EventEmitter.update_paddle(player.get_location(),
                                         direction,
                                         paddle_position,
                                         skip_sid)

    @staticmethod
    def _get_fixed_paddle_position(client_paddle_position: float,
                                   paddle: Paddle) -> Optional[float]:
        position_on_server: float = paddle.get_position()[1]
        paddle_movement: float = paddle.get_movement()[1]

        max_player_position: float = (position_on_server
                                      + paddle_movement * settings.AUTHORIZED_DELAY)

        if paddle_movement > 0.:
            if client_paddle_position > max_player_position:
                return position_on_server
        elif client_paddle_position < max_player_position:
            return position_on_server
        return None

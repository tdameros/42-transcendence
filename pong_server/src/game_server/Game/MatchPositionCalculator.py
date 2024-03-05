import numpy

import settings
from Game.MatchLocation import MatchLocation


class MatchPositionCalculator(object):
    # This is a cache to avoid calculating the same position multiple times
    match_positions: dict[MatchLocation, numpy.ndarray] = {}

    @staticmethod
    def get_position(match_location: MatchLocation) -> numpy.ndarray:
        match_position = MatchPositionCalculator.match_positions.get(match_location)
        if match_position is not None:
            return match_position.copy()

        if match_location.game_round == 0:
            x, y = MatchPositionCalculator._calculate_x_y_first_game_round(match_location)
        else:
            x, y = MatchPositionCalculator._calculate_x_y_not_first_game_round(match_location)

        match_position = numpy.array([x, y, 0.], dtype=float)
        MatchPositionCalculator.match_positions[match_location] = match_position
        return match_position.copy()

    @staticmethod
    def _calculate_x_y_first_game_round(match_location: MatchLocation) -> tuple[float, float]:
        matches_to_the_left: float = match_location.match * settings.MATCH_SIZE[0]
        offsets_of_left_matches: float = (match_location.match
                                          * settings.MATCHES_X_OFFSET)
        half_match_size: float = settings.MATCH_SIZE[0] * .5
        x: float = (settings.BASE_OFFSET
                    + half_match_size
                    + matches_to_the_left
                    + offsets_of_left_matches)

        half_match_size: float = settings.MATCH_SIZE[1] * .5
        y: float = settings.BASE_OFFSET + half_match_size
        return x, y

    @staticmethod
    def _calculate_x_y_not_first_game_round(match_location: MatchLocation
                                            ) -> tuple[float, float]:
        match_below_left: MatchLocation = MatchLocation(match_location.game_round - 1,
                                                        match_location.match * 2)
        match_below_right: MatchLocation = MatchLocation(match_below_left.game_round,
                                                         match_below_left.match + 1)
        x: float = ((MatchPositionCalculator._get_x_position(match_below_left)
                     + MatchPositionCalculator._get_x_position(match_below_right))
                    * .5)

        matches_below: float = match_location.game_round * settings.MATCH_SIZE[1]
        offsets_of_below_matches: float = (match_location.game_round
                                           * settings.MATCHES_Y_OFFSET)
        half_match_size: float = settings.MATCH_SIZE[1] * .5
        y: float = (settings.BASE_OFFSET
                    + half_match_size
                    + matches_below
                    + offsets_of_below_matches)
        return x, y

    @staticmethod
    def _get_x_position(match_location: MatchLocation) -> float:
        match_position = MatchPositionCalculator.match_positions.get(match_location)
        if match_position is not None:
            return match_position[0]
        return MatchPositionCalculator.get_position(match_location)[0]

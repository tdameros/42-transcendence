from api.models import Match


class MatchUtils:
    @staticmethod
    def get_next_match_id(match_id: int, nb_matches: int) -> int:
        return int((nb_matches - match_id) / 2) + (match_id + 1) % 2

    @staticmethod
    def matches_to_json(matches: list[Match]) -> dict[str, list[any]]:
        matches_data = [MatchUtils.match_to_json(match) for match in matches]
        data = {
            'nb-matches': len(matches),
            'matches': matches_data
        }

        return data

    @staticmethod
    def match_to_json(match: Match):
        return {
            'id': match.match_id,
            'status': MatchUtils.match_status_to_string(match.status),
            'player_1': {
                'user_id': match.player_1.user_id,
                'nickname': match.player_1.nickname
            } if match.player_1 is not None else None,
            'player_2': {
                'user_id': match.player_2.user_id,
                'nickname': match.player_2.nickname
            } if match.player_2 is not None else None,
            'player_1_score': match.player_1_score,
            'player_2_score': match.player_2_score,
            'winner': {
                'user_id': match.winner.user_id,
                'nickname': match.winner.nickname
            } if match.winner is not None else None
        }

    @staticmethod
    def match_status_to_string(status: int):
        match_status_msg = ["Not played", "In progress", "Finished"]

        return match_status_msg[status]

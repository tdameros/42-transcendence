from tournament.get_user import get_username_by_id


class TournamentUtils:
    @staticmethod
    def tournament_to_json(tournaments, jwt):
        tournaments_data = [{
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'nb-players': tournament.players.count(),
            'is-private': tournament.is_private,
            'status': TournamentUtils.status_to_string(tournament.status),
            'admin': get_username_by_id(tournament.admin_id, jwt)
        } for tournament in tournaments]

        return tournaments_data

    @staticmethod
    def status_to_string(status: int) -> str:
        status_string = ['Created', 'In progress', 'Finished']

        return status_string[status]

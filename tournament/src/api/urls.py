from django.urls import path

from api.views.delete_inactive_tournament import DeleteInactiveTournamentView
from api.views.generate_matches_views import GenerateMatchesView
from api.views.manage_match_views import (AddPointView, EndMatchView,
                                          StartMatchView)
from api.views.manage_tournament_views import (ManageTournamentView,
                                               StartTournamentView)
from api.views.matches_views import MatchesView
from api.views.self_ongoing_tournament import SelfOnGoingTournament
from api.views.tournament_players_views import (AnonymizePlayerView,
                                                TournamentPlayersView)
from api.views.tournament_views import TournamentView

urlpatterns = [
    path('', TournamentView.as_view(), name='tournament'),
    path('<int:tournament_id>/', ManageTournamentView.as_view(), name='manage-tournament'),
    path('<int:tournament_id>/start/', StartTournamentView.as_view(), name='start-tournament'),
    path('<int:tournament_id>/players/', TournamentPlayersView.as_view(), name='tournament-players'),
    path('<int:tournament_id>/matches/', MatchesView.as_view(), name='matches'),
    path('<int:tournament_id>/matches/generate/', GenerateMatchesView.as_view(), name='generate-matches'),
    path('<int:tournament_id>/match/start/', StartMatchView.as_view(), name='start-match'),
    path('<int:tournament_id>/match/end/', EndMatchView.as_view(), name='end-match'),
    path('<int:tournament_id>/match/add-point/', AddPointView.as_view(), name='add-point'),
    path('player/anonymize/', AnonymizePlayerView.as_view(), name='player'),
    path('self/ongoing/', SelfOnGoingTournament.as_view(), name='self-ongoing'),
    path('delete-inactive/', DeleteInactiveTournamentView.as_view(), name='delete-inactive-tournament')
]

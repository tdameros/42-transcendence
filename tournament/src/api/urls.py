from django.urls import path

from api.views.generate_matches_views import GenerateMatchesView
from api.views.manage_tournament_views import ManageTournamentView
from api.views.matches_views import ManageMatchesView, MatchesView
from api.views.tournament_players_views import (AnonymizePlayerView,
                                                TournamentPlayersView)
from api.views.tournament_views import TournamentView

urlpatterns = [
    path('', TournamentView.as_view(), name='tournament'),
    path('<int:tournament_id>', ManageTournamentView.as_view(), name='manage-tournament'),
    path('<int:tournament_id>/players', TournamentPlayersView.as_view(), name='tournament-players'),
    path('<int:tournament_id>/matches', MatchesView.as_view(), name='matches'),
    path('<int:tournament_id>/matches/generate', GenerateMatchesView.as_view(), name='generate-matches'),
    path('<int:tournament_id>/matches/<int:match_id>', ManageMatchesView.as_view(), name='manage-match'),
    path('player/anonymize', AnonymizePlayerView.as_view(), name='player')
]

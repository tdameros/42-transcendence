from django.urls import path

from api.views.tournament_views import TournamentView
from api.views.manage_tournament_views import ManageTournamentView, UpdateSettingsView
from api.views.tournament_players_views import TournamentPlayersView

urlpatterns = [
    path('', TournamentView.as_view(), name='tournament'),
    path('<int:tournament_id>', ManageTournamentView.as_view(), name='manage-tournament'),
    path('<int:tournament_id>/players', TournamentPlayersView.as_view(), name='tournament-players'),
    path('<int:tournament_id>/update-settings', UpdateSettingsView.as_view(), name='update-settings'),
]

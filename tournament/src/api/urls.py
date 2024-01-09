from django.urls import path

from api.views.tournament_views import TournamentView
from api.views.manage_tournament_views import ManageTournamentView

urlpatterns = [
    path('', TournamentView.as_view(), name='tournament'),
    path('<int:tournament_id>', ManageTournamentView.as_view(), name='manage-tournament'),
]

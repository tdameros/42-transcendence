from django.urls import path
from api.views import TournamentView


urlpatterns = [
    path('', TournamentView.as_view()),
]

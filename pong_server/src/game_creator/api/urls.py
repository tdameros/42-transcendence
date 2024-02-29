from django.urls import path

from api.views.CreateGameView import CreateGameView
from api.views.CreatePrivateGameView import CreatePrivateGameView
from api.views.RemovePlayersCurrentGameView import RemovePlayersCurrentGameView

urlpatterns = [
    path('create_game/',
         CreateGameView.as_view(),
         name='create_game'),
    path('create_private_game/',
         CreatePrivateGameView.as_view(),
         name='create_private_game'),
    path('remove_players_current_game/',
         RemovePlayersCurrentGameView.as_view(),
         name='remove_players_current_game')
]

from django.urls import path

from api.views.CreateGameView import CreateGameView
from api.views.GetMyGamePortView import GetMyGamePortView
from api.views.GetPlayersGamePortView import GetPlayersGamePortView
from api.views.RemovePlayersCurrentGameView import RemovePlayersCurrentGameView

urlpatterns = [
    path('create_game/',
         CreateGameView.as_view(),
         name='create_game'),
    path('remove_players_current_game/',
         RemovePlayersCurrentGameView.as_view(),
         name='remove_players_current_game'),
    path('/game_creator/get_players_game_port/',
         GetPlayersGamePortView.as_view(),
         name='get_players_game_port'),
    path('/game_creator/get_my_game_port/',
         GetMyGamePortView.as_view(),
         name='get_my_game_port'),
]

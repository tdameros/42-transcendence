from django.urls import path

from api.views import CreateGameView, CreatePrivateGameView

urlpatterns = [
    path('', CreateGameView.as_view(), name='create_game'),
    path('private/', CreatePrivateGameView.as_view(), name='create_private_game'),
]

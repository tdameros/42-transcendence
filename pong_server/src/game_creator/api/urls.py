from django.urls import path

from api.views import CreateGameView

urlpatterns = [
    path('', CreateGameView.as_view(), name='create_game'),
]

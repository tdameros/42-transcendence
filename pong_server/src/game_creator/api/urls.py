from api.views import CreateGameView
from django.urls import path

urlpatterns = [
    path('', CreateGameView.as_view(), name='create_game'),
]

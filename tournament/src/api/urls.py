from django.urls import path
from api.views import Tournament


urlpatterns = [
    path('', Tournament.as_view()),
]

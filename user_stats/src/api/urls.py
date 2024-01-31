from django.urls import path

from api.views.match import MatchView
from api.views.user import UserView
from api.views.user_history import UserHistoryView

urlpatterns = [
    path('user/<int:user_id>/', UserView.as_view(), name='user'),
    path('user/<int:user_id>/history/', UserHistoryView.as_view(), name='user_history'),
    path('match/', MatchView.as_view(), name='match'),
]

from django.urls import path

from api.views.match import MatchView
from api.views.user import UserView
from api.views.user_history import UserHistoryView
from api.views.user_progress import UserProgressView

urlpatterns = [
    path('user/<int:user_id>/', UserView.as_view(), name='user'),
    path('user/<int:user_id>/history/', UserHistoryView.as_view(), name='user_history'),
    path('user/<int:user_id>/progress/', UserProgressView.as_view(), name='user_progress'),
    path('match/', MatchView.as_view(), name='match'),
]

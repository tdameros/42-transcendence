from api.views.match import MatchView
from api.views.user import UserView
from api.views.user_graph import UserGraphEloView
from api.views.user_graph import UserGraphMatchesPlayedView
from api.views.user_graph import UserGraphWinRateView
from api.views.user_history import UserHistoryView
from api.views.user_progress import UserProgressView
from django.urls import path


urlpatterns = [
    path('user/<int:user_id>/', UserView.as_view(), name='user'),
    path('user/<int:user_id>/history/', UserHistoryView.as_view(), name='user_history'),
    path('user/<int:user_id>/progress/', UserProgressView.as_view(), name='user_progress'),
    path('user/<int:user_id>/graph/elo/', UserGraphEloView.as_view(), name='user_graph_elo'),
    path('user/<int:user_id>/graph/win_rate/', UserGraphWinRateView.as_view(), name='user_graph_win_rate'),
    path('match/', MatchView.as_view(), name='match'),
    path(
        'user/<int:user_id>/graph/matches_played/',
        UserGraphMatchesPlayedView.as_view(),
        name='user_graph_matches_played'
    ),
]

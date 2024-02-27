from django.urls import path

from api.views.match import MatchView
from api.views.ranking import RankingView
from api.views.user import UserView
from api.views.user_friends import UserFriendsView
from api.views.user_graph import (UserGraphEloView, UserGraphMatchesPlayedView,
                                  UserGraphWinRateView)
from api.views.user_history import UserHistoryView
from api.views.user_progress import UserProgressView

urlpatterns = [
    path('user/<int:user_id>/', UserView.as_view(), name='user'),
    path('user/<int:user_id>/history/', UserHistoryView.as_view(), name='user_history'),
    path('user/<int:user_id>/progress/', UserProgressView.as_view(), name='user_progress'),
    path('user/<int:user_id>/graph/elo/', UserGraphEloView.as_view(), name='user_graph_elo'),
    path('user/<int:user_id>/graph/win_rate/', UserGraphWinRateView.as_view(), name='user_graph_win_rate'),
    path('user/<int:user_id>/friends/', UserFriendsView.as_view(), name='user_friends'),
    path('match/', MatchView.as_view(), name='match'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path(
        'user/<int:user_id>/graph/matches_played/',
        UserGraphMatchesPlayedView.as_view(),
        name='user_graph_matches_played'
    ),
]

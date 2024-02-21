from django.urls import path

from api.views.friend_notification import AddFriendNotificationView
from api.views.notification import (DeleteUserNotificationView,
                                    UserNotificationView)

urlpatterns = [
    path('user/', UserNotificationView.as_view(), name='user-notification'),
    path('user/<int:notification_id>/', DeleteUserNotificationView.as_view(), name='delete-user-notification'),
    path('new-friend/', NewFriendNotificationView.as_view(), name='new-friend-notification'),
    path('friend/add/', AddFriendNotificationView.as_view(), name='add-friend-notification'),
]

from django.urls import path

from api.views.friend_notification import (AddFriendNotificationView,
                                           DeleteFriendNotificationView)
from api.views.notification import (DeleteUserNotificationView,
                                    UserNotificationView)

urlpatterns = [
    path('user/', UserNotificationView.as_view(), name='user-notification'),
    path('user/<int:notification_id>/', DeleteUserNotificationView.as_view(), name='delete-user-notification'),
    path('friend/add/', AddFriendNotificationView.as_view(), name='add-friend-notification'),
    path('friend/delete/', DeleteFriendNotificationView.as_view(), name='delete-friend-notification'),
]

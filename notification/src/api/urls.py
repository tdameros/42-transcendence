from django.urls import path

from api.views.notification_views import (DeleteUserNotificationView,
                                          UserNotificationView)

urlpatterns = [
    path('user/', UserNotificationView.as_view(), name='user-notification'),
    path('user/<int:notification_id>/', DeleteUserNotificationView.as_view(), name='delete-user-notification')
]

from django.urls import path
from api.views.notification_views import UserNotificationView, DeleteUserNotificationView
from api.views.views import index

urlpatterns = [
    path('', index, name='index'),
    path('user/', UserNotificationView.as_view(), name='user-notification'),
    path('user/<int:notification_id>/', DeleteUserNotificationView.as_view(), name='delete-user-notification')
]

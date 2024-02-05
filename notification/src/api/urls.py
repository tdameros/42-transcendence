from django.urls import path
from api.views.notification_views import UserNotificationView
from api.views.views import index

urlpatterns = [
    path('', index, name='index'),
    path('user/', UserNotificationView.as_view(), name='notification'),
]

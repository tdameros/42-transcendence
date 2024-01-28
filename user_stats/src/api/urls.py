from django.urls import path

from api.views.user import UserView

urlpatterns = [
    path('<int:user_id>', UserView.as_view(), name='user'),
]

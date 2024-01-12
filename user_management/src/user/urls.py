from django.urls import path

from .views import (IsUsernameTakenView, RefreshJWT, SignInView, SignUpView,
                    UserIdView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refresh-access-jwt/', RefreshJWT.as_view(), name='refresh-access-jwt'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
    path('<str:user_id>/', UserIdView.as_view(), name='user-id')
]

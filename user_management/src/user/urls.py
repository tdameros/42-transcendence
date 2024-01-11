from django.urls import path

from .views import IsUsernameTakenView, RefreshJWT, SignInView, SignUpView, IsEmailTakenView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refresh-jwt/', RefreshJWT.as_view(), name='refresh-jwt'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
    path('email-exist/', IsEmailTakenView.as_view(), name='email-exist'),
]

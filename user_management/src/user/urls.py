from django.urls import path
from .views import SignUpView, SignInView, IsUsernameTakenView, RefreshJWT, ForgotPasswordView, \
    CheckForgotPasswordCodeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refresh-jwt/', RefreshJWT.as_view(), name='refresh-jwt'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
    path('forgot-password/send-code/', ForgotPasswordView.as_view(), name='forgot-password-send-code'),
    path('forgot-password/check-code/', CheckForgotPasswordCodeView.as_view(), name='forgot-password-check-code'),
]

from django.urls import path

from .views import (ForgotPasswordChangePasswordView,
                    ForgotPasswordCheckCodeView, ForgotPasswordSendCodeView,
                    IsEmailTakenView, IsUsernameTakenView, RefreshJWT,
                    SearchUsernameView, SignInView, SignUpView, UserIdView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refresh-access-jwt/', RefreshJWT.as_view(), name='refresh-access-jwt'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
    path('email-exist/', IsEmailTakenView.as_view(), name='email-exist'),
    path('forgot-password/send-code/', ForgotPasswordSendCodeView.as_view(), name='forgot-password-send-code'),
    path('forgot-password/check-code/',  ForgotPasswordCheckCodeView.as_view(), name='forgot-password-check-code'),
    path('forgot-password/change-password/', ForgotPasswordChangePasswordView.as_view(),
         name='forgot-password-change-password'),
    path('search-username/', SearchUsernameView.as_view(), name='search-username'),
    path('<str:user_id>/', UserIdView.as_view(), name='user-id')
]

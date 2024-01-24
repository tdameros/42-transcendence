from django.conf.urls.static import static
from django.urls import path

from user.views.OAuth import BaseOAuth, OAuthCallback
from user.views.views import (ForgotPasswordChangePasswordView,
                              ForgotPasswordCheckCodeView,
                              ForgotPasswordSendCodeView, IsEmailTakenView,
                              IsUsernameTakenView, RefreshJWT,
                              SearchUsernameView, SignInView, SignUpView,
                              UserIdView)
from user_management import settings

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
    path('oauth/<str:auth_service>', BaseOAuth.as_view(), name='oauth'),
    path('oauth/callback/<str:auth_service>', OAuthCallback.as_view(), name='oauth-callback'),
    path('<str:user_id>/', UserIdView.as_view(), name='user-id')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


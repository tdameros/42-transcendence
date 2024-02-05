from django.conf.urls.static import static
from django.urls import path

from user.views.forgot_password import (ForgotPasswordChangePasswordView,
                                        ForgotPasswordCheckCodeView,
                                        ForgotPasswordSendCodeView)
from user.views.is_email_taken import IsEmailTakenView
from user.views.is_username_taken import IsUsernameTakenView
from user.views.oauth import OAuth, OAuthCallback
from user.views.refresh_JWT import RefreshJWT
from user.views.search_username import SearchUsernameView
from user.views.sign_in import SignInView
from user.views.sign_up import SignUpView
from user.views.update_infos import UpdateInfos
from user.views.user_id import UserIdView
from user.views.username import UsernameView
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
    path('oauth/<str:auth_service>/', OAuth.as_view(), name='oauth'),
    path('oauth/callback/<str:auth_service>/', OAuthCallback.as_view(), name='oauth-callback'),
    path('update-infos/', UpdateInfos.as_view(), name='update-infos'),
    path('/id/<int:user_id>/', UserIdView.as_view(), name='user-id'),
    path('<str:username>/', UsernameView.as_view(), name='username'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

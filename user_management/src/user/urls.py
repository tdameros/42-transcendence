from django.conf.urls.static import static
from django.urls import path

from user.views.avatar import AvatarView
from user.views.delete_account import DeleteAccountView
from user.views.forgot_password import (ForgotPasswordChangePasswordView,
                                        ForgotPasswordCheckCodeView,
                                        ForgotPasswordSendCodeView)
from user.views.friends import (FriendsAcceptView, FriendsDeclineView,
                                FriendsRequestView, FriendsView)
from user.views.is_email_taken import IsEmailTakenView
from user.views.is_username_taken import IsUsernameTakenView
from user.views.oauth import OAuth, OAuthCallback
from user.views.refresh_JWT import RefreshJWT
from user.views.search_username import SearchUsernameView
from user.views.sign_in import SignInView
from user.views.sign_up import SignUpView
from user.views.two_fa import Disable2fa, Enable2fa, Verify2fa
from user.views.update_infos import UpdateInfos
from user.views.user_id import UserIdListView, UserIdView
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
    path('2fa/enable/', Enable2fa.as_view(), name='enable-2fa'),
    path('2fa/disable/', Disable2fa.as_view(), name='disable-2fa'),
    path('2fa/verify/', Verify2fa.as_view(), name='verify-2fa'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('friends/request/', FriendsRequestView.as_view(), name='friends-request'),
    path('friends/accept/', FriendsAcceptView.as_view(), name='friends-accept'),
    path('friends/decline/', FriendsDeclineView.as_view(), name='friends-decline'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('id-list/', UserIdListView.as_view(), name='user-id-list'),
    path('id/<int:user_id>/', UserIdView.as_view(), name='user-id'),
    path('avatar/<str:username>/', AvatarView.as_view(), name='avatar'),
    path('<str:username>/', UsernameView.as_view(), name='username'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

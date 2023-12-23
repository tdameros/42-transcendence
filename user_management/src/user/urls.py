from django.urls import path
from .views import SignUpView, SignInView, IsUsernameTakenView, RefreshJWT


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refreshJWT/', RefreshJWT.as_view(), name='refreshJWT'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
]

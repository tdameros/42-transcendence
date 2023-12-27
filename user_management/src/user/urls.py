from django.urls import path

from .views import IsUsernameTakenView, SignInView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('username-exist/', IsUsernameTakenView.as_view(), name='username-exist'),
]

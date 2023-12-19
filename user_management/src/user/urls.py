from django.urls import path
from .views import SignUpView, SignInView, IsUsernameTakenView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
]

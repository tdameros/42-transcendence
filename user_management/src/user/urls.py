from django.urls import path
from .views import SignUpView, UserView, EncodeJwtView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('<int:user_id>/', UserView.as_view()),
    path('<int:user_id>/encode/', EncodeJwtView.as_view()),
]

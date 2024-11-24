from django.urls import path
from apps.users.views import UserSignUpView, UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
]
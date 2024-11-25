from django.urls import path
from apps.users.views import UserSignUpView, UserLoginView, ObtainAuthTokenWithUserDetails

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('token/', ObtainAuthTokenWithUserDetails.as_view(), name='api-token-auth'),
]
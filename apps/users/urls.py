from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import UserSignUpView, CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]

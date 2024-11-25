from django.urls import path
from apps.users.views import UserSignUpView, UserLoginView, ObtainAuthTokenWithUserDetails, UserPreferenceDetailView, UserPreferenceListCreateView, UserLogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/', ObtainAuthTokenWithUserDetails.as_view(), name='api-token-auth'),
    path('preferences/', UserPreferenceListCreateView.as_view(), name='user-preference-list-create'),
    path('preferences/<int:pk>/', UserPreferenceDetailView.as_view(), name='user-preference-detail'),
]
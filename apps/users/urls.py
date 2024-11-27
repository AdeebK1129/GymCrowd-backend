"""
URL Configuration for the Users App

This module defines the URL patterns for the Users app. The endpoints allow 
clients to manage user authentication, token generation, and user-specific preferences.

Endpoints:
1. `/login/` - Authenticates a user and retrieves their details. Corresponds to the `UserLoginView`.
2. `/signup/` - Creates a new user account. Corresponds to the `UserSignUpView`.
3. `/logout/` - Logs out the authenticated user by deleting their token. Corresponds to the `UserLogoutView`.
4. `/token/` - Authenticates a user, generates an authentication token, and retrieves user details. 
   Corresponds to the `ObtainAuthTokenWithUserDetails` view.
5. `/preferences/` - Lists all preferences for the authenticated user or creates a new preference. 
   Corresponds to the `UserPreferenceListCreateView`.
6. `/preferences/<int:pk>/` - Retrieves, updates, or deletes a specific user preference by ID. 
   Corresponds to the `UserPreferenceDetailView`.

These views use Django REST Framework's API views to handle authentication, user-specific operations, 
and data serialization.

Dependencies:
    - `django.urls.path`: For defining URL patterns.
    - Views from `apps.users.views`: Correspond to the endpoints and implement 
      the logic for handling requests.
"""

from django.urls import path
from apps.users.views import (
    UserSignUpView, 
    UserLoginView, 
    ObtainAuthTokenWithUserDetails, 
    UserPreferenceDetailView, 
    UserPreferenceListCreateView, 
    UserLogoutView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),  
    # POST /api/users/login/ - Authenticate a user and retrieve their details.

    path('signup/', UserSignUpView.as_view(), name='user-signup'),  
    # POST /api/users/signup/ - Create a new user account.

    path('logout/', UserLogoutView.as_view(), name='user-logout'),  
    # POST /api/users/logout/ - Log out the authenticated user by deleting their token.

    path('token/', ObtainAuthTokenWithUserDetails.as_view(), name='api-token-auth'),  
    # POST /api/users/token/ - Authenticate a user, generate a token, and retrieve user details.

    path('preferences/', UserPreferenceListCreateView.as_view(), name='user-preference-list-create'),  
    # GET /api/users/preferences/ - List all preferences for the authenticated user.
    # POST /api/users/preferences/ - Create a new preference for the authenticated user.

    path('preferences/<int:pk>/', UserPreferenceDetailView.as_view(), name='user-preference-detail'),  
    # GET /api/users/preferences/<pk>/ - Retrieve details of a specific user preference.
    # PUT/PATCH /api/users/preferences/<pk>/ - Update the specified user preference.
    # DELETE /api/users/preferences/<pk>/ - Delete the specified user preference.
]

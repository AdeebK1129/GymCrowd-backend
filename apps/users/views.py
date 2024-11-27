"""
Views for the Users App

This module defines API views for managing users and their preferences. The views handle
operations such as user authentication (login, logout, and token generation), account creation,
and managing user-specific preferences.

Classes:
1. `UserLoginView`: Handles user login and returns user details upon successful authentication.
2. `UserSignUpView`: Handles user registration, allowing new accounts to be created.
3. `UserLogoutView`: Handles user logout by deleting the authentication token.
4. `ObtainAuthTokenWithUserDetails`: Handles login by returning a token and user details.
5. `UserPreferenceListCreateView`: Handles listing all preferences or creating a new one for a user.
6. `UserPreferenceDetailView`: Handles retrieving, updating, or deleting a specific user preference.

Dependencies:
- `APIView` and `generics` from `rest_framework`: Base classes for defining API views.
- `User` and `UserPreference` from `apps.users.models`: Models for user and preference data.
- `UserSerializer` and `UserPreferenceSerializer`: Serializers for structuring API responses.
- `Token` from `rest_framework.authtoken.models`: Provides token-based authentication for users.
- `authenticate` from `django.contrib.auth`: Validates user credentials.

Each view specifies exact routes and HTTP methods in its documentation to enhance clarity.
"""

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.timezone import now
from apps.users.models import User, UserPreference
from apps.users.serializers import UserSerializer, UserPreferenceSerializer


class UserLoginView(APIView):
    """
    API view for handling user login.

    Routes:
    - POST /api/users/login/

    Features:
    - Authenticates users based on their `username` and `password`.
    - Updates the user's last login timestamp upon successful authentication.
    - Returns the user's details in the response.

    Methods:
    - `POST /api/users/login/`: Authenticates the user and returns their details.

    Permissions:
    - No authentication required.

    Attributes:
        None.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            user.last_login = now()
            user.save()

            serializer = UserSerializer(user)
            return Response(
                {"user": serializer.data, "message": "Login successful."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserSignUpView(APIView):
    """
    API view for handling user sign-up.

    Routes:
    - POST /api/users/signup/

    Features:
    - Allows users to create an account by providing their name, email, username, and password.
    - Ensures that the username and email are unique.
    - Hashes the password before saving the user to the database.

    Methods:
    - `POST /api/users/signup/`: Creates a new user account.

    Permissions:
    - No authentication required.

    Attributes:
        None.
    """
    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not name or not email or not username or not password:
            return Response(
                {"error": "Name, email, username, and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "An account with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "An account with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User(name=name, email=email, username=username)
        user.set_password(password)
        user.save()

        return Response(
            {
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "username": user.username,
                },
                "message": "Account created successfully.",
            },
            status=status.HTTP_201_CREATED
        )


class UserLogoutView(APIView):
    """
    API view for handling user logout.

    Routes:
    - POST /api/users/logout/

    Features:
    - Deletes the authentication token for the logged-in user.

    Methods:
    - `POST /api/users/logout/`: Logs out the user by deleting their token.

    Permissions:
    - Requires authentication.

    Attributes:
        None.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK,
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "No token found for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ObtainAuthTokenWithUserDetails(APIView):
    """
    API view for handling user authentication and token generation.

    Routes:
    - POST /api/users/auth-token/

    Features:
    - Authenticates users based on their `username` and `password`.
    - Generates a new authentication token for valid credentials.
    - Returns the user's details along with the token.

    Methods:
    - `POST /api/users/auth-token/`: Returns a token and user details upon successful login.

    Permissions:
    - No authentication required.

    Attributes:
        None.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            user.last_login = now()
            user.save()

            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            serializer = UserSerializer(user)
            return Response(
                {"token": token.key, "user": serializer.data, "message": "Login successful."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserPreferenceListCreateView(generics.ListCreateAPIView):
    """
    API view for managing user preferences.

    Routes:
    - GET /api/users/preferences/
    - POST /api/users/preferences/

    Features:
    - Lists all preferences for the authenticated user.
    - Allows the authenticated user to create a new preference.

    Methods:
    - `GET /api/users/preferences/`: Returns all preferences for the logged-in user.
    - `POST /api/users/preferences/`: Creates a new preference for the user.

    Permissions:
    - Requires authentication.

    Attributes:
        serializer_class (UserPreferenceSerializer): Serializer for structuring the response.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for managing a specific user preference.

    Routes:
    - GET /api/users/preferences/<int:pk>/
    - PUT /api/users/preferences/<int:pk>/
    - PATCH /api/users/preferences/<int:pk>/
    - DELETE /api/users/preferences/<int:pk>/

    Features:
    - Retrieves a specific preference by its primary key.
    - Updates the specified preference with valid data.
    - Deletes the specified preference from the database.

    Methods:
    - `GET /api/users/preferences/<int:pk>/`: Retrieves details of the specified preference.
    - `PUT/PATCH /api/users/preferences/<int:pk>/`: Updates the specified preference.
    - `DELETE /api/users/preferences/<int:pk>/`: Deletes the specified preference.

    Permissions:
    - Requires authentication.

    Attributes:
        serializer_class (UserPreferenceSerializer): Serializer for structuring the response.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Preference deleted successfully."}, status=status.HTTP_200_OK)

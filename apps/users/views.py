from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User, UserPreference
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from apps.users.serializers import UserSerializer, UserPreferenceSerializer
from django.contrib.auth import authenticate


class UserLoginView(APIView):
    """
    Handle user login requests.

    Users log in with `username` and `password`. If valid, the response contains user details.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the user by username
            user = User.objects.get(username=username)

            # Verify the password
            if user.check_password(password):
                serializer = UserSerializer(user)
                return Response(
                    {"user": serializer.data, "message": "Login successful."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid username or password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserSignUpView(APIView):
    """
    Handle user sign-up requests.

    This view allows users to create an account by providing their name,
    email, username, and password. The password is securely hashed before being
    stored in the database.
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

        try:
            # Create a new user
            user = User(
                name=name,
                email=email,
                username=username,
            )
            user.set_password(password)  # Hash the password
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
        except Exception as e:
            return Response(
                {"error": f"Failed to create account: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ObtainAuthTokenWithUserDetails(APIView):
    """
    Handle user authentication and token generation.

    Users log in with their `username` and `password`. If valid, a token is returned
    along with the user details.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            # Fetch or create the token for the authenticated user
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    
class UserPreferenceListCreateView(generics.ListCreateAPIView):
    """
    GET: List all preferences for the authenticated user.
    POST: Create a new preference for the authenticated user.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific preference by ID.
    PUT/PATCH: Update an existing preference.
    DELETE: Delete a preference.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Preference deleted successfully."}, status=status.HTTP_200_OK)

    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from apps.users.serializers import UserSerializer

class UserLoginView(APIView):
    """
    Handle user login requests.

    This view validates the user's email and password and returns a response
    with user details if the credentials are correct.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)

            # Check if the provided password matches the stored password hash
            if check_password(password, user.password_hash):
                serializer = UserSerializer(user)
                return Response(
                    {"user": serializer.data, "message": "Login successful."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid email or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserSignUpView(APIView):
    """
    Handle user sign-up requests.

    This view allows users to create an account by providing their name,
    email, and password. The password is securely hashed before being
    stored in the database.
    """

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            return Response(
                {"error": "Name, email, and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "An account with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new user
            user = User.objects.create(
                name=name,
                email=email,
                password_hash=make_password(password)
            )

            serializer = UserSerializer(user)
            return Response(
                {"user": serializer.data, "message": "Account created successfully."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to create account: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
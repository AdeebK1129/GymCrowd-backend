from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from django.contrib.auth.hashers import check_password, make_password
from apps.users.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


# Custom JWT Token Serializer to include user details in the response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims (optional)
        token['name'] = user.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Add user details to the response
        data.update({
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            }
        })
        return data


# Custom JWT Token View to use the custom serializer
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserLoginView(APIView):
    """
    Handle user login requests.
    """

    permission_classes = [AllowAny]

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
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                # Include user details in the response
                serializer = UserSerializer(user)
                return Response(
                    {"user": serializer.data, "tokens": tokens, "message": "Login successful."},
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
    """

    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

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
            print('user created')
            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            print('token generated')

            # Include user details in the response
            serializer = UserSerializer(user)
            return Response(
                {"user": serializer.data, "tokens": tokens, "message": "Account created successfully."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to create account: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

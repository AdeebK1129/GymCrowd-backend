"""
Models for the Users App

This module defines the database models for managing user accounts and preferences. These
models form the foundation for user authentication, account management, and gym-specific
customizations. The `User` model extends Django's `AbstractBaseUser` to provide a flexible
authentication system, while the `UserPreference` model captures user-specific gym preferences.

The models include:
1. `User`: Represents a system user, including their personal details and authentication data.
2. `UserPreference`: Represents user-defined preferences for gym crowd levels and associated gyms.

These models leverage Django's ORM (Object-Relational Mapping) to provide seamless database
interactions and ensure data integrity. They are essential components of the application's
user management and preference systems.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from apps.gyms.models import Gym


class UserManager(BaseUserManager):
    """
    Custom manager for the `User` model.

    This manager provides methods to create regular users and superusers, handling
    the specifics of password hashing and field validation. It serves as the primary
    interface for creating and retrieving user instances.

    Methods:
        - `create_user`: Creates a new user instance with the given credentials.
        - `create_superuser`: Creates a superuser with elevated permissions.

    Example:
        >>> manager = UserManager()
        >>> user = manager.create_user(username="johndoe", email="johndoe@example.com", password="password123")
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the specified credentials.

        Args:
            username (str): The unique username for the user.
            email (str): The user's email address, used for communication and identification.
            password (str, optional): The plaintext password, which is securely hashed.
            **extra_fields: Additional fields to include in the user record.

        Raises:
            ValueError: If `username` or `email` is not provided.

        Returns:
            User: The created user instance.
        """
        if not username:
            raise ValueError("The Username field is required")
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with elevated permissions.

        Args:
            username (str): The unique username for the superuser.
            email (str): The superuser's email address.
            password (str, optional): The plaintext password, which is securely hashed.
            **extra_fields: Additional fields to include in the superuser record.

        Raises:
            ValueError: If `is_staff` or `is_superuser` is not set to `True`.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Represents an authenticated user in the system.

    This model stores essential user data such as their username, email, and password.
    It extends Django's `AbstractBaseUser` to provide custom authentication logic and
    fields, allowing for a flexible user management system.

    Attributes:
        user_id (int): Auto-incrementing primary key for uniquely identifying a user.
        username (str): The unique username used for login.
        name (str): The full name of the user.
        email (str): The user's email address, used for identification and communication.
        password (str): A hashed representation of the user's password.
        created_at (datetime): Timestamp of when the user was created.
        is_active (bool): Indicates whether the user account is active.
        is_staff (bool): Indicates whether the user has staff privileges.
        is_superuser (bool): Indicates whether the user has superuser privileges.

    Methods:
        __str__(): Returns the username of the user as its string representation.
    """

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)  # AbstractBaseUser expects this field
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.username


class UserPreference(models.Model):
    """
    Represents a user's preferences for gym crowd levels.

    This model links a user to a specific gym and stores their maximum acceptable
    crowd level. It enables users to customize their experience based on their
    comfort levels with gym occupancy.

    Attributes:
        preference_id (int): Auto-incrementing primary key for uniquely identifying a preference.
        user (ForeignKey): A reference to the associated `User` instance.
        gym (ForeignKey): A reference to the associated `Gym` instance.
        max_crowd_level (float): The user's maximum acceptable crowd level at the gym.
        created_at (datetime): Timestamp indicating when the preference was created.

    Methods:
        __str__(): Returns a string representation combining the user's name and gym's name.
    """

    preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='user_preferences')
    max_crowd_level = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.gym.name}"

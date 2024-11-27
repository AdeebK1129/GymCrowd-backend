"""
Serializers for the Users App

This module defines serializers for the `User` and `UserPreference` models, enabling
controlled serialization and deserialization of model instances into JSON and other
representations. These serializers are integral to the API, providing a structured
and validated exchange of data between clients and the server.

The serializers include:
1. `UserPreferenceSerializer`: Handles serialization of user preferences related to gyms.
2. `UserSerializer`: Serializes user data and includes nested relationships for preferences,
   workouts, and notifications.

Dependencies:
- `rest_framework.serializers`: Provides base classes and fields for creating DRF serializers.
- `User`, `UserPreference`, `UserWorkout`, and `Notification`: Models representing users, their
   preferences, workouts, and notifications, respectively.

Each serializer enforces data integrity, ensures appropriate permissions, and defines the structure
of API responses to maintain consistency across the application.
"""

from rest_framework import serializers
from apps.users.models import User, UserPreference
from apps.workouts.models import UserWorkout
from apps.notifications.models import Notification


class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for the `UserPreference` model.

    This serializer converts instances of `UserPreference` into structured data for API responses
    and handles validation for creating or updating preferences. It links user preferences to gyms
    using primary keys and enforces read-only behavior for user associations.

    Attributes:
        gym (PrimaryKeyRelatedField): Represents the associated gym's primary key.

    Meta:
        model (UserPreference): Specifies the model being serialized.
        fields (list[str]): Specifies fields included in the serialization:
            - `preference_id`: Unique ID of the preference.
            - `user`: A reference to the associated `User` instance (read-only).
            - `gym`: Primary key of the associated gym.
            - `max_crowd_level`: Maximum acceptable crowd level for the user.
            - `created_at`: Timestamp of preference creation.

    Features:
    - Read-only user field ensures preferences cannot change ownership via the API.
    - Validates gym associations using primary keys, avoiding circular imports.

    Example Usage:
    - Serializing a preference:
        {
            "preference_id": 42,
            "user": 1,
            "gym": 7,
            "max_crowd_level": 0.8,
            "created_at": "2024-11-26T12:00:00Z"
        }
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserPreference
        fields = ['preference_id', 'user', 'gym', 'max_crowd_level', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `User` model.

    This serializer provides a complete representation of user data, including nested
    relationships for preferences, workouts, and notifications. It ensures efficient
    handling of user-related data while maintaining separation of concerns for nested models.

    Attributes:
        preferences (UserPreferenceSerializer): Nested serializer for the user's preferences.
        workouts (PrimaryKeyRelatedField): References to workouts associated with the user.
        notifications (PrimaryKeyRelatedField): References to notifications linked to the user.

    Meta:
        model (User): Specifies the model being serialized.
        fields (list[str]): Specifies fields included in the serialization:
            - `user_id`: Unique ID of the user.
            - `username`: The username used for authentication.
            - `name`: Full name of the user.
            - `email`: Email address of the user.
            - `preferences`: Nested preferences for gyms (read-only).
            - `workouts`: Primary keys of the user's associated workouts.
            - `notifications`: Primary keys of the user's associated notifications.

    Features:
    - Nested preferences allow detailed representations of user settings for gyms.
    - Workouts and notifications use primary key references to avoid circular imports.
    - Read-only behavior for nested fields prevents unintended updates through the API.

    Example Usage:
    - Serializing a user:
        {
            "user_id": 1,
            "username": "johndoe",
            "name": "John Doe",
            "email": "johndoe@example.com",
            "preferences": [
                {
                    "preference_id": 42,
                    "user": 1,
                    "gym": 7,
                    "max_crowd_level": 0.8,
                    "created_at": "2024-11-26T12:00:00Z"
                }
            ],
            "workouts": [101, 102],
            "notifications": [201, 202]
        }
    """

    preferences = UserPreferenceSerializer(many=True, read_only=True)
    workouts = serializers.PrimaryKeyRelatedField(many=True, queryset=UserWorkout.objects.all())
    notifications = serializers.PrimaryKeyRelatedField(many=True, queryset=Notification.objects.all())

    class Meta:
        model = User
        fields = ['user_id', 'username', 'name', 'email', 'preferences', 'workouts', 'notifications']

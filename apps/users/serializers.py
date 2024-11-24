"""
Serializers for the Users App

This module defines serializers for the `User` and `UserPreference` models,
enabling controlled serialization and deserialization of model instances into
representations such as JSON. These serializers are used in API endpoints to
facilitate data exchange between the client and server while adhering to validation
rules and nested relationships.

The serializers include:
1. `UserPreferenceSerializer` - Serializes user preferences related to gyms.
2. `UserSerializer` - Serializes users and includes nested preferences, workouts, and notifications.

Dependencies:
- `rest_framework.serializers`: Base classes for defining DRF serializers.
- Other serializers (`GymSerializer`, `UserWorkoutSerializer`, and `NotificationSerializer`)
  are imported to handle nested representations.

Each serializer ensures data integrity, enforces read-only or write-specific behaviors,
and defines the structure of API responses.
"""

from rest_framework import serializers
from apps.users.models import User, UserPreference
from apps.gyms.serializers import GymSerializer
from apps.workouts.serializers import UserWorkoutSerializer
from apps.notifications.serializers import NotificationSerializer


class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for the `UserPreference` model.

    This serializer handles the conversion of `UserPreference` model instances
    into a structured representation (e.g., JSON) and vice versa. It includes
    gym-related preferences with a nested representation of the associated `Gym`.

    Attributes:
        gym (GymSerializer): A nested serializer for the `Gym` model, included
            as a read-only field to display gym information in the response.

    Meta:
        model (UserPreference): Specifies the `UserPreference` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `preference_id`: The unique identifier of the preference.
            - `user`: A reference to the associated `User` model.
            - `gym`: Nested details of the associated `Gym` model.
            - `max_crowd_level`: The maximum crowd level the user prefers.
            - `created_at`: Timestamp of when the preference was created.

    Example:
        Serialized Response:
        {
            "preference_id": 1,
            "user": 12,
            "gym": {
                "id": 5,
                "name": "Downtown Gym",
                "location": "Main Street"
            },
            "max_crowd_level": 0.7,
            "created_at": "2024-01-01T12:00:00Z"
        }
    """

    gym = GymSerializer(read_only=True)

    class Meta:
        model = UserPreference
        fields = ['preference_id', 'user', 'gym', 'max_crowd_level', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `User` model.

    This serializer provides a structured representation of user data, including
    nested representations for user preferences, workouts, and notifications.
    It is designed to ensure that related data is serialized and presented in a
    user-friendly format while enforcing read-only constraints for nested fields.

    Attributes:
        preferences (UserPreferenceSerializer): A nested serializer for the user's
            preferences, representing one-to-many relationships with the `UserPreference` model.
            It is read-only and serialized using `UserPreferenceSerializer`.
        workouts (UserWorkoutSerializer): A nested serializer for the user's workouts,
            representing one-to-many relationships with the `UserWorkout` model.
            It is read-only and serialized using `UserWorkoutSerializer`.
        notifications (NotificationSerializer): A nested serializer for the user's notifications,
            representing one-to-many relationships with the `Notification` model.
            It is read-only and serialized using `NotificationSerializer`.

    Meta:
        model (User): Specifies the `User` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `user_id`: The unique identifier of the user.
            - `name`: The full name of the user.
            - `email`: The email address of the user.
            - `preferences`: A nested representation of the user's gym preferences.
            - `workouts`: A nested representation of the user's workouts.
            - `notifications`: A nested representation of the user's notifications.

    Example:
        Serialized Response:
        {
            "user_id": 12,
            "name": "John Doe",
            "email": "johndoe@example.com",
            "preferences": [
                {
                    "preference_id": 1,
                    "gym": {
                        "id": 5,
                        "name": "Downtown Gym",
                        "location": "Main Street"
                    },
                    "max_crowd_level": 0.7,
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ],
            "workouts": [
                {
                    "workout_id": 3,
                    "type": "Cardio",
                    "duration": 45
                }
            ],
            "notifications": [
                {
                    "notification_id": 8,
                    "message": "Workout session booked",
                    "read": false
                }
            ]
        }
    """

    preferences = UserPreferenceSerializer(many=True, read_only=True)
    workouts = UserWorkoutSerializer(many=True, read_only=True)
    notifications = NotificationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'preferences', 'workouts', 'notifications']

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
- Related fields use `PrimaryKeyRelatedField` to avoid circular imports while
  maintaining references to nested models like gyms, workouts, and notifications.

Each serializer ensures data integrity, enforces read-only or write-specific behaviors,
and defines the structure of API responses.
"""

from rest_framework import serializers
from apps.users.models import User, UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for the `UserPreference` model.

    This serializer handles the conversion of `UserPreference` model instances
    into a structured representation (e.g., JSON) and vice versa. It includes
    gym-related preferences represented by a primary key to avoid circular imports.

    Attributes:
        gym (PrimaryKeyRelatedField): A reference to the associated gym's primary key.

    Meta:
        model (UserPreference): Specifies the `UserPreference` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `preference_id`: The unique identifier of the preference.
            - `user`: A reference to the associated `User` model.
            - `gym`: The primary key of the associated gym.
            - `max_crowd_level`: The maximum crowd level the user prefers.
            - `created_at`: Timestamp of when the preference was created.
    """

    gym = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserPreference
        fields = ['preference_id', 'user', 'gym', 'max_crowd_level', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `User` model.

    This serializer provides a structured representation of user data, including
    references for user preferences, workouts, and notifications represented
    by their primary keys to avoid circular imports.

    Attributes:
        preferences (UserPreferenceSerializer): A nested serializer for the user's
            preferences, representing one-to-many relationships with the `UserPreference` model.
            It is read-only and serialized using `UserPreferenceSerializer`.
        workouts (PrimaryKeyRelatedField): A reference to the user's workouts, represented
            by their primary keys.
        notifications (PrimaryKeyRelatedField): A reference to the user's notifications,
            represented by their primary keys.

    Meta:
        model (User): Specifies the `User` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `user_id`: The unique identifier of the user.
            - `name`: The full name of the user.
            - `email`: The email address of the user.
            - `preferences`: A nested representation of the user's gym preferences.
            - `workouts`: A reference to the user's workouts by primary key.
            - `notifications`: A reference to the user's notifications by primary key.
    """

    preferences = UserPreferenceSerializer(many=True, read_only=True)
    workouts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    notifications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'preferences', 'workouts', 'notifications']
        extra_kwargs = {
            'user_id': {'source': 'pk', 'read_only': True}
        }

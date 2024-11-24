"""
Serializers for the Gyms App

This module defines serializers for the `Gym` and `CrowdData` models,
enabling structured serialization and deserialization of model instances into
representations such as JSON. These serializers are used in API endpoints to
facilitate data exchange between the client and server while adhering to validation
rules and nested relationships.

The serializers include:
1. `CrowdDataSerializer` - Serializes crowd data related to gym occupancy levels.
2. `GymSerializer` - Serializes gym details, including nested crowd data, user preferences,
   and notifications.

Dependencies:
- `rest_framework.serializers`: Base classes for defining DRF serializers.
- Other serializers (`UserPreferenceSerializer` and `NotificationSerializer`)
  are imported to handle nested representations.

Each serializer ensures data integrity, enforces read-only or write-specific behaviors,
and defines the structure of API responses.
"""

from rest_framework import serializers
from apps.gyms.models import Gym, CrowdData
from apps.users.serializers import UserPreferenceSerializer
from apps.notifications.serializers import NotificationSerializer


class CrowdDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CrowdData` model.

    This serializer handles the conversion of `CrowdData` model instances into a structured
    representation (e.g., JSON) and vice versa. It links crowd data to its associated `Gym`
    model and is designed for use in both API responses and request validation.

    Attributes:
        gym (PrimaryKeyRelatedField): A reference to the `Gym` model, allowing the API to
            link crowd data to a specific gym using its primary key.

    Meta:
        model (CrowdData): Specifies the `CrowdData` model for serialization.
        fields (list[str]): A list of fields included in the serialized representation:
            - `crowd_id`: The unique identifier of the crowd data entry.
            - `gym`: The primary key of the associated gym.
            - `occupancy`: The occupancy percentage of the gym.
            - `last_updated`: Timestamp of when the crowd data was last updated.

    Example:
        Serialized Response:
        {
            "crowd_id": 42,
            "gym": 3,
            "occupancy": 0.85,
            "last_updated": "2024-01-01T15:00:00Z"
        }
    """

    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())

    class Meta:
        model = CrowdData
        fields = ['crowd_id', 'gym', 'occupancy', 'last_updated']


class GymSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Gym` model.

    This serializer provides a structured representation of gym data, including nested
    representations for related models such as crowd data, user preferences, and notifications.
    It is designed to support read-only nested relationships, ensuring that related data is
    correctly structured for API responses.

    Attributes:
        crowd_data (CrowdDataSerializer): A nested serializer for crowd data associated with the gym.
            - `many=True`: Indicates that a gym can have multiple crowd data entries.
            - `read_only=True`: Ensures that crowd data is included for read-only purposes.
        user_preferences (UserPreferenceSerializer): A nested serializer for user preferences linked
            to the gym.
            - `many=True`: Indicates that a gym can be linked to multiple user preferences.
            - `read_only=True`: Ensures that user preferences are included for read-only purposes.
        notifications (NotificationSerializer): A nested serializer for notifications related to the gym.
            - `many=True`: Indicates that a gym can have multiple notifications.
            - `read_only=True`: Ensures that notifications are included for read-only purposes.

    Meta:
        model (Gym): Specifies the `Gym` model for serialization.
        fields (list[str]): A list of fields included in the serialized representation:
            - `gym_id`: The unique identifier of the gym.
            - `name`: The name of the gym.
            - `location`: The address or location of the gym.
            - `type`: The category or type of the gym (e.g., fitness, yoga).
            - `crowd_data`: A nested representation of associated crowd data entries.
            - `user_preferences`: A nested representation of associated user preferences.
            - `notifications`: A nested representation of associated notifications.

    Example:
        Serialized Response:
        {
            "gym_id": 1,
            "name": "Downtown Gym",
            "location": "123 Main Street, Cityville",
            "type": "Fitness",
            "crowd_data": [
                {
                    "crowd_id": 42,
                    "gym": 1,
                    "occupancy": 0.75,
                    "last_updated": "2024-01-01T15:00:00Z"
                }
            ],
            "user_preferences": [
                {
                    "preference_id": 5,
                    "user": 12,
                    "gym": {
                        "gym_id": 1,
                        "name": "Downtown Gym",
                        "location": "123 Main Street, Cityville",
                        "type": "Fitness"
                    },
                    "max_crowd_level": 0.5,
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ],
            "notifications": [
                {
                    "notification_id": 8,
                    "title": "Class Canceled",
                    "message": "Today's yoga class has been canceled.",
                    "created_at": "2024-01-01T10:00:00Z"
                }
            ]
        }
    """

    crowd_data = CrowdDataSerializer(many=True, read_only=True)
    user_preferences = UserPreferenceSerializer(many=True, read_only=True)
    notifications = NotificationSerializer(many=True, read_only=True)

    class Meta:
        model = Gym
        fields = ['gym_id', 'name', 'location', 'type', 'crowd_data', 'user_preferences', 'notifications']

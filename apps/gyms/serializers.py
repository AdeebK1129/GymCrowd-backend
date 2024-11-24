"""
Serializers for the Gyms App

This module defines serializers for the `Gym` and `CrowdData` models,
enabling structured serialization and deserialization of model instances into
representations such as JSON. These serializers are used in API endpoints to
facilitate data exchange between the client and server while adhering to validation
rules and nested relationships.

The serializers include:
1. `CrowdDataSerializer` - Serializes crowd data related to gym occupancy levels.
2. `GymSerializer` - Serializes gym details, including nested crowd data and references 
   to user preferences and notifications by their primary keys.

Dependencies:
- `rest_framework.serializers`: Provides base classes for defining serializers.
- To avoid circular imports, nested relationships use `PrimaryKeyRelatedField` for user preferences and notifications.

Each serializer ensures data integrity, enforces read-only or write-specific behaviors,
and defines the structure of API responses.
"""

from rest_framework import serializers
from apps.gyms.models import Gym, CrowdData


class CrowdDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CrowdData` model.

    This serializer handles the conversion of `CrowdData` model instances into a structured
    representation (e.g., JSON) and vice versa. It links crowd data to its associated `Gym`
    model using a primary key reference.

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
    representations for related crowd data and references to user preferences and notifications 
    by their primary keys.

    Attributes:
        crowd_data (CrowdDataSerializer): A nested serializer for crowd data associated with the gym.
            - `many=True`: Indicates that a gym can have multiple crowd data entries.
            - `read_only=True`: Ensures that crowd data is included for read-only purposes.
        user_preferences (PrimaryKeyRelatedField): References to user preferences linked to the gym,
            represented by their primary keys. Avoids importing `UserPreferenceSerializer`.
        notifications (PrimaryKeyRelatedField): References to notifications related to the gym,
            represented by their primary keys. Avoids importing `NotificationSerializer`.

    Meta:
        model (Gym): Specifies the `Gym` model for serialization.
        fields (list[str]): A list of fields included in the serialized representation:
            - `gym_id`: The unique identifier of the gym.
            - `name`: The name of the gym.
            - `location`: The address or location of the gym.
            - `type`: The category or type of the gym (e.g., fitness, yoga).
            - `crowd_data`: A nested representation of associated crowd data entries.
            - `user_preferences`: References to associated user preferences by primary key.
            - `notifications`: References to associated notifications by primary key.

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
            "user_preferences": [12, 15],
            "notifications": [8, 9]
        }
    """

    crowd_data = CrowdDataSerializer(many=True, read_only=True)
    user_preferences = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Reference by primary key
    notifications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Reference by primary key

    class Meta:
        model = Gym
        fields = ['gym_id', 'name', 'location', 'type', 'crowd_data', 'user_preferences', 'notifications']

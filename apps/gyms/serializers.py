"""
Serializers for the Gyms App

This module provides serializers for the `Gym` and `CrowdData` models, facilitating structured
serialization and deserialization of these models into formats such as JSON for use in RESTful APIs.
The serializers ensure data validation and consistency while enabling nested or flat data representations
for API responses.

Classes:
1. `CrowdDataSerializer`: Handles serialization and deserialization of crowd data entries.
2. `GymSerializer`: Provides structured representation of gym details, including related crowd data,
   user preferences, and notifications as nested or primary key references.

Dependencies:
- `rest_framework.serializers`: Django REST framework classes used to define custom serializers.
- Models `Gym` and `CrowdData` from `apps.gyms.models`.

Each serializer focuses on ensuring data integrity and providing appropriate views for client-server communication.
"""

from rest_framework import serializers
from apps.gyms.models import Gym, CrowdData


class CrowdDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CrowdData` model.

    Converts `CrowdData` instances to and from structured formats, such as JSON. This serializer
    handles fields for the gym's occupancy, percentage of capacity used, and the last updated timestamp.

    Features:
    - Links crowd data to gyms via a primary key relationship.
    - Provides fields for occupancy and percentage full, ensuring accurate gym utilization data.
    - Includes the timestamp of the last update for tracking real-time data.

    Attributes:
        gym (PrimaryKeyRelatedField): Links to the associated `Gym` model, enabling the API to
            reference gyms by their primary keys in serialized data.

    Meta:
        model (CrowdData): Specifies the `CrowdData` model for the serializer.
        fields (list[str]): Fields included in the serialized representation:
            - `crowd_id`: Unique identifier for the crowd data.
            - `gym`: Primary key of the related gym.
            - `occupancy`: Current number of people at the gym.
            - `percentage_full`: Percentage of the gym's capacity that is occupied.
            - `last_updated`: Timestamp of the last update.
    """

    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())

    class Meta:
        model = CrowdData
        fields = ['crowd_id', 'gym', 'occupancy', 'percentage_full', 'last_updated']


class GymSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Gym` model.

    Converts `Gym` instances to and from structured formats like JSON. Includes nested representations
    of associated `CrowdData` and references to `UserPreference` and `Notification` models by primary key.

    Features:
    - Provides a comprehensive view of gym data, including related crowd data.
    - Supports nested serialization for `CrowdData`, allowing detailed responses.
    - Exposes user preferences and notifications linked to the gym as primary key references.

    Attributes:
        crowd_data (CrowdDataSerializer): Nested representation of all associated crowd data entries for the gym.
            - `many=True`: Indicates that multiple crowd data records can exist for a gym.
            - `read_only=True`: Specifies that the data is only available for read operations.
        user_preferences (PrimaryKeyRelatedField): Primary key references to user preferences linked to the gym.
        notifications (PrimaryKeyRelatedField): Primary key references to notifications related to the gym.

    Meta:
        model (Gym): Specifies the `Gym` model for the serializer.
        fields (list[str]): Fields included in the serialized representation:
            - `gym_id`: Unique identifier of the gym.
            - `name`: Name of the gym.
            - `location`: Address or general location of the gym.
            - `type`: Category or type of the gym (e.g., fitness, yoga).
            - `crowd_data`: Nested representations of associated crowd data entries.
            - `user_preferences`: Primary key references to user preferences.
            - `notifications`: Primary key references to related notifications.
    """

    crowd_data = CrowdDataSerializer(many=True, read_only=True)
    user_preferences = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    notifications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Gym
        fields = ['gym_id', 'name', 'location', 'type', 'crowd_data', 'user_preferences', 'notifications']

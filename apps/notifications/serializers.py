"""
Serializers for the Notifications App

This module defines the serializer for the `Notification` model, facilitating
controlled serialization and deserialization of notification instances into 
structured representations such as JSON. The `NotificationSerializer` ensures
data consistency and integrates references for associated users and gyms.

Purpose:
- The `NotificationSerializer` bridges the gap between the `Notification` model and 
  API responses or incoming payloads by structuring model data in a standardized 
  format and validating incoming requests.

Features:
- Allows the representation of user and gym relationships through their primary keys 
  to simplify data structures and avoid potential circular imports.
- Implements read-only constraints for user references and supports dynamic gym associations 
  by including a queryset for validation.

Dependencies:
- `rest_framework.serializers`: Provides base classes for defining serializers.
- `Notification`: The model being serialized, representing notifications sent to users.
- `User` and `Gym`: Models associated with the notification, referenced via primary keys.

The `NotificationSerializer` is utilized in notifications-related API endpoints to 
facilitate structured data exchange while enforcing validation rules.
"""

from rest_framework import serializers
from apps.notifications.models import Notification
from apps.gyms.models import Gym


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Notification` model.

    This serializer converts instances of the `Notification` model into a structured
    representation (e.g., JSON) and vice versa. It references the user and gym associated
    with the notification by their primary keys, ensuring that detailed information can
    be retrieved while avoiding circular imports.

    Attributes:
        user (PrimaryKeyRelatedField): A reference to the associated user, represented
            by their primary key. This field is read-only to prevent modification of user
            associations via the serializer.
        gym (PrimaryKeyRelatedField): A reference to the associated gym, represented
            by its primary key. This field includes a queryset to validate gym associations 
            during deserialization.

    Meta:
        model (Notification): Specifies the `Notification` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `notification_id`: The unique identifier of the notification.
            - `user`: A reference to the associated user by primary key.
            - `gym`: A reference to the associated gym by primary key.
            - `message`: The message content of the notification.
            - `sent_at`: Timestamp indicating when the notification was sent.

    Example:
        Serialized Response:
        {
            "notification_id": 15,
            "user": 12,
            "gym": 3,
            "message": "Your workout session is scheduled for tomorrow at 10 AM.",
            "sent_at": "2024-01-01T12:00:00Z"
        }

    Methods:
        None explicitly defined; this serializer relies on DRF's base `ModelSerializer`
        methods for validation, serialization, and deserialization.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())

    class Meta:
        model = Notification
        fields = ['notification_id', 'user', 'gym', 'message', 'sent_at']

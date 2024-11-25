"""
Serializers for the Notifications App

This module defines the serializer for the `Notification` model, facilitating
controlled serialization and deserialization of notification instances into 
structured representations such as JSON. The `NotificationSerializer` ensures
data consistency and integrates references for associated users and gyms.

The serializer includes:
1. `NotificationSerializer` - Serializes notifications, including references 
   to related users and gyms by their primary keys.

Dependencies:
- `rest_framework.serializers`: Provides base classes for defining serializers.
- To avoid circular imports, nested fields use `PrimaryKeyRelatedField` for user and gym associations.

The `NotificationSerializer` enforces read-only constraints for these references
and ensures accurate structuring of API responses for notifications-related endpoints.
"""

from rest_framework import serializers
from apps.notifications.models import Notification
from apps.users.models import User
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
            by their primary key. Avoids importing the `UserSerializer` to prevent circular imports.
        gym (PrimaryKeyRelatedField): A reference to the associated gym, represented
            by its primary key. Avoids importing the `GymSerializer` to prevent circular imports.

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
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all(), read_only=False)

    class Meta:
        model = Notification
        fields = ['notification_id', 'user', 'gym', 'message', 'sent_at']

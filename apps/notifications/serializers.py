"""
Serializers for the Notifications App

This module defines the serializer for the `Notification` model, facilitating
controlled serialization and deserialization of notification instances into 
structured representations such as JSON. The `NotificationSerializer` ensures
data consistency and integrates nested relationships for associated users and gyms.

The serializer includes:
1. `NotificationSerializer` - Serializes notifications, including nested representations 
   of related users and gyms.

Dependencies:
- `rest_framework.serializers`: Provides base classes for defining serializers.
- Other serializers (`UserSerializer`, `GymSerializer`) are imported to handle nested 
  representations of user and gym data.

The `NotificationSerializer` enforces read-only constraints for nested fields and 
ensures accurate structuring of API responses for notifications-related endpoints.
"""

from rest_framework import serializers
from apps.notifications.models import Notification
from apps.users.serializers import UserSerializer
from apps.gyms.serializers import GymSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Notification` model.

    This serializer converts instances of the `Notification` model into a structured
    representation (e.g., JSON) and vice versa. It incorporates nested representations
    for the user and gym associated with the notification, ensuring that detailed
    information is presented in API responses while maintaining data integrity.

    Attributes:
        user (UserSerializer): A nested serializer for the `User` model, included as 
            a read-only field to display details about the user who received the notification.
        gym (GymSerializer): A nested serializer for the `Gym` model, included as a 
            read-only field to display details about the gym related to the notification.

    Meta:
        model (Notification): Specifies the `Notification` model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - `notification_id`: The unique identifier of the notification.
            - `user`: Nested details of the associated user who received the notification.
            - `gym`: Nested details of the associated gym the notification pertains to.
            - `message`: The message content of the notification.
            - `sent_at`: Timestamp indicating when the notification was sent.

    Example:
        Serialized Response:
        {
            "notification_id": 15,
            "user": {
                "user_id": 12,
                "name": "John Doe",
                "email": "johndoe@example.com"
            },
            "gym": {
                "gym_id": 3,
                "name": "Downtown Gym",
                "location": "Main Street",
                "type": "Fitness"
            },
            "message": "Your workout session is scheduled for tomorrow at 10 AM.",
            "sent_at": "2024-01-01T12:00:00Z"
        }
    """

    user = UserSerializer(read_only=True)  # Nested user details
    gym = GymSerializer(read_only=True)  # Nested gym details

    class Meta:
        model = Notification
        fields = ['notification_id', 'user', 'gym', 'message', 'sent_at']

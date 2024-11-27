"""
Models for the Notifications App

This module defines the database model for managing notifications in the application.
The `Notification` model captures information related to messages sent to users about
specific gyms, including the associated user, gym, and timestamp details.

Purpose:
- The `Notification` model supports the application's messaging functionality by recording
  updates, alerts, and user-specific information tied to gym activities or crowd levels.
- This model facilitates user engagement by linking messages to both users and gyms,
  ensuring personalized and contextually relevant communication.

Relationships:
- `Notification` is linked to the `User` model to associate messages with specific users.
- `Notification` is linked to the `Gym` model to provide contextual information about the
  notification's subject (e.g., gym-related updates).

Dependencies:
- `django.db.models`: Provides the base `Model` class and field types for defining attributes.
- `apps.users.models.User`: Imports the `User` model for establishing user-specific notifications.
- `apps.gyms.models.Gym`: Imports the `Gym` model to associate notifications with specific gyms.

The model ensures data integrity and leverages Django's ORM for database abstraction,
allowing efficient querying and relationships.
"""

from django.db import models
from apps.users.models import User
from apps.gyms.models import Gym


class Notification(models.Model):
    """
    Represents a notification sent to a user about a specific gym.

    This model stores information about notifications generated within the application.
    Each notification is linked to a specific user and gym, and includes a textual message
    as well as a timestamp for when the notification was sent. It is designed to facilitate
    user engagement and communication regarding gym-related updates or events.

    Attributes:
        notification_id (int): Auto-incrementing primary key for uniquely identifying a notification.
        user (ForeignKey): A foreign key linking to the `User` model. Deletion of the user 
            cascades and removes associated notifications.
        gym (ForeignKey): A foreign key linking to the `Gym` model. Deletion of the gym
            cascades and removes associated notifications.
        message (str): The content of the notification message. Stored as a `TextField`
            to accommodate messages of varying lengths.
        sent_at (datetime): Timestamp indicating when the notification was sent. Automatically
            populated using `auto_now_add`.

    Methods:
        __str__(): Provides a human-readable representation of the notification, combining
        the user's name and the gym's name.

    Related Models:
        - `User`: A user can have multiple notifications stored in the database.
        - `Gym`: A gym can have multiple notifications related to its activities or updates.

    Example:
        >>> user = User.objects.get(name="John Doe")
        >>> gym = Gym.objects.get(name="Downtown Gym")
        >>> notification = Notification(user=user, gym=gym, message="Your workout is scheduled.")
        >>> print(notification)
        Notification for John Doe at Downtown Gym
    """

    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a human-readable representation of the notification.

        Returns:
            str: A string combining the user's name and the gym's name.
        """
        return f"Notification for {self.user.name} at {self.gym.name}"

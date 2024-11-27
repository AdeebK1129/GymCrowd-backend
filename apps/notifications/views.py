"""
Views for the Notifications App

This module defines API views for the `Notification` model, using Django REST Framework (DRF).
These views handle operations for listing, creating, retrieving, updating, and deleting notifications,
as well as retrieving notifications specific to a user.

Classes:
1. `NotificationListCreateView`: Handles listing all notifications or creating a new notification.
2. `NotificationDetailView`: Handles retrieving, updating, or deleting a specific notification.
3. `UserNotificationsView`: Handles retrieving all notifications for a specific user.

Dependencies:
- `generics` from `rest_framework`: Provides base classes for creating API views.
- `Notification` from `apps.notifications.models`: The model representing notifications.
- `NotificationSerializer` from `apps.notifications.serializers`: Serializer for structuring notification data.
- `IsAuthenticated` from `rest_framework.permissions`: Ensures authenticated access to restricted endpoints.

Each view specifies exact routes in its documentation to enhance clarity on its role in the API.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all notifications or creating a new notification.

    Routes:
    - GET /api/notifications/
    - POST /api/notifications/

    This view uses the `generics.ListCreateAPIView` class from Django REST Framework, which
    provides built-in support for handling HTTP GET and POST requests. It interacts with the
    `Notification` model and uses the `NotificationSerializer` to structure and validate data.

    Features:
    - Handles listing all `Notification` instances when accessed via a GET request.
    - Allows creating a new `Notification` instance when accessed via a POST request, provided
      the user is authenticated.

    Permissions:
    - Only authenticated users can create notifications.
    - All users can view notifications without authentication.

    Attributes:
        queryset (QuerySet): All `Notification` instances in the database.
        serializer_class (NotificationSerializer): Serializer for validation and structuring responses.

    Methods:
        - `GET /api/notifications/`: Returns a list of all notifications.
        - `POST /api/notifications/`: Creates a new notification (requires authentication).

    Example Usage:
    - GET Request: Returns a JSON array of all notifications.
    - POST Request: Accepts a JSON payload to create a new notification.

    Dependencies:
    - `NotificationSerializer`: Validates and serializes `Notification` data.
    - `IsAuthenticated`: Ensures only authenticated users can create notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        """
        Dynamically sets permissions based on the HTTP method.

        Returns:
            list: A list of permission classes.
        """
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        """
        Saves the new notification with the current authenticated user.

        Args:
            serializer (NotificationSerializer): The serializer instance containing valid data.
        """
        serializer.save(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific notification.

    Routes:
    - GET /api/notifications/<int:pk>/
    - PUT /api/notifications/<int:pk>/
    - PATCH /api/notifications/<int:pk>/
    - DELETE /api/notifications/<int:pk>/

    This view uses the `generics.RetrieveUpdateDestroyAPIView` class from Django REST Framework,
    which provides built-in support for handling HTTP GET, PUT, PATCH, and DELETE requests. The view
    interacts with the `Notification` model and uses the `NotificationSerializer` to structure and validate data.

    Features:
    - Retrieves a specific `Notification` instance by its primary key using a GET request.
    - Updates the specified notification with new data using PUT or PATCH requests.
    - Deletes the specified notification from the database using a DELETE request.

    Permissions:
    - Only authenticated users can update or delete notifications.

    Attributes:
        queryset (QuerySet): All `Notification` instances in the database.
        serializer_class (NotificationSerializer): Serializer for validation and structuring responses.
        permission_classes (list): Specifies that the view requires authentication.

    Methods:
        - `GET /api/notifications/<int:pk>/`: Retrieves details of the notification with the specified primary key.
        - `PUT/PATCH /api/notifications/<int:pk>/`: Updates the specified notification with valid data.
        - `DELETE /api/notifications/<int:pk>/`: Deletes the specified notification.

    Example Usage:
    - GET Request: Returns the details of the specified notification.
    - DELETE Request: Deletes the specified notification and returns a success response.

    Dependencies:
    - `NotificationSerializer`: Validates and serializes `Notification` data.
    - `IsAuthenticated`: Ensures only authenticated users can perform updates or deletions.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class UserNotificationsView(generics.ListAPIView):
    """
    API view for retrieving all notifications for a specific user.

    Routes:
    - GET /api/notifications/user/<int:user_id>/

    This view uses the `generics.ListAPIView` class from Django REST Framework, which provides
    built-in support for handling HTTP GET requests to list model instances. It filters the
    `Notification` model to return notifications associated with a specific user, identified by their user ID.

    Features:
    - Retrieves all `Notification` instances linked to a specific user.

    Attributes:
        serializer_class (NotificationSerializer): Serializer for structuring the API response.

    Methods:
        - `GET /api/notifications/user/<int:user_id>/`: Returns all notifications for the specified user.

    Example Usage:
    - GET Request: Returns a JSON array of notifications for the user with the specified ID.

    Dependencies:
    - `NotificationSerializer`: Structures the response data for notifications.
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Filters the `Notification` queryset to return entries for the specified user.

        Returns:
            QuerySet: A queryset of `Notification` instances associated with the user.
        """
        user_id = self.kwargs.get('user_id')
        return Notification.objects.filter(user_id=user_id)

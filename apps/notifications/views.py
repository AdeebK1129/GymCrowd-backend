# apps/notifications/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

class NotificationListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all notifications or creating a new notification.

    Permissions:
        - Requires authentication for creating notifications.

    Methods:
        - `GET`: List all notifications.
        - `POST`: Create a new notification.

    Example:
        GET /api/notifications/ -> Returns a list of all notifications.
        POST /api/notifications/ -> Creates a new notification (requires authentication).
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, or deleting a single notification.

    Permissions:
        - Requires authentication for updates and deletions.

    Methods:
        - `GET`: Retrieve a single notification.
        - `PUT/PATCH`: Update a notification.
        - `DELETE`: Delete a notification.

    Example:
        GET /api/notifications/1/ -> Returns the notification with ID 1.
        DELETE /api/notifications/1/ -> Deletes the notification with ID 1 (requires authentication).
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class UserNotificationsView(generics.ListAPIView):
    """
    Retrieves all notifications for a specific user.

    Example:
        GET /api/notifications/user/12/ -> Returns all notifications for the user with ID 12.
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Notification.objects.filter(user_id=user_id)

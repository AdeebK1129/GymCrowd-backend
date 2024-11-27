"""
URLs for the Notifications App

This module defines the URL patterns for the Notifications API. It maps endpoints to their respective views,
enabling operations such as listing, creating, retrieving, updating, and deleting notifications, as well as
fetching notifications specific to a user.

Endpoints:
1. `NotificationListCreateView`: Handles listing all notifications or creating a new notification.
    - URL: `/notifications/`
    - Methods: GET, POST
2. `NotificationDetailView`: Handles retrieving, updating, or deleting a specific notification by its primary key.
    - URL: `/notifications/<int:pk>/`
    - Methods: GET, PUT, PATCH, DELETE
3. `UserNotificationsView`: Handles retrieving all notifications associated with a specific user.
    - URL: `/notifications/user/<int:user_id>/`
    - Methods: GET

Dependencies:
- `path` from `django.urls`: Provides a method for defining URL patterns.
- `NotificationListCreateView`, `NotificationDetailView`, `UserNotificationsView`: Views from `apps.notifications.views`
  that handle the business logic for each endpoint.

Each URL pattern corresponds to a specific API endpoint and ensures that the correct view is called based on the
provided route and HTTP method.
"""

from django.urls import path
from apps.notifications.views import NotificationListCreateView, NotificationDetailView, UserNotificationsView

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),  
    # Endpoint: /notifications/
    # Methods: GET (list all notifications), POST (create a new notification)

    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),  
    # Endpoint: /notifications/<int:pk>/
    # Methods: GET (retrieve a specific notification), PUT/PATCH (update a specific notification),
    # DELETE (delete a specific notification)

    path('user/<int:user_id>/', UserNotificationsView.as_view(), name='user-notifications'),  
    # Endpoint: /notifications/user/<int:user_id>/
    # Methods: GET (retrieve all notifications for a specific user)
]

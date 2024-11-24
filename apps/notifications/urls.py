# apps/notifications/urls.py
from django.urls import path
from apps.notifications.views import NotificationListCreateView, NotificationDetailView, UserNotificationsView

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),  # List all/create notifications
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),  # Retrieve, update, delete notification
    path('user/<int:user_id>/', UserNotificationsView.as_view(), name='user-notifications'),  # Get all notifications for a user
]

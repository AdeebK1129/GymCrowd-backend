"""
Project-Wide URL Configuration

This module defines the root URL patterns for the Django project. It serves as the entry point 
for all app-specific routes, delegating path matching to the included URL configurations 
for each app. The structure adheres to Django's `urlpatterns` pattern for handling requests.

Endpoints:
1. `/admin/` - Provides access to the Django admin interface.
2. `/api/users/` - Includes all user-related endpoints from the `users` app.
3. `/api/gyms/` - Includes all gym-related endpoints from the `gyms` app.
4. `/api/workouts/` - Includes all workout-related endpoints from the `workouts` app.
5. `/api/notifications/` - Includes all notification-related endpoints from the `notifications` app.

Dependencies:
- `django.contrib.admin`: Provides the built-in admin interface for managing the application.
- `django.urls.include`: Allows inclusion of app-specific URL configurations into the root URL patterns.
- `django.urls.path`: Facilitates the definition of URL patterns.

Each app is responsible for managing its own detailed URL configurations, which are included here to centralize routing.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface
    path('api/users/', include('users.urls')),  # User-related endpoints
    path('api/gyms/', include('gyms.urls')),  # Gym-related endpoints
    path('api/workouts/', include('workouts.urls')),  # Workout-related endpoints
    path('api/notifications/', include('notifications.urls')),  # Notification-related endpoints
]

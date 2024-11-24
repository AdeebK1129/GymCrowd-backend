from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/gyms/', include('gyms.urls')),
    path('api/workouts/', include('workouts.urls')),
    path('api/notifications/', include('notifications.urls')),
]

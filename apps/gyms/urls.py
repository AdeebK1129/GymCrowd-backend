"""
URL Configuration for the Gyms App

This module defines the URL patterns for the Gyms API. It maps routes to views that handle 
gym and crowd data-related operations, including listing, retrieving details, and managing crowd data entries.

Endpoints:
1. `GymListView`: Handles listing all gym instances.
    - URL: `/gyms/`
    - Methods: GET
2. `GymDetailView`: Handles retrieving detailed information for a specific gym by its unique identifier.
    - URL: `/gyms/<int:gym_id>/`
    - Methods: GET
3. `CrowdDataListView`: Handles listing all crowd data entries or creating a new crowd data entry.
    - URL: `/gyms/crowddata/`
    - Methods: GET, POST
4. `CrowdDataDetailView`: Handles retrieving, updating, or deleting specific crowd data entries by their primary key.
    - URL: `/gyms/crowddata/<int:pk>/`
    - Methods: GET, PUT, PATCH, DELETE

Dependencies:
- `path` from `django.urls`: Provides a method for defining URL patterns.
- Views from `apps.gyms.views`: Correspond to the endpoints and handle request logic using Django REST Framework (DRF).

Each URL pattern is associated with a specific view class that processes incoming HTTP requests and 
returns the appropriate responses based on the operation being performed.
"""

from django.urls import path
from apps.gyms.views import GymListView, GymDetailView, CrowdDataListView, CrowdDataDetailView

urlpatterns = [
    path("", GymListView.as_view(), name="gym-list"),
    # Endpoint: /gyms/
    # Methods: GET (list all gyms)

    path("<int:gym_id>/", GymDetailView.as_view(), name="gym-detail"),
    # Endpoint: /gyms/<int:gym_id>/
    # Methods: GET (retrieve details of a specific gym by its gym_id)

    path("crowddata/", CrowdDataListView.as_view(), name="crowddata-list"),
    # Endpoint: /gyms/crowddata/
    # Methods: GET (list all crowd data entries), POST (create a new crowd data entry)

    path("crowddata/<int:pk>/", CrowdDataDetailView.as_view(), name="crowddata-detail"),
    # Endpoint: /gyms/crowddata/<int:pk>/
    # Methods: GET (retrieve details of a specific crowd data entry), 
    # PUT/PATCH (update the specified entry), DELETE (remove the specified entry)
]

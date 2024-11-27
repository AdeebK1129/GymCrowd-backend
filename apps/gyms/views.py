"""
Views for the Gyms App

This module defines API views for the `Gym` and `CrowdData` models, using Django REST Framework (DRF).
These views handle operations such as retrieving, creating, updating, and deleting resources while leveraging
generic DRF classes for streamlined functionality.

Classes:
1. `GymListView`: Handles listing all gym instances.
2. `GymDetailView`: Handles retrieving details of a specific gym by its unique identifier.
3. `CrowdDataListView`: Handles listing all crowd data entries or creating a new entry.
4. `CrowdDataDetailView`: Handles retrieving, updating, or deleting a specific crowd data entry.

Dependencies:
- `generics` from `rest_framework`: Provides base classes for creating API views.
- `Gym` and `CrowdData` from `apps.gyms.models`: Models representing gyms and crowd data.
- `GymSerializer` and `CrowdDataSerializer` from `apps.gyms.serializers`: Serializers for structuring model data.

Each view specifies exact routes in its documentation to enhance clarity on its role in the API.
"""

from rest_framework import generics
from apps.gyms.models import Gym, CrowdData
from apps.gyms.serializers import GymSerializer, CrowdDataSerializer


class GymListView(generics.ListAPIView):
    """
    API view for listing all gyms.

    Route:
    - GET /gyms/

    This view uses the `generics.ListAPIView` class from Django REST Framework, which provides
    built-in support for handling HTTP GET requests to list model instances. The view interacts
    with the `Gym` model and uses the `GymSerializer` to convert model instances into structured
    JSON data.

    Features:
    - Automatically queries all `Gym` instances and prefetches related `crowd_data` for efficiency.
    - Returns a list of gyms, including their details and associated crowd data.

    Attributes:
        queryset (QuerySet): All `Gym` instances with prefetched `crowd_data` for optimized queries.
        serializer_class (GymSerializer): Serializer class to structure the API response.

    Example Usage:
    - URL: `/gyms/`
    - HTTP Method: GET
    - Response: A list of all gyms in JSON format.
    """
    queryset = Gym.objects.prefetch_related("crowd_data").all()
    serializer_class = GymSerializer


class GymDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a specific gym.

    Route:
    - GET /gyms/<gym_id>/

    This view uses the `generics.RetrieveAPIView` class from Django REST Framework, which provides
    built-in support for handling HTTP GET requests to retrieve a single model instance by its unique identifier.
    The view interacts with the `Gym` model and uses the `GymSerializer` to structure the response.

    Features:
    - Automatically queries a specific `Gym` instance based on its `gym_id`.
    - Prefetches related `crowd_data` for optimized queries.

    Attributes:
        queryset (QuerySet): All `Gym` instances with prefetched `crowd_data` for optimized retrieval.
        serializer_class (GymSerializer): Serializer class to structure the API response.
        lookup_field (str): Specifies `gym_id` as the field to query for retrieving the gym.

    Example Usage:
    - URL: `/gyms/<gym_id>/`
    - HTTP Method: GET
    - Response: Details of the gym with the specified `gym_id` in JSON format.
    """
    queryset = Gym.objects.prefetch_related("crowd_data").all()
    serializer_class = GymSerializer
    lookup_field = "gym_id"


class CrowdDataListView(generics.ListCreateAPIView):
    """
    API view for listing all crowd data or creating a new entry.

    Routes:
    - GET /gyms/crowddata/
    - POST /gyms/crowddata/

    This view uses the `generics.ListCreateAPIView` class from Django REST Framework, which provides
    built-in support for handling HTTP GET and POST requests. The view interacts with the `CrowdData` model
    and uses the `CrowdDataSerializer` for serialization and validation.

    Features:
    - Handles listing all `CrowdData` entries when accessed via a GET request.
    - Allows creating a new `CrowdData` entry when accessed via a POST request with valid data.

    Attributes:
        queryset (QuerySet): All `CrowdData` instances in the database.
        serializer_class (CrowdDataSerializer): Serializer class for validation and structuring responses.

    Example Usage:
    - URL: `/gyms/crowddata/`
    - HTTP Methods:
        - GET: Returns a list of all crowd data entries.
        - POST: Accepts a JSON payload to create a new crowd data entry.

    Dependencies:
    - `CrowdDataSerializer`: Ensures that only valid data is used to create or update `CrowdData` entries.
    """
    queryset = CrowdData.objects.all()
    serializer_class = CrowdDataSerializer


class CrowdDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific crowd data entry.

    Routes:
    - GET /gyms/crowddata/<pk>/
    - PUT /gyms/crowddata/<pk>/
    - PATCH /gyms/crowddata/<pk>/
    - DELETE /gyms/crowddata/<pk>/

    This view uses the `generics.RetrieveUpdateDestroyAPIView` class from Django REST Framework,
    which provides built-in support for handling HTTP GET, PUT, PATCH, and DELETE requests. The view
    interacts with the `CrowdData` model and uses the `CrowdDataSerializer` for serialization and validation.

    Features:
    - Retrieves a specific `CrowdData` entry by its primary key (pk) using a GET request.
    - Updates the specified entry with new data when accessed via a PUT or PATCH request.
    - Deletes the specified entry when accessed via a DELETE request.

    Attributes:
        queryset (QuerySet): All `CrowdData` instances in the database.
        serializer_class (CrowdDataSerializer): Serializer class for validation and structuring responses.

    Example Usage:
    - URL: `/gyms/crowddata/<pk>/`
    - HTTP Methods:
        - GET: Retrieves details of the specified `CrowdData` entry.
        - PUT/PATCH: Updates the specified entry with valid data.
        - DELETE: Removes the specified entry from the database.
    """
    queryset = CrowdData.objects.all()
    serializer_class = CrowdDataSerializer

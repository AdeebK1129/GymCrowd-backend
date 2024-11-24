from rest_framework import generics
from apps.gyms.models import Gym, CrowdData
from apps.gyms.serializers import GymSerializer, CrowdDataSerializer

class GymListView(generics.ListAPIView):
    queryset = Gym.objects.prefetch_related("crowd_data").all()
    serializer_class = GymSerializer


class GymDetailView(generics.RetrieveAPIView):
    queryset = Gym.objects.prefetch_related("crowd_data").all()
    serializer_class = GymSerializer
    lookup_field = "id"

class CrowdDataListView(generics.ListCreateAPIView):
    """
    View for listing all CrowdData or creating a new entry.
    """
    queryset = CrowdData.objects.all()
    serializer_class = CrowdDataSerializer


class CrowdDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific CrowdData entry.
    """
    queryset = CrowdData.objects.all()
    serializer_class = CrowdDataSerializer
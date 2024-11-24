from rest_framework import generics
from apps.workouts.models import Exercise
from apps.workouts.serializers import ExerciseSerializer

class ExerciseListView(generics.ListAPIView):
    """
    API view to retrieve a list of exercises.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific exercise by ID.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'exercise_id'

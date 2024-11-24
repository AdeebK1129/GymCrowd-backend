from rest_framework import generics
from .models import Exercise, UserWorkout, WorkoutExercise
from .serializers import ExerciseSerializer, UserWorkoutSerializer, WorkoutExerciseSerializer
from rest_framework.permissions import IsAuthenticated

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

# User Workout Views
class UserWorkoutListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve all workout sessions for the authenticated user.
    POST: Create a new workout session for the authenticated user.
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter workouts by the current authenticated user
        return UserWorkout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the workout with the authenticated user
        serializer.save(user=self.request.user)


class UserWorkoutDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a specific workout session by ID for the authenticated user.
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserWorkout.objects.filter(user=self.request.user)


# Workout Exercise Views
class WorkoutExerciseListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve all workout exercises for the authenticated user's workouts.
    POST: Add a new exercise to a specific workout.
    """
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter exercises by workouts belonging to the authenticated user
        return WorkoutExercise.objects.filter(workout__user=self.request.user)
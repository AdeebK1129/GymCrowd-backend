"""
Views for the Workouts App

This module defines API views for managing exercises, user workouts, and the exercises
within workouts. These views handle operations such as retrieving exercise lists, managing
user-specific workout sessions, and managing exercises within those sessions.

Classes:
1. `ExerciseListView`: Handles retrieving a list of all exercises.
2. `ExerciseDetailView`: Handles retrieving details of a specific exercise by ID.
3. `UserWorkoutListCreateView`: Handles listing all workouts for an authenticated user or creating a new workout.
4. `UserWorkoutDetailView`: Handles retrieving details of a specific workout for an authenticated user.
5. `WorkoutExerciseListCreateView`: Handles listing or adding exercises within a user's workout.

Dependencies:
- `generics` from `rest_framework`: Base classes for creating API views.
- Models (`Exercise`, `UserWorkout`, `WorkoutExercise`) from `apps.workouts.models`: Represent exercises, workouts, and their relationships.
- Serializers (`ExerciseSerializer`, `UserWorkoutSerializer`, `WorkoutExerciseSerializer`) from `apps.workouts.serializers`: Handle validation and structuring of API data.
- `IsAuthenticated` from `rest_framework.permissions`: Ensures endpoints are protected for authenticated users.

Each view specifies exact routes and HTTP methods in its documentation to enhance clarity.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.workouts.models import Exercise, UserWorkout, WorkoutExercise
from apps.workouts.serializers import ExerciseSerializer, UserWorkoutSerializer, WorkoutExerciseSerializer


class ExerciseListView(generics.ListAPIView):
    """
    API view for retrieving a list of all exercises.

    Routes:
    - GET /api/exercises/

    Features:
    - Lists all available exercises in the database.

    Methods:
    - `GET /api/exercises/`: Returns a list of all exercises.

    Permissions:
    - No authentication required.

    Attributes:
        queryset (QuerySet): All `Exercise` instances in the database.
        serializer_class (ExerciseSerializer): Serializer for structuring the response.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a specific exercise.

    Routes:
    - GET /api/exercises/<int:exercise_id>/

    Features:
    - Retrieves a single exercise instance by its unique identifier.

    Methods:
    - `GET /api/exercises/<int:exercise_id>/`: Returns details of the specified exercise.

    Permissions:
    - No authentication required.

    Attributes:
        queryset (QuerySet): All `Exercise` instances in the database.
        serializer_class (ExerciseSerializer): Serializer for structuring the response.
        lookup_field (str): Specifies `exercise_id` as the field to query for retrieving the exercise.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'exercise_id'


class UserWorkoutListCreateView(generics.ListCreateAPIView):
    """
    API view for managing user workout sessions.

    Routes:
    - GET /api/workouts/
    - POST /api/workouts/

    Features:
    - Lists all workout sessions for the authenticated user.
    - Allows the authenticated user to create a new workout session.

    Methods:
    - `GET /api/workouts/`: Returns all workouts for the authenticated user.
    - `POST /api/workouts/`: Creates a new workout session for the authenticated user.

    Permissions:
    - Requires authentication.

    Attributes:
        serializer_class (UserWorkoutSerializer): Serializer for structuring the response.
        permission_classes (list): Ensures that only authenticated users can access this endpoint.
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters the `UserWorkout` queryset to return workouts for the authenticated user.

        Returns:
            QuerySet: A queryset of `UserWorkout` instances associated with the user.
        """
        return UserWorkout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Saves the new workout session with the current authenticated user.

        Args:
            serializer (UserWorkoutSerializer): The serializer instance containing valid data.
        """
        serializer.save(user=self.request.user)


class UserWorkoutDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a specific user workout session.

    Routes:
    - GET /api/workouts/<int:pk>/

    Features:
    - Retrieves a single workout session instance by its unique identifier for the authenticated user.

    Methods:
    - `GET /api/workouts/<int:pk>/`: Returns details of the specified workout.

    Permissions:
    - Requires authentication.

    Attributes:
        serializer_class (UserWorkoutSerializer): Serializer for structuring the response.
        permission_classes (list): Ensures that only authenticated users can access this endpoint.
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters the `UserWorkout` queryset to return workouts for the authenticated user.

        Returns:
            QuerySet: A queryset of `UserWorkout` instances associated with the user.
        """
        return UserWorkout.objects.filter(user=self.request.user)


class WorkoutExerciseListCreateView(generics.ListCreateAPIView):
    """
    API view for managing exercises within a user's workouts.

    Routes:
    - GET /api/workouts/exercises/
    - POST /api/workouts/exercises/

    Features:
    - Lists all exercises within the authenticated user's workouts.
    - Allows the authenticated user to add a new exercise to a specific workout.

    Methods:
    - `GET /api/workouts/exercises/`: Returns all exercises within the user's workouts.
    - `POST /api/workouts/exercises/`: Adds a new exercise to a specific workout.

    Permissions:
    - Requires authentication.

    Attributes:
        serializer_class (WorkoutExerciseSerializer): Serializer for structuring the response.
        permission_classes (list): Ensures that only authenticated users can access this endpoint.
    """
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters the `WorkoutExercise` queryset to return exercises within workouts
        belonging to the authenticated user.

        Returns:
            QuerySet: A queryset of `WorkoutExercise` instances associated with the user's workouts.
        """
        return WorkoutExercise.objects.filter(workout__user=self.request.user)

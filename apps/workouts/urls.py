"""
URL Configuration for the Workouts App

This module defines the URL patterns for the Workouts app. The endpoints allow 
clients to access workout-related data, including exercises, user-specific workouts, 
and exercises within those workouts.

Endpoints:
1. `/exercises/` - Lists all exercises. Corresponds to the `ExerciseListView`.
2. `/exercises/<int:exercise_id>/` - Retrieves detailed information about a specific 
   exercise based on its unique ID. Corresponds to the `ExerciseDetailView`.
3. `/` - Lists all user workouts or creates a new workout. Corresponds to the `UserWorkoutListCreateView`.
4. `/<int:pk>/` - Retrieves detailed information about a specific user workout. 
   Corresponds to the `UserWorkoutDetailView`.
5. `/workout-exercises/` - Lists all workout exercises for the authenticated user's workouts 
   or adds a new exercise to a workout. Corresponds to the `WorkoutExerciseListCreateView`.

These views use Django REST Framework's generic API views to manage data serialization 
and response generation efficiently.

Dependencies:
    - `django.urls.path`: For defining URL patterns.
    - Views from `apps.workouts.views`: Correspond to the endpoints and implement 
      the logic for handling requests.
"""

from django.urls import path
from .views import (
    ExerciseListView, 
    ExerciseDetailView, 
    UserWorkoutListCreateView, 
    UserWorkoutDetailView, 
    WorkoutExerciseListCreateView
)

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),  
    # GET /api/exercises/ - List all exercises.

    path('exercises/<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise-detail'),  
    # GET /api/exercises/<exercise_id>/ - Retrieve details of a specific exercise.

    path('', UserWorkoutListCreateView.as_view(), name='user-workout-list-create'),  
    # GET /api/workouts/ - List all user workouts.
    # POST /api/workouts/ - Create a new workout for the authenticated user.

    path('<int:pk>/', UserWorkoutDetailView.as_view(), name='user-workout-detail'),  
    # GET /api/workouts/<pk>/ - Retrieve details of a specific user workout.

    path('workout-exercises/', WorkoutExerciseListCreateView.as_view(), name='workout-exercise-list-create'),  
    # GET /api/workouts/workout-exercises/ - List all exercises in the authenticated user's workouts.
    # POST /api/workouts/workout-exercises/ - Add a new exercise to a specific workout.
]

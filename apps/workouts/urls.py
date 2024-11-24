from django.urls import path
from .views import ExerciseListView, ExerciseDetailView, UserWorkoutListCreateView, UserWorkoutDetailView, WorkoutExerciseListCreateView 


urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),  # Route for all exercises
    path('exercises/<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise-detail'),  # Route for specific exercise
    path('workouts/', UserWorkoutListCreateView.as_view(), name='user-workout-list-create'),
    path('workouts/<int:pk>/', UserWorkoutDetailView.as_view(), name='user-workout-detail'),
    path('workout-exercises/', WorkoutExerciseListCreateView.as_view(), name='workout-exercise-list-create'),
]

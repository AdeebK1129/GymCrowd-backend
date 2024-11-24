from django.urls import path
from .views import ExerciseListView, ExerciseDetailView, UserWorkoutListCreateView, UserWorkoutDetailView, WorkoutExerciseListCreateView 


urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),  # GET all exercises
    path('exercises/<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise-detail'),  # GET specific exercise
    path('', UserWorkoutListCreateView.as_view(), name='user-workout-list-create'),  # POST and GET workouts
    path('<int:pk>/', UserWorkoutDetailView.as_view(), name='user-workout-detail'),  # GET specific workout
    path('workout-exercises/', WorkoutExerciseListCreateView.as_view(), name='workout-exercise-list-create'),  # POST and GET exercises for workouts
]

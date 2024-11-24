from django.urls import path
from apps.workouts.views import ExerciseListView, ExerciseDetailView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),  # Route for all exercises
    path('exercises/<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise-detail'),  # Route for specific exercise
]

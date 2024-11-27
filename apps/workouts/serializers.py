"""
Serializers for the Workouts App

This module defines serializers for the Exercise, UserWorkout, and WorkoutExercise models,
enabling controlled serialization and deserialization of model instances into structured
representations such as JSON. These serializers facilitate the exchange of fitness-related
data between the client and server, ensuring data integrity, validation, and proper nesting of relationships.

The serializers include:
1. `ExerciseSerializer`: Serializes details of a fitness exercise.
2. `WorkoutExerciseSerializer`: Serializes individual exercises within a workout, 
   including nested exercise details.
3. `UserWorkoutSerializer`: Serializes a user's workout session, including nested 
   exercises and references to the associated user.

Dependencies:
- `rest_framework.serializers`: Provides base classes for defining serializers.
- Nested fields use `PrimaryKeyRelatedField` for user associations to avoid circular imports.

Each serializer ensures data consistency and enforces read-only or write-specific
behaviors while defining the structure of API responses for the workouts app.
"""

from rest_framework import serializers
from apps.workouts.models import Exercise, UserWorkout, WorkoutExercise


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Exercise` model.

    Converts `Exercise` instances into structured formats such as JSON, including key details like
    the exercise name, body part targeted, equipment required, and step-by-step instructions.

    Meta:
        model (Exercise): Specifies the `Exercise` model for the serializer.
        fields (list[str]): Includes all key attributes:
            - `exercise_id`: Unique identifier of the exercise.
            - `name`: Name of the exercise.
            - `body_part`: The primary body part targeted.
            - `equipment`: Equipment required for the exercise.
            - `gif_url`: Optional URL to a demonstration GIF.
            - `target`: The primary muscle group worked by the exercise.
            - `secondary_muscles`: Secondary muscles affected by the exercise.
            - `instructions`: Step-by-step instructions.

    Features:
    - Validates input data when creating or updating exercises.
    - Facilitates representation of exercises in API responses.
    """

    class Meta:
        model = Exercise
        fields = ['exercise_id', 'name', 'body_part', 'equipment', 'gif_url', 'target', 'secondary_muscles', 'instructions']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the `WorkoutExercise` model.

    Provides a detailed representation of exercises performed in a workout, including links
    to associated exercises and specific workout details like sets, reps, and weights.

    Attributes:
        exercise (PrimaryKeyRelatedField): References the associated `Exercise` by primary key.

    Meta:
        model (WorkoutExercise): Specifies the `WorkoutExercise` model for serialization.
        fields (list[str]): Includes the following attributes:
            - `entry_id`: Unique identifier for the workout exercise entry.
            - `workout`: Reference to the associated workout session.
            - `exercise`: Primary key of the associated exercise.
            - `sets`: Number of sets performed.
            - `reps`: Number of repetitions per set.
            - `weight`: Weight used during the exercise.

    Features:
    - Nested exercise details available in workout contexts.
    - Ensures accurate representation of workout data in API responses.
    """

    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())

    class Meta:
        model = WorkoutExercise
        fields = ['entry_id', 'workout', 'exercise', 'sets', 'reps', 'weight']


class UserWorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the `UserWorkout` model.

    Captures a structured representation of a user's workout session, including associated exercises
    and user information. Supports nested serialization of exercises performed in the session.

    Attributes:
        user (PrimaryKeyRelatedField): Reference to the user associated with the workout.
        workout_exercises (WorkoutExerciseSerializer): Nested serializer for exercises in the workout.

    Meta:
        model (UserWorkout): Specifies the `UserWorkout` model for serialization.
        fields (list[str]): Includes:
            - `workout_id`: Unique identifier for the workout session.
            - `user`: Reference to the user who performed the workout.
            - `date`: Date of the workout.
            - `created_at`: Timestamp of when the workout was logged.
            - `workout_exercises`: Nested representation of exercises in the workout.

    Features:
    - Handles nested workout data for seamless API integration.
    - Validates user associations and ensures integrity in workout data storage.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = UserWorkout
        fields = ['workout_id', 'user', 'date', 'created_at', 'workout_exercises']

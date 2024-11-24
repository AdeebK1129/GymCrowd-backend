"""
Serializers for the Workouts App

This module defines serializers for the Exercise, UserWorkout, and WorkoutExercise models,
enabling controlled serialization and deserialization of model instances into structured
representations such as JSON. These serializers facilitate the exchange of fitness-related
data between the client and server, ensuring data integrity, validation, and proper nesting of relationships.

The serializers include:
1. ExerciseSerializer - Serializes details of a fitness exercise.
2. WorkoutExerciseSerializer - Serializes individual exercises within a workout, 
   including nested exercise details.
3. UserWorkoutSerializer - Serializes a user's workout session, including nested 
   exercises and references to the associated user.

Dependencies:
- rest_framework.serializers: Provides base classes for defining serializers.
- Nested fields use PrimaryKeyRelatedField for user associations to avoid circular imports.

Each serializer ensures data consistency and enforces read-only or write-specific
behaviors while defining the structure of API responses for the workouts app.
"""

from rest_framework import serializers
from apps.workouts.models import Exercise, UserWorkout, WorkoutExercise


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exercise model.

    This serializer handles the conversion of Exercise model instances into a
    structured representation (e.g., JSON) and vice versa. It includes all key
    attributes describing a fitness exercise, such as its name, targeted body part,
    required equipment, and instructions.

    Meta:
        model (Exercise): Specifies the Exercise model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - exercise_id: The unique identifier of the exercise.
            - name: The name of the exercise (e.g., "Squat").
            - body_part: The primary body part targeted (e.g., "Legs").
            - equipment: Optional equipment required for the exercise.
            - gif_url: Optional URL to a demonstration GIF of the exercise.
            - target: The primary muscle group targeted by the exercise.
            - secondary_muscles: Comma-separated list of secondary muscles.
            - instructions: Detailed steps for performing the exercise.

    Example:
        Serialized Response:
        {
            "exercise_id": 1,
            "name": "Squat",
            "body_part": "Legs",
            "equipment": "Barbell",
            "gif_url": "http://example.com/squat.gif",
            "target": "Quadriceps",
            "secondary_muscles": "Hamstrings,Glutes",
            "instructions": "Stand with feet shoulder-width apart..."
        }
    """

    class Meta:
        model = Exercise
        fields = ['exercise_id', 'name', 'body_part', 'equipment', 'gif_url', 'target', 'secondary_muscles', 'instructions']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkoutExercise model.

    This serializer provides a structured representation of individual exercise entries
    within a workout session. It includes nested details of the associated Exercise and
    logs information such as sets, reps, and weights used.

    Attributes:
        exercise (ExerciseSerializer): A nested serializer for the Exercise model, included
            as a read-only field to display exercise details in the response.

    Meta:
        model (WorkoutExercise): Specifies the WorkoutExercise model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - entry_id: The unique identifier of the workout exercise entry.
            - workout: A reference to the associated workout session.
            - exercise: Nested details of the associated exercise.
            - sets: The number of sets performed.
            - reps: The number of repetitions per set.
            - weight: Optional weight used during the exercise.

    Example:
        Serialized Response:
        {
            "entry_id": 3,
            "workout": 1,
            "exercise": {
                "exercise_id": 2,
                "name": "Bench Press",
                "body_part": "Chest",
                "equipment": "Barbell",
                "gif_url": "http://example.com/benchpress.gif",
                "target": "Pectorals",
                "secondary_muscles": "Triceps",
                "instructions": "Lie flat on a bench..."
            },
            "sets": 3,
            "reps": 10,
            "weight": 60.0
        }
    """

    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['entry_id', 'workout', 'exercise', 'sets', 'reps', 'weight']


class UserWorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserWorkout model.

    This serializer provides a structured representation of a user's workout session, 
    including nested representations of the exercises performed during the workout and
    a reference to the associated user.

    Attributes:
        user (PrimaryKeyRelatedField): A reference to the associated user represented
            by their primary key to avoid circular imports.
        workout_exercises (WorkoutExerciseSerializer): A nested serializer for exercises 
            performed during the workout session, representing a one-to-many relationship 
            with the WorkoutExercise model.

    Meta:
        model (UserWorkout): Specifies the UserWorkout model for serialization.
        fields (list[str]): A list of fields to include in the serialized representation:
            - workout_id: The unique identifier of the workout session.
            - user: A reference to the associated user by primary key.
            - date: The date the workout session took place.
            - created_at: Timestamp indicating when the workout session was logged.
            - workout_exercises: Nested details of exercises performed during the workout.

    Example:
        Serialized Response:
        {
            "workout_id": 1,
            "user": 12,
            "date": "2024-01-01",
            "created_at": "2024-01-01T12:00:00Z",
            "workout_exercises": [
                {
                    "entry_id": 3,
                    "workout": 1,
                    "exercise": {
                        "exercise_id": 2,
                        "name": "Bench Press",
                        "body_part": "Chest",
                        "equipment": "Barbell",
                        "gif_url": "http://example.com/benchpress.gif",
                        "target": "Pectorals",
                        "secondary_muscles": "Triceps",
                        "instructions": "Lie flat on a bench..."
                    },
                    "sets": 3,
                    "reps": 10,
                    "weight": 60.0
                }
            ]
        }
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Avoid importing UserSerializer
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = UserWorkout
        fields = ['workout_id', 'user', 'date', 'created_at', 'workout_exercises']

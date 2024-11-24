"""
Models for the Workouts App

This module contains the database models for managing exercises, user workouts, 
and detailed workout entries. Each model defines the structure for storing fitness-related
data and their associations, providing a foundation for tracking user activities and exercise details.

The models include:
1. Exercise - Represents a specific fitness exercise, detailing its attributes 
   like targeted body parts, required equipment, and instructions.
2. UserWorkout - Represents a user's workout session, linking it to the user 
   and logging the date of the session.
3. WorkoutExercise - Represents individual exercise entries within a workout, 
   capturing details like sets, repetitions, and weights used.

These models utilize Django's ORM (Object-Relational Mapping) to abstract database 
operations and efficiently manage fitness-related data.
"""

from django.db import models
from apps.users.models import User


class Exercise(models.Model):
    """
    Represents a fitness exercise with detailed attributes.

    This model defines the structure for storing information about a specific exercise, 
    including its name, targeted body part, required equipment, and step-by-step instructions. 
    Exercises can be linked to multiple workout sessions through the WorkoutExercise model.

    Attributes:
        exercise_id (int): Auto-incrementing primary key for uniquely identifying an exercise.
        name (str): The name of the exercise (e.g., "Bench Press"). Stored as a CharField with a max length of 255.
        body_part (str): The primary body part targeted by the exercise (e.g., "Chest").
        equipment (str): Optional field specifying the required equipment (e.g., "Barbell").
        gif_url (str): Optional URL for a demonstration GIF of the exercise. Stored as a TextField.
        target (str): The primary muscle group targeted by the exercise (e.g., "Pectorals").
        secondary_muscles (str): Optional comma-separated list of secondary muscles targeted.
        instructions (str): Detailed instructions on how to perform the exercise.

    Methods:
        __str__(): Returns the name of the exercise.

    Related Models:
        - WorkoutExercise: Links this model to workout sessions in the UserWorkout model.

    Example:
        >>> exercise = Exercise(name="Squat", body_part="Legs", target="Quadriceps")
        >>> print(exercise)
        Squat
    """

    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    body_part = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100, null=True, blank=True)
    gif_url = models.TextField(null=True, blank=True)
    target = models.CharField(max_length=100)
    secondary_muscles = models.TextField(null=True, blank=True)
    instructions = models.TextField()

    def __str__(self):
        """
        Provides a human-readable representation of the exercise.

        Returns:
            str: The name of the exercise.
        """
        return self.name


class UserWorkout(models.Model):
    """
    Represents a user's workout session.

    This model logs a workout session for a user, capturing the date of the workout 
    and linking it to the associated user. Multiple exercises can be associated with 
    a workout session through the WorkoutExercise model.

    Attributes:
        workout_id (int): Auto-incrementing primary key for uniquely identifying a workout session.
        user (ForeignKey): A foreign key linking to the User model, representing the user who performed the workout.
        date (date): The date the workout session took place.
        created_at (datetime): Timestamp indicating when the workout session was logged.

    Methods:
        __str__(): Returns a string representation of the workout, including the user's name and workout date.

    Related Models:
        - WorkoutExercise: Links this model to specific exercises performed during the workout.

    Example:
        >>> user = User.objects.get(name="Jane Doe")
        >>> workout = UserWorkout(user=user, date="2024-01-01")
        >>> print(workout)
        Workout by Jane Doe on 2024-01-01
    """

    workout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a human-readable representation of the user workout.

        Returns:
            str: A string combining the user's name and the workout date.
        """
        return f"Workout by {self.user.name} on {self.date}"


class WorkoutExercise(models.Model):
    """
    Represents an individual exercise entry within a workout session.

    This model stores detailed information about a specific exercise performed during a 
    workout, including the number of sets, repetitions, and optional weight. Each entry 
    is linked to a workout session and an exercise.

    Attributes:
        entry_id (int): Auto-incrementing primary key for uniquely identifying a workout exercise entry.
        workout (ForeignKey): A foreign key linking to the UserWorkout model, representing the workout session.
        exercise (ForeignKey): A foreign key linking to the Exercise model, representing the exercise performed.
        sets (int): The number of sets performed for this exercise.
        reps (int): The number of repetitions performed in each set.
        weight (float): Optional field specifying the weight used for the exercise (in kilograms).

    Methods:
        __str__(): Returns a string representation of the workout exercise, including the exercise name, sets, and reps.

    Related Models:
        - UserWorkout: Links this model to the workout session the exercise is part of.
        - Exercise: Links this model to the exercise being performed.

    Example:
        >>> exercise = Exercise.objects.get(name="Bench Press")
        >>> workout = UserWorkout.objects.get(workout_id=1)
        >>> workout_exercise = WorkoutExercise(workout=workout, exercise=exercise, sets=3, reps=10, weight=80)
        >>> print(workout_exercise)
        Bench Press - 3x10
    """

    entry_id = models.AutoField(primary_key=True)
    workout = models.ForeignKey(UserWorkout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workout_entries')
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        """
        Provides a human-readable representation of the workout exercise.

        Returns:
            str: A string combining the exercise name, sets, and reps.
        """
        return f"{self.exercise.name} - {self.sets}x{self.reps}"
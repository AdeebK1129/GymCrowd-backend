"""
Models for the Users App

This module contains the database models for managing user information and preferences.
Each model defines a specific table structure in the database, along with fields and
relationships necessary for interacting with the users and their preferences in the application.

The models include:
1. `User` - Represents a system user, including personal details and account credentials.
2. `UserPreference` - Represents user-specific preferences related to gym crowd levels and gym association.

These models utilize Django's ORM (Object-Relational Mapping) to abstract database
operations, enabling efficient interactions without needing raw SQL.
"""

from django.db import models
from apps.gyms.models import Gym


class User(models.Model):
    """
    Represents a user of the application.

    This model defines the core attributes for a user, including their ID, name, email,
    hashed password, and creation timestamp. It is designed to provide essential
    user account information and serves as the primary table for user-related data.

    Attributes:
        user_id (int): Auto-incrementing primary key for uniquely identifying a user.
        name (str): The full name of the user. Stored as a `CharField` with a max length of 100.
        email (str): Unique email address used for user identification and communication.
            This field uses Django's `EmailField` to validate email format.
        password_hash (str): Hashed representation of the user's password.
            Stored as a `TextField` to accommodate various hashing techniques (e.g., bcrypt).
        created_at (datetime): Timestamp indicating when the user account was created.
            Automatically populated using `auto_now_add`.

    Methods:
        __str__(): Returns the string representation of the user, which is their name.

    Related Models:
        - `UserPreference`: Each user may have multiple preferences defined by the `UserPreference` model.

    Example:
        >>> user = User(name="John Doe", email="johndoe@example.com")
        >>> print(user)
        John Doe
    """

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    password_hash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a human-readable representation of the user.

        Returns:
            str: The name of the user.
        """
        return self.name


class UserPreference(models.Model):
    """
    Represents a user's preferences related to gym crowd levels and gym selection.

    This model captures specific preferences set by a user for a particular gym. 
    It links the user to a gym and allows customization of acceptable crowd levels.
    The `UserPreference` model is linked to the `User` model via a foreign key, establishing 
    a one-to-many relationship (one user can have multiple preferences). Additionally, 
    it is linked to the `Gym` model, signifying which gym the preference applies to.

    Attributes:
        preference_id (int): Auto-incrementing primary key for uniquely identifying a user preference.
        user (ForeignKey): A foreign key linking to the `User` model. Deletion of the user 
            cascades and removes associated preferences.
        gym (ForeignKey): A foreign key linking to the `Gym` model. Deletion of the gym
            cascades and removes associated user preferences.
        max_crowd_level (float): The maximum crowd level the user finds acceptable at a gym.
            Stored as a `FloatField` to allow precise crowd level specifications.
        created_at (datetime): Timestamp indicating when the preference was created.
            Automatically populated using `auto_now_add`.

    Methods:
        __str__(): Returns a string representation of the user preference, combining the 
        user's name and the gym's name.

    Related Models:
        - `User`: A user can have multiple preferences for different gyms.
        - `Gym`: A gym can have multiple user preferences indicating acceptable crowd levels.

    Example:
        >>> user = User.objects.get(name="John Doe")
        >>> gym = Gym.objects.get(name="Downtown Gym")
        >>> preference = UserPreference(user=user, gym=gym, max_crowd_level=0.7)
        >>> print(preference)
        John Doe - Downtown Gym
    """

    preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='user_preferences')
    max_crowd_level = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a human-readable representation of the user preference.

        Returns:
            str: A string combining the user's name and the gym's name.
        """
        return f"{self.user.name} - {self.gym.name}"
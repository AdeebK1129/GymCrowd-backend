"""
Models for the Gyms App

This module defines the database models for representing gyms and their associated crowd data.
The models enable the persistence and relational management of gym and occupancy details in the database.

Classes:
1. `Gym` - Represents a gym entity, including its name, location, type, and creation timestamp.
2. `CrowdData` - Represents the crowd data for a gym, capturing occupancy metrics, percentage full, 
   and the timestamp of the latest update.

Relationships:
- `CrowdData` has a many-to-one relationship with `Gym`, meaning each gym can have multiple associated crowd data entries.

Dependencies:
- `django.db.models`: Provides the base `Model` class and field types such as `CharField`, `TextField`, 
  `IntegerField`, `FloatField`, and `DateTimeField`.
"""

from django.db import models


class Gym(models.Model):
    """
    Represents a gym in the system.

    This model stores essential details about a gym, including its name, location, type, 
    and the date it was added to the system. Each gym may have multiple associated crowd data records.

    Attributes:
        gym_id (AutoField): Primary key for the gym, auto-incremented.
        name (CharField): The name of the gym (e.g., "Downtown Fitness"), with a maximum length of 255 characters.
        location (TextField): The gym's address or general location.
        type (CharField): The type or category of the gym (e.g., "Fitness", "Yoga").
        created_at (DateTimeField): Timestamp for when the gym entry was created, set automatically.

    Relationships:
        - One-to-many relationship with `CrowdData`:
          - Gym -> CrowdData: A gym can have multiple crowd data records.
          - Reverse access via `crowd_data` (e.g., `gym.crowd_data.all()`).

    Methods:
        __str__(): Returns the gym's name as its string representation.

    Example:
        A gym entry might represent:
        {
            "gym_id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main St, Cityville",
            "type": "Fitness",
            "created_at": "2024-01-01T12:00:00Z"
        }
    """

    gym_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.TextField()
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CrowdData(models.Model):
    """
    Represents crowd data for a gym.

    This model captures dynamic metrics about a gym's current occupancy, including the number of people present,
    the percentage of the gym's capacity in use, and the timestamp of the latest update. 

    Attributes:
        crowd_id (AutoField): Primary key for the crowd data entry.
        gym (ForeignKey): Links the crowd data to a specific `Gym` instance. Deleting the gym removes its related data.
        occupancy (IntegerField): Number of people currently checked in.
        percentage_full (FloatField): Percentage of gym capacity currently in use. Nullable for cases without data.
        last_updated (DateTimeField): Timestamp of the most recent update.

    Relationships:
        - Many-to-one relationship with `Gym`:
          - CrowdData -> Gym: Each crowd data entry corresponds to one gym.
          - Reverse access via `gym.crowd_data` (e.g., `gym.crowd_data.all()`).

    Methods:
        __str__(): Returns a formatted string representation of the gym's crowd data, 
        including its name, current occupancy, and percentage full.

    Example:
        A crowd data entry might represent:
        {
            "crowd_id": 101,
            "gym": {
                "gym_id": 1,
                "name": "Downtown Fitness"
            },
            "occupancy": 35,
            "percentage_full": 70.0,
            "last_updated": "2024-01-01T15:00:00Z"
        }
    """

    crowd_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='crowd_data')
    occupancy = models.IntegerField()
    percentage_full = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        """
        String representation of the CrowdData instance.

        Returns:
            str: A string combining the gym's name, occupancy count, and percentage full.
        """
        occupancy_str = f"{self.occupancy} people"
        percentage_str = f"{self.percentage_full:.2f}%" if self.percentage_full is not None else "NA"
        return f"{self.gym.name} - {occupancy_str}, {percentage_str}"

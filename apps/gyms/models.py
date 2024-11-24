"""
Models for the Gyms App

This module defines the database models for representing gyms and their associated crowd data.
The models are used to persist data and establish relationships between gyms and occupancy details.

Classes:
1. `Gym` - Represents a gym, including its name, location, type, and creation date.
2. `CrowdData` - Represents crowd data for a gym, including occupancy, percentage full, and the timestamp of the last update.

Relationships:
- `CrowdData` has a many-to-one relationship with `Gym`, enabling each gym to have multiple crowd data entries.

Dependencies:
- `django.db.models`: Provides the base `Model` class and field types for defining attributes.
"""

from django.db import models


class Gym(models.Model):
    """
    Represents a gym in the system.

    This model stores information about gyms, including their name, location, type, and the
    timestamp of their creation. Each gym may have multiple associated crowd data records,
    defining its current occupancy status over time.

    Attributes:
        gym_id (AutoField): Primary key for the gym, auto-incremented.
        name (CharField): The name of the gym, with a maximum length of 255 characters.
        location (TextField): The address or general location of the gym.
        type (CharField): The type or category of the gym (e.g., fitness, yoga, climbing),
            with a maximum length of 100 characters.
        created_at (DateTimeField): Timestamp indicating when the gym record was created.
            Automatically set upon creation.

    Relationships:
        - One-to-many relationship with `CrowdData`:
            - Gym -> CrowdData: A gym can have multiple crowd data entries.
            - Reverse relation: `crowd_data` (e.g., `gym.crowd_data.all()` retrieves all related entries).

    Methods:
        __str__(): Returns the name of the gym as its string representation.

    Example:
        A gym entry might represent:
        ```json
        {
            "gym_id": 1,
            "name": "Downtown Gym",
            "location": "123 Main Street, Cityville",
            "type": "Fitness",
            "created_at": "2024-01-01T12:00:00Z"
        }
        ```
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

    This model stores information about gym occupancy, including the number of people checked in,
    the percentage full, and the timestamp of the last update. The data is linked to a specific
    gym through a foreign key relationship. The `percentage_full` field is nullable to handle cases
    where no data is available (e.g., when the gym is closed).

    Attributes:
        crowd_id (AutoField): Primary key for the crowd data entry, auto-incremented.
        gym (ForeignKey): A reference to the associated `Gym` model, establishing a many-to-one
            relationship. If a gym is deleted, all related crowd data entries are also deleted.
        occupancy (IntegerField): The number of people currently checked into the gym.
        percentage_full (FloatField): The percentage of gym capacity currently in use, represented
            as a float (e.g., 64.0 for 64%). This field is nullable and may be blank if no data is available.
        last_updated (DateTimeField): Timestamp of the most recent update to the crowd data.

    Relationships:
        - Many-to-one relationship with `Gym`:
            - CrowdData -> Gym: Each crowd data entry is linked to one gym.
            - Reverse relation: `gym.crowd_data` retrieves all associated crowd data entries.

    Methods:
        __str__(): Returns a formatted string combining the gym name, occupancy, and percentage full.

    Example:
        A crowd data entry might represent:
        ```json
        {
            "crowd_id": 10,
            "gym": {
                "gym_id": 1,
                "name": "Downtown Gym"
            },
            "occupancy": 32,
            "percentage_full": 64.0,
            "last_updated": "2024-01-01T15:00:00Z"
        }
        ```
    """

    crowd_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='crowd_data')
    occupancy = models.IntegerField()  # Number of people checked in
    percentage_full = models.FloatField(null=True, blank=True)  # Nullable percentage full
    last_updated = models.DateTimeField()

    def __str__(self):
        occupancy_str = f"{self.occupancy} people"
        percentage_str = f"{self.percentage_full:.2f}%" if self.percentage_full is not None else "NA"
        return f"{self.gym.name} - {occupancy_str}, {percentage_str}"

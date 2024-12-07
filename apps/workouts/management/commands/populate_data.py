"""
Data Population Management Command for the GymCrowd Project

This command populates the database with initial data for exercises and gyms. It is designed to 
handle data insertion and updates for the `Exercise` and `Gym` models, ensuring that existing 
records are updated without duplication while adding new entries as required.

Modules and Features:
1. `populate_exercises`: Reads data from a JSON file (`exercises.json`), processes it, and inserts 
   or updates exercise records in the database.
2. `populate_gyms`: Initializes gym data from a predefined dataset and ensures gym records 
   are updated or added as needed.

Dependencies:
- `os`, `pandas`, `json`: For managing file paths and efficient data manipulation.
- `django`: For database interaction using the ORM.
- `logging`: To log the progress and errors during execution.

Execution:
- Run this command via `python manage.py populate_data` to initialize the database with 
  default exercises and gym data. The command can be rerun to update existing records or add 
  new entries without causing duplication.

"""

import os
import logging
import pandas as pd
import json
from django.core.management.base import BaseCommand
from apps.workouts.models import Exercise
from apps.gyms.models import Gym


class Command(BaseCommand):
    """
    Custom Django management command for populating the database with initial data.

    Attributes:
        help (str): Description of the management command displayed in the help menu.
    """

    help = 'Populates the database with initial exercise and gym data'

    def handle(self, *args, **options):
        """
        Main entry point for the command. Executes the data population functions for exercises
        and gyms sequentially. Logs the progress and outcomes of each operation, providing a 
        summary of the database updates or errors encountered.
        """
        try:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
            logging.info("Starting data population...")
            self.populate_exercises()
            self.populate_gyms()
            logging.info("Data population completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred during data population: {e}")

    def populate_exercises(self):
        """
        Populate the database with exercise data.

        Reads exercise data from a JSON file (`exercises.json`), processes it, and populates the 
        `Exercise` model. Existing records are updated, and new records are inserted in bulk 
        for efficiency.

        Steps:
        1. Reads the JSON file and processes the data using `pandas`.
        2. Updates existing exercise records based on the exercise name.
        3. Inserts new exercise records in bulk using Django's ORM.

        Logging:
        - Logs the number of updated and newly inserted records.
        - Logs errors if the JSON file is missing or if any exception occurs.

        Dependencies:
        - `pandas`: For efficient data manipulation.
        - `json`: For reading exercise data.

        Raises:
        - Logs errors if the JSON file is not found or processing fails.
        """
        try:
            logging.info("Populating exercises...")
            json_file_path = os.path.join(os.path.dirname(__file__), 'exercises.json')

            if not os.path.exists(json_file_path):
                logging.error(f"Exercises file not found: {json_file_path}")
                return

            with open(json_file_path, 'r') as f:
                exercise_data = json.load(f)

            df = pd.DataFrame(exercise_data)

            # Transform data for secondary muscles and instructions
            df['secondaryMuscles'] = df['secondaryMuscles'].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
            df['instructions'] = df['instructions'].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

            # Fetch existing exercises from the database
            existing_exercises = set(Exercise.objects.values_list('name', flat=True))

            # Split data into new and existing records
            df_existing = df[df['name'].isin(existing_exercises)]
            df_new = df[~df['name'].isin(existing_exercises)]

            # Update existing records
            for _, row in df_existing.iterrows():
                Exercise.objects.filter(name=row['name']).update(
                    body_part=row['bodyPart'],
                    equipment=row['equipment'],
                    gif_url=row['gifUrl'],
                    target=row['target'],
                    secondary_muscles=row['secondaryMuscles'],
                    instructions=row['instructions'],
                )

            # Bulk insert new records
            new_records = [
                Exercise(
                    name=row['name'],
                    body_part=row['bodyPart'],
                    equipment=row['equipment'],
                    gif_url=row['gifUrl'],
                    target=row['target'],
                    secondary_muscles=row['secondaryMuscles'],
                    instructions=row['instructions'],
                )
                for _, row in df_new.iterrows()
            ]
            Exercise.objects.bulk_create(new_records, batch_size=500)
            logging.info(f"Inserted {len(new_records)} new exercises.")
        except Exception as e:
            logging.error(f"Error populating exercises: {e}")

    def populate_gyms(self):
        """
        Populate the database with gym data.

        Initializes gym data using a predefined dataset. Updates existing records if the gym 
        already exists, and inserts new records in bulk for efficiency.

        Steps:
        1. Defines a dataset of gym details as a list of dictionaries.
        2. Updates existing gym records based on the gym name.
        3. Inserts new gym records in bulk using Django's ORM.

        Logging:
        - Logs the number of updated and newly inserted gym records.
        - Logs errors if any exception occurs during processing.

        Dependencies:
        - `pandas`: For efficient data manipulation.

        Raises:
        - Logs errors if processing fails or unexpected issues occur.
        """
        try:
            logging.info("Populating gyms...")
            gym_data = [
                {"name": "Helen Newman Fitness Center", "location": "163 Cradit Farm Dr, Ithaca, NY 14850", "type": "Fitness"},
                {"name": "Noyes Fitness Center", "location": "306 West Ave, Ithaca, NY 14850", "type": "Fitness"},
                {"name": "Teagle Down Fitness Center", "location": "512 Campus Rd, Ithaca, NY 14853", "type": "Fitness"},
                {"name": "Teagle Up Fitness Center", "location": "512 Campus Rd, Ithaca, NY 14853", "type": "Fitness"},
                {"name": "Toni Morrison Fitness Center", "location": "18 Sisson Pl, Ithaca, NY 14850", "type": "Fitness"},
                {"name": "HNH Court 1 Basketball", "location": "163 Cradit Farm Dr, Ithaca, NY 14850", "type": "Fitness"},
                {"name": "HNH Court 2 Volleyball/Badminton", "location": "163 Cradit Farm Dr, Ithaca, NY 14850", "type": "Fitness"},
                {"name": "Noyes Court Basketball", "location": "306 West Ave, Ithaca, NY 14850", "type": "Fitness"},
            ]

            df = pd.DataFrame(gym_data)
            existing_gyms = set(Gym.objects.values_list('name', flat=True))

            # Split data into new and existing records
            df_existing = df[df['name'].isin(existing_gyms)]
            df_new = df[~df['name'].isin(existing_gyms)]

            # Update existing records
            for _, row in df_existing.iterrows():
                Gym.objects.filter(name=row['name']).update(location=row['location'], type=row['type'])
            logging.info(f"Updated {len(df_existing)} existing gyms.")

            # Bulk insert new gyms
            new_records = [Gym(name=row['name'], location=row['location'], type=row['type']) for _, row in df_new.iterrows()]
            Gym.objects.bulk_create(new_records, batch_size=500)
            logging.info(f"Inserted {len(new_records)} new gyms.")
        except Exception as e:
            logging.error(f"Error populating gyms: {e}")

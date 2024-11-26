import os
import sys
import django
import logging

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymcrowd.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# Import models
from apps.workouts.models import Exercise
from apps.gyms.models import Gym
import pandas as pd
import json

def populate_exercises():
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

def populate_gyms():
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

if __name__ == "__main__":
    try:
        logging.info("Starting data population...")
        populate_exercises()
        populate_gyms()
        logging.info("Data population completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during data population: {e}")

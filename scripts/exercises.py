# Import necessary libraries
import os
import django
import pandas as pd
import json

# Set up Django environment
os.chdir("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymcrowd.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" 
django.setup()

# Import models
from apps.workouts.models import Exercise

# Load JSON data into a pandas DataFrame
json_file_path = 'scripts/exercises.json'

with open(json_file_path, 'r') as f:
    exercise_data = json.load(f)

# Convert JSON data to pandas DataFrame
df = pd.DataFrame(exercise_data)
df.head()  # Display the first few rows for verification

# Transform data for secondary muscles and instructions
df['secondaryMuscles'] = df['secondaryMuscles'].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
df['instructions'] = df['instructions'].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
df.head()  # Check transformed data

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

# Import necessary libraries
import os
import django
import pandas as pd

os.chdir("..")  # Adjust the path to point to the root of your project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymcrowd.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.gyms.models import Gym

gym_data = [
    {
        "name": "Helen Newman Fitness Center",
        "location": "163 Cradit Farm Dr, Ithaca, NY 14850",
        "type": "Fitness",
    },
    {
        "name": "Noyes Fitness Center",
        "location": "306 West Ave, Ithaca, NY 14850",
        "type": "Fitness",
    },
    {
        "name": "Teagle Down Fitness Center",
        "location": "512 Campus Rd, Ithaca, NY 14853",
        "type": "Fitness",
    },
    {
        "name": "Teagle Up Fitness Center",
        "location": "512 Campus Rd, Ithaca, NY 14853",
        "type": "Fitness",
    },
    {
        "name": "Toni Morrison Fitness Center",
        "location": "18 Sisson Pl, Ithaca, NY 14850",
        "type": "Fitness",
    },
        {
        "name": "HNH Court 1 Basketball",
        "location": "163 Cradit Farm Dr, Ithaca, NY 14850",
        "type": "Fitness",
    },
        {
        "name": "HNH Court 2 Volleyball/Badminton",
        "location": "163 Cradit Farm Dr, Ithaca, NY 14850",
        "type": "Fitness",
    },
        {
        "name": "Noyes Court Basketball",
        "location": "306 West Ave, Ithaca, NY 14850",
        "type": "Fitness",
    }
]

df = pd.DataFrame(gym_data)
print(f"Loaded {len(df)} gyms from the dataset.")
df.head()

existing_gyms = set(Gym.objects.values_list('name', flat=True))

# Split data into new and existing records
df_existing = df[df['name'].isin(existing_gyms)]
df_new = df[~df['name'].isin(existing_gyms)]

print(f"Existing gyms: {len(df_existing)}")
print(f"New gyms: {len(df_new)}")

for _, row in df_existing.iterrows():
    Gym.objects.filter(name=row['name']).update(
        location=row['location'],
        type=row['type'],
    )
print("Updated existing gyms.")

# Bulk insert new gyms
new_records = [
    Gym(
        name=row['name'],
        location=row['location'],
        type=row['type'],
    )
    for _, row in df_new.iterrows()
]
Gym.objects.bulk_create(new_records, batch_size=500)

print(f"Inserted {len(new_records)} new gyms.")

# Verify the database content
total_gyms = Gym.objects.count()
print(f"Total gyms in the database: {total_gyms}")

# Display some records from the database
Gym.objects.all()[:5]  # Display the first 5 records

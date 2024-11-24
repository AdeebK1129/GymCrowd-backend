import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apps.gyms.models import Gym, CrowdData


def scrape_gym_data():
    """
    Scrapes gym data from the Connect2Concepts website and updates the database.
    """
    url = "https://www.connect2concepts.com/connect2/?type=bar&key=355de24d-d0e4-4262-ae97-bc0c78b92839&loc_status=false"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code} \n")  # Debug: Check response status

    if response.status_code != 200:
        raise Exception("Failed to fetch gym data")

    soup = BeautifulSoup(response.text, "html.parser")
    facilities = soup.find_all("div", class_="barChart")
    print(f"Number of facilities found: {len(facilities)} \n")  # Debug: Check number of facilities found

    data_list = []

    for facility in facilities:
        try:
            # Extract gym name (strip excess whitespace)
            raw_text = facility.text.strip()
            name_element = raw_text.split("Last Count:")[0].strip()  # Extract everything before "Last Count:"
            name = name_element if name_element else "Unknown"
            print(f"Name: {name} \n")  # Debug: Print extracted name

            # Extract last count
            count_text = facility.text.split("Last Count: ")[1].split("Updated:")[0].strip()
            count = count_text if count_text else "NA"
            print(f"Count: {count} \n")  # Debug: Print extracted count

            # Extract updated timestamp
            updated_text = facility.text.split("Updated: ")[1].split("\n")[0].strip()
            updated = updated_text if updated_text else None
            print(f"Updated: {updated} \n")  # Debug: Print extracted updated timestamp

            # Extract percentage full
            percentage_element = facility.find("span", class_="barChart__value")
            percentage_full = (
                float(percentage_element.text.replace("%", "").strip()) if percentage_element and percentage_element.text != "NA" else None
            )
            print(f"Percentage Full: {percentage_full} \n")  # Debug: Print extracted percentage full

            # Parse occupancy (if count is not NA)
            occupancy = 0 if count == "NA" else int(count)
            print(f"Occupancy: {occupancy} \n")  # Debug: Print parsed occupancy

            # Parse updated time (if available)
            updated_time = (
                datetime.strptime(updated, "%m/%d/%Y %I:%M %p") if updated else None
            )
            print(f"Updated Time: {updated_time} \n")  # Debug: Print parsed datetime object

            # Search for existing gym and create CrowdData entry
            try:
                gym = Gym.objects.get(name=name)  # Match based on existing name
                print(f"Found existing gym: {gym.name} \n")
            except Gym.DoesNotExist:
                print(f"No matching gym found for {name}. Skipping entry. \n")
                continue

            data_list.append({
                "gym": gym,
                "occupancy": occupancy,
                "percentage_full": percentage_full,
                "last_updated": updated_time,
            })
        except Exception as e:
            print(f"Error parsing facility data: {e} \n")  # Debug: Log any parsing errors

    print(f"Final Data List: {data_list} \n")  # Debug: Check the final data list before updating the database

    # Update the database
    for data in data_list:
        try:
            CrowdData.objects.update_or_create(
                gym=data["gym"],
                defaults={
                    "occupancy": data["occupancy"],
                    "percentage_full": data["percentage_full"],
                    "last_updated": data["last_updated"],
                },
            )
            print(f"Updated CrowdData for gym: {data['gym'].name} \n")  # Debug: Confirm database update
        except Exception as e:
            print(f"Error updating database: {e} \n")  # Debug: Log any database errors

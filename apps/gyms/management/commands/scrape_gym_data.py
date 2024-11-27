from django.core.management.base import BaseCommand
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apps.gyms.models import Gym, CrowdData

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Command(BaseCommand):
    help = "Scrape gym data from the external source and update the database."

    def handle(self, *args, **options):
        self.scrape_gym_data()

    def scrape_gym_data(self):
        """
        Scrapes gym data from the Connect2Concepts website and updates the database.
        """
        logging.info("Starting gym data scraping...")
        url = "https://www.connect2concepts.com/connect2/?type=bar&key=355de24d-d0e4-4262-ae97-bc0c78b92839&loc_status=false"
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        try:
            response = requests.get(url, headers=headers)
            logging.info(f"Status Code: {response.status_code}")

            if response.status_code != 200:
                raise Exception("Failed to fetch gym data")

            soup = BeautifulSoup(response.text, "html.parser")
            facilities = soup.find_all("div", class_="barChart")
            logging.info(f"Number of facilities found: {len(facilities)}")

            data_list = []

            for facility in facilities:
                try:
                    raw_text = facility.text.strip()
                    name = raw_text.split("Last Count:")[0].strip()
                    count_text = facility.text.split("Last Count: ")[1].split("Updated:")[0].strip()
                    count = 0 if count_text == "NA" else int(count_text)
                    updated_text = facility.text.split("Updated: ")[1].split("\n")[0].strip()
                    updated_time = datetime.strptime(updated_text, "%m/%d/%Y %I:%M %p") if updated_text else None
                    percentage_element = facility.find("span", class_="barChart__value")
                    percentage_full = (
                        float(percentage_element.text.replace("%", "").strip()) if percentage_element and percentage_element.text != "NA" else None
                    )

                    # Fetch the gym from the database
                    gym = Gym.objects.get(name=name)
                    logging.info(f"Found gym: {gym.name}")

                    data_list.append({
                        "gym": gym,
                        "occupancy": count,
                        "percentage_full": percentage_full,
                        "last_updated": updated_time,
                    })
                except Gym.DoesNotExist:
                    logging.warning(f"No matching gym found for {name}. Skipping entry.")
                except Exception as e:
                    logging.error(f"Error parsing facility data: {e}")

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
                    logging.info(f"Updated CrowdData for gym: {data['gym'].name}")
                except Exception as e:
                    logging.error(f"Error updating database: {e}")

        except Exception as e:
            logging.error(f"Scraper error: {e}")

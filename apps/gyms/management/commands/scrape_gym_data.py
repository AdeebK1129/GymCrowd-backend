"""
Management Command for Scraping Gym Data

This module defines a custom Django management command to scrape gym data from an 
external source (Connect2Concepts) and update the database. The scraping logic fetches 
occupancy, crowd percentage, and last updated timestamps for gyms and stores them in 
the database, associating the data with the appropriate `Gym` and `CrowdData` models.

This script ensures that gym crowd data is periodically refreshed and reflects real-time 
occupancy levels. It utilizes the Django ORM for interacting with database models and 
employs robust error handling to manage potential scraping issues.

Dependencies:
    - `django.core.management.base.BaseCommand`: Provides the base class for management commands.
    - `requests`: Enables HTTP requests for fetching external data.
    - `bs4.BeautifulSoup`: Parses HTML content to extract relevant data.
    - `datetime.datetime`: Handles date and time parsing for occupancy updates.
    - `logging`: Configures logging to provide detailed runtime feedback.
"""

from django.core.management.base import BaseCommand
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apps.gyms.models import Gym, CrowdData

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Command(BaseCommand):
    """
    Custom Django management command to scrape gym data.

    This command scrapes gym data from the Connect2Concepts API and updates 
    the `Gym` and `CrowdData` models in the database. It fetches details such 
    as occupancy, percentage full, and last updated timestamp for each gym.

    Attributes:
        help (str): A brief description of the command, displayed in Django's 
            management command help menu.
    """

    help = "Scrape gym data from the external source and update the database."

    def handle(self, *args, **options):
        """
        Entry point for the management command.

        Executes the `scrape_gym_data` method to perform the scraping task. 
        This method is called when the management command is executed via the 
        command line.

        Args:
            *args: Variable length argument list for the command.
            **options: Arbitrary keyword arguments passed to the command.

        Returns:
            None

        Raises:
            Any exceptions during execution are logged for debugging.
        """
        self.scrape_gym_data()

    def scrape_gym_data(self):
        """
        Scrapes gym data from the Connect2Concepts website and updates the database.

        The method fetches gym data using the `requests` library and processes the 
        HTML content using `BeautifulSoup`. It extracts gym details such as name, 
        occupancy count, percentage full, and last updated timestamp. The data is 
        associated with the corresponding `Gym` model entry, and the `CrowdData` 
        table is updated accordingly.

        Steps:
            1. Send an HTTP GET request to fetch gym data from the external source.
            2. Parse the HTML content using BeautifulSoup.
            3. Extract relevant data for each gym and match it with the database.
            4. Update the `CrowdData` model with the new data or create an entry 
               if it does not exist.
            5. Handle errors such as missing gyms or failed HTTP requests gracefully.

        External API:
            Connect2Concepts API - Fetches gym data from:
            `https://www.connect2concepts.com/connect2/?type=bar&key=<key>&loc_status=false`

        Returns:
            None

        Raises:
            - HTTPError: If the HTTP request fails.
            - Gym.DoesNotExist: If a gym is not found in the database.
            - Other exceptions are logged for debugging purposes.
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
                    # Extract gym details
                    raw_text = facility.text.strip()
                    name = raw_text.split("Last Count:")[0].strip()
                    count_text = facility.text.split("Last Count: ")[1].split("Updated:")[0].strip()
                    count = 0 if count_text == "NA" else int(count_text)
                    updated_text = facility.text.split("Updated: ")[1].split("\n")[0].strip()
                    updated_time = datetime.strptime(updated_text, "%m/%d/%Y %I:%M %p") if updated_text else None
                    percentage_element = facility.find("span", class_="barChart__value")
                    percentage_full = (
                        float(percentage_element.text.replace("%", "").strip()) 
                        if percentage_element and percentage_element.text != "NA" 
                        else None
                    )

                    # Fetch the gym from the database
                    gym = Gym.objects.get(name=name)
                    logging.info(f"Found gym: {gym.name}")

                    # Append data for database update
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

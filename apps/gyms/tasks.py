from celery import shared_task
from apps.gyms.scraper import scrape_gym_data

@shared_task
def scrape_and_update_gym_data():
    """
    Periodically scrape gym data and update the database.
    """
    try:
        scrape_gym_data()
    except Exception as e:
        print(f"Error during scraping: {e}")

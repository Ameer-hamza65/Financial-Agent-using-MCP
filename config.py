import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    BRIGHT_DATA_API_TOKEN = os.getenv("BRIGHT_DATA_API_TOKEN")
    WEB_UNLOCKER_ZONE = os.getenv("WEB_UNLOCKER_ZONE", "unblocker")
    BROWSER_ZONE = os.getenv("BROWSER_ZONE", "scraping_browser")
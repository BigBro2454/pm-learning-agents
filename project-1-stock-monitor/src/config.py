import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

    # Application Settings
    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300")) # Default 5 minutes
    
    # Topic to monitor
    TOPIC = os.getenv("TOPIC", "Artificial Intelligence and Machine Learning")
    
    # RSS Feeds to monitor
    RSS_FEEDS = [
        "https://news.google.com/rss/search?q=" + TOPIC.replace(" ", "+"),
        # Add more RSS feeds here if needed
    ]

    # Database Path
    DB_PATH = "memory.db"

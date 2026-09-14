import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key for Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model configurations
MODEL_NAME = "gemini-2.5-flash"  # Flash model is fast and suitable for this task

# Negotiation parameters
MAX_ROUNDS = 5  # Maximum number of negotiation rounds before giving up

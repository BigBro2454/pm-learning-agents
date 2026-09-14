import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Check for required API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set. Please set it in your .env file.")

# Initialize the Gemini client
# The google-genai library uses the GEMINI_API_KEY environment variable by default if passed to genai.Client()
# or we can pass it explicitly.
client = genai.Client(api_key=GEMINI_API_KEY)

# Define the default model to use
DEFAULT_MODEL = "gemini-2.5-flash"

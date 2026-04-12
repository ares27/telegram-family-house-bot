# Loads .env and centralizes constants
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Convert comma-separated string to a list of integers
raw_ids = os.getenv("FAMILY_IDS", "")
FAMILY_IDS = [int(i.strip()) for i in raw_ids.split(",") if i.strip()]
FAMILY_GROUP_ID = int(os.getenv("FAMILY_GROUP_ID") or "0")

# Render External URL for keep-alive ping
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# Add other settings here
KNOWLEDGE_FILE = "knowledge.txt"

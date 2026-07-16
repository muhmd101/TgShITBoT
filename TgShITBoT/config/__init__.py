from dotenv import load_dotenv
from os import getenv
import time
load_dotenv()

API_ID = int(
    getenv("API_ID")
)

API_HASH = getenv("API_HASH")

SESSION_STRING = getenv("SESSION_STRING")

PREFIXES = [".", "!", "/"]

START_TIME = time.time()

REDIS_DB_URI = getenv(
    "REDIS_DB_URI",
    "redis://localhost:6379"
)
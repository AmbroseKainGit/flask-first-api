import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "http://localhost:6379")
QUEUES = ["email", "default"]

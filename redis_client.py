import os
import redis
import time

from dotenv import load_dotenv
load_dotenv()
redis_url = os.getenv('REDIS_URL')
redis_client = redis.Redis.from_url(redis_url)
import os

from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
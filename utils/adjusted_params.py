import os
from dotenv import load_dotenv

load_dotenv()

MIN_PRICE_IN_CENTS = int(os.getenv('MIN_PRICE_IN_CENTS', 100))
MIN_NUMBER_OF_ITEMS = int(os.getenv('NUMBER_OF_ITEMS', 10))
OUTPUT_FILE_NAME = os.getenv('OUTPUT_FILE_NAME', 'dataset')
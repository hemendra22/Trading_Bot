import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

def get_client():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    base_url = os.getenv("BASE_URL")

    client = Client(api_key, api_secret)

    # Set Binance Futures Testnet URL
    client.FUTURES_URL = base_url

    return client

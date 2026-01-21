import os
import requests
from datetime import date
from typing import Dict

from dotenv import load_dotenv

from src.application.exchange_rate_service import ExchangeRateService

load_dotenv()

class OpenExchangeAdapter(ExchangeRateService):
    BASE_URL = "https://openexchangerates.org/api"

    def __init__(self):
        self.app_id = os.getenv("OPEN_EXCHANGE_APP_ID")
        self.cache: Dict[str, float] = {}

    def get_rate(self, currency: str, date_obj: date) -> float:
        if currency == "USD":
            return 1.0

        cache_key = f"{date_obj.isoformat()}-{currency}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        date_str = date_obj.strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/historical/{date_str}.json?app_id={self.app_id}&symbols={currency}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"][currency]
            self.cache[cache_key] = rate
            return rate
        except requests.exceptions.RequestException as e:
            # In a real application, we would have more robust error handling
            print(f"Error fetching exchange rate: {e}")
            return 1.0 # Fallback to 1.0 in case of an error

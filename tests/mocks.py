from src.application.exchange_rate_service import ExchangeRateService
from datetime import date

class MockExchangeAdapter(ExchangeRateService):
    def get_rate(self, currency: str, date: date) -> float:
        if currency == "CLP":
            return 100.0
        return 1.0

from abc import ABC, abstractmethod
from datetime import date

class ExchangeRateService(ABC):
    @abstractmethod
    def get_rate(self, currency: str, date: date) -> float:
        pass

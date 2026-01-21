from pydantic import BaseModel, Field
from datetime import date
from typing import Dict

class Expense(BaseModel):
    id: str
    amount: float
    currency: str
    date: date
    category: str

class Employee(BaseModel):
    id: str
    name: str
    last_name: str
    cost_center: str

class Policy(BaseModel):
    base_currency: str = "USD"
    antiquity_limit_pending: int = 30
    antiquity_limit_rejected: int = 60
    limits_per_category: Dict[str, Dict[str, float]] = Field(
        default_factory=lambda: {
            "food": {
                "approved": 100.0,
                "pending": 150.0
            }
        }
    )
    prohibited_cost_centers_for_categories: Dict[str, str] = Field(
        default_factory=lambda: {
            "core_engineering": "food",
        }
    )


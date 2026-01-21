import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict

import pandas as pd

from src.application.exchange_rate_service import ExchangeRateService
from src.domain.models import Employee, Expense, Policy
from src.domain.rules_engine import evaluate_expense
from src.infrastructure.open_exchange_adapter import OpenExchangeAdapter


def analyze_expenses(
    file_path: str, exchange_rate_service: ExchangeRateService
) -> Dict[str, Any]:
    """
    Analyzes a CSV file of expenses, detects anomalies, and validates them against the rules engine.

    Args:
        file_path: The path to the CSV file.
        exchange_rate_service: The service to use for fetching exchange rates.

    Returns:
        A dictionary containing the analysis results.
    """
    try:
        df = pd.read_csv(file_path, skipinitialspace=True)
        # Clean string columns to avoid issues with duplicates due to leading/trailing spaces
        for col in df.select_dtypes(['object']).columns:
            df[col] = df[col].str.strip()
    except FileNotFoundError:
        return {"error": "File not found."}

    # Anomaly Detection
    duplicates = df[df.duplicated(subset=["monto", "moneda", "fecha"], keep=False)]
    negative_amounts = df[df["monto"] < 0]

    anomalies = {
        "duplicates": duplicates.to_dict("records"),
        "negative_amounts": negative_amounts.to_dict("records"),
    }

    results = []
    status_breakdown = {
        "APROBADO": 0,
        "PENDIENTE": 0,
        "RECHAZADO": 0,
    }

    exchange_rates = {}
    policy = Policy()
    analysis_date = datetime.now().date()

    # N+1 Optimization
    unique_date_currencies = (
        df[df["moneda"] != policy.base_currency][["fecha", "moneda"]]
        .drop_duplicates()
    )
    for _, row in unique_date_currencies.iterrows():
        date = datetime.strptime(row["fecha"], "%Y-%m-%d").date()
        currency = row["moneda"]
        # Corrected argument order
        rate = exchange_rate_service.get_rate(currency, date)
        exchange_rates[f"{date}-{currency}"] = rate

    for _, row in df.iterrows():
        expense = Expense(
            id=row["gasto_id"],
            amount=row["monto"],
            currency=row["moneda"],
            date=datetime.strptime(row["fecha"], "%Y-%m-%d").date(),
            category=row["categoria"],
        )
        employee = Employee(
            id=row["empleado_id"],
            name=row["empleado_nombre"],
            last_name=row["empleado_apellido"],
            cost_center=row["empleado_cost_center"],
        )

        rate = 1.0
        if expense.currency != policy.base_currency:
            rate = exchange_rates.get(f"{expense.date}-{expense.currency}", 1.0)

        # Check if the current row is among the duplicates
        is_duplicate = row.name in duplicates.index

        status, alerts = evaluate_expense(
            expense, employee, policy, analysis_date, rate, is_duplicate
        )

        results.append(
            {
                "gasto_id": expense.id,
                "status": status,
                "alertas": alerts,
            }
        )
        status_breakdown[status] += 1

    return {
        "summary": {
            "total_expenses": len(df),
            "status_breakdown": status_breakdown,
            "anomalies": anomalies,
        },
        "results": results,
    }


if __name__ == "__main__":

    class _MockExchangeAdapter(ExchangeRateService):
        """Local mock for CLI execution without an API key."""
        def get_rate(self, currency: str, date: datetime.date) -> float:
            if currency == "CLP":
                return 1000.0
            return 1.0

    parser = argparse.ArgumentParser(description="Analyze historical expense data.")
    parser.add_argument(
        "file_path", help="Path to the historical expense data CSV file."
    )
    args = parser.parse_args()

    service: ExchangeRateService
    if os.getenv("OPEN_EXCHANGE_APP_ID"):
        service = OpenExchangeAdapter()
    else:
        print("WARN: OPEN_EXCHANGE_APP_ID not set. Using mock exchange rate service.")
        service = _MockExchangeAdapter()

    analysis = analyze_expenses(args.file_path, service)
    print(json.dumps(analysis, indent=4, default=str))

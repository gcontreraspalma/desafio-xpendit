from datetime import date, timedelta
from typing import List, Tuple

from src.domain.models import Expense, Employee, Policy

STATUS_APPROVED = "APROBADO"
STATUS_PENDING = "PENDIENTE"
STATUS_REJECTED = "RECHAZADO"

def evaluate_expense(expense: Expense, employee: Employee, policy: Policy, current_date: date, exchange_rate: float = 1.0, is_duplicate: bool = False) -> Tuple[str, List[str]]:
    alerts = []
    statuses_from_rules = [] # Collect statuses from each rule evaluation

    # Rule: Negative Amounts (Priority anomaly)
    if expense.amount < 0:
        statuses_from_rules.append(STATUS_REJECTED)
        alerts.append({"code": "NEGATIVE_AMOUNT", "message": "El monto del gasto no puede ser negativo."})

    # Rule: Duplicates (Anomaly)
    if is_duplicate:
        statuses_from_rules.append(STATUS_PENDING)
        alerts.append({"code": "DUPLICATE_EXPENSE", "message": "Se ha detectado un posible gasto duplicado (mismo monto, moneda y fecha)."})

    # Rule 1: Antiquity
    days_diff = (current_date - expense.date).days
    if days_diff > policy.antiquity_limit_rejected:
        statuses_from_rules.append(STATUS_REJECTED)
        alerts.append({"code": "EXPENSE_TOO_OLD", "message": "Gasto presentado fuera de termino."})
    elif policy.antiquity_limit_pending < days_diff <= policy.antiquity_limit_rejected:
        statuses_from_rules.append(STATUS_PENDING)
        alerts.append({"code": "EXPENSE_LATE", "message": "Gasto presentado fuera de termino."})
    elif 0 <= days_diff <= policy.antiquity_limit_pending:
        statuses_from_rules.append(STATUS_APPROVED)
   
    # Rule 2: Food Limits
    if expense.category in policy.limits_per_category:
        limit = policy.limits_per_category[expense.category]
        amount_in_usd = expense.amount / exchange_rate if expense.currency != policy.base_currency else expense.amount
        
        if amount_in_usd > limit["pending"]:
            statuses_from_rules.append(STATUS_REJECTED)
            alerts.append({"code": "FOOD_LIMIT_EXCEEDED", "message": "Monto del gasto de comida excede el limite."})
        elif limit["approved"] < amount_in_usd <= limit["pending"]:
            statuses_from_rules.append(STATUS_PENDING)
            alerts.append({"code": "FOOD_LIMIT_NEAR_EXCEEDED", "message": "Monto del gasto de comida excede el limite."})
        elif amount_in_usd <= limit["approved"]:
            statuses_from_rules.append(STATUS_APPROVED)

    # Rule 3: Cost Center
    if employee.cost_center in policy.prohibited_cost_centers_for_categories and \
       policy.prohibited_cost_centers_for_categories[employee.cost_center] == expense.category:
        statuses_from_rules.append(STATUS_REJECTED)
        alerts.append({"code": "INVALID_COST_CENTER_EXPENSE", "message": "Gastos de comida no permitidos para este centro de costos."})

    # Final Status Resolution
    if STATUS_REJECTED in statuses_from_rules:
        final_status = STATUS_REJECTED
    elif STATUS_PENDING in statuses_from_rules:
        final_status = STATUS_PENDING
    elif STATUS_APPROVED in statuses_from_rules:
        final_status = STATUS_APPROVED
    else:
        # "Por defecto: Si no aplica ninguna regla, el estado es PENDIENTE (sin alertas)."
        final_status = STATUS_PENDING
        
    return final_status, alerts
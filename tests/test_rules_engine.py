from datetime import date, timedelta
import pytest

from src.domain.models import Expense, Employee, Policy
from src.domain.rules_engine import evaluate_expense, STATUS_APPROVED, STATUS_PENDING, STATUS_REJECTED

@pytest.fixture
def employee():
    return Employee(id="1", name="John", last_name="Doe", cost_center="engineering")

@pytest.fixture
def core_engineering_employee():
    return Employee(id="2", name="Jane", last_name="Doe", cost_center="core_engineering")

@pytest.fixture
def default_policy():
    return Policy()

# --- Antiquity Tests ---

def test_antiquity_edge_case_30_days(employee, default_policy):
    # Exactly 30 days should be APPROVED
    expense = Expense(id="1", amount=50, currency="USD", date=date.today() - timedelta(days=30), category="other")
    status, _ = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_APPROVED

def test_antiquity_edge_case_60_days(employee, default_policy):
    # Exactly 60 days should be PENDING
    expense = Expense(id="1", amount=50, currency="USD", date=date.today() - timedelta(days=60), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_PENDING
    assert any(a["code"] == "EXPENSE_LATE" for a in alerts)

# --- Food Limit Tests ---

def test_food_limit_edge_case_100_usd(employee, default_policy):
    # Exactly 100 USD should be APPROVED
    expense = Expense(id="1", amount=100, currency="USD", date=date.today(), category="food")
    status, _ = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_APPROVED

def test_food_limit_edge_case_150_usd(employee, default_policy):
    # Exactly 150 USD should be PENDING
    expense = Expense(id="1", amount=150, currency="USD", date=date.today(), category="food")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_PENDING
    assert any(a["code"] == "FOOD_LIMIT_NEAR_EXCEEDED" for a in alerts)

# --- Anomaly Rules (Negative & Duplicates) ---

def test_rule_anomaly_negative_amount(employee, default_policy):
    expense = Expense(id="1", amount=-10, currency="USD", date=date.today(), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_REJECTED
    assert any(a["code"] == "NEGATIVE_AMOUNT" for a in alerts)

def test_rule_anomaly_is_duplicate(employee, default_policy):
    expense = Expense(id="1", amount=50, currency="USD", date=date.today(), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today(), is_duplicate=True)
    assert status == STATUS_PENDING
    assert any(a["code"] == "DUPLICATE_EXPENSE" for a in alerts)

# --- Conflict Resolution & Overlaps ---

def test_resolution_hierarchy_rejected_wins_over_pending(employee, default_policy):
    # Case: A duplicate expense that is also > 60 days old
    expense = Expense(id="1", amount=50, currency="USD", date=date.today() - timedelta(days=61), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today(), is_duplicate=True)
    assert status == STATUS_REJECTED
    # Should have both alerts
    codes = [a["code"] for a in alerts]
    assert "DUPLICATE_EXPENSE" in codes
    assert "EXPENSE_TOO_OLD" in codes

def test_resolution_hierarchy_pending_wins_over_approved(employee, default_policy):
    # Case: Approved by novelty (10 days) but Pending by duplicate
    expense = Expense(id="1", amount=50, currency="USD", date=date.today() - timedelta(days=10), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today(), is_duplicate=True)
    assert status == STATUS_PENDING
    assert any(a["code"] == "DUPLICATE_EXPENSE" for a in alerts)

# --- Original Requirements Coverage ---

def test_cost_center_food_rejected_for_engineering(core_engineering_employee, default_policy):
    expense = Expense(id="1", amount=50, currency="USD", date=date.today(), category="food")
    status, alerts = evaluate_expense(expense, core_engineering_employee, default_policy, date.today())
    assert status == STATUS_REJECTED
    assert any(a["code"] == "INVALID_COST_CENTER_EXPENSE" for a in alerts)

def test_default_status_pending_for_future_dates(employee, default_policy):
    # Date in the future doesn't trigger antiquity rules
    expense = Expense(id="1", amount=50, currency="USD", date=date.today() + timedelta(days=5), category="other")
    status, alerts = evaluate_expense(expense, employee, default_policy, date.today())
    assert status == STATUS_PENDING
    assert not alerts

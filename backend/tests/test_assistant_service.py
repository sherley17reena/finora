from unittest.mock import patch

from app.assistant_service import handle_assistant_message
from app.models import Transaction


@patch("app.assistant_service.understand_message")
def test_assistant_routes_total_expenses(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "get_total_expenses",
        "amount": None,
        "purchase_amount": None,
        "category": None,
        "description": None,
        "date": None,
        "goal_name": None,
    }

    result = handle_assistant_message(
        db,
        "How much have I spent this month?"
    )

    assert result["status"] == "success"
    assert result["result"]["agent"] == "Expense Agent"
    assert (
        result["result"]["data"]["total_expenses"]
        == 30
    )


@patch("app.assistant_service.understand_message")
def test_assistant_adds_expense(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "add_expense",
        "amount": 25,
        "purchase_amount": None,
        "category": "Food",
        "description": "Dinner",
        "date": "2026-09-20",
        "goal_name": None,
    }

    result = handle_assistant_message(
        db,
        "I spent $25 on dinner."
    )

    assert result["status"] == "success"
    assert result["result"]["agent"] == "Expense Agent"

    expense = (
        db.query(Transaction)
        .filter(
            Transaction.description == "Dinner"
        )
        .first()
    )

    assert expense is not None
    assert expense.amount == 25
    assert expense.category == "Food"


@patch("app.assistant_service.understand_message")
def test_assistant_routes_savings_goal(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "get_savings_progress",
        "amount": None,
        "purchase_amount": None,
        "category": None,
        "description": None,
        "date": None,
        "goal_name": "Vacation",
    }

    result = handle_assistant_message(
        db,
        "How is my Vacation goal going?"
    )

    assert result["status"] == "success"
    assert result["result"]["agent"] == "Savings Agent"

    data = result["result"]["data"]

    assert data["name"] == "Vacation"
    assert data["progress_percentage"] == 20


@patch("app.assistant_service.understand_message")
def test_assistant_routes_budget(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "get_budget_status",
        "amount": None,
        "purchase_amount": None,
        "category": "Food",
        "description": None,
        "date": None,
        "goal_name": None,
    }

    result = handle_assistant_message(
        db,
        "How am I doing on my Food budget?"
    )

    assert result["status"] == "success"
    assert result["result"]["agent"] == "Budget Agent"

    data = result["result"]["data"]

    assert data["budget_amount"] == 500
    assert data["spent_amount"] == 20
    assert data["remaining_amount"] == 480


@patch("app.assistant_service.understand_message")
def test_assistant_multi_agent_purchase(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "analyze_purchase",
        "amount": None,
        "purchase_amount": 500,
        "category": None,
        "description": None,
        "date": None,
        "goal_name": "Vacation",
    }

    result = handle_assistant_message(
        db,
        (
            "Can I afford a $500 phone and still "
            "reach my Vacation goal?"
        )
    )

    assert result["status"] == "success"

    workflow = result["result"]

    assert (
        workflow["workflow"]
        == "purchase_with_savings_analysis"
    )

    assert workflow["agents_used"] == [
        "Budget Agent",
        "Savings Agent",
    ]

    assert (
        workflow["purchase_analysis"]["purchase_amount"]
        == 500
    )

    assert (
        workflow["savings_analysis"]["name"]
        == "Vacation"
    )


@patch("app.assistant_service.understand_message")
def test_assistant_handles_unknown_request(
    mock_understand_message,
    db
):
    mock_understand_message.return_value = {
        "action": "unknown",
        "amount": None,
        "purchase_amount": None,
        "category": None,
        "description": None,
        "date": None,
        "goal_name": None,
    }

    result = handle_assistant_message(
        db,
        "Tell me something unrelated."
    )

    assert result["status"] == "error"
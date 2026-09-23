from app.coordinator import FinanceCoordinator
from app.models import AgentLog


def test_expense_agent_total(db):
    coordinator = FinanceCoordinator(db)

    result = coordinator.auto_route(
        "get_total_expenses"
    )

    assert result["status"] == "success"
    assert result["agent"] == "Expense Agent"

    assert (
        result["data"]["total_expenses"]
        == 30
    )


def test_savings_agent_progress(db):
    coordinator = FinanceCoordinator(db)

    result = coordinator.auto_route(
        "get_savings_progress",
        goal_id=1
    )

    assert result["status"] == "success"
    assert result["agent"] == "Savings Agent"

    data = result["data"]

    assert data["name"] == "Vacation"
    assert data["target_amount"] == 3000
    assert data["current_amount"] == 600
    assert data["remaining_amount"] == 2400
    assert data["progress_percentage"] == 20


def test_food_budget_status(db):
    coordinator = FinanceCoordinator(db)

    result = coordinator.auto_route(
        "get_budget_status",
        budget_id=1
    )

    assert result["status"] == "success"
    assert result["agent"] == "Budget Agent"

    data = result["data"]

    assert data["budget_amount"] == 500
    assert data["spent_amount"] == 20
    assert data["remaining_amount"] == 480
    assert data["percentage_used"] == 4


def test_agent_action_is_logged(db):
    coordinator = FinanceCoordinator(db)

    coordinator.auto_route(
        "get_total_expenses"
    )

    log = (
        db.query(AgentLog)
        .order_by(AgentLog.id.desc())
        .first()
    )

    assert log is not None
    assert log.agent == "Expense Agent"
    assert log.action == "get_total_expenses"
    assert log.tool == "get_total_expenses"
    assert log.arguments == "{}"
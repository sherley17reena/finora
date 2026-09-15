from sqlalchemy.orm import Session

from app.agents.expense_agent import ExpenseAgent
from app.agents.savings_agent import SavingsAgent
from app.agents.budget_agent import BudgetAgent
from app.tools import log_agent_action


class FinanceCoordinator:

    def __init__(self, db: Session):
        self.db = db
        self.expense_agent = ExpenseAgent(db)
        self.savings_agent = SavingsAgent(db)
        self.budget_agent = BudgetAgent(db)

    # -------------------------------------------------
    # Manual routing
    # -------------------------------------------------
    def route(self, agent_name: str, action: str, **kwargs):

        if agent_name == "expense":
            return self.expense_agent.handle(action, **kwargs)

        if agent_name == "savings":
            return self.savings_agent.handle(action, **kwargs)

        if agent_name == "budget":
            return self.budget_agent.handle(action, **kwargs)

        return {
            "status": "error",
            "message": "Unknown agent"
        }

    # -------------------------------------------------
    # Automatic routing
    # -------------------------------------------------
    def auto_route(self, action: str, **kwargs):

        expense_actions = {
            "get_expenses",
            "get_total_expenses",
            "add_expense"
        }

        savings_actions = {
            "get_savings_goals",
            "get_savings_progress",
            "calculate_monthly_savings_needed"
        }

        budget_actions = {
            "get_budgets",
            "get_budget_status",
            "simulate_purchase"
        }

        if action in expense_actions:
            return self.expense_agent.handle(action, **kwargs)

        if action in savings_actions:
            return self.savings_agent.handle(action, **kwargs)

        if action in budget_actions:
            return self.budget_agent.handle(action, **kwargs)

        return {
            "status": "error",
            "message": "No agent found for this action"
        }

    # -------------------------------------------------
    # Multi-agent purchase analysis
    # -------------------------------------------------
    def analyze_purchase_with_savings(
        self,
        purchase_amount: float,
        goal_id: int
    ):

        # Step 1: Ask Budget Agent about affordability
        budget_result = self.budget_agent.handle(
            "simulate_purchase",
            purchase_amount=purchase_amount
        )

        # Log Budget Agent activity
        log_agent_action(
            db=self.db,
            agent="Budget Agent",
            action="simulate_purchase",
            tool="simulate_purchase",
            arguments=f"purchase_amount={purchase_amount}",
            result=str(budget_result)
        )

        # Step 2: Ask Savings Agent about savings goal
        savings_result = self.savings_agent.handle(
            "get_savings_progress",
            goal_id=goal_id
        )

        # Log Savings Agent activity
        log_agent_action(
            db=self.db,
            agent="Savings Agent",
            action="get_savings_progress",
            tool="get_savings_progress",
            arguments=f"goal_id={goal_id}",
            result=str(savings_result)
        )

        # Step 3: Check for errors
        if budget_result["status"] != "success":
            return budget_result

        if savings_result["status"] != "success":
            return savings_result

        budget_data = budget_result["data"]
        savings_data = savings_result["data"]

        # Step 4: Use BOTH agents to make a decision
        can_afford = budget_data["can_afford"]
        money_after_purchase = budget_data["money_after_purchase"]

        savings_remaining = savings_data["remaining_amount"]

        if not can_afford:
            decision = (
                "This purchase is not affordable based on "
                "your current available income."
            )

        elif money_after_purchase >= savings_remaining:
            decision = (
                "You can afford this purchase and still have "
                "enough available income to cover your remaining "
                "savings goal."
            )

        else:
            decision = (
                "You can afford this purchase, but it may slow "
                "your progress toward your savings goal."
            )

        # Step 5: Combine results from both agents
        return {
            "workflow": "purchase_with_savings_analysis",
            "status": "success",
            "agents_used": [
                "Budget Agent",
                "Savings Agent"
            ],
            "purchase_analysis": budget_data,
            "savings_analysis": savings_data,
            "decision": decision
        }
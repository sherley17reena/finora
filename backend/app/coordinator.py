import json

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
    # Execute an agent action and log it
    # -------------------------------------------------
    def _execute_and_log(
        self,
        agent,
        agent_name: str,
        action: str,
        **kwargs
    ):
        result = agent.handle(action, **kwargs)

        log_agent_action(
            db=self.db,
            agent=agent_name,
            action=action,
            tool=action,
            arguments=json.dumps(
                kwargs,
                default=str
            ),
            result=json.dumps(
                result,
                default=str
            )
        )

        return result

    # -------------------------------------------------
    # Manual routing
    # -------------------------------------------------
    def route(
        self,
        agent_name: str,
        action: str,
        **kwargs
    ):

        if agent_name == "expense":
            return self._execute_and_log(
                self.expense_agent,
                "Expense Agent",
                action,
                **kwargs
            )

        if agent_name == "savings":
            return self._execute_and_log(
                self.savings_agent,
                "Savings Agent",
                action,
                **kwargs
            )

        if agent_name == "budget":
            return self._execute_and_log(
                self.budget_agent,
                "Budget Agent",
                action,
                **kwargs
            )

        return {
            "status": "error",
            "message": "Unknown agent"
        }

    # -------------------------------------------------
    # Automatic routing
    # -------------------------------------------------
    def auto_route(
        self,
        action: str,
        **kwargs
    ):

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
            return self._execute_and_log(
                self.expense_agent,
                "Expense Agent",
                action,
                **kwargs
            )

        if action in savings_actions:
            return self._execute_and_log(
                self.savings_agent,
                "Savings Agent",
                action,
                **kwargs
            )

        if action in budget_actions:
            return self._execute_and_log(
                self.budget_agent,
                "Budget Agent",
                action,
                **kwargs
            )

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

        # Step 1: Budget Agent checks affordability
        budget_result = self.auto_route(
            "simulate_purchase",
            purchase_amount=purchase_amount
        )

        if budget_result["status"] != "success":
            return budget_result

        # Step 2: Savings Agent checks goal progress
        savings_result = self.auto_route(
            "get_savings_progress",
            goal_id=goal_id
        )

        if savings_result["status"] != "success":
            return savings_result

        budget_data = budget_result["data"]
        savings_data = savings_result["data"]

        # Step 3: Combine both agent results
        can_afford = budget_data["can_afford"]

        money_after_purchase = (
            budget_data["money_after_purchase"]
        )

        savings_remaining = (
            savings_data["remaining_amount"]
        )

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

        # Step 4: Return combined multi-agent result
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
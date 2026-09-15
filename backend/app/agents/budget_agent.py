from sqlalchemy.orm import Session

from app.tools import (
    get_budgets,
    get_budget_status,
    simulate_purchase
)


class BudgetAgent:

    def __init__(self, db: Session):
        self.db = db
        self.name = "Budget Agent"

    def handle(self, action: str, **kwargs):

        # Action 1: Get all budgets
        if action == "get_budgets":

            budgets = get_budgets(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": budgets
            }

        # Action 2: Check one budget
        if action == "get_budget_status":

            status = get_budget_status(
                self.db,
                budget_id=kwargs["budget_id"]
            )

            if status is None:
                return {
                    "agent": self.name,
                    "action": action,
                    "status": "error",
                    "message": "Budget not found"
                }

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": status
            }

        # Action 3: Simulate a purchase
        if action == "simulate_purchase":

            simulation = simulate_purchase(
                self.db,
                purchase_amount=kwargs["purchase_amount"]
            )

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": simulation
            }

        # Unknown action
        return {
            "agent": self.name,
            "action": action,
            "status": "error",
            "message": "Unknown action"
        }
from sqlalchemy.orm import Session

from app.tools import (
    get_savings_goals,
    get_savings_progress,
    calculate_monthly_savings_needed
)


class SavingsAgent:

    def __init__(self, db: Session):
        self.db = db
        self.name = "Savings Agent"

    def handle(self, action: str, **kwargs):

        # Action 1: Get all savings goals
        if action == "get_savings_goals":

            goals = get_savings_goals(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": goals
            }

        # Action 2: Calculate progress for one goal
        if action == "get_savings_progress":

            progress = get_savings_progress(
                self.db,
                goal_id=kwargs["goal_id"]
            )

            if progress is None:
                return {
                    "agent": self.name,
                    "action": action,
                    "status": "error",
                    "message": "Savings goal not found"
                }

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": progress
            }

        # Action 3: Calculate monthly savings needed
        if action == "calculate_monthly_savings_needed":

            calculation = calculate_monthly_savings_needed(
                self.db,
                goal_id=kwargs["goal_id"]
            )

            if calculation is None:
                return {
                    "agent": self.name,
                    "action": action,
                    "status": "error",
                    "message": "Savings goal not found"
                }

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": calculation
            }

        # Unknown action
        return {
            "agent": self.name,
            "action": action,
            "status": "error",
            "message": "Unknown action"
        }

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models import Budget
from app.tools import (
    get_budgets,
    get_budget_status,
    simulate_purchase,
)


class BudgetAgent:
    def __init__(self, db: Session):
        self.db = db
        self.name = "Budget Agent"

    def handle(self, action: str, **kwargs):

        # Existing feature: list budgets
        if action == "get_budgets":
            budgets = get_budgets(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": budgets,
            }

        # Existing feature: check budget status
        if action == "get_budget_status":
            status = get_budget_status(
                self.db,
                budget_id=kwargs["budget_id"],
            )

            if status is None:
                return {
                    "agent": self.name,
                    "action": action,
                    "status": "error",
                    "message": "Budget not found",
                }

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": status,
            }

        # Existing feature: simulate purchase
        if action == "simulate_purchase":
            simulation = simulate_purchase(
                self.db,
                purchase_amount=kwargs["purchase_amount"],
            )

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": simulation,
            }

        # New feature: preview a budget change
        if action in (
            "increase_budget",
            "decrease_budget",
            "set_budget",
        ):
            return self.preview_budget_change(
                action=action,
                category=kwargs.get("category"),
                amount=kwargs.get("amount"),
                budget_amount=kwargs.get("budget_amount"),
                month=kwargs.get("month"),
            )

        return {
            "agent": self.name,
            "action": action,
            "status": "error",
            "message": "Unknown action",
        }

    def preview_budget_change(
        self,
        action,
        category,
        amount=None,
        budget_amount=None,
        month=None,
    ):
        # Default to the current month
        current_month = date.today().strftime("%Y-%m")

        if month is None:
            month = current_month

        # Only current-month updates are supported for now
        if month != current_month:
            return {
                "agent": self.name,
                "action": action,
                "status": "error",
                "message": (
                    "Finora currently supports budget changes "
                    "for the current month only."
                ),
            }

        if not category or not category.strip():
            return {
                "agent": self.name,
                "action": action,
                "status": "error",
                "message": "Please specify a budget category.",
            }

        # Find the budget for the correct month
        budget = (
            self.db.query(Budget)
            .filter(
                Budget.month == month,
                Budget.category.ilike(category.strip()),
            )
            .first()
        )

        if budget is None:
            return {
                "agent": self.name,
                "action": action,
                "status": "error",
                "message": (
                    f"No {category} budget exists for {month}. "
                    "Please create one before updating it."
                ),
            }

        # Convert money to decimal values for calculations
        def money(value):
            return Decimal(str(value)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

        old_amount = money(budget.budget_amount)

        try:
            if action in ("increase_budget", "decrease_budget"):
                if amount is None or money(amount) <= 0:
                    raise ValueError(
                        "The adjustment amount must be greater than zero."
                    )

                adjustment = money(amount)

                if action == "increase_budget":
                    new_amount = old_amount + adjustment
                else:
                    new_amount = old_amount - adjustment

            elif action == "set_budget":
                if budget_amount is None:
                    raise ValueError(
                        "Please provide the new budget amount."
                    )

                new_amount = money(budget_amount)

            else:
                raise ValueError("Unsupported budget action.")

            if not new_amount.is_finite():
                raise ValueError("Please provide a valid amount.")

            if new_amount < 0:
                raise ValueError(
                    "A budget cannot be reduced below zero."
                )

        except (ValueError, TypeError, ArithmeticError) as error:
            return {
                "agent": self.name,
                "action": action,
                "status": "error",
                "message": str(error),
            }

        # Important: this is a preview only.
        # No database changes are made here.
        return {
            "agent": self.name,
            "action": action,
            "status": "confirmation_required",
            "message": (
                f"Change your {budget.category} budget "
                f"from ${old_amount:,.2f} "
                f"to ${new_amount:,.2f} for {month}?"
            ),
            "data": {
                "budget_id": budget.id,
                "category": budget.category,
                "month": month,
                "old_amount": float(old_amount),
                "new_amount": float(new_amount),
            },
        }

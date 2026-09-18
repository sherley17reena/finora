from sqlalchemy.orm import Session

from app.tools import (
    add_expense,
    get_expenses,
    get_total_expenses,
)


class ExpenseAgent:

    def __init__(self, db: Session):
        self.db = db
        self.name = "Expense Agent"

    def handle(self, action: str, **kwargs):

        if action == "get_expenses":
            expenses = get_expenses(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": expenses,
            }

        if action == "get_total_expenses":
            total = get_total_expenses(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": {
                    "total_expenses": total
                },
            }

        if action == "add_expense":
            expense = add_expense(
                db=self.db,
                date=kwargs["date"],
                description=kwargs["description"],
                amount=kwargs["amount"],
                category=kwargs["category"],
            )

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": {
                    "id": expense.id,
                    "date": expense.date,
                    "description": expense.description,
                    "amount": expense.amount,
                    "category": expense.category,
                },
            }

        return {
            "agent": self.name,
            "action": action,
            "status": "error",
            "message": "Unknown action",
        }
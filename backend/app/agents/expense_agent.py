from sqlalchemy.orm import Session

from app.tools import add_expense, get_expenses, get_total_expenses


class ExpenseAgent:

    def __init__(self, db: Session):
        self.db = db
        self.name = "Expense Agent"

    def handle(self, action: str, **kwargs):

        # Action 1: Get all expenses
        if action == "get_expenses":

            expenses = get_expenses(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": expenses
            }

        # Action 2: Calculate total expenses
        if action == "get_total_expenses":

            total = get_total_expenses(self.db)

            return {
                "agent": self.name,
                "action": action,
                "status": "success",
                "data": {
                    "total_expenses": total
                }
            }

        # Action 3: Add a new expense
        # if action == "add_expense":

        #     expense = add_expense(
        #         db=self.db,
        #         date=kwargs["date"],
        #         description=kwargs["description"],
        #         amount=kwargs["amount"],
        #         category=kwargs["category"]
        #     )

        #     return {
        #         "agent": self.name,
        #         "action": action,
        #         "status": "success",
        #         "data": {
        #             "id": expense.id,
        #             "date": expense.date,
        #             "description": expense.description,
        #             "amount": expense.amount,
        #             "category": expense.category
        #         }
        #     }

        # Unknown action
        return {
            "agent": self.name,
            "action": action,
            "status": "error",
            "message": "Unknown action"
        }
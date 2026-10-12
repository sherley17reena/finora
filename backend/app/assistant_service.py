
from sqlalchemy.orm import Session

from app.coordinator import FinanceCoordinator
from app.llm.orchestrator import understand_message
from app.models import SavingsGoal, Budget

from datetime import date

def friendly_response(result, success_message):
    """Convert an agent result into a chat-friendly response."""

    if result.get("status") != "success":
        return {
            "status": "error",
            "message": result.get(
                "message",
                "I couldn't complete that request."
            ),
            "result": result,
        }

    return {
        "status": "success",
        "message": success_message,
        "result": result,
    }


def handle_assistant_message(db: Session, message: str):
    if not message or not message.strip():
        return {
            "status": "error",
            "message": "Please enter a message.",
        }

    try:
        intent = understand_message(message)

        if not isinstance(intent, dict):
            return {
                "status": "error",
                "message": "I couldn't understand that request. Could you rephrase it?",
            }

        action = intent.get("action")
        coordinator = FinanceCoordinator(db)

        # 1. Add an expense
        if action == "add_expense":
            required_fields = [
                "amount", "category", "description", "date"
            ]

            missing_fields = [
                field for field in required_fields
                if intent.get(field) is None
            ]

            if missing_fields:
                return {
                    "status": "error",
                    "message": (
                        "I need a little more information to add "
                        "that expense: " + ", ".join(missing_fields) + "."
                    ),
                    "missing_fields": missing_fields,
                    "intent": intent,
                }

            amount = float(intent["amount"])
            category = str(intent["category"])

            if amount <= 0:
                raise ValueError("The expense amount must be greater than zero.")

            result = coordinator.auto_route(
                "add_expense",
                amount=amount,
                category=category,
                description=intent["description"],
                date=intent["date"],
            )

            response = friendly_response(
                result,
                f"I've added your {amount:,.2f} expense "
                f"for {intent['description']} under {category}."
            )
            response["intent"] = intent
            return response

        # 2. Total expenses
        if action == "get_total_expenses":
            result = coordinator.auto_route("get_total_expenses")

            if result.get("status") != "success":
                return friendly_response(
                    result,
                    "I couldn't retrieve your expenses."
                )

            total = result["data"]["total_expenses"]
            month_name = date.today().strftime("%B %Y")

            response = friendly_response(
                result,
                f"You've spent ${total:,.2f} so far in {month_name}."
            )

            response["intent"] = intent
            return response
        # 3. Savings goal progress
        if action == "get_savings_progress":
            goal_name = intent.get("goal_name")

            if not goal_name:
                return {
                    "status": "error",
                    "message": "Which savings goal would you like to check?",
                    "intent": intent,
                }

            goal = (
                db.query(SavingsGoal)
                .filter(SavingsGoal.name.ilike(goal_name))
                .first()
            )

            if goal is None:
                return {
                    "status": "error",
                    "message": f"I couldn't find a savings goal named '{goal_name}'.",
                    "intent": intent,
                }

            result = coordinator.auto_route(
                "get_savings_progress",
                goal_id=goal.id,
            )

            response = friendly_response(
                result,
                f"Here's your progress toward {goal.name}."
            )
            response["intent"] = intent
            return response

        # 4. Budget status
        if action == "get_budget_status":
            category = intent.get("category")

            if not category:
                return {
                    "status": "error",
                    "message": "Which budget category would you like to check?",
                    "intent": intent,
                }

            current_month = date.today().strftime("%Y-%m")

            budget = (
                db.query(Budget)
                .filter(
                    Budget.category.ilike(category),
                    Budget.month == current_month
                )
                .first()
            )

            if budget is None:
                return {
                    "status": "error",
                            "message": (
                                f"You don't have a {category} budget "
                                f"for {current_month} yet. "
                                "You can create one from the Budgets page."
                            ),
                    "intent": intent,
                }

            result = coordinator.auto_route(
                "get_budget_status",
                budget_id=budget.id,
            )

            response = friendly_response(
                result,
                f"Here's the status of your {category} budget."
            )
            response["intent"] = intent
            return response

        # 5. Purchase analysis
        if action == "analyze_purchase":
            purchase_amount = intent.get("purchase_amount")
            goal_name = intent.get("goal_name")

            if purchase_amount is None:
                return {
                    "status": "error",
                    "message": "How much does the purchase cost?",
                    "intent": intent,
                }

            purchase_amount = float(purchase_amount)

            if purchase_amount <= 0:
                raise ValueError("The purchase amount must be greater than zero.")

            if not goal_name:
                result = coordinator.auto_route(
                    "simulate_purchase",
                    purchase_amount=purchase_amount,
                )

                response = friendly_response(
                    result,
                    f"Here's your affordability analysis "
                    f"for a {purchase_amount:,.2f} purchase."
                )
                response["intent"] = intent
                return response

            goal = (
                db.query(SavingsGoal)
                .filter(SavingsGoal.name.ilike(goal_name))
                .first()
            )

            if goal is None:
                return {
                    "status": "error",
                    "message": f"I couldn't find a savings goal named '{goal_name}'.",
                    "intent": intent,
                }

            result = coordinator.analyze_purchase_with_savings(
                purchase_amount=purchase_amount,
                goal_id=goal.id,
            )

            response = friendly_response(
                result,
                result.get(
                    "decision",
                    "Here's your purchase and savings analysis."
                ),
            )
            response["intent"] = intent
            return response

        return {
            "status": "error",
            "message": (
                "I can't handle that request yet. "
                "Try asking about expenses, budgets, "
                "savings goals, or a planned purchase."
            ),
            "intent": intent,
        }

    except (ValueError, TypeError) as error:
        return {
            "status": "error",
            "message": str(error),
        }

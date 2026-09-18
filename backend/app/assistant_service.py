from sqlalchemy.orm import Session

from app.coordinator import FinanceCoordinator
from app.llm.orchestrator import understand_message


def handle_assistant_message(db: Session, message: str):
    intent = understand_message(message)

    action = intent.get("action")

    if action == "add_expense":
        required_fields = [
            "amount",
            "category",
            "description",
            "date",
        ]

        missing_fields = [
            field
            for field in required_fields
            if intent.get(field) is None
        ]

        if missing_fields:
            return {
                "status": "error",
                "message": (
                    "I need more information before "
                    "I can add this expense."
                ),
                "missing_fields": missing_fields,
            }

        coordinator = FinanceCoordinator(db)

        result = coordinator.auto_route(
            "add_expense",
            amount=float(intent["amount"]),
            category=intent["category"],
            description=intent["description"],
            date=intent["date"],
        )

        return {
            "status": result["status"],
            "intent": intent,
            "result": result,
        }
    if action == "get_total_expenses":
        coordinator = FinanceCoordinator(db)

        result = coordinator.auto_route(
            "get_total_expenses"
        )

        return {
            "status": result["status"],
            "intent": intent,
            "result": result,
        }

    if action == "get_savings_progress":
        goal_name = intent.get("goal_name")

        if not goal_name:
            return {
                "status": "error",
                "message": "Please tell me which savings goal you mean.",
                "intent": intent,
            }

        from app.models import SavingsGoal

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

        coordinator = FinanceCoordinator(db)

        result = coordinator.auto_route(
            "get_savings_progress",
            goal_id=goal.id
        )

        return {
            "status": result["status"],
            "intent": intent,
            "result": result,
        }

    if action == "get_budget_status":
        category = intent.get("category")

        if not category:
            return {
                "status": "error",
                "message": "Please tell me which budget category you mean.",
                "intent": intent,
            }

        from app.models import Budget

        budget = (
            db.query(Budget)
            .filter(Budget.category.ilike(category))
            .order_by(Budget.id.desc())
            .first()
        )

        if budget is None:
            return {
                "status": "error",
                "message": f"I couldn't find a {category} budget.",
                "intent": intent,
            }

        coordinator = FinanceCoordinator(db)

        result = coordinator.auto_route(
            "get_budget_status",
            budget_id=budget.id
        )

        return {
            "status": result["status"],
            "intent": intent,
            "result": result,
        }
    if action == "analyze_purchase":
        purchase_amount = intent.get("purchase_amount")
        goal_name = intent.get("goal_name")

        if purchase_amount is None:
            return {
                "status": "error",
                "message": "Please tell me the purchase amount.",
                "intent": intent,
            }

        coordinator = FinanceCoordinator(db)

        # Purchase analysis without a savings goal
        if not goal_name:
            result = coordinator.auto_route(
                "simulate_purchase",
                purchase_amount=float(purchase_amount)
            )

            return {
                "status": result["status"],
                "intent": intent,
                "result": result,
            }

        # Purchase analysis with a savings goal
        from app.models import SavingsGoal

        goal = (
            db.query(SavingsGoal)
            .filter(SavingsGoal.name.ilike(goal_name))
            .first()
        )

        if goal is None:
            return {
                "status": "error",
                "message": (
                    f"I couldn't find a savings goal "
                    f"named '{goal_name}'."
                ),
                "intent": intent,
            }

        result = coordinator.analyze_purchase_with_savings(
            purchase_amount=float(purchase_amount),
            goal_id=goal.id
        )

        return {
            "status": result["status"],
            "intent": intent,
            "result": result,
        }
    
    return {
        "status": "error",
        "message": "This request is not supported yet.",
        "intent": intent,
    }
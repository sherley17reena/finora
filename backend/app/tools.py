from sqlalchemy.orm import Session

from .models import Transaction, FinancialProfile, SavingsGoal, Budget
from datetime import date, datetime

def add_expense(
    db: Session,
    date: str,
    description: str,
    amount: float,
    category: str
):
    expense = Transaction(
        date=date,
        description=description,
        amount=amount,
        category=category,
        type="expense"
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(db: Session):
    expenses = (
        db.query(Transaction)
        .filter(Transaction.type == "expense")
        .all()
    )

    return expenses


def get_income(db: Session):
    profile = db.query(FinancialProfile).first()

    if profile is None:
        return 0

    return profile.monthly_income

def calculate_remaining_income(db: Session):
    profile = db.query(FinancialProfile).first()

    if profile is None:
        return 0

    total_expenses = (
        profile.rent
        + profile.tuition
        + profile.groceries
        + profile.transport
        + profile.utilities
        + profile.lifestyle_costs
    )

    remaining_income = profile.monthly_income - total_expenses

    return remaining_income

def simulate_purchase(db: Session, purchase_amount: float):
    remaining_income = calculate_remaining_income(db)

    money_after_purchase = remaining_income - purchase_amount

    can_afford = money_after_purchase >= 0

    return {
        "purchase_amount": purchase_amount,
        "remaining_income": remaining_income,
        "money_after_purchase": money_after_purchase,
        "can_afford": can_afford
    }
def get_total_expenses(db: Session):
    expenses = get_expenses(db)

    total = sum(expense.amount for expense in expenses)

    return total

def get_savings_goals(db: Session):
    return db.query(SavingsGoal).all()


def get_savings_progress(db: Session, goal_id: int):
    goal = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.id == goal_id)
        .first()
    )

    if goal is None:
        return None

    if goal.target_amount <= 0:
        progress_percentage = 0
    else:
        progress_percentage = (
            goal.current_amount / goal.target_amount
        ) * 100

    remaining_amount = goal.target_amount - goal.current_amount

    return {
        "goal_id": goal.id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "remaining_amount": remaining_amount,
        "progress_percentage": round(progress_percentage, 2),
        "target_date": goal.target_date
    }

def calculate_monthly_savings_needed(db: Session, goal_id: int):
    goal = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.id == goal_id)
        .first()
    )

    if goal is None:
        return None

    target_date = datetime.strptime(
        goal.target_date,
        "%Y-%m-%d"
    ).date()

    today = date.today()

    months_remaining = (
        (target_date.year - today.year) * 12
        + (target_date.month - today.month)
    )

    remaining_amount = goal.target_amount - goal.current_amount

    if remaining_amount <= 0:
        monthly_savings_needed = 0

    elif months_remaining <= 0:
        monthly_savings_needed = remaining_amount

    else:
        monthly_savings_needed = remaining_amount / months_remaining

    return {
        "goal_id": goal.id,
        "name": goal.name,
        "remaining_amount": remaining_amount,
        "months_remaining": months_remaining,
        "monthly_savings_needed": round(monthly_savings_needed, 2)
    }

def get_budgets(db: Session):
    return db.query(Budget).all()


def get_budget_status(db: Session, budget_id: int):
    budget = (
        db.query(Budget)
        .filter(Budget.id == budget_id)
        .first()
    )

    if budget is None:
        return None

    remaining_amount = budget.budget_amount - budget.spent_amount

    if budget.budget_amount <= 0:
        percentage_used = 0
    else:
        percentage_used = (
            budget.spent_amount / budget.budget_amount
        ) * 100

    return {
        "budget_id": budget.id,
        "month": budget.month,
        "category": budget.category,
        "budget_amount": budget.budget_amount,
        "spent_amount": budget.spent_amount,
        "remaining_amount": remaining_amount,
        "percentage_used": round(percentage_used, 2)
    }
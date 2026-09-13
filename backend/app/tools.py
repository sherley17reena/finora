from sqlalchemy.orm import Session

from .models import Transaction, FinancialProfile


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
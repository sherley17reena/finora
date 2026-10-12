
from datetime import date, datetime
from math import ceil

from sqlalchemy.orm import Session

from .models import (
    Transaction,
    FinancialProfile,
    SavingsGoal,
    Budget,
    AgentLog,
)


# ==========================================
# 1. EXPENSE MANAGEMENT
# ==========================================

def add_expense(
    db: Session,
    date: str,
    description: str,
    amount: float,
    category: str,
):

    raise ValueError(
    "Rent, Tuition, and Utilities are already "
    "deducted automatically from the financial profile."
    )

    """Create a new expense transaction."""

    expense = Transaction(
        date=date,
        description=description,
        amount=amount,
        category=category.strip(),
        type="expense",
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(db: Session):
    """Return all expense transactions."""

    return (
        db.query(Transaction)
        .filter(Transaction.type == "expense")
        .all()
    )


def get_current_month_expenses(db: Session):
    """Return expenses recorded in the current month."""

    current_month = date.today().strftime("%Y-%m")

    expenses = get_expenses(db)

    return [
        expense
        for expense in expenses
        if expense.date
        and str(expense.date).startswith(current_month)
    ]


def get_current_month_expense_total(db: Session):
    """Calculate total expenses for the current month."""

    expenses = get_current_month_expenses(db)

    total = sum(
        expense.amount
        for expense in expenses
    )

    return round(total, 2)


def get_total_expenses(db: Session):
    """
    Return current-month expenses.

    Preserves the existing behavior expected
    by Finora's agents and dashboard.
    """

    return get_current_month_expense_total(db)


# ==========================================
# 2. FINANCIAL PROFILE AND INCOME
# ==========================================

def get_income(db: Session):
    """Retrieve monthly income from the profile."""

    profile = db.query(FinancialProfile).first()

    if profile is None:
        return 0

    return profile.monthly_income


def calculate_remaining_income(db: Session):
    """
    Calculate available monthly income.

    Assumption:
    Rent, tuition, and utilities are fixed
    commitments that are not also recorded
    as expense transactions.

    Groceries, transport, and lifestyle costs
    are tracked through actual transactions.
    """

    profile = db.query(FinancialProfile).first()

    if profile is None:
        return 0

    fixed_commitments = (
        profile.rent
        + profile.tuition
        + profile.utilities
    )

    current_month_spending = (
        get_current_month_expense_total(db)
    )

    remaining_income = (
        profile.monthly_income
        - fixed_commitments
        - current_month_spending
    )

    return round(remaining_income, 2)


def simulate_purchase(
    db: Session,
    purchase_amount: float,
):
    """Estimate affordability of a purchase."""

    remaining_income = calculate_remaining_income(db)

    money_after_purchase = (
        remaining_income - purchase_amount
    )

    can_afford = money_after_purchase >= 0

    return {
        "purchase_amount": purchase_amount,
        "remaining_income": remaining_income,
        "money_after_purchase": round(
            money_after_purchase, 2
        ),
        "can_afford": can_afford,
    }


# ==========================================
# 3. SAVINGS GOAL MANAGEMENT
# ==========================================

def get_savings_goals(db: Session):
    """Return all savings goals."""

    return db.query(SavingsGoal).all()


def get_savings_progress(
    db: Session,
    goal_id: int,
):
    """Calculate progress toward a savings goal."""

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

    remaining_amount = max(
        0,
        goal.target_amount - goal.current_amount,
    )

    return {
        "goal_id": goal.id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "remaining_amount": round(
            remaining_amount, 2
        ),
        "progress_percentage": round(
            progress_percentage, 2
        ),
        "target_date": goal.target_date,
    }


def calculate_monthly_savings_needed(
    db: Session,
    goal_id: int,
):
    """
    Estimate savings needed per month.

    Uses approximate 30-day planning periods.
    """

    goal = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.id == goal_id)
        .first()
    )

    if goal is None:
        return None

    target_date = datetime.strptime(
        str(goal.target_date),
        "%Y-%m-%d",
    ).date()

    today = date.today()

    remaining_amount = max(
        0,
        goal.target_amount - goal.current_amount,
    )

    days_remaining = (
        target_date - today
    ).days

    if remaining_amount == 0:
        months_remaining = 0
        monthly_savings_needed = 0

    elif days_remaining <= 0:
        months_remaining = 0
        monthly_savings_needed = remaining_amount

    else:
        months_remaining = max(
            1,
            ceil(days_remaining / 30),
        )

        monthly_savings_needed = (
            remaining_amount / months_remaining
        )

    return {
        "goal_id": goal.id,
        "name": goal.name,
        "remaining_amount": round(
            remaining_amount, 2
        ),
        "months_remaining": months_remaining,
        "monthly_savings_needed": round(
            monthly_savings_needed, 2
        ),
    }


# ==========================================
# 4. BUDGET MANAGEMENT
# ==========================================

def get_budgets(db: Session):
    """Return all budgets."""

    return db.query(Budget).all()


def get_budget_status(
    db: Session,
    budget_id: int,
):
    """
    Calculate budget spending using
    matching expense transactions.

    Matches by month and category.
    """

    budget = (
        db.query(Budget)
        .filter(Budget.id == budget_id)
        .first()
    )

    if budget is None:
        return None

    transactions = (
        db.query(Transaction)
        .filter(Transaction.type == "expense")
        .all()
    )

    spent_amount = 0

    budget_category = (
        budget.category.strip().casefold()
    )

    for transaction in transactions:

        if not transaction.date:
            continue

        transaction_month = (
            str(transaction.date)[:7]
        )

        transaction_category = (
            (transaction.category or "")
            .strip()
            .casefold()
        )

        if (
            transaction_month == budget.month
            and transaction_category == budget_category
        ):
            spent_amount += transaction.amount

    remaining_amount = (
        budget.budget_amount - spent_amount
    )

    if budget.budget_amount <= 0:
        percentage_used = 0
    else:
        percentage_used = (
            spent_amount / budget.budget_amount
        ) * 100

    return {
        "budget_id": budget.id,
        "month": budget.month,
        "category": budget.category,
        "budget_amount": budget.budget_amount,
        "spent_amount": round(
            spent_amount, 2
        ),
        "remaining_amount": round(
            remaining_amount, 2
        ),
        "percentage_used": round(
            percentage_used, 2
        ),
    }


# ==========================================
# 5. AGENT ACTIVITY LOGGING
# ==========================================

def log_agent_action(
    db: Session,
    agent: str,
    action: str,
    tool: str,
    arguments: str,
    result: str,
):
    """Store an agent action in the database."""

    log = AgentLog(
        agent=agent,
        action=action,
        tool=tool,
        arguments=arguments,
        result=result,
        timestamp=datetime.now().isoformat(),
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

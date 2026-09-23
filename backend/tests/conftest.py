from datetime import date

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import (
    FinancialProfile,
    Transaction,
    SavingsGoal,
    Budget,
)


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False
        },
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    # --------------------------------
    # Current month for durable tests
    # --------------------------------

    current_month = date.today().strftime("%Y-%m")

    # --------------------------------
    # Financial profile
    # --------------------------------

    profile = FinancialProfile(
        monthly_income=5000,
        rent=1500,
        tuition=500,
        groceries=300,
        transport=300,
        utilities=100,
        lifestyle_costs=500,
    )

    session.add(profile)

    # --------------------------------
    # Transactions
    # --------------------------------

    transaction_1 = Transaction(
        date=f"{current_month}-10",
        description="Lunch",
        amount=20,
        category="Food",
        type="expense",
    )

    transaction_2 = Transaction(
        date=f"{current_month}-12",
        description="Bus",
        amount=10,
        category="Transport",
        type="expense",
    )

    session.add_all([
        transaction_1,
        transaction_2,
    ])

    # --------------------------------
    # Savings goal
    # --------------------------------

    goal = SavingsGoal(
        name="Vacation",
        target_amount=3000,
        current_amount=600,
        target_date="2030-06-01",
    )

    session.add(goal)

    # --------------------------------
    # Food budget for current month
    # --------------------------------

    budget = Budget(
        month=current_month,
        category="Food",
        budget_amount=500,
        spent_amount=0,
    )

    session.add(budget)

    session.commit()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
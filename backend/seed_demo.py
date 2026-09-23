from datetime import date

from app.database import Base, engine, SessionLocal
from app.models import (
    FinancialProfile,
    Transaction,
    SavingsGoal,
    Budget,
    AgentLog,
)


def seed_demo_data():
    print("Resetting Finora demo database...")

    # Remove existing tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        current_month = date.today().strftime("%Y-%m")

        # --------------------------------
        # Financial Profile
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

        db.add(profile)

        # --------------------------------
        # Transactions
        # --------------------------------

        transactions = [
            Transaction(
                date=f"{current_month}-03",
                description="Groceries",
                amount=85,
                category="Food",
                type="expense",
            ),
            Transaction(
                date=f"{current_month}-06",
                description="Bus pass",
                amount=45,
                category="Transport",
                type="expense",
            ),
            Transaction(
                date=f"{current_month}-10",
                description="Lunch",
                amount=18,
                category="Food",
                type="expense",
            ),
            Transaction(
                date=f"{current_month}-14",
                description="Coffee",
                amount=7,
                category="Food",
                type="expense",
            ),
            Transaction(
                date=f"{current_month}-18",
                description="Movie",
                amount=20,
                category="Entertainment",
                type="expense",
            ),
        ]

        db.add_all(transactions)

        # --------------------------------
        # Savings Goal
        # --------------------------------

        vacation_goal = SavingsGoal(
            name="Vacation",
            target_amount=3000,
            current_amount=900,
            target_date="2027-06-01",
        )

        db.add(vacation_goal)

        # --------------------------------
        # Budgets
        # --------------------------------

        budgets = [
            Budget(
                month=current_month,
                category="Food",
                budget_amount=500,
                spent_amount=0,
            ),
            Budget(
                month=current_month,
                category="Transport",
                budget_amount=250,
                spent_amount=0,
            ),
            Budget(
                month=current_month,
                category="Entertainment",
                budget_amount=200,
                spent_amount=0,
            ),
        ]

        db.add_all(budgets)

        db.commit()

        print("Finora demo database created successfully.")
        print()
        print("Demo profile:")
        print("Monthly income: $5,000")
        print("Savings goal: Vacation ($900 / $3,000)")
        print("Budgets: Food, Transport, Entertainment")
        print("Transactions: 5")
        print("Agent activity: clean")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
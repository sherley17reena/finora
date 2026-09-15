from app.database import SessionLocal
from app.agents.expense_agent import ExpenseAgent


db = SessionLocal()

try:
    agent = ExpenseAgent(db)

    # Test 1: Get all expenses
    print("=== TEST 1: GET EXPENSES ===")

    result = agent.handle("get_expenses")

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    print("\nExpenses:")

    for expense in result["data"]:
        print(
            expense.id,
            expense.date,
            expense.description,
            expense.amount,
            expense.category
        )

    # Test 2: Get total expenses
    print("\n=== TEST 2: TOTAL EXPENSES ===")

    result = agent.handle("get_total_expenses")

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])
    print("Total expenses:", result["data"]["total_expenses"])

    # Test 3: Add an expense
    print("\n=== TEST 3: ADD EXPENSE ===")

    result = agent.handle(
        "add_expense",
        date="2026-09-15",
        description="Bus ticket",
        amount=10,
        category="Transport"
    )

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])
    print("Added expense:", result["data"])

finally:
    db.close()
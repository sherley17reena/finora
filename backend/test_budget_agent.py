from app.database import SessionLocal
from app.agents.budget_agent import BudgetAgent


db = SessionLocal()

try:
    agent = BudgetAgent(db)

    # Test 1: Get all budgets
    print("=== TEST 1: GET BUDGETS ===")

    result = agent.handle("get_budgets")

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    print("\nBudgets:")

    for budget in result["data"]:
        print(
            budget.id,
            budget.month,
            budget.category,
            budget.budget_amount,
            budget.spent_amount
        )

    # Test 2: Check budget status
    print("\n=== TEST 2: BUDGET STATUS ===")

    result = agent.handle(
        "get_budget_status",
        budget_id=1
    )

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    if result["status"] == "success":
        print("Category:", result["data"]["category"])
        print("Budget:", result["data"]["budget_amount"])
        print("Spent:", result["data"]["spent_amount"])
        print("Remaining:", result["data"]["remaining_amount"])
        print("Percentage used:", result["data"]["percentage_used"], "%")
    else:
        print("Message:", result["message"])

    # Test 3: Simulate a purchase
    print("\n=== TEST 3: PURCHASE SIMULATION ===")

    result = agent.handle(
        "simulate_purchase",
        purchase_amount=400
    )

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])
    print("Purchase amount:", result["data"]["purchase_amount"])
    print("Remaining income:", result["data"]["remaining_income"])
    print("Money after purchase:", result["data"]["money_after_purchase"])
    print("Can afford:", result["data"]["can_afford"])

finally:
    db.close()
from app.database import SessionLocal
from app.coordinator import FinanceCoordinator


db = SessionLocal()

try:
    coordinator = FinanceCoordinator(db)

    # Test 1: Route to Expense Agent
    print("=== TEST 1: EXPENSE AGENT ===")

    result = coordinator.route(
        agent_name="expense",
        action="get_total_expenses"
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Total expenses:", result["data"]["total_expenses"])

    # Test 2: Route to Savings Agent
    print("\n=== TEST 2: SAVINGS AGENT ===")

    result = coordinator.route(
        agent_name="savings",
        action="get_savings_progress",
        goal_id=1
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Goal:", result["data"]["name"])
    print("Progress:", result["data"]["progress_percentage"], "%")

    # Test 3: Route to Budget Agent
    print("\n=== TEST 3: BUDGET AGENT ===")

    result = coordinator.route(
        agent_name="budget",
        action="simulate_purchase",
        purchase_amount=400
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Can afford:", result["data"]["can_afford"])
    print("Money after purchase:", result["data"]["money_after_purchase"])

    # Test 4: Automatic routing - Expense Agent
    print("\n=== TEST 4: AUTO ROUTE EXPENSE ===")

    result = coordinator.auto_route(
        action="get_total_expenses"
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Total expenses:", result["data"]["total_expenses"])


    # Test 5: Automatic routing - Savings Agent
    print("\n=== TEST 5: AUTO ROUTE SAVINGS ===")

    result = coordinator.auto_route(
        action="get_savings_progress",
        goal_id=1
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Goal:", result["data"]["name"])
    print("Progress:", result["data"]["progress_percentage"], "%")


    # Test 6: Automatic routing - Budget Agent
    print("\n=== TEST 6: AUTO ROUTE BUDGET ===")

    result = coordinator.auto_route(
        action="simulate_purchase",
        purchase_amount=400
    )

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Can afford:", result["data"]["can_afford"])

    # Test 7: Multi-agent purchase analysis
    print("\n=== TEST 7: MULTI-AGENT PURCHASE ANALYSIS ===")

    result = coordinator.analyze_purchase_with_savings(
        purchase_amount=1000,
        goal_id=1
    )

    print("Workflow:", result["workflow"])
    print("Status:", result["status"])
    print("Agents used:", result["agents_used"])

    print("\nPurchase Analysis:")
    print(
        "Can afford:",
        result["purchase_analysis"]["can_afford"]
    )
    print(
        "Money after purchase:",
        result["purchase_analysis"]["money_after_purchase"]
    )

    print("\nSavings Analysis:")
    print(
        "Goal:",
        result["savings_analysis"]["name"]
    )
    print(
        "Progress:",
        result["savings_analysis"]["progress_percentage"],
        "%"
    )
    print(
        "Remaining:",
        result["savings_analysis"]["remaining_amount"]
    )

    print("\nDecision:")
    print(result["decision"])
    
finally:
    db.close()
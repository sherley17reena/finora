from app.database import SessionLocal
from app.agents.savings_agent import SavingsAgent


db = SessionLocal()

try:
    agent = SavingsAgent(db)

    # Test 1: Get all savings goals
    print("=== TEST 1: GET SAVINGS GOALS ===")

    result = agent.handle("get_savings_goals")

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    print("\nSavings Goals:")

    for goal in result["data"]:
        print(
            goal.id,
            goal.name,
            goal.current_amount,
            goal.target_amount,
            goal.target_date
        )

    # Test 2: Calculate progress for goal ID 1
    print("\n=== TEST 2: SAVINGS PROGRESS ===")

    result = agent.handle(
        "get_savings_progress",
        goal_id=1
    )

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    if result["status"] == "success":
        print("Goal:", result["data"]["name"])
        print("Target:", result["data"]["target_amount"])
        print("Saved:", result["data"]["current_amount"])
        print("Remaining:", result["data"]["remaining_amount"])
        print("Progress:", result["data"]["progress_percentage"], "%")
    else:
        print("Message:", result["message"])

    # Test 3: Calculate monthly savings needed
    print("\n=== TEST 3: MONTHLY SAVINGS NEEDED ===")

    result = agent.handle(
        "calculate_monthly_savings_needed",
        goal_id=1
    )

    print("Agent:", result["agent"])
    print("Action:", result["action"])
    print("Status:", result["status"])

    if result["status"] == "success":
        print("Goal:", result["data"]["name"])
        print("Remaining amount:", result["data"]["remaining_amount"])
        print("Months remaining:", result["data"]["months_remaining"])
        print(
            "Monthly savings needed:",
            result["data"]["monthly_savings_needed"]
        )
    else:
        print("Message:", result["message"])

finally:
    db.close()
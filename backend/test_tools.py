from app.database import SessionLocal
from app.tools import (
#    add_expense,
    get_expenses,
    get_income,
    calculate_remaining_income,
    simulate_purchase
)

db = SessionLocal()

try:
    print("Monthly income:")
    print(get_income(db))

#    print("\nAdding test expense...")
#    expense = add_expense(
#       db=db,
#       date="2026-09-14",
#       description="Coffee",
#       amount=5,
#       category="Food"
#   )

#    print(f"Created expense with ID: {expense.id}")

    print("\nAll expenses:")
    expenses = get_expenses(db)

    for item in expenses:
        print(
            item.id,
            item.date,
            item.description,
            item.amount,
            item.category
        )

finally:
    db.close()

print("\nRemaining income:")
print(calculate_remaining_income(db))

print("\nPurchase simulation:")
print(simulate_purchase(db, 400))
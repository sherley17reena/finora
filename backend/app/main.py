from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.coordinator import FinanceCoordinator
from app.assistant_service import handle_assistant_message

from .database import SessionLocal
from app.models import (
    FinancialProfile,
    Transaction,
    SavingsGoal,
    Budget,
    AgentLog
)
from .schemas import (
    FinancialProfileCreate,
    FinancialProfileUpdate,
    TransactionCreate,
    TransactionUpdate,
    SavingsGoalCreate,
    SavingsGoalUpdate,
    BudgetCreate,
    BudgetUpdate,
    PurchaseAnalysisRequest,
    AssistantMessageRequest,
)

from app.tools import (
    calculate_remaining_income,
    get_total_expenses,
    get_savings_progress
)

FIXED_EXPENSE_CATEGORIES = {
    "rent",
    "tuition",
    "utilities",
}


def validate_transaction_category(category: str, transaction_type: str):
    if (
        transaction_type.strip().casefold() == "expense"
        and category.strip().casefold() in FIXED_EXPENSE_CATEGORIES
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "Rent, Tuition, and Utilities are already "
                "deducted automatically from your financial profile. "
                "Do not add them as expense transactions."
            ),
        )
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/assistant")
def assistant(message: AssistantMessageRequest, db: Session = Depends(get_db)):
    try:
        return handle_assistant_message(
            db,
            message.message
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

@app.get("/")
def home():
    return {"message": "Welcome to Finora"}


@app.post("/profile")
def create_profile(
    profile: FinancialProfileCreate,
    db: Session = Depends(get_db)
):
    new_profile = FinancialProfile(
        monthly_income=profile.monthly_income,
        rent=profile.rent,
        tuition=profile.tuition,
        groceries=profile.groceries,
        transport=profile.transport,
        utilities=profile.utilities,
        lifestyle_costs=profile.lifestyle_costs
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Financial profile created successfully",
        "profile_id": new_profile.id
    }

@app.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(FinancialProfile).first()

    if profile is None:
        return {"message": "No financial profile found"}

    return {
        "id": profile.id,
        "monthly_income": profile.monthly_income,
        "rent": profile.rent,
        "tuition": profile.tuition,
        "groceries": profile.groceries,
        "transport": profile.transport,
        "utilities": profile.utilities,
        "lifestyle_costs": profile.lifestyle_costs
    }

@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    validate_transaction_category(
        transaction.category,
        transaction.type,
    )

    new_transaction = Transaction(
        date=transaction.date,
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category.strip(),
        type=transaction.type,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "message": "Transaction created successfully",
        "transaction_id": new_transaction.id,
    }

@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

@app.post("/savings-goals")
def create_savings_goal(
    goal: SavingsGoalCreate,
    db: Session = Depends(get_db)
):
    new_goal = SavingsGoal(
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        target_date=goal.target_date
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return {
        "message": "Savings goal created successfully",
        "goal_id": new_goal.id
    }

@app.get("/savings-goals")
def get_savings_goals(db: Session = Depends(get_db)):
    goals = db.query(SavingsGoal).all()

    return goals

@app.post("/budgets")
def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db)
):
    new_budget = Budget(
        month=budget.month,
        category=budget.category,
        budget_amount=budget.budget_amount,
        spent_amount=budget.spent_amount
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return {
        "message": "Budget created successfully",
        "budget_id": new_budget.id
    }


@app.get("/budgets")
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).all()

    return budgets

@app.post("/analyze-purchase")
def analyze_purchase(
    request: PurchaseAnalysisRequest,
    db: Session = Depends(get_db)
):
    coordinator = FinanceCoordinator(db)

    result = coordinator.analyze_purchase_with_savings(
        purchase_amount=request.purchase_amount,
        goal_id=request.goal_id
    )

    return result

@app.get("/agent-logs")
def get_agent_logs(db: Session = Depends(get_db)):

    logs = (
        db.query(AgentLog)
        .order_by(AgentLog.id.desc())
        .all()
    )

    return [
        {
            "id": log.id,
            "agent": log.agent,
            "action": log.action,
            "tool": log.tool,
            "arguments": log.arguments,
            "result": log.result,
            "timestamp": log.timestamp
        }
        for log in logs
    ]

@app.get("/dashboard-summary")
def get_dashboard_summary(
    db: Session = Depends(get_db)
):
    profile = db.query(FinancialProfile).first()

    if profile is None:
        return {
            "status": "error",
            "message": "No financial profile found"
        }

    # Monthly financial calculations
    remaining_income = calculate_remaining_income(db)
    total_expenses = get_total_expenses(db)

    # Calculate overall savings progress
    goals = db.query(SavingsGoal).all()

    total_savings_target = sum(
        goal.target_amount for goal in goals
    )

    total_savings_saved = sum(
        goal.current_amount for goal in goals
    )

    if total_savings_target > 0:
        savings_progress = round(
            (
                total_savings_saved
                / total_savings_target
            ) * 100,
            2
        )
    else:
        savings_progress = 0

    return {
        "monthly_income": profile.monthly_income,
        "available_income": remaining_income,
        "total_expenses": total_expenses,
        "savings_progress": savings_progress
    }


@app.get("/savings-goals/{goal_id}/progress")
def get_savings_goal_progress(
    goal_id: int,
    db: Session = Depends(get_db)
):
    coordinator = FinanceCoordinator(db)

    result = coordinator.route(
        agent_name="savings",
        action="get_savings_progress",
        goal_id=goal_id
    )

    return result

@app.get("/budgets/{budget_id}/status")
def get_budget_status_by_id(
    budget_id: int,
    db: Session = Depends(get_db)
):
    coordinator = FinanceCoordinator(db)

    result = coordinator.route(
        agent_name="budget",
        action="get_budget_status",
        budget_id=budget_id
    )

    return result
@app.patch("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updates: TransactionUpdate,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    data = updates.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )

    updated_category = data.get(
        "category",
        transaction.category,
    )

    updated_type = data.get(
        "type",
        transaction.type,
    )

    validate_transaction_category(
        updated_category,
        updated_type,
    )

    for field, value in data.items():
        if field == "category":
            value = value.strip()

        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return {
        "message": "Transaction updated successfully",
        "transaction": transaction,
    }

@app.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted successfully",
        "transaction_id": transaction_id
    }

@app.patch("/savings-goals/{goal_id}")
def update_savings_goal(
    goal_id: int,
    updates: SavingsGoalUpdate,
    db: Session = Depends(get_db)
):
    goal = db.get(SavingsGoal, goal_id)

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Savings goal not found"
        )

    data = updates.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null"
        )

    for field, value in data.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    return {
        "message": "Savings goal updated successfully",
        "goal": goal
    }


@app.delete("/savings-goals/{goal_id}")
def delete_savings_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    goal = db.get(SavingsGoal, goal_id)

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Savings goal not found"
        )

    db.delete(goal)
    db.commit()

    return {
        "message": "Savings goal deleted successfully",
        "goal_id": goal_id
    }

@app.patch("/budgets/{budget_id}")
def update_budget(
    budget_id: int,
    updates: BudgetUpdate,
    db: Session = Depends(get_db)
):
    budget = db.get(Budget, budget_id)

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    data = updates.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null"
        )

    for field, value in data.items():
        setattr(budget, field, value)

    db.commit()
    db.refresh(budget)

    return {
        "message": "Budget updated successfully",
        "budget": budget
    }


@app.delete("/budgets/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    budget = db.get(Budget, budget_id)

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    db.delete(budget)
    db.commit()

    return {
        "message": "Budget deleted successfully",
        "budget_id": budget_id
    }

@app.patch("/profile")
def update_profile(
    updates: FinancialProfileUpdate,
    db: Session = Depends(get_db)
):
    profile = db.query(FinancialProfile).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found"
        )

    data = updates.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null"
        )

    for field, value in data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return {
        "message": "Financial profile updated successfully",
        "profile": profile
    }

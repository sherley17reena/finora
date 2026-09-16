from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.coordinator import FinanceCoordinator

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
    TransactionCreate,
    SavingsGoalCreate,
    BudgetCreate,
    PurchaseAnalysisRequest
)

from app.tools import (
    calculate_remaining_income,
    get_total_expenses,
    get_savings_progress
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
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
    new_transaction = Transaction(
        date=transaction.date,
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category,
        type=transaction.type
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "message": "Transaction created successfully",
        "transaction_id": new_transaction.id
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
def get_dashboard_summary(db: Session = Depends(get_db)):

    profile = db.query(FinancialProfile).first()

    if profile is None:
        return {
            "status": "error",
            "message": "No financial profile found"
        }

    remaining_income = calculate_remaining_income(db)
    total_expenses = get_total_expenses(db)

    goals = db.query(SavingsGoal).all()

    savings_progress = 0

    if goals:
        progress = get_savings_progress(
            db,
            goal_id=goals[0].id
        )

        if progress:
            savings_progress = progress["progress_percentage"]

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
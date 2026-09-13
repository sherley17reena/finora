from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import FinancialProfile, Transaction
from .schemas import FinancialProfileCreate, TransactionCreate


app = FastAPI()


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
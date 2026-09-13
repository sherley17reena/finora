from pydantic import BaseModel


class FinancialProfileCreate(BaseModel):
    monthly_income: float
    rent: float = 0
    tuition: float = 0
    groceries: float = 0
    transport: float = 0
    utilities: float = 0
    lifestyle_costs: float = 0

class TransactionCreate(BaseModel):
    date: str
    description: str
    amount: float
    category: str
    type: str
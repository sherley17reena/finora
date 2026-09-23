
from typing import Literal, Optional
from pydantic import BaseModel, Field

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

class SavingsGoalCreate(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0
    target_date: str

class BudgetCreate(BaseModel):
    month: str
    category: str
    budget_amount: float
    spent_amount: float = 0

class PurchaseAnalysisRequest(BaseModel):
    purchase_amount: float
    goal_id: int

class AssistantMessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=1000
    )

class AssistantIntent(BaseModel):
    action: Literal[
        "add_expense",
        "get_total_expenses",
        "get_savings_progress",
        "get_budget_status",
        "analyze_purchase",
        "unknown",
    ]

    amount: Optional[float] = Field(
        default=None,
        gt=0
    )

    purchase_amount: Optional[float] = Field(
        default=None,
        gt=0
    )

    category: Optional[
        Literal[
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Utilities",
            "Education",
            "Health",
            "Housing",
            "Other",
        ]
    ] = None

    description: Optional[str] = None
    date: Optional[str] = None
    goal_name: Optional[str] = None
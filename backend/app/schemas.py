
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date

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
        "increase_budget",
        "decrease_budget",
        "set_budget",
        "unknown",
    ]

    amount: Optional[float] = Field(
        default=None,
        gt=0
    )

    budget_amount: Optional[float] = Field(
        default=None,
        ge=0
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


class TransactionUpdate(BaseModel):
    date: Optional[str] = None
    description: Optional[str] = Field(
        default=None, min_length=1
    )
    amount: Optional[float] = Field(
        default=None, gt=0
    )
    category: Optional[str] = Field(
        default=None, min_length=1
    )
    type: Optional[Literal["income", "expense"]] = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        if value is not None:
            date.fromisoformat(value)
        return value


class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=1
    )
    target_amount: Optional[float] = Field(
        default=None, gt=0
    )
    current_amount: Optional[float] = Field(
        default=None, ge=0
    )
    target_date: Optional[str] = None

    @field_validator("target_date")
    @classmethod
    def validate_target_date(cls, value):
        if value is not None:
            date.fromisoformat(value)
        return value


class BudgetUpdate(BaseModel):
    month: Optional[str] = Field(
        default=None, pattern=r"^\d{4}-(0[1-9]|1[0-2])$"
    )
    category: Optional[str] = Field(
        default=None, min_length=1
    )
    budget_amount: Optional[float] = Field(
        default=None, ge=0
    )
    spent_amount: Optional[float] = Field(
        default=None, ge=0
    )


class FinancialProfileUpdate(BaseModel):
    monthly_income: Optional[float] = Field(
        default=None, ge=0
    )
    rent: Optional[float] = Field(
        default=None, ge=0
    )
    tuition: Optional[float] = Field(
        default=None, ge=0
    )
    groceries: Optional[float] = Field(
        default=None, ge=0
    )
    transport: Optional[float] = Field(
        default=None, ge=0
    )
    utilities: Optional[float] = Field(
        default=None, ge=0
    )
    lifestyle_costs: Optional[float] = Field(
        default=None, ge=0
    )
from sqlalchemy import Column, Integer, String, Float
from .database import Base


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(Integer, primary_key=True, index=True)

    monthly_income = Column(Float, default=0)

    rent = Column(Float, default=0)
    tuition = Column(Float, default=0)
    groceries = Column(Float, default=0)
    transport = Column(Float, default=0)
    utilities = Column(Float, default=0)
    lifestyle_costs = Column(Float, default=0)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(String)
    description = Column(String)
    amount = Column(Float)
    category = Column(String)
    type = Column(String)

class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    target_amount = Column(Float)
    current_amount = Column(Float, default=0)

    target_date = Column(String)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)

    month = Column(String)
    category = Column(String)

    budget_amount = Column(Float)
    spent_amount = Column(Float, default=0)

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)

    agent = Column(String)
    action = Column(String)
    tool = Column(String)

    arguments = Column(String)
    result = Column(String)

    timestamp = Column(String)
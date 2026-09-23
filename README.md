# Finora

Finora is a full-stack, multi-agent personal finance assistant that combines natural-language AI with deterministic financial tools.

Users can track expenses, monitor budgets, follow savings goals, and ask financial questions in natural language. Finora uses Gemini to interpret user intent, then routes requests through specialized finance agents that execute calculations and database operations using deterministic Python tools.

## Features

- Track and categorize expenses
- Monitor monthly spending
- Create and track savings goals
- Create category-based monthly budgets
- Analyze purchase affordability
- Ask finance questions in natural language
- Coordinate multiple specialized agents for complex requests
- Record agent activity for observability
- Validate LLM-generated intents before execution
- Run automated tests without requiring live Gemini API calls

## Multi-Agent System

Finora contains three specialized agents:

### Expense Agent

Handles expense-related operations such as:

- adding expenses
- retrieving transactions
- calculating current-month spending

### Savings Agent

Handles savings-related operations such as:

- retrieving savings goals
- calculating goal progress
- calculating remaining savings requirements

### Budget Agent

Handles budget and affordability operations such as:

- retrieving budgets
- calculating category spending
- checking remaining budget
- simulating purchases

The `FinanceCoordinator` routes requests to the appropriate agent and coordinates multiple agents when a request requires more than one financial perspective.

## Architecture

```text
                    ┌──────────────────────┐
                    │     React Client     │
                    │   Finora Dashboard   │
                    └──────────┬───────────┘
                               │
                               │ HTTP / JSON
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │     REST Backend     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Assistant Service   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Gemini LLM      │
                    │ Intent Understanding │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Pydantic Validation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Finance Coordinator  │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
        ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
        │ Expense Agent  │ │Savings Agent │ │ Budget Agent │
        └───────┬────────┘ └──────┬───────┘ └──────┬───────┘
                │                 │                │
                └─────────────────┼────────────────┘
                                  ▼
                       ┌────────────────────┐
                       │ Deterministic      │
                       │ Financial Tools    │
                       └─────────┬──────────┘
                                 │
                                 ▼
                       ┌────────────────────┐
                       │ SQLAlchemy / SQLite│
                       └────────────────────┘
```

## Design Principle

Finora separates language understanding from financial execution.

**The LLM interprets intent. Python performs financial calculations and database operations.**

Gemini is not responsible for calculating balances, budget usage, savings progress, or affordability. Instead, it converts natural-language requests into structured intents.

Those intents are validated using Pydantic before they are allowed to reach the finance system.

This reduces hallucination risk and keeps financial operations deterministic and testable.

## Example Multi-Agent Workflow

A user can ask:

> Can I afford a $500 phone and still reach my Vacation savings goal?

Finora processes the request as follows:

```text
Natural-language request
        │
        ▼
Gemini intent extraction
        │
        ▼
Pydantic validation
        │
        ▼
Finance Coordinator
        │
        ├──────────────► Budget Agent
        │                 │
        │                 ▼
        │          Purchase simulation
        │
        └──────────────► Savings Agent
                          │
                          ▼
                   Savings progress
        │
        ▼
Combined decision
```

The Budget Agent determines whether the purchase is affordable, while the Savings Agent evaluates progress toward the selected savings goal.

The coordinator combines both results into a single response.

## Agent Observability

Finora records agent executions in an `AgentLog` table.

Each log contains:

- agent name
- action
- tool
- arguments
- result
- timestamp

The React application includes an Agent Activity page that allows agent execution to be inspected from the UI.

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

### AI

- Google Gemini API
- Structured intent extraction
- Multi-agent orchestration

### Testing

- pytest
- temporary SQLite test database
- mocked LLM intents

## Project Structure

```text
Finora/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── llm/
│   │   ├── assistant_service.py
│   │   ├── coordinator.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── tools.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_assistant_service.py
│   │   └── test_finance_agents.py
│   ├── .env.example
│   ├── create_db.py
│   ├── pytest.ini
│   ├── requirements.txt
│   └── seed_demo.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── docs/
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <https://github.com/sherley17reena/finora>
cd Finora
```

### 2. Set up the backend

```bash
cd backend

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Gemini

Copy the example environment file:

```bash
cp .env.example .env
```

Add your Gemini API key to:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit the real `.env` file.

### 4. Create demo data

```bash
python seed_demo.py
```

This creates a reproducible local demo database containing a financial profile, transactions, budgets, and a savings goal.

### 5. Start the backend

```bash
uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, typically:

```text
http://localhost:5173
```

## Example Assistant Prompts

Try requests such as:

```text
How much have I spent this month?

How am I doing on my Food budget?

How is my Vacation savings goal going?

I spent $15 on lunch today.

Can I afford a $500 phone and still reach my Vacation savings goal?
```

## Testing

Finora includes automated tests for the finance agents, coordinator logging, assistant routing, savings calculations, budget calculations, expense creation, and multi-agent purchase analysis.

Gemini is mocked during assistant tests, so automated testing does not consume API quota.

Run:

```bash
cd backend
pytest -v
```

## Security and Reliability

Finora includes several safeguards around LLM integration:

- API keys are stored in environment variables
- `.env` files are excluded from Git
- Gemini output is parsed as structured JSON
- Pydantic validates actions and supported categories
- monetary values are validated before execution
- financial calculations are performed by deterministic Python functions
- agent actions are logged for observability

## Future Improvements

Potential extensions include:

- user authentication
- PostgreSQL support
- recurring transactions
- spending analytics and charts
- conversational history
- deployment with managed cloud infrastructure

## Project Status

Finora V1 implements a complete local full-stack multi-agent finance workflow with LLM-based intent understanding, deterministic financial execution, agent observability, and automated testing.
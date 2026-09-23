import json
from datetime import date

from pydantic import ValidationError

from app.llm.gemini_client import ask_gemini
from app.schemas import AssistantIntent


def understand_message(message: str):
    today = date.today().isoformat()

    prompt = f"""
You are the intent router for Finora, a personal finance application.

Your ONLY job is to understand the user's request and return valid JSON.
Do not perform financial calculations yourself.

Available actions:

1. add_expense
Required:
- amount
- category
- description
- date

Expense categories:

- Food
- Transport
- Shopping
- Entertainment
- Utilities
- Education
- Health
- Housing
- Other

Category rules:
- Restaurant, dinner, lunch, breakfast, groceries, coffee, and snacks -> Food
- Bus, taxi, Uber, train, fuel, and transportation -> Transport
- Movies, games, concerts, and subscriptions -> Entertainment
- Clothes, electronics, and general purchases -> Shopping
- Tuition, textbooks, and school costs -> Education
- Rent and housing costs -> Housing
- Medical and pharmacy expenses -> Health
- Electricity, water, internet, and phone bills -> Utilities
- If no category clearly applies -> Other

Always return one of these exact category names for add_expense.

2. get_total_expenses

3. get_savings_progress
Required:
- goal_name

4. get_budget_status
Required:
- category

5. analyze_purchase
Required:
- purchase_amount
Optional:
- goal_name

6. unknown

Today's date is {today}.

Rules:
- Return JSON only.
- Do not use Markdown.
- Do not explain the result.
- Monetary values must be numbers.
- Monetary values must be greater than zero when provided.
- If the user says "today", use {today}.
- Choose only one of the actions listed above.
- Never invent a savings goal or budget category.
- If required information is missing, use null.

Expected format:

{{
    "action": "action_name",
    "amount": null,
    "purchase_amount": null,
    "category": null,
    "description": null,
    "date": null,
    "goal_name": null
}}

User message:
{message}
"""

    try:
        response = ask_gemini(prompt)

        raw_intent = json.loads(response)

        validated_intent = AssistantIntent.model_validate(
            raw_intent
        )

        return validated_intent.model_dump()

    except json.JSONDecodeError:
        return {
            "action": "unknown",
            "error": "Gemini returned invalid JSON",
        }

    except ValidationError as error:
        return {
            "action": "unknown",
            "error": "Gemini returned an invalid intent",
            "validation_errors": error.errors(),
        }

    except Exception as error:
        return {
            "action": "unknown",
            "error": "Finora could not process the AI request",
            "details": str(error),
        }
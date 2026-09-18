import { useState } from "react";
import { askFinora } from "../api/finoraApi";

function Assistant({ onDataChanged }) {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!message.trim()) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResponse(null);

      const data = await askFinora(message);

      setResponse(data);
      
      if (
        data.status === "success" &&
        data.intent?.action === "add_expense"
      ) {
        onDataChanged?.();
      }

    } catch (err) {
      console.error(err);
      setError(
        "Finora couldn't process your request. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function getResponseMessage() {
    if (!response) {
      return "";
    }

    if (response.status === "error") {
      return response.message || "I couldn't complete that request.";
    }

    const result = response.result;

    if (!result) {
      return "Request completed.";
    }

    if (result.workflow === "purchase_with_savings_analysis") {
      return result.decision;
    }

    if (result.action === "add_expense") {
      const data = result.data;

      return `Added $${data.amount.toLocaleString()} for ${
        data.description
      } under ${data.category}.`;
    }

    if (result.action === "get_total_expenses") {
      return `You've spent $${result.data.total_expenses.toLocaleString()} this month.`;
    }

    if (result.action === "get_savings_progress") {
      const data = result.data;

      return `${data.name} is ${data.progress_percentage}% complete. You have saved $${data.current_amount.toLocaleString()} of your $${data.target_amount.toLocaleString()} goal.`;
    }

    if (result.action === "get_budget_status") {
      const data = result.data;

      return `You've used ${data.percentage_used}% of your ${data.category} budget. You have $${data.remaining_amount.toLocaleString()} remaining.`;
    }

    if (result.action === "simulate_purchase") {
      const data = result.data;

      if (data.can_afford) {
        return `You can afford this purchase. You would have $${data.money_after_purchase.toLocaleString()} remaining.`;
      }

      return "This purchase is not affordable based on your current available income.";
    }

    return "Request completed successfully.";
  }

  function getAgentsUsed() {
    if (!response?.result) {
      return [];
    }

    if (response.result.agents_used) {
      return response.result.agents_used;
    }

    if (response.result.agent) {
      return [response.result.agent];
    }

    return [];
  }

  return (
    <>
      <header>
        <p className="welcome">AI Financial Assistant</p>

        <h2>Finora Assistant</h2>

        <p className="subtitle">
          Ask Finora about your expenses, budgets,
          savings goals, or purchase decisions.
        </p>
      </header>

      <section className="panel">
        <h3>Ask Finora</h3>

        <form
          className="expense-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="assistantMessage">
              What would you like to know?
            </label>

            <textarea
              id="assistantMessage"
              rows="4"
              placeholder="Can I afford a $500 phone and still reach my Vacation goal?"
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              disabled={loading}
              required
            />
          </div>

          <button
            className="add-expense-button"
            type="submit"
            disabled={loading}
          >
            {loading ? "Finora is thinking..." : "Ask Finora"}
          </button>
        </form>

        {error && (
          <p className="form-message">
            {error}
          </p>
        )}
      </section>

      {response && (
        <section className="panel">
          <h3>Finora's Response</h3>

          <div className="assistant-decision">
            <strong>Finora</strong>
            <p>{getResponseMessage()}</p>
          </div>

          {getAgentsUsed().length > 0 && (
            <p>
              <strong>Agents used:</strong>{" "}
              {getAgentsUsed().join(" • ")}
            </p>
          )}
        </section>
      )}
    </>
  );
}

export default Assistant;
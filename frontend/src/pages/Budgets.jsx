import { useState } from "react";
import ProgressBar from "../components/ProgressBar";
import { createBudget } from "../api/finoraApi";

function Budgets({
  budgets,
  budgetStatus,
  onBudgetsUpdated,
}) {
  const [form, setForm] = useState({
    month: "",
    category: "",
    budget_amount: "",
  });

  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setMessage("");
    setIsSubmitting(true);

    try {
      await createBudget({
        month: form.month,
        category: form.category,
        budget_amount: Number(form.budget_amount),
        spent_amount: 0,
      });

      setForm({
        month: "",
        category: "",
        budget_amount: "",
      });

      setMessage("Budget created successfully.");

      await onBudgetsUpdated();
    } catch (error) {
      console.error("Error creating budget:", error);
      setMessage("Could not create budget.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <header>
        <p className="welcome">Budget Agent</p>
        <h2>Budgets</h2>

        <p className="subtitle">
          Set monthly spending limits and track your actual spending.
        </p>
      </header>

      <section className="panel">
        <h3>Create Budget</h3>

        <form
          className="expense-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="budgetMonth">
              Month
            </label>

            <input
              id="budgetMonth"
              name="month"
              type="month"
              value={form.month}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="budgetCategory">
              Category
            </label>

            <input
              id="budgetCategory"
              name="category"
              type="text"
              placeholder="Food"
              value={form.category}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="budgetAmount">
              Budget Limit
            </label>

            <input
              id="budgetAmount"
              name="budget_amount"
              type="number"
              min="0.01"
              step="0.01"
              placeholder="500"
              value={form.budget_amount}
              onChange={handleChange}
              required
            />
          </div>

          <button
            className="add-expense-button"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Creating..."
              : "Create Budget"}
          </button>
        </form>

        {message && (
          <p className="form-message">
            {message}
          </p>
        )}
      </section>

      <section className="panel">
        <h3>Your Budgets</h3>

        {budgets.length === 0 ? (
          <p>No budgets found.</p>
        ) : (
          <div className="savings-list">
            {budgets.map((budget) => {
              const status = budgetStatus[budget.id];

              const percentageUsed =
                status?.percentage_used ?? 0;

              return (
                <div
                  className="savings-goal"
                  key={budget.id}
                >
                  <div className="savings-goal-header">
                    <div>
                      <h3>{budget.category}</h3>
                      <p>Month: {budget.month}</p>
                    </div>

                    <strong>
                      {status
                        ? `${percentageUsed}% used`
                        : "Loading..."}
                    </strong>
                  </div>

                  <ProgressBar value={percentageUsed} />

                  {status && (
                    <>
                      <div className="savings-amounts">
                        <span>
                          Budget: $
                          {status.budget_amount.toLocaleString()}
                        </span>

                        <span>
                          Spent: $
                          {status.spent_amount.toLocaleString()}
                        </span>
                      </div>

                      <p className="savings-remaining">
                        Remaining: $
                        {status.remaining_amount.toLocaleString()}
                      </p>
                    </>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </section>
    </>
  );
}

export default Budgets;
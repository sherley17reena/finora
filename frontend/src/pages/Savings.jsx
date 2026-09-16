import { useState } from "react";
import ProgressBar from "../components/ProgressBar";
import { createSavingsGoal } from "../api/finoraApi";

function Savings({
  savingsGoals,
  savingsProgress,
  onGoalsUpdated,
}) {
  const [form, setForm] = useState({
    name: "",
    target_amount: "",
    current_amount: "",
    target_date: "",
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
      await createSavingsGoal({
        name: form.name,
        target_amount: Number(form.target_amount),
        current_amount: Number(form.current_amount || 0),
        target_date: form.target_date,
      });

      setForm({
        name: "",
        target_amount: "",
        current_amount: "",
        target_date: "",
      });

      setMessage("Savings goal created successfully.");

      await onGoalsUpdated();
    } catch (error) {
      console.error("Error creating savings goal:", error);
      setMessage("Could not create savings goal.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <header>
        <p className="welcome">Savings Agent</p>

        <h2>Savings Goals</h2>

        <p className="subtitle">
          Create goals and track your savings progress.
        </p>
      </header>

      <section className="panel">
        <h3>Create Savings Goal</h3>

        <form
          className="expense-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="goalName">
              Goal Name
            </label>

            <input
              id="goalName"
              name="name"
              type="text"
              placeholder="Vacation"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="targetAmount">
              Target Amount
            </label>

            <input
              id="targetAmount"
              name="target_amount"
              type="number"
              min="0.01"
              step="0.01"
              placeholder="3000"
              value={form.target_amount}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="currentAmount">
              Already Saved
            </label>

            <input
              id="currentAmount"
              name="current_amount"
              type="number"
              min="0"
              step="0.01"
              placeholder="500"
              value={form.current_amount}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="targetDate">
              Target Date
            </label>

            <input
              id="targetDate"
              name="target_date"
              type="date"
              value={form.target_date}
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
              : "Create Goal"}
          </button>
        </form>

        {message && (
          <p className="form-message">
            {message}
          </p>
        )}
      </section>

      <section className="panel">
        <h3>Your Savings Goals</h3>

        {savingsGoals.length === 0 ? (
          <p>No savings goals found.</p>
        ) : (
          <div className="savings-list">
            {savingsGoals.map((goal) => {
              const progressData =
                savingsProgress[goal.id];

              const progress =
                progressData?.progress_percentage ?? 0;

              return (
                <div
                  className="savings-goal"
                  key={goal.id}
                >
                  <div className="savings-goal-header">
                    <div>
                      <h3>{goal.name}</h3>

                      <p>
                        Target date: {goal.target_date}
                      </p>
                    </div>

                    <strong>
                      {progressData
                        ? `${progress}%`
                        : "Loading..."}
                    </strong>
                  </div>

                  <ProgressBar value={progress} />

                  <div className="savings-amounts">
                    <span>
                      Saved: $
                      {goal.current_amount.toLocaleString()}
                    </span>

                    <span>
                      Goal: $
                      {goal.target_amount.toLocaleString()}
                    </span>
                  </div>

                  {progressData && (
                    <p className="savings-remaining">
                      Remaining: $
                      {progressData.remaining_amount.toLocaleString()}
                    </p>
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

export default Savings;
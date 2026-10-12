
import { useState } from "react";
import ProgressBar from "../components/ProgressBar";

import {
  createBudget,
  updateBudget,
  deleteBudget,
} from "../api/finoraApi";

const emptyForm = {
  month: "",
  category: "",
  budget_amount: "",
};

function Budgets({
  budgets,
  budgetStatus,
  onBudgetsUpdated,
}) {
  const [form, setForm] = useState({ ...emptyForm });
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ ...emptyForm });
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  // -----------------------------
  // Create Budget
  // -----------------------------

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
        category: form.category.trim(),
        budget_amount: Number(form.budget_amount),
        spent_amount: 0,
      });

      await onBudgetsUpdated();

      setForm({ ...emptyForm });
      setMessage("Budget created successfully.");
    } catch (error) {
      console.error("Error creating budget:", error);
      setMessage("Could not create budget.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // -----------------------------
  // Edit Budget
  // -----------------------------

  const startEditing = (budget) => {
    setEditingId(budget.id);

    setEditForm({
      month: budget.month,
      category: budget.category,
      budget_amount: String(budget.budget_amount),
    });

    setMessage("");
  };

  const handleEditChange = (event) => {
    const { name, value } = event.target;

    setEditForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditForm({ ...emptyForm });
  };

  const handleSave = async (event) => {
    event.preventDefault();

    if (editingId === null) return;

    setSaving(true);
    setMessage("");

    try {
      await updateBudget(editingId, {
        month: editForm.month,
        category: editForm.category.trim(),
        budget_amount: Number(editForm.budget_amount),
      });

      await onBudgetsUpdated();

      cancelEditing();
      setMessage("Budget updated successfully.");
    } catch (error) {
      console.error("Error updating budget:", error);
      setMessage("Could not update budget.");
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------
  // Delete Budget
  // -----------------------------

  const handleDelete = async (budgetId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this budget?"
    );

    if (!confirmed) return;

    setDeletingId(budgetId);
    setMessage("");

    try {
      await deleteBudget(budgetId);

      await onBudgetsUpdated();

      if (editingId === budgetId) {
        cancelEditing();
      }

      setMessage("Budget deleted successfully.");
    } catch (error) {
      console.error("Error deleting budget:", error);
      setMessage("Could not delete budget.");
    } finally {
      setDeletingId(null);
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

      {/* Create Budget */}
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
            {isSubmitting ? "Creating..." : "Create Budget"}
          </button>
        </form>
      </section>

      {message && (
        <section className="panel">
          <p className="form-message" role="status">
            {message}
          </p>
        </section>
      )}

      {/* Budget List */}
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

              const isEditing = editingId === budget.id;

              return (
                <div
                  className="savings-goal"
                  key={budget.id}
                >
                  {isEditing ? (
                    <form
                      className="expense-form"
                      onSubmit={handleSave}
                    >
                      <h3>Edit Budget</h3>

                      <div className="form-group">
                        <label htmlFor={`edit-month-${budget.id}`}>
                          Month
                        </label>
                        <input
                          id={`edit-month-${budget.id}`}
                          name="month"
                          type="month"
                          value={editForm.month}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`edit-category-${budget.id}`}>
                          Category
                        </label>
                        <input
                          id={`edit-category-${budget.id}`}
                          name="category"
                          type="text"
                          value={editForm.category}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`edit-limit-${budget.id}`}>
                          Budget Limit
                        </label>
                        <input
                          id={`edit-limit-${budget.id}`}
                          name="budget_amount"
                          type="number"
                          min="0.01"
                          step="0.01"
                          value={editForm.budget_amount}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="transaction-actions">
                        <button
                          type="submit"
                          disabled={saving}
                        >
                          {saving ? "Saving..." : "Save Changes"}
                        </button>

                        <button
                          type="button"
                          onClick={cancelEditing}
                          disabled={saving}
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  ) : (
                    <>
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
                              {Number(
                                status.budget_amount
                              ).toLocaleString()}
                            </span>

                            <span>
                              Spent: $
                              {Number(
                                status.spent_amount
                              ).toLocaleString()}
                            </span>
                          </div>

                          <p className="savings-remaining">
                            Remaining: $
                            {Number(
                              status.remaining_amount
                            ).toLocaleString()}
                          </p>
                        </>
                      )}

                      <div className="transaction-actions">
                        <button
                          type="button"
                          onClick={() => startEditing(budget)}
                          disabled={saving || deletingId !== null}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() => handleDelete(budget.id)}
                          disabled={saving || deletingId !== null}
                        >
                          {deletingId === budget.id
                            ? "Deleting..."
                            : "Delete"}
                        </button>
                      </div>
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

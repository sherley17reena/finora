
import { useState } from "react";
import ProgressBar from "../components/ProgressBar";

import {
  createSavingsGoal,
  updateSavingsGoal,
  deleteSavingsGoal,
} from "../api/finoraApi";

function Savings({
  savingsGoals,
  savingsProgress,
  onGoalsUpdated,
}) {
  const emptyForm = {
    name: "",
    target_amount: "",
    current_amount: "",
    target_date: "",
  };

  const [form, setForm] = useState(emptyForm);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Editing state
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  // -----------------------------
  // Create Goal
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
      await createSavingsGoal({
        name: form.name.trim(),
        target_amount: Number(form.target_amount),
        current_amount: Number(form.current_amount || 0),
        target_date: form.target_date,
      });

      await onGoalsUpdated();

      setForm({ ...emptyForm });
      setMessage("Savings goal created successfully.");
    } catch (error) {
      console.error("Error creating savings goal:", error);
      setMessage("Could not create savings goal.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // -----------------------------
  // Edit Goal
  // -----------------------------

  const startEditing = (goal) => {
    setEditingId(goal.id);

    setEditForm({
      name: goal.name,
      target_amount: String(goal.target_amount),
      current_amount: String(goal.current_amount),
      target_date: goal.target_date,
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
      await updateSavingsGoal(editingId, {
        name: editForm.name.trim(),
        target_amount: Number(editForm.target_amount),
        current_amount: Number(editForm.current_amount),
        target_date: editForm.target_date,
      });

      await onGoalsUpdated();

      cancelEditing();
      setMessage("Savings goal updated successfully.");
    } catch (error) {
      console.error("Error updating savings goal:", error);
      setMessage("Could not update savings goal.");
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------
  // Delete Goal
  // -----------------------------

  const handleDelete = async (goalId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this savings goal?"
    );

    if (!confirmed) return;

    setDeletingId(goalId);
    setMessage("");

    try {
      await deleteSavingsGoal(goalId);

      await onGoalsUpdated();

      if (editingId === goalId) {
        cancelEditing();
      }

      setMessage("Savings goal deleted successfully.");
    } catch (error) {
      console.error("Error deleting savings goal:", error);
      setMessage("Could not delete savings goal.");
    } finally {
      setDeletingId(null);
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

      {/* Create Savings Goal */}
      <section className="panel">
        <h3>Create Savings Goal</h3>

        <form
          className="expense-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="goalName">Goal Name</label>
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
            {isSubmitting ? "Creating..." : "Create Goal"}
          </button>
        </form>
      </section>

      {/* Feedback */}
      {message && (
        <section className="panel">
          <p className="form-message" role="status">
            {message}
          </p>
        </section>
      )}

      {/* Savings Goal List */}
      <section className="panel">
        <h3>Your Savings Goals</h3>

        {savingsGoals.length === 0 ? (
          <p>No savings goals found.</p>
        ) : (
          <div className="savings-list">
            {savingsGoals.map((goal) => {
              const progressData = savingsProgress[goal.id];

              const progress =
                progressData?.progress_percentage ?? 0;

              const isEditing = editingId === goal.id;

              return (
                <div
                  className="savings-goal"
                  key={goal.id}
                >
                  {isEditing ? (
                    <form
                      className="expense-form"
                      onSubmit={handleSave}
                    >
                      <h3>Edit Savings Goal</h3>

                      <div className="form-group">
                        <label htmlFor={`edit-name-${goal.id}`}>
                          Goal Name
                        </label>
                        <input
                          id={`edit-name-${goal.id}`}
                          name="name"
                          type="text"
                          value={editForm.name}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`edit-target-${goal.id}`}>
                          Target Amount
                        </label>
                        <input
                          id={`edit-target-${goal.id}`}
                          name="target_amount"
                          type="number"
                          min="0.01"
                          step="0.01"
                          value={editForm.target_amount}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`edit-current-${goal.id}`}>
                          Already Saved
                        </label>
                        <input
                          id={`edit-current-${goal.id}`}
                          name="current_amount"
                          type="number"
                          min="0"
                          step="0.01"
                          value={editForm.current_amount}
                          onChange={handleEditChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`edit-date-${goal.id}`}>
                          Target Date
                        </label>
                        <input
                          id={`edit-date-${goal.id}`}
                          name="target_date"
                          type="date"
                          value={editForm.target_date}
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
                          {Number(
                            goal.current_amount
                          ).toLocaleString()}
                        </span>

                        <span>
                          Goal: $
                          {Number(
                            goal.target_amount
                          ).toLocaleString()}
                        </span>
                      </div>

                      {progressData && (
                        <p className="savings-remaining">
                          Remaining: $
                          {Number(
                            progressData.remaining_amount
                          ).toLocaleString()}
                        </p>
                      )}

                      <div className="transaction-actions">
                        <button
                          type="button"
                          onClick={() => startEditing(goal)}
                          disabled={deletingId !== null || saving}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() => handleDelete(goal.id)}
                          disabled={deletingId !== null || saving}
                        >
                          {deletingId === goal.id
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

export default Savings;

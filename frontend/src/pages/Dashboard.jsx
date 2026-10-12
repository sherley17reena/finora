import { useEffect, useState } from "react";

import {
  getFinancialProfile,
  updateFinancialProfile,
} from "../api/finoraApi";

const profileFields = [
  { name: "monthly_income", label: "Monthly Income" },
  { name: "rent", label: "Rent" },
  { name: "tuition", label: "Tuition" },
  { name: "groceries", label: "Groceries" },
  { name: "transport", label: "Transport" },
  { name: "utilities", label: "Utilities" },
  { name: "lifestyle_costs", label: "Lifestyle Costs" },
];

function Dashboard({ summary, onProfileUpdated }) {
  const [profile, setProfile] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getFinancialProfile();

        setProfile(data);
        setEditForm(data);
      } catch (error) {
        console.error("Error loading profile:", error);
        setMessage("Could not load financial profile.");
      }
    }

    loadProfile();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setEditForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function startEditing() {
    setEditForm({ ...profile });
    setMessage("");
    setIsEditing(true);
  }

  function cancelEditing() {
    setEditForm({ ...profile });
    setMessage("");
    setIsEditing(false);
  }

  async function handleSave(event) {
    event.preventDefault();

    setSaving(true);
    setMessage("");

    try {
      const updates = {};

      for (const field of profileFields) {
        updates[field.name] = Number(editForm[field.name]);
      }

      await updateFinancialProfile(updates);

      const updatedProfile = await getFinancialProfile();

      setProfile(updatedProfile);
      setEditForm(updatedProfile);

      if (onProfileUpdated) {
        await onProfileUpdated();
      }

      setIsEditing(false);
      setMessage("Financial profile updated successfully.");
    } catch (error) {
      console.error("Error updating profile:", error);
      setMessage("Could not update financial profile.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <header>
        <p className="welcome">Welcome back</p>

        <h2>Your Financial Dashboard</h2>

        <p className="subtitle">
          Track your money and understand your financial progress.
        </p>
      </header>

      <section className="cards">
        <div className="card">
          <p>Monthly Income</p>
          <h3>
            {summary
              ? `$${summary.monthly_income.toLocaleString()}`
              : "Loading..."}
          </h3>
        </div>

        <div className="card">
          <p>Available Income</p>
          <h3>
            {summary
              ? `$${summary.available_income.toLocaleString()}`
              : "Loading..."}
          </h3>
        </div>

        <div className="card">
          <p>Expenses This Month</p>
          <h3>
            {summary
              ? `$${summary.total_expenses.toLocaleString()}`
              : "Loading..."}
          </h3>
        </div>

        <div className="card">
          <p>Savings Goal</p>
          <h3>
            {summary
              ? `${summary.savings_progress}%`
              : "Loading..."}
          </h3>
        </div>
      </section>

      <section className="panel">
        <h3>Financial Profile</h3>

        <p className="subtitle">
          Manage your income and regular monthly expenses.
        </p>

        {!profile ? (
          <p>Profile not loaded.</p>
        ) : isEditing ? (
          <form className="expense-form" onSubmit={handleSave}>
            {profileFields.map((field) => (
              <div className="form-group" key={field.name}>
                <label htmlFor={field.name}>
                  {field.label}
                </label>

                <input
                  id={field.name}
                  name={field.name}
                  type="number"
                  min="0"
                  step="0.01"
                  value={editForm[field.name] ?? ""}
                  onChange={handleChange}
                  required
                />
              </div>
            ))}

            <div className="transaction-actions">
              <button type="submit" disabled={saving}>
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
            <div className="profile-details">
              {profileFields.map((field) => (
                <div className="profile-item" key={field.name}>
                  <span>{field.label}</span>
                  <strong>
                    ${Number(profile[field.name]).toLocaleString()}
                  </strong>
                </div>
              ))}
            </div>

            <button
              className="add-expense-button"
              type="button"
              onClick={startEditing}
            >
              Edit Financial Profile
            </button>
          </>
        )}

        {message && (
          <p className="form-message">{message}</p>
        )}
      </section>

      <section className="panel">
        <h3>Finora is ready</h3>

        <p>
          Your Expense, Savings, and Budget agents are connected
          through the Finance Coordinator.
        </p>
      </section>
    </>
  );
}

export default Dashboard;
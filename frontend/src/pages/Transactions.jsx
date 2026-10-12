import { useState } from "react";

function Transactions({
  transactions,
  expenseForm,
  message,
  onExpenseChange,
  onAddExpense,
  onUpdateTransaction,
  onDeleteTransaction,
}) {
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [saving, setSaving] = useState(false);

  function startEditing(transaction) {
    setEditingId(transaction.id);

    setEditForm({
      description: transaction.description,
      amount: transaction.amount,
      category: transaction.category,
      date: transaction.date,
      type: transaction.type,
    });
  }

  function handleEditChange(event) {
    const { name, value } = event.target;

    setEditForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSave(event) {
    event.preventDefault();
    setSaving(true);

    try {
      await onUpdateTransaction(editingId, {
        ...editForm,
        amount: Number(editForm.amount),
      });

      setEditingId(null);
    } catch (error) {
      console.error("Failed to update transaction:", error);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(transactionId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this transaction?"
    );

    if (!confirmed) return;

    try {
      await onDeleteTransaction(transactionId);
    } catch (error) {
      console.error("Failed to delete transaction:", error);
    }
  }

  return (
    <>
      <header>
        <p className="welcome">Expense Agent</p>
        <h2>Transactions</h2>
        <p className="subtitle">
          View and manage your financial transactions.
        </p>
      </header>

      <section className="panel">
        <h3>Add Expense</h3>

        <form className="expense-form" onSubmit={onAddExpense}>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <input
              id="description"
              name="description"
              type="text"
              placeholder="Coffee"
              value={expenseForm.description}
              onChange={onExpenseChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="amount">Amount</label>
            <input
              id="amount"
              name="amount"
              type="number"
              step="0.01"
              min="0.01"
              value={expenseForm.amount}
              onChange={onExpenseChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category</label>
            <input
              id="category"
              name="category"
              type="text"
              value={expenseForm.category}
              onChange={onExpenseChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">Date</label>
            <input
              id="date"
              name="date"
              type="date"
              value={expenseForm.date}
              onChange={onExpenseChange}
              required
            />
          </div>

          <button className="add-expense-button" type="submit">
            Add Expense
          </button>
        </form>
      </section>

      <section className="panel">
        <h3>Your Transactions</h3>

        {message && <p className="form-message">{message}</p>}

        {transactions.length === 0 ? (
          <p>No transactions found.</p>
        ) : (
          <div className="transaction-list">
            {transactions.map((transaction) => (
              <div className="transaction-row" key={transaction.id}>
                {editingId === transaction.id ? (
                  <form
                    className="expense-form"
                    onSubmit={handleSave}
                  >
                    <input
                      name="description"
                      value={editForm.description}
                      onChange={handleEditChange}
                      required
                    />

                    <input
                      name="amount"
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={editForm.amount}
                      onChange={handleEditChange}
                      required
                    />

                    <input
                      name="category"
                      value={editForm.category}
                      onChange={handleEditChange}
                      required
                    />

                    <input
                      name="date"
                      type="date"
                      value={editForm.date}
                      onChange={handleEditChange}
                      required
                    />

                    <div className="transaction-actions">
                      <button type="submit" disabled={saving}>
                        {saving ? "Saving..." : "Save"}
                      </button>

                      <button
                        type="button"
                        disabled={saving}
                        onClick={() => setEditingId(null)}
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                ) : (
                  <>
                    <div>
                      <strong>{transaction.description}</strong>
                      <p>
                        {transaction.date} · {transaction.category}
                      </p>
                    </div>

                    <strong>
                      ${Number(transaction.amount).toFixed(2)}
                    </strong>

                    <div className="transaction-actions">
                      <button
                        type="button"
                        onClick={() => startEditing(transaction)}
                      >
                        Edit
                      </button>

                      <button
                        type="button"
                        onClick={() => handleDelete(transaction.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default Transactions;
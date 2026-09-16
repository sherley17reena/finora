function Transactions({
  transactions,
  expenseForm,
  message,
  onExpenseChange,
  onAddExpense,
}) {
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

        <form
          className="expense-form"
          onSubmit={onAddExpense}
        >
          <div className="form-group">
            <label htmlFor="description">
              Description
            </label>

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
            <label htmlFor="amount">
              Amount
            </label>

            <input
              id="amount"
              name="amount"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="6.00"
              value={expenseForm.amount}
              onChange={onExpenseChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">
              Category
            </label>

            <input
              id="category"
              name="category"
              type="text"
              placeholder="Food"
              value={expenseForm.category}
              onChange={onExpenseChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">
              Date
            </label>

            <input
              id="date"
              name="date"
              type="date"
              value={expenseForm.date}
              onChange={onExpenseChange}
              required
            />
          </div>

          <button
            className="add-expense-button"
            type="submit"
          >
            Add Expense
          </button>
        </form>

        {message && (
          <p className="form-message">
            {message}
          </p>
        )}
      </section>

      <section className="panel">
        <h3>Your Transactions</h3>

        {transactions.length === 0 ? (
          <p>No transactions found.</p>
        ) : (
          <div className="transaction-list">
            {transactions.map((transaction) => (
              <div
                className="transaction-row"
                key={transaction.id}
              >
                <div>
                  <strong>
                    {transaction.description}
                  </strong>

                  <p>
                    {transaction.date} · {transaction.category}
                  </p>
                </div>

                <strong>
                  ${transaction.amount.toFixed(2)}
                </strong>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default Transactions;
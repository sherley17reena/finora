function Dashboard({ summary }) {
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
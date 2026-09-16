import ProgressBar from "../components/ProgressBar";

function Budgets({ budgets, budgetStatus }) {
  return (
    <>
      <header>
        <p className="welcome">Budget Agent</p>
        <h2>Budgets</h2>

        <p className="subtitle">
          Track your monthly spending limits and remaining budget.
        </p>
      </header>

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
                <div className="savings-goal" key={budget.id}>
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
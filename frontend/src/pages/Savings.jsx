import ProgressBar from "../components/ProgressBar";

function Savings({ savingsGoals, savingsProgress }) {
  return (
    <>
      <header>
        <p className="welcome">Savings Agent</p>
        <h2>Savings Goals</h2>
        <p className="subtitle">
          Track your savings progress and financial goals.
        </p>
      </header>

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

              return (
                <div className="savings-goal" key={goal.id}>
                  <div className="savings-goal-header">
                    <div>
                      <h3>{goal.name}</h3>
                      <p>Target date: {goal.target_date}</p>
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
                      Saved: ${goal.current_amount.toLocaleString()}
                    </span>

                    <span>
                      Goal: ${goal.target_amount.toLocaleString()}
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
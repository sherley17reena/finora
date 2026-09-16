function Assistant({
  savingsGoals,
  purchaseAmount,
  selectedGoalId,
  purchaseAnalysis,
  assistantLoading,
  assistantError,
  onPurchaseAmountChange,
  onGoalChange,
  onAnalyzePurchase,
}) {
  return (
    <>
      <header>
        <p className="welcome">Multi-Agent Analysis</p>
        <h2>Finora Assistant</h2>

        <p className="subtitle">
          See how a purchase could affect your finances
          and savings goals.
        </p>
      </header>

      <section className="panel">
        <h3>Can I afford this purchase?</h3>

        <form
          className="expense-form"
          onSubmit={onAnalyzePurchase}
        >
          <div className="form-group">
            <label htmlFor="purchaseAmount">
              Purchase Amount
            </label>

            <input
              id="purchaseAmount"
              type="number"
              min="0.01"
              step="0.01"
              placeholder="1000"
              value={purchaseAmount}
              onChange={onPurchaseAmountChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="savingsGoal">
              Savings Goal
            </label>

            <select
              id="savingsGoal"
              value={selectedGoalId}
              onChange={onGoalChange}
              required
            >
              <option value="">
                Select a savings goal
              </option>

              {savingsGoals.map((goal) => (
                <option key={goal.id} value={goal.id}>
                  {goal.name}
                </option>
              ))}
            </select>
          </div>

          <button
            className="add-expense-button"
            type="submit"
            disabled={assistantLoading}
          >
            {assistantLoading
              ? "Analyzing..."
              : "Analyze Purchase"}
          </button>
        </form>

        {assistantError && (
          <p className="form-message">
            {assistantError}
          </p>
        )}
      </section>

      {purchaseAnalysis?.status === "success" && (
        <section className="panel">
          <h3>Finora's Analysis</h3>

          <div className="assistant-result">
            <p>
              <strong>Purchase:</strong>{" "}
              $
              {purchaseAnalysis.purchase_analysis
                .purchase_amount
                .toLocaleString()}
            </p>

            <p>
              <strong>Available income:</strong>{" "}
              $
              {purchaseAnalysis.purchase_analysis
                .remaining_income
                .toLocaleString()}
            </p>

            <p>
              <strong>Money after purchase:</strong>{" "}
              $
              {purchaseAnalysis.purchase_analysis
                .money_after_purchase
                .toLocaleString()}
            </p>

            <p>
              <strong>Savings goal:</strong>{" "}
              {purchaseAnalysis.savings_analysis.name}
            </p>

            <p>
              <strong>Savings progress:</strong>{" "}
              {
                purchaseAnalysis.savings_analysis
                  .progress_percentage
              }
              %
            </p>

            <p>
              <strong>Still needed for goal:</strong>{" "}
              $
              {purchaseAnalysis.savings_analysis
                .remaining_amount
                .toLocaleString()}
            </p>
          </div>

          <div className="assistant-decision">
            <strong>Finora</strong>
            <p>{purchaseAnalysis.decision}</p>
          </div>

          <p>
            <strong>Agents used:</strong>{" "}
            {purchaseAnalysis.agents_used.join(" • ")}
          </p>
        </section>
      )}
    </>
  );
}

export default Assistant;
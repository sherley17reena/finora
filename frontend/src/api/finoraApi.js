const API_BASE_URL = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getDashboardSummary() {
  return request("/dashboard-summary");
}

export function getTransactions() {
  return request("/transactions");
}

export function createTransaction(transaction) {
  return request("/transactions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(transaction),
  });
}

export function getSavingsGoals() {
  return request("/savings-goals");
}

export function getSavingsProgress(goalId) {
  return request(`/savings-goals/${goalId}/progress`);
}

export function createSavingsGoal(goal) {
  return request("/savings-goals", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(goal),
  });
}

export function getBudgets() {
  return request("/budgets");
}

export function getBudgetStatus(budgetId) {
  return request(`/budgets/${budgetId}/status`);
}

export function analyzePurchase(purchaseAmount, goalId) {
  return request("/analyze-purchase", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      purchase_amount: Number(purchaseAmount),
      goal_id: Number(goalId),
    }),
  });
}

export function getAgentLogs() {
  return request("/agent-logs");
}

export function createBudget(budget) {
  return request("/budgets", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(budget),
  });
}
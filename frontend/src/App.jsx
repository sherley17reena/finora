import { useEffect, useState } from "react";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Savings from "./pages/Savings";
import Budgets from "./pages/Budgets";
import Assistant from "./pages/Assistant";
import AgentActivity from "./pages/AgentActivity";

import Sidebar from "./components/Sidebar";

function App() {
  const [summary, setSummary] = useState(null);
  const [activePage, setActivePage] = useState("dashboard");
  const [transactions, setTransactions] = useState([]);
  const [savingsGoals, setSavingsGoals] = useState([]);
  const [savingsProgress, setSavingsProgress] = useState({});
  const [budgets, setBudgets] = useState([]);
  const [budgetStatus, setBudgetStatus] = useState({});

  const [purchaseAmount, setPurchaseAmount] = useState("");
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [purchaseAnalysis, setPurchaseAnalysis] = useState(null);
  const [assistantLoading, setAssistantLoading] = useState(false);
  const [assistantError, setAssistantError] = useState("");

  const [expenseForm, setExpenseForm] = useState({
    description: "",
    amount: "",
    category: "",
    date: "",
  });

  const [message, setMessage] = useState("");

  const [agentLogs, setAgentLogs] = useState([]);

  const fetchAgentLogs = () => {
    fetch("http://127.0.0.1:8000/agent-logs")
      .then((response) => response.json())
      .then((data) => {
        setAgentLogs(data);
      })
      .catch((error) => {
        console.error("Error fetching agent logs:", error);
      });
  };

  // Fetch dashboard data
  const fetchDashboard = () => {
    fetch("http://127.0.0.1:8000/dashboard-summary")
      .then((response) => response.json())
      .then((data) => {
        setSummary(data);
      })
      .catch((error) => {
        console.error("Error fetching dashboard:", error);
      });
  };

  // Fetch transaction data
  const fetchTransactions = () => {
    fetch("http://127.0.0.1:8000/transactions")
      .then((response) => response.json())
      .then((data) => {
        setTransactions(data);
      })
      .catch((error) => {
        console.error("Error fetching transactions:", error);
      });
  };

  // Fetch savings goals and Savings Agent calculations
  const fetchSavingsGoals = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/savings-goals"
      );

      const goals = await response.json();

      setSavingsGoals(goals);

      const progressResults = {};

      for (const goal of goals) {
        const progressResponse = await fetch(
          `http://127.0.0.1:8000/savings-goals/${goal.id}/progress`
        );

        const progressData = await progressResponse.json();

        if (progressData.status === "success") {
          progressResults[goal.id] = progressData.data;
        }
      }

      setSavingsProgress(progressResults);
    } catch (error) {
      console.error("Error fetching savings goals:", error);
    }
  };

  // Fetch budgets and Budget Agent calculations
  const fetchBudgets = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/budgets"
      );

      const budgetData = await response.json();

      setBudgets(budgetData);

      const statusResults = {};

      for (const budget of budgetData) {
        const statusResponse = await fetch(
          `http://127.0.0.1:8000/budgets/${budget.id}/status`
        );

        const statusData = await statusResponse.json();

        if (statusData.status === "success") {
          statusResults[budget.id] = statusData.data;
        }
      }

      setBudgetStatus(statusResults);
    } catch (error) {
      console.error("Error fetching budgets:", error);
    }
  };

  useEffect(() => {
    fetchDashboard();
    fetchTransactions();
    fetchSavingsGoals();
    fetchBudgets();
    fetchAgentLogs();
  }, []);

  // Update expense form fields
  const handleExpenseChange = (event) => {
    const { name, value } = event.target;

    setExpenseForm((previousForm) => ({
      ...previousForm,
      [name]: value,
    }));
  };

  // Add a new expense
  const handleAddExpense = async (event) => {
    event.preventDefault();

    setMessage("");

    const newExpense = {
      date: expenseForm.date,
      description: expenseForm.description,
      amount: Number(expenseForm.amount),
      category: expenseForm.category,
      type: "expense",
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/transactions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newExpense),
        }
      );

      if (!response.ok) {
        throw new Error("Could not add expense");
      }

      setExpenseForm({
        description: "",
        amount: "",
        category: "",
        date: "",
      });

      setMessage("Expense added successfully.");

      fetchTransactions();
      fetchDashboard();
      fetchBudgets();
      
    } catch (error) {
      console.error("Error adding expense:", error);
      setMessage("Could not add expense. Please try again.");
    }
  };
  const handleAnalyzePurchase = async (event) => {
  event.preventDefault();

  setAssistantLoading(true);
  setAssistantError("");
  setPurchaseAnalysis(null);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/analyze-purchase",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          purchase_amount: Number(purchaseAmount),
          goal_id: Number(selectedGoalId),
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Could not analyze purchase");
    }

    const data = await response.json();

      setPurchaseAnalysis(data);
    } catch (error) {
      console.error("Error analyzing purchase:", error);

      setAssistantError(
        "Could not analyze the purchase. Please try again."
      );
    } finally {
      setAssistantLoading(false);
    }
  };
  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        onPageChange={(page) => {
          setActivePage(page);

          if (page === "activity") {
            fetchAgentLogs();
          }
        }}
      />

      <main className="main-content">

        {activePage === "dashboard" && (
          <Dashboard summary={summary} />
        )}

        {activePage === "transactions" && (
          <Transactions
            transactions={transactions}
            expenseForm={expenseForm}
            message={message}
            onExpenseChange={handleExpenseChange}
            onAddExpense={handleAddExpense}
          />
        )}

       {activePage === "savings" && (
          <Savings
            savingsGoals={savingsGoals}
            savingsProgress={savingsProgress}
            onGoalsUpdated={async () => {
              await fetchSavingsGoals();
              fetchDashboard();
            }}
          />
        )}

        {activePage === "budgets" && (
          <Budgets
            budgets={budgets}
            budgetStatus={budgetStatus}
            onBudgetsUpdated={fetchBudgets}
          />
        )}
        {activePage === "assistant" && (
          <Assistant
            savingsGoals={savingsGoals}
            purchaseAmount={purchaseAmount}
            selectedGoalId={selectedGoalId}
            purchaseAnalysis={purchaseAnalysis}
            assistantLoading={assistantLoading}
            assistantError={assistantError}
            onPurchaseAmountChange={(event) =>
              setPurchaseAmount(event.target.value)
            }
            onGoalChange={(event) =>
              setSelectedGoalId(event.target.value)
            }
            onAnalyzePurchase={handleAnalyzePurchase}
          />
        )}

        {activePage === "activity" && (
          <AgentActivity
            agentLogs={agentLogs}
            onRefresh={fetchAgentLogs}
          />
        )}
      </main>
    </div>
  );
}

export default App;
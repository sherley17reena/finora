import { useEffect, useState } from "react";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Savings from "./pages/Savings";
import Budgets from "./pages/Budgets";
import Assistant from "./pages/Assistant";
import AgentActivity from "./pages/AgentActivity";

import Sidebar from "./components/Sidebar";

import {
  updateTransaction,
  deleteTransaction,
} from "./api/finoraApi";

function App() {
  const [summary, setSummary] = useState(null);
  const [activePage, setActivePage] = useState("dashboard");

  const [transactions, setTransactions] = useState([]);

  const [savingsGoals, setSavingsGoals] = useState([]);
  const [savingsProgress, setSavingsProgress] = useState({});

  const [budgets, setBudgets] = useState([]);
  const [budgetStatus, setBudgetStatus] = useState({});

  const [agentLogs, setAgentLogs] = useState([]);

  const [expenseForm, setExpenseForm] = useState({
    description: "",
    amount: "",
    category: "",
    date: "",
  });

  const [message, setMessage] = useState("");

  
  // -----------------------------
  // Agent Activity
  // -----------------------------

  const fetchAgentLogs = () => {
    fetch("http://127.0.0.1:8000/agent-logs")
      .then((response) => response.json())
      .then((data) => {
        setAgentLogs(data);
      })
      .catch((error) => {
        console.error(
          "Error fetching agent logs:",
          error
        );
      });
  };


  // -----------------------------
  // Dashboard
  // -----------------------------

  const fetchDashboard = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/dashboard-summary"
      );

      if (!response.ok) {
        throw new Error("Could not fetch dashboard");
      }

      const data = await response.json();
      setSummary(data);
    } catch (error) {
      console.error("Error fetching dashboard:", error);
      throw error;
    }
};


  // -----------------------------
  // Transactions
  // -----------------------------

  const fetchTransactions = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/transactions"
      );

      if (!response.ok) {
        throw new Error("Could not fetch transactions");
      }

      const data = await response.json();
      setTransactions(data);
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error;
    }
  };


  // -----------------------------
  // Savings
  // -----------------------------

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

        const progressData =
          await progressResponse.json();

        if (progressData.status === "success") {
          progressResults[goal.id] =
            progressData.data;
        }
      }

      setSavingsProgress(progressResults);
    } catch (error) {
      console.error(
        "Error fetching savings goals:",
        error
      );
    }
  };


  // -----------------------------
  // Budgets
  // -----------------------------

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

        const statusData =
          await statusResponse.json();

        if (statusData.status === "success") {
          statusResults[budget.id] =
            statusData.data;
        }
      }

      setBudgetStatus(statusResults);
    } catch (error) {
      console.error(
        "Error fetching budgets:",
        error
      );
    }
  };


  // -----------------------------
  // Initial Data Load
  // -----------------------------

  useEffect(() => {
    fetchDashboard();
    fetchTransactions();
    fetchSavingsGoals();
    fetchBudgets();
    fetchAgentLogs();
  }, []);


  // -----------------------------
  // Expense Form
  // -----------------------------

  const handleExpenseChange = (event) => {
    const { name, value } = event.target;

    setExpenseForm((previousForm) => ({
      ...previousForm,
      [name]: value,
    }));
  };


  // -----------------------------
  // Add Expense
  // -----------------------------

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
        throw new Error(
          "Could not add expense"
        );
      }

      setExpenseForm({
        description: "",
        amount: "",
        category: "",
        date: "",
      });

      setMessage(
        "Expense added successfully."
      );

      // Refresh affected financial data
      fetchTransactions();
      fetchDashboard();
      fetchBudgets();

    } catch (error) {
      console.error(
        "Error adding expense:",
        error
      );

      setMessage(
        "Could not add expense. Please try again."
      );
    }
  };

  // -----------------------------
  // Update Transaction
  // -----------------------------

  const handleUpdateTransaction = async (transactionId, updates) => {
   setMessage("");

  try {
    await updateTransaction(transactionId, updates);

    setMessage("Transaction updated successfully.");

    // Refresh financial information
    await Promise.all([
      fetchTransactions(),
      fetchDashboard(),
      fetchBudgets(),
    ]);

  } catch (error) {
    console.error("Error updating transaction:", error);

    setMessage("Could not update transaction. Please try again.");

    throw error;
  }
};


  // -----------------------------
  // Delete Transaction
  // -----------------------------

  const handleDeleteTransaction = async (transactionId) => {
    setMessage("");

    try {
      await deleteTransaction(transactionId);

      setMessage("Transaction deleted successfully.");

      // Refresh financial information
      await Promise.all([
        fetchTransactions(),
        fetchDashboard(),
        fetchBudgets(),
      ]);

    } catch (error) {
      console.error("Error deleting transaction:", error);

      setMessage("Could not delete transaction. Please try again.");

      throw error;
    }
  };

  // -----------------------------
  // Refresh after AI changes data
  // -----------------------------

  const handleAssistantDataChange = () => {
    fetchTransactions();
    fetchDashboard();
    fetchSavingsGoals();
    fetchBudgets();
    fetchAgentLogs();
  };


  // -----------------------------
  // Application
  // -----------------------------

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
          <Dashboard
            summary={summary}
            onProfileUpdated={fetchDashboard}
          />
        )}


        {activePage === "transactions" && (
          <Transactions
            transactions={transactions}
            expenseForm={expenseForm}
            message={message}
            onExpenseChange={
              handleExpenseChange
            }
            onAddExpense={
              handleAddExpense
            }
            onUpdateTransaction={handleUpdateTransaction}
            onDeleteTransaction={handleDeleteTransaction}
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
            onBudgetsUpdated={
              fetchBudgets
            }
          />
        )}


        {activePage === "assistant" && (
          <Assistant
            onDataChanged={
              handleAssistantDataChange
            }
          />
        )}


        {activePage === "activity" && (
          <AgentActivity
            agentLogs={agentLogs}
            onRefresh={
              fetchAgentLogs
            }
          />
        )}

      </main>
    </div>
  );
}


export default App;
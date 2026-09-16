function Sidebar({ activePage, onPageChange }) {
  const navigation = [
    { id: "dashboard", label: "Dashboard" },
    { id: "transactions", label: "Transactions" },
    { id: "savings", label: "Savings" },
    { id: "budgets", label: "Budgets" },
    { id: "assistant", label: "Finora Assistant" },
    { id: "activity", label: "Agent Activity" },
  ];

  return (
    <aside className="sidebar">
      <h1>Finora</h1>

      <p className="tagline">
        Your personal finance assistant
      </p>

      <nav>
        {navigation.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => onPageChange(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
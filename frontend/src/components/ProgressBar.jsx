function ProgressBar({ value }) {
  const safeValue = Math.min(Math.max(value ?? 0, 0), 100);

  return (
    <div className="progress-bar">
      <div
        className="progress-fill"
        style={{
          width: `${safeValue}%`,
        }}
      />
    </div>
  );
}

export default ProgressBar;
function StatusBadge({ status }) {
  const styles = {
    PENDING: "bg-slate-100 text-slate-700 ring-slate-200",
    CALL_INITIATED: "bg-blue-100 text-blue-700 ring-blue-200",
    IN_PROGRESS: "bg-cyan-100 text-cyan-700 ring-cyan-200",
    QUALIFIED: "bg-emerald-100 text-emerald-700 ring-emerald-200",
    NOT_INTERESTED: "bg-rose-100 text-rose-700 ring-rose-200",
    CALLBACK_REQUESTED: "bg-amber-100 text-amber-800 ring-amber-200",
    NEEDS_REVIEW: "bg-violet-100 text-violet-700 ring-violet-200",
    FAILED: "bg-red-900 text-white ring-red-900"
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold ring-1 ${
        styles[status] || "bg-slate-100 text-slate-700 ring-slate-200"
      }`}
    >
      {status || "UNKNOWN"}
    </span>
  );
}

export default StatusBadge;
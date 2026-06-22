import { useMemo, useState } from "react";
import StatusBadge from "./StatusBadge";

function CallLogs({ logs }) {
  const [statusFilter, setStatusFilter] = useState("ALL");

  const statuses = useMemo(() => {
    const unique = new Set(logs.map((log) => log.status).filter(Boolean));
    return ["ALL", ...Array.from(unique)];
  }, [logs]);

  const filteredLogs = logs.filter((log) => {
    return statusFilter === "ALL" || log.status === statusFilter;
  });

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h3 className="text-xl font-black text-slate-950">Call Logs</h3>
          <p className="mt-1 text-sm text-slate-500">
            Saved transcripts, AI result, reason, and confidence score.
          </p>
        </div>

        <select
          className="rounded-2xl border border-slate-300 px-4 py-3 text-sm font-semibold outline-none focus:ring-2 focus:ring-blue-500"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>

      {filteredLogs.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 p-8 text-center">
          <p className="text-3xl">📝</p>
          <p className="mt-2 font-bold text-slate-700">No call logs found</p>
          <p className="text-sm text-slate-500">Webhook results will appear here.</p>
        </div>
      )}

      <div className="space-y-4">
        {filteredLogs.map((log, index) => (
          <div key={log._id || index} className="rounded-2xl border border-slate-200 p-5">
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div>
                <p className="font-black text-slate-900">Lead ID: {log.lead_id}</p>
                <p className="mt-1 text-xs text-slate-500">
                  {log.created_at || "No timestamp"}
                </p>
              </div>

              <StatusBadge status={log.status} />
            </div>

            <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2">
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-xs font-black uppercase text-slate-500">Reason</p>
                <p className="mt-1 text-sm text-slate-700">{log.reason || "-"}</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-xs font-black uppercase text-slate-500">Confidence</p>
                <p className="mt-1 text-sm font-bold text-slate-700">
                  {log.confidence ?? "-"}
                </p>
              </div>
            </div>

            <div className="mt-4 rounded-2xl bg-slate-950 p-4 text-sm leading-6 text-slate-100">
              <p className="mb-2 text-xs font-black uppercase tracking-wider text-slate-400">
                Transcript
              </p>
              {log.transcript || "-"}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default CallLogs;
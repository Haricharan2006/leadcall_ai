import { useMemo, useState } from "react";
import StatusBadge from "./StatusBadge";

function LeadTable({ leads, onResetLead }) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");

  const statuses = useMemo(() => {
    const unique = new Set(leads.map((lead) => lead.status).filter(Boolean));
    return ["ALL", ...Array.from(unique)];
  }, [leads]);

  const filteredLeads = useMemo(() => {
    return leads.filter((lead) => {
      const searchText = `${lead.name} ${lead.phone} ${lead.status} ${lead.location || ""}`
        .toLowerCase();

      const matchesSearch = searchText.includes(search.toLowerCase());
      const matchesStatus =
        statusFilter === "ALL" || lead.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [leads, search, statusFilter]);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <h3 className="text-xl font-black text-slate-950">Lead Directory</h3>
          <p className="mt-1 text-sm text-slate-500">
            Search, filter, and track all tenant leads.
          </p>
        </div>

        <div className="flex flex-col gap-3 md:flex-row">
          <input
            className="rounded-2xl border border-slate-300 px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search leads..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

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
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200">
        <table className="w-full min-w-[950px] border-collapse text-sm">
          <thead>
            <tr className="bg-slate-100 text-left text-xs font-black uppercase tracking-wider text-slate-500">
              <th className="px-4 py-4">Lead</th>
              <th className="px-4 py-4">Phone</th>
              <th className="px-4 py-4">Status</th>
              <th className="px-4 py-4">Budget</th>
              <th className="px-4 py-4">Location</th>
              <th className="px-4 py-4">Timeline</th>
              <th className="px-4 py-4">Attempts</th>
              <th className="px-4 py-4">Action</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-200">
            {filteredLeads.map((lead) => (
              <tr key={lead.lead_id} className="hover:bg-slate-50">
                <td className="px-4 py-4">
                  <p className="font-black text-slate-900">{lead.name}</p>
                  <p className="text-xs text-slate-500">{lead.lead_id}</p>
                </td>

                <td className="px-4 py-4 font-medium text-slate-700">
                  {lead.phone}
                </td>

                <td className="px-4 py-4">
                  <StatusBadge status={lead.status} />
                </td>

                <td className="px-4 py-4 text-slate-700">{lead.budget || "-"}</td>
                <td className="px-4 py-4 text-slate-700">{lead.location || "-"}</td>
                <td className="px-4 py-4 text-slate-700">{lead.timeline || "-"}</td>
                <td className="px-4 py-4 text-slate-700">{lead.attempt_count || 0}</td>

                <td className="px-4 py-4">
                  <button
                    onClick={() => onResetLead(lead.lead_id)}
                    className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-700"
                  >
                    Reset
                  </button>
                </td>
              </tr>
            ))}

            {filteredLeads.length === 0 && (
              <tr>
                <td colSpan="8" className="px-4 py-10 text-center text-slate-500">
                  No leads found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default LeadTable;
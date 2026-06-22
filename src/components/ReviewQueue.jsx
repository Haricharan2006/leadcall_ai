import StatusBadge from "./StatusBadge";

function ReviewQueue({ leads, onResetLead }) {
  const reviewLeads = leads.filter((lead) => lead.status === "NEEDS_REVIEW");

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h3 className="text-xl font-black text-slate-950">Human Review Queue</h3>
          <p className="mt-1 text-sm text-slate-500">
            Low-confidence or unclear AI outcomes appear here.
          </p>
        </div>

        <div className="rounded-2xl bg-violet-100 px-4 py-2 text-sm font-black text-violet-700">
          {reviewLeads.length}
        </div>
      </div>

      {reviewLeads.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 p-8 text-center">
          <p className="text-3xl">✅</p>
          <p className="mt-2 font-bold text-slate-700">No leads need review</p>
          <p className="text-sm text-slate-500">AI workflow is currently clean.</p>
        </div>
      )}

      <div className="space-y-4">
        {reviewLeads.map((lead) => (
          <div key={lead.lead_id} className="rounded-2xl border border-slate-200 p-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="font-black text-slate-900">{lead.name}</p>
                <p className="text-sm text-slate-500">{lead.phone}</p>
                <p className="mt-1 text-xs text-slate-400">{lead.lead_id}</p>
              </div>

              <div className="flex items-center gap-3">
                <StatusBadge status={lead.status} />

                <button
                  onClick={() => onResetLead(lead.lead_id)}
                  className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-700"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ReviewQueue;
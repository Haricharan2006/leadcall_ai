function Header({
  companies,
  selectedCompany,
  onCompanyChange,
  onRefresh,
  onStartCampaign,
  campaignLoading,
  lastUpdated,
  error
}) {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 px-5 py-4 backdrop-blur lg:px-8">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-blue-600">
            Multi-Tenant SaaS Dashboard
          </p>
          <h2 className="mt-1 text-2xl font-black text-slate-950">
            Agentic Voice Lead Qualification
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Live tenant leads, AI call outcomes, human review queue, and webhook logs.
          </p>
        </div>

        <div className="flex flex-col gap-3 md:flex-row md:items-center">
          <select
            className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold outline-none focus:ring-2 focus:ring-blue-500"
            value={selectedCompany}
            onChange={(e) => onCompanyChange(e.target.value)}
          >
            {companies.map((company) => (
              <option key={company.company_id} value={company.company_id}>
                {company.name}
              </option>
            ))}
          </select>

          <button
            onClick={onRefresh}
            className="rounded-2xl border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700 hover:bg-slate-100"
          >
            Refresh
          </button>

          <button
            onClick={onStartCampaign}
            disabled={campaignLoading}
            className="rounded-2xl bg-blue-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-blue-200 hover:bg-blue-700 disabled:bg-blue-300"
          >
            {campaignLoading ? "Starting..." : "Start Campaign"}
          </button>
        </div>
      </div>

      <div className="mt-3 flex flex-col gap-2 text-xs md:flex-row md:items-center md:justify-between">
        <p className="text-slate-500">
          Last updated: <span className="font-semibold">{lastUpdated || "Not loaded yet"}</span>
        </p>

        {error && (
          <p className="rounded-full bg-rose-100 px-3 py-1 font-semibold text-rose-700">
            {error}
          </p>
        )}
      </div>
    </header>
  );
}

export default Header;
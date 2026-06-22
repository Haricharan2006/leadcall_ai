import { useEffect, useMemo, useState } from "react";
import {
  addLead,
  getAnalytics,
  getCallLogs,
  getCompanies,
  getLeads,
  resetLead,
  startCampaign
} from "./api";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatCard from "./components/StatCard";
import AddLeadForm from "./components/AddLeadForm";
import LeadTable from "./components/LeadTable";
import ReviewQueue from "./components/ReviewQueue";
import CallLogs from "./components/CallLogs";
import StatusBadge from "./components/StatusBadge";

function App() {
  const [activeSection, setActiveSection] = useState("overview");
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [leads, setLeads] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [logs, setLogs] = useState([]);
  const [initialLoading, setInitialLoading] = useState(true);
  const [campaignLoading, setCampaignLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");

  const selectedCompanyData = useMemo(() => {
    return companies.find((company) => company.company_id === selectedCompany);
  }, [companies, selectedCompany]);

  const qualifiedRate = useMemo(() => {
    const total = analytics?.total_leads || 0;
    const qualified = analytics?.qualified || 0;

    if (total === 0) return 0;

    return Math.round((qualified / total) * 100);
  }, [analytics]);

  async function loadCompanies() {
    try {
      setError("");

      const data = await getCompanies();
      const list = Array.isArray(data) ? data : [];

      setCompanies(list);

      if (list.length > 0 && !selectedCompany) {
        setSelectedCompany(list[0].company_id);
      }
    } catch (err) {
      console.error(err);
      setError("Backend not connected. Start FastAPI server.");
    } finally {
      setInitialLoading(false);
    }
  }

  async function loadDashboard(companyId = selectedCompany) {
    if (!companyId) return;

    try {
      setError("");

      const [leadsData, analyticsData, logsData] = await Promise.all([
        getLeads(companyId),
        getAnalytics(companyId),
        getCallLogs(companyId)
      ]);

      setLeads(Array.isArray(leadsData) ? leadsData : []);
      setAnalytics(analyticsData || {});
      setLogs(Array.isArray(logsData) ? [...logsData].reverse() : []);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      console.error(err);
      setError("Dashboard refresh failed. Check backend terminal.");
    }
  }

  async function handleAddLead(payload) {
    try {
      setError("");
      await addLead(payload);
      await loadDashboard();
    } catch (err) {
      console.error(err);
      alert("Lead add failed. Check backend.");
    }
  }

  async function handleResetLead(leadId) {
    try {
      setError("");
      await resetLead(leadId);
      await loadDashboard();
    } catch (err) {
      console.error(err);
      alert("Lead reset failed.");
    }
  }

  async function handleStartCampaign() {
    const ok = confirm(
      "Start campaign only after adding real Vapi API keys in backend .env. Continue?"
    );

    if (!ok) return;

    setCampaignLoading(true);

    try {
      setError("");
      const result = await startCampaign(selectedCompany);
      alert(result.message || "Campaign processed.");
      await loadDashboard();
    } catch (err) {
      console.error(err);
      alert("Campaign failed. Add Vapi keys or check backend terminal.");
    } finally {
      setCampaignLoading(false);
    }
  }

  useEffect(() => {
    loadCompanies();
  }, []);

  useEffect(() => {
    if (selectedCompany) {
      loadDashboard(selectedCompany);
    }
  }, [selectedCompany]);

  useEffect(() => {
    const timer = setInterval(() => {
      if (selectedCompany) {
        loadDashboard(selectedCompany);
      }
    }, 5000);

    return () => clearInterval(timer);
  }, [selectedCompany]);

  if (initialLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100">
        <div className="rounded-3xl bg-white p-8 text-center shadow-xl">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600"></div>
          <h1 className="mt-5 text-xl font-black text-slate-900">Loading LeadCall AI</h1>
          <p className="mt-1 text-sm text-slate-500">Connecting to FastAPI backend...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        companyName={selectedCompanyData?.name}
      />

      <div className="min-w-0 flex-1">
        <Header
          companies={companies}
          selectedCompany={selectedCompany}
          onCompanyChange={setSelectedCompany}
          onRefresh={() => loadDashboard()}
          onStartCampaign={handleStartCampaign}
          campaignLoading={campaignLoading}
          lastUpdated={lastUpdated}
          error={error}
        />

        <main className="space-y-6 p-5 lg:p-8">
          {activeSection === "overview" && (
            <>
              <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <StatCard
                  title="Total Leads"
                  value={analytics?.total_leads ?? 0}
                  subtitle="All leads under selected tenant"
                  tone="dark"
                />
                <StatCard
                  title="Qualified"
                  value={analytics?.qualified ?? 0}
                  subtitle={`${qualifiedRate}% qualification rate`}
                  tone="green"
                />
                <StatCard
                  title="Callbacks"
                  value={analytics?.callback_requested ?? 0}
                  subtitle="Customers asked for later call"
                  tone="amber"
                />
                <StatCard
                  title="Needs Review"
                  value={analytics?.needs_review ?? 0}
                  subtitle="Human-in-loop required"
                  tone="violet"
                />
              </section>

              <section className="grid grid-cols-1 gap-4 xl:grid-cols-4">
                <StatCard title="Pending" value={analytics?.pending ?? 0} tone="blue" />
                <StatCard title="Calls Started" value={analytics?.call_initiated ?? 0} tone="dark" />
                <StatCard title="Not Interested" value={analytics?.not_interested ?? 0} tone="red" />
                <StatCard title="Failed" value={analytics?.failed ?? 0} tone="red" />
              </section>

              <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-xl font-black text-slate-950">Recent Leads</h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Latest tenant lead statuses.
                  </p>

                  <div className="mt-5 space-y-3">
                    {leads.slice(0, 5).map((lead) => (
                      <div
                        key={lead.lead_id}
                        className="flex items-center justify-between rounded-2xl border border-slate-200 p-4"
                      >
                        <div>
                          <p className="font-black text-slate-900">{lead.name}</p>
                          <p className="text-sm text-slate-500">{lead.phone}</p>
                        </div>

                        <StatusBadge status={lead.status} />
                      </div>
                    ))}

                    {leads.length === 0 && (
                      <p className="rounded-2xl border border-dashed border-slate-300 p-6 text-center text-slate-500">
                        No leads found.
                      </p>
                    )}
                  </div>
                </div>

                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-xl font-black text-slate-950">System Health</h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Backend, database, workflow, and webhook readiness.
                  </p>

                  <div className="mt-5 grid grid-cols-1 gap-3">
                    <div className="rounded-2xl bg-emerald-50 p-4">
                      <p className="font-black text-emerald-700">MongoDB Atlas Connected</p>
                      <p className="text-sm text-emerald-600">Lead and call-log data is live.</p>
                    </div>

                    <div className="rounded-2xl bg-blue-50 p-4">
                      <p className="font-black text-blue-700">FastAPI Backend Running</p>
                      <p className="text-sm text-blue-600">Swagger APIs are active.</p>
                    </div>

                    <div className="rounded-2xl bg-violet-50 p-4">
                      <p className="font-black text-violet-700">LangGraph Workflow Enabled</p>
                      <p className="text-sm text-violet-600">
                        Transcript evaluation updates lead status.
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            </>
          )}

          {activeSection === "leads" && (
            <>
              <AddLeadForm companyId={selectedCompany} onAddLead={handleAddLead} />
              <LeadTable leads={leads} onResetLead={handleResetLead} />
            </>
          )}

          {activeSection === "campaign" && (
            <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <p className="text-xs font-bold uppercase tracking-widest text-blue-600">
                Campaign Control Center
              </p>

              <h3 className="mt-2 text-3xl font-black text-slate-950">
                Outbound AI Calling Campaign
              </h3>

              <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-500">
                This starts calls for all PENDING leads of the selected tenant.
                Vapi calls customers, webhook receives transcript, LangGraph evaluates the result,
                and MongoDB updates each lead automatically.
              </p>

              <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-slate-100 p-5">
                  <p className="text-sm text-slate-500">Selected Tenant</p>
                  <p className="mt-1 font-black text-slate-900">
                    {selectedCompanyData?.name || "-"}
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-100 p-5">
                  <p className="text-sm text-slate-500">Pending Leads</p>
                  <p className="mt-1 font-black text-slate-900">
                    {analytics?.pending ?? 0}
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-100 p-5">
                  <p className="text-sm text-slate-500">Webhook Logs</p>
                  <p className="mt-1 font-black text-slate-900">{logs.length}</p>
                </div>
              </div>

              <button
                onClick={handleStartCampaign}
                disabled={campaignLoading}
                className="mt-8 rounded-2xl bg-blue-600 px-8 py-4 text-sm font-black text-white shadow-lg shadow-blue-200 hover:bg-blue-700 disabled:bg-blue-300"
              >
                {campaignLoading ? "Starting Campaign..." : "Start Outbound Campaign"}
              </button>

              <p className="mt-4 rounded-2xl bg-amber-50 p-4 text-sm font-semibold text-amber-800">
                Use this only after adding real Vapi keys in backend .env.
              </p>
            </section>
          )}

          {activeSection === "review" && (
            <ReviewQueue leads={leads} onResetLead={handleResetLead} />
          )}

          {activeSection === "logs" && <CallLogs logs={logs} />}
        </main>
      </div>
    </div>
  );
}

export default App;
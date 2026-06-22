const items = [
  { id: "overview", label: "Overview", icon: "📊" },
  { id: "leads", label: "Lead Directory", icon: "👥" },
  { id: "campaign", label: "Campaigns", icon: "📞" },
  { id: "review", label: "Human Review", icon: "🧠" },
  { id: "logs", label: "Call Logs", icon: "📝" }
];

function Sidebar({ activeSection, onSectionChange, companyName }) {
  return (
    <aside className="hidden min-h-screen w-72 shrink-0 bg-slate-950 text-white lg:block">
      <div className="border-b border-white/10 px-7 py-6">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 text-xl font-black">
            AI
          </div>

          <div>
            <h1 className="text-xl font-black tracking-tight">LeadCall AI</h1>
            <p className="text-xs text-slate-400">Voice Orchestrator</p>
          </div>
        </div>
      </div>

      <div className="px-5 py-6">
        <p className="mb-3 px-3 text-xs font-bold uppercase tracking-widest text-slate-500">
          Workspace
        </p>

        <div className="mb-6 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs text-slate-400">Current Tenant</p>
          <p className="mt-1 text-sm font-bold">{companyName || "Loading..."}</p>
        </div>

        <nav className="space-y-2">
          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => onSectionChange(item.id)}
              className={`flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-semibold transition ${
                activeSection === item.id
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-950/40"
                  : "text-slate-300 hover:bg-white/10 hover:text-white"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="absolute bottom-6 w-72 px-5">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-sm font-bold">Advanced Stack</p>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            FastAPI · MongoDB Atlas · LangGraph · Vapi · React · Tailwind
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
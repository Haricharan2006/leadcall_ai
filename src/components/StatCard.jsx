function StatCard({ title, value, subtitle, tone = "dark" }) {
  const tones = {
    dark: "from-slate-950 to-slate-800 text-white",
    blue: "from-blue-700 to-blue-500 text-white",
    green: "from-emerald-700 to-emerald-500 text-white",
    amber: "from-amber-600 to-orange-500 text-white",
    red: "from-rose-700 to-red-500 text-white",
    violet: "from-violet-700 to-purple-500 text-white"
  };

  return (
    <div className={`rounded-3xl bg-gradient-to-br ${tones[tone]} p-5 shadow-lg`}>
      <p className="text-sm font-medium opacity-80">{title}</p>
      <h2 className="mt-3 text-4xl font-black tracking-tight">{value}</h2>
      <p className="mt-2 text-xs opacity-75">{subtitle || "Live system metric"}</p>
    </div>
  );
}

export default StatCard;
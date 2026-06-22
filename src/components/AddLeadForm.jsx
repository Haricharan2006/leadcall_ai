import { useState } from "react";

function AddLeadForm({ companyId, onAddLead }) {
  const [form, setForm] = useState({
    name: "",
    phone: ""
  });

  const [saving, setSaving] = useState(false);

  function updateField(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value
    }));
  }

  async function submitForm(e) {
    e.preventDefault();

    if (!form.name.trim() || !form.phone.trim()) {
      alert("Enter customer name and phone number.");
      return;
    }

    setSaving(true);

    try {
      await onAddLead({
        company_id: companyId,
        name: form.name.trim(),
        phone: form.phone.trim()
      });

      setForm({
        name: "",
        phone: ""
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h3 className="text-xl font-black text-slate-950">Add New Lead</h3>
        <p className="mt-1 text-sm text-slate-500">
          Add a customer to the selected tenant. Lead starts with PENDING status.
        </p>
      </div>

      <form onSubmit={submitForm} className="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <input
          className="rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Customer name"
          value={form.name}
          onChange={(e) => updateField("name", e.target.value)}
        />

        <input
          className="rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="+91 phone number"
          value={form.phone}
          onChange={(e) => updateField("phone", e.target.value)}
        />

        <button
          disabled={saving}
          className="rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-100 hover:bg-emerald-700 disabled:bg-emerald-300"
        >
          {saving ? "Adding..." : "Add Lead"}
        </button>
      </form>
    </section>
  );
}

export default AddLeadForm;
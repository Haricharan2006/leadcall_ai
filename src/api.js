const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const contentType = response.headers.get("content-type");
  const data = contentType?.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    throw new Error(
      typeof data === "string"
        ? data
        : data.detail || data.message || "API request failed"
    );
  }

  return data;
}

export function getCompanies() {
  return request("/api/companies");
}

export function getLeads(companyId) {
  return request(`/api/leads/${companyId}`);
}

export function getAnalytics(companyId) {
  return request(`/api/analytics/${companyId}`);
}

export function getCallLogs(companyId) {
  return request(`/api/call-logs/${companyId}`);
}

export function addLead(payload) {
  return request("/api/leads", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function resetLead(leadId) {
  return request(`/api/leads/${leadId}/reset`, {
    method: "PATCH"
  });
}

export function startCampaign(companyId) {
  return request(`/api/campaigns/start/${companyId}`, {
    method: "POST"
  });
}
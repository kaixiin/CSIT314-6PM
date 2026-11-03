// api.js
// Backend data loaders: every GET that fills the shared state in state.js.
// Loads after state.js and before ui.js.

// NOTE for the backend dev: these GET endpoints are *assumed* to follow the
// same /api/admin/profiles, /api/admin/accounts, /api/id/companies paths already used for
// create/update/delete -- please confirm the real paths and response shape
// (an array directly, vs. {profiles: [...]} etc.) and adjust the `|| data ||`
// fallbacks below if needed.
async function fetchProfiles() {
  try {
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/admin/profiles`, { credentials: 'include' });
    const data = await res.json();
    profiles = data.profiles || data || [];
  } catch (error) {
    console.error('Failed to load profiles:', error);
  }
}
async function fetchAccounts() {
  try {
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/admin/accounts`, { credentials: 'include' });
    const data = await res.json();
    accounts = data.accounts || data || [];
  } catch (error) {
    console.error('Failed to load accounts:', error);
  }
}
async function fetchCompanyProfile(accountId) {
  try {
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies/${accountId}`, { credentials: 'include' });
    if (res.status === 404) { delete companyProfiles[accountId]; return; }
    const data = await res.json();
    companyProfiles[accountId] = data.company || data;
  } catch (error) {
    console.error('Failed to load company profile:', error);
  }
}
async function fetchCompanies(query) {
  try {
    const qs = query ? `?q=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies${qs}`, { credentials: 'include' });
    const data = await res.json();
    otherCompanies = data.companies || data || [];
  } catch (error) {
    console.error('Failed to load companies:', error);
  }
}

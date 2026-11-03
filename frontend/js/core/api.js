// api.js
// Backend data loaders: every GET that fills the shared state in state.js.
// Loads after state.js and before ui.js.

const toProfile = p => ({
  id: p.profile_id,
  name: p.name,
  accountType: p.account_type,
  desc: p.description || "",
  status: p.is_suspended ? "Suspended" : "Active"
});

async function fetchProfiles(query) {
  try {
    const qs = query ? `?q=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/admin/profiles${qs}`, { credentials: 'include' });
    if (!res.ok) {
      console.error('Failed to load profiles: HTTP', res.status);
      profiles = [];
      return;
    }
    const data = await res.json();
    profiles = (data.profiles || []).map(toProfile);
  } catch (error) {
    console.error('Failed to load profiles:', error);
    profiles = [];
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

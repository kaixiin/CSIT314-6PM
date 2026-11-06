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
    const body = await res.json();
    profiles = (body.data || []).map(toProfile);
  } catch (error) {
    console.error('Failed to load profiles:', error);
    profiles = [];
  }
}
const toAccount = a => ({
  id: a.account_id,
  name: a.username,
  email: a.email,
  profileId: a.profile_id,
  status: a.is_suspended ? "Suspended" : "Active"
});

async function fetchAccounts(query) {
  try {
    const qs = query ? `?q=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/admin/accounts${qs}`, { credentials: 'include' });
    if (!res.ok) {
      console.error('Failed to load accounts: HTTP', res.status);
      accounts = [];
      return;
    }
    const body = await res.json();
    accounts = (body.accounts || []).map(toAccount);
  } catch (error) {
    console.error('Failed to load accounts:', error);
    accounts = [];
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

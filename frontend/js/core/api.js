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
const toCompany = c => ({
  id: c.company_id,
  accountId: c.account_id,
  name: c.company_name,
  desc: c.description || "",
  addr: c.address || "",
  phone: c.contact_number || "",
  email: c.email || "",
  logo: c.logo_url && c.logo_url.startsWith("/") ? API_CONFIG.BASE_URL + c.logo_url : (c.logo_url || "")
});

// The backend takes the account from the session, so accountId is only the
// key this company is stored under in companyProfiles.
async function fetchCompanyProfile(accountId) {
  try {
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/id/company`, { credentials: 'include' });
    if (!res.ok) {
      if (res.status !== 404) console.error('Failed to load company profile: HTTP', res.status);
      delete companyProfiles[accountId];
      return;
    }
    const body = await res.json();
    companyProfiles[accountId] = toCompany(body.company);
  } catch (error) {
    console.error('Failed to load company profile:', error);
  }
}
async function fetchCompanies(query) {
  try {
    const qs = query ? `?q=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies${qs}`, { credentials: 'include' });
    if (!res.ok) {
      console.error('Failed to load companies: HTTP', res.status);
      otherCompanies = [];
      return;
    }
    const body = await res.json();
    otherCompanies = (body.companies || []).map(toCompany);
  } catch (error) {
    console.error('Failed to load companies:', error);
    otherCompanies = [];
  }
}

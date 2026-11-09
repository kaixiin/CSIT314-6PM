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

// ---- IDPs, categories and shortlists ----
// Every call returns { ok, data }. On failure, data.message says why, so a
// route that doesn't exist yet shows a message instead of crashing the page.
async function api(method, path, body) {
  try {
    const res = await fetch(`${API_CONFIG.BASE_URL}${path}`, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include'
    });
    const data = await res.json().catch(() => ({ message: "The server did not respond as expected." }));
    return { ok: res.ok, data };
  } catch (error) {
    console.error(`${method} ${path} failed:`, error);
    return { ok: false, data: { message: "Cannot connect to the server." } };
  }
}

const imageUrl = u => (u && u.startsWith("/") ? API_CONFIG.BASE_URL + u : (u || ""));

const toIdp = i => ({
  id: i.idp_id,
  accountId: i.account_id,
  categoryId: i.category_id,
  categoryName: i.category_name || "",
  title: i.title,
  desc: i.description || "",
  location: i.location || "",
  budget: Number(i.budget) || 0,
  status: i.status,
  images: (i.images || []).map(imageUrl),
  createdAt: i.created_at || "",
  designer: i.designer || "",
  companyName: i.company_name || "",
  companyEmail: i.company_email || "",
  companyPhone: i.company_phone || "",
  saved: !!i.is_saved
});

const toCategory = c => ({
  id: c.category_id,
  name: c.name,
  desc: c.description || "",
  status: c.is_suspended ? "Suspended" : "Active",
  idps: (c.idps || []).map(toIdp)
});

const queryString = params => {
  const q = new URLSearchParams(Object.entries(params).filter(([, v]) => v));
  return q.toString() ? `?${q}` : "";
};

async function fetchMyIdps(status, query) {
  const r = await api("GET", `/api/id/idps${queryString({ q: (query || "").trim(), status })}`);
  loadError[status] = !r.ok;
  myIdps[status] = r.ok ? r.data.idps.map(toIdp) : [];
}

async function fetchIdCategories() {
  const r = await api("GET", "/api/id/categories");
  idpCategories = r.ok ? r.data.categories.map(toCategory) : [];
}

async function fetchBrowseIdps(query, categoryId) {
  const r = await api("GET", `/api/customer/idps${queryString({ q: (query || "").trim(), category_id: categoryId })}`);
  loadError.browse = !r.ok;
  browseIdpList = r.ok ? r.data.idps.map(toIdp) : [];
}

async function fetchCustomerCategories() {
  const r = await api("GET", "/api/customer/categories");
  customerCategories = r.ok ? r.data.categories.map(toCategory) : [];
}

async function fetchFavourites(query) {
  const r = await api("GET", `/api/customer/favourites${queryString({ q: (query || "").trim() })}`);
  loadError.favourites = !r.ok;
  favourites = r.ok ? r.data.idps.map(toIdp) : [];
}

async function fetchPmCategories(query) {
  const r = await api("GET", `/api/pm/categories${queryString({ q: (query || "").trim() })}`);
  loadError.categories = !r.ok;
  pmCategories = r.ok ? r.data.categories.map(toCategory) : [];
}

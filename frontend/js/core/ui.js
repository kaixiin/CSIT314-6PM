// ui.js
// Screen helpers, list/detail rendering, the confirmation dialog, the central
// view router show(), and navigation click handling.
// Loads after state.js and api.js.

const esc = s => s.replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const msg = (id, text, err) => { $(id).textContent = text; $(id).className = "msg" + (err ? " err" : ""); };
const flash = t => { $("ok").textContent = t; $("ok").className = "on"; setTimeout(() => $("ok").className = "", 2500); };
const badge = s => `<span class="badge ${s === "Suspended" ? "suspended" : "active"}">${s}</span>`;
const fmtMoney = n => "$" + Number(n).toLocaleString("en-US", { maximumFractionDigits: 2 });
const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

// Searches on the backend shortly after typing stops. The result is only shown
// if the box still holds what was searched for, so a slow reply can't overwrite a newer one.
function wireSearch(inputId, load, render) {
  let timer;
  $(inputId).addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      const query = $(inputId).value;
      await load(query);
      if ($(inputId).value === query) render();
    }, 250);
  });
}

const adminViews = ["dash","profiles","profileDetail","create","accounts","accountDetail","newAccount"];
const idViews = ["ccNoProfile","ccCreate","ccView","ccEdit","browseCompanies","competitorView","currentIdps","pastIdps","idpCreate","idpDetail"];
const customerViews = ["browseIdps","idpView","shortlist"];
const pmViews = ["categories","categoryCreate","categoryDetail","reports"];
const defaultIdView = () => companyProfiles[me.id] ? "ccView" : "ccNoProfile";

const NAV = {
  admin: [["dash","Dashboard"],["profiles","Profiles"],["accounts","Accounts"]],
  id: [["currentIdps","Current IDPs"],["pastIdps","Past IDPs"],["ccView","My Company"],["browseCompanies","Browse Companies"]],
  customer: [["shortlist","My Shortlist"],["browseIdps","Browse IDPs"]],
  pm: [["categories","Categories"],["reports","Reports"]]
};

function profileRow(p) {
  return `<div class="row" data-open-profile="${p.id}">
    <div class="ico"></div>
    <div style="flex:1">
      <div class="nm">${esc(p.name)} ${badge(p.status)}</div>
      <div class="sub">${esc(p.desc) || "No description"}</div>
    </div>
    <div class="chev">&rsaquo;</div>
  </div>`;
}
const profileName = id => (profiles.find(p => p.id === id) || {}).name || "Unknown";
const profileOptions = selectedId => profiles.map(p =>
  `<option value="${p.id}" ${p.id === selectedId ? "selected" : ""}>${esc(p.name)}</option>`).join("");

function accountRow(a) {
  return `<div class="row" data-open-account="${a.id}">
    <div class="ico"></div>
    <div style="flex:1">
      <div class="nm">${esc(a.name)} ${badge(a.status)}</div>
      <div class="sub">${esc(a.email)}</div>
      <div class="sub">Profile: ${esc(profileName(a.profileId))}</div>
    </div>
    <div class="chev">&rsaquo;</div>
  </div>`;
}
function renderProfileList(filter) {
  const q = (filter || "").trim().toLowerCase();
  const matches = profiles.filter(p => p.name.toLowerCase().includes(q));
  $("profileList").innerHTML = matches.length ? matches.map(profileRow).join("")
    : `<div class="empty">${q ? `No profiles match "${esc(filter)}".` : "No user profiles found."}</div>`;
}
function renderAccountList(filter) {
  const q = (filter || "").trim().toLowerCase();
  const matches = accounts.filter(a => a.name.toLowerCase().includes(q) || a.email.toLowerCase().includes(q));
  $("accountList").innerHTML = matches.length ? matches.map(accountRow).join("") : `<div class="empty">No accounts match "${esc(filter)}".</div>`;
}
function openProfile(id) {
  const p = profiles.find(x => x.id === id);
  if (!p) return;
  openProfileId = id;
  $("pdName").textContent = p.name;
  $("pdBadge").className = "badge " + (p.status === "Suspended" ? "suspended" : "active");
  $("pdBadge").textContent = p.status;
  $("pdUsername").value = p.name;
  $("pdDesc").value = p.desc;
  $("pdSuspendBtn").textContent = p.status === "Suspended" ? "Reactivate" : "Suspend";
  msg("profileDetailMsg", "Review and update this profile's details, or " + (p.status === "Suspended" ? "reactivate it to restore login access." : "suspend it to block members from logging in."));
  show("profileDetail");
}
function openAccount(id) {
  const a = accounts.find(x => x.id === id);
  if (!a) return;
  openAccountId = id;
  $("adName").textContent = a.name;
  $("adBadge").className = "badge " + (a.status === "Suspended" ? "suspended" : "active");
  $("adBadge").textContent = a.status;
  $("adFullname").value = a.name;
  $("adEmail").value = a.email;
  $("adProfile").innerHTML = profileOptions(a.profileId);
  $("adSuspendBtn").textContent = a.status === "Suspended" ? "Reactivate" : "Suspend";
  msg("accountDetailMsg", "Review and update this account's details, or " + (a.status === "Suspended" ? "reactivate it to restore login access." : "suspend it to block the user from logging in."));
  show("accountDetail");
}

// ---- Company profile (ID) read/display helpers ----
// NOTE: these only *render* company-profile data onto the screen. The actual
// create / update / delete form handlers for the ID role (companyCreateForm,
// companyEditForm, #ccDeleteBtn, #companySearch) are NOT wired here -- that's
// the Sprint 3 JS to be added separately (js/id/company.js).
const showLogo = (imgId, url) => {
  if (url) $(imgId).src = url; else $(imgId).removeAttribute("src");
  $(imgId).hidden = !url;
};
function renderCompanyView() {
  const p = companyProfiles[me.id];
  if (!p) return;
  showLogo("vLogo", p.logo);
  $("vName").textContent = p.name;
  $("vDesc").textContent = p.desc;
  $("vEmail").textContent = p.email;
  $("vPhone").textContent = p.phone || "Not provided";
  $("vAddr").textContent = p.addr || "Not provided";
}
function renderCompanyList(filter) {
  const q = (filter || "").trim().toLowerCase();
  const matches = otherCompanies.filter(c => c.name.toLowerCase().includes(q));
  $("companyList").innerHTML = matches.length
    ? matches.map(c => `<div class="row" data-open-competitor="${otherCompanies.indexOf(c)}">
        <div class="ico">${c.logo ? `<img src="${esc(c.logo)}" alt="">` : ""}</div>
        <div style="flex:1">
          <div class="nm">${esc(c.name)}</div>
          <div class="sub">${esc(c.desc)}</div>
        </div>
        <div class="chev">&rsaquo;</div>
      </div>`).join("")
    : `<div class="empty">${q ? `No companies match "${esc(filter)}".` : "No other companies found."}</div>`;
}
function openCompetitor(i) {
  const c = otherCompanies[i];
  if (!c) return;
  showLogo("xLogo", c.logo);
  $("xName").textContent = c.name;
  $("xDesc").textContent = c.desc;
  show("competitorView");
}
function fillCompanyEditForm() {
  const p = companyProfiles[me.id];
  if (!p) return;
  $("ecname").value = p.name;
  $("ecdesc").value = p.desc;
  $("ecemail").value = p.email;
  $("ecphone").value = p.phone || "";
  $("ecaddr").value = p.addr || "";
  $("eclogo").value = "";
  showLogo("eclogoPreview", p.logo);
  msg("ccEditMsg", "Keep your company profile up to date so customers see accurate information.");
}

// Shared confirmation modal -- replaces the browser's native confirm()
// popup with the styled dialog from the wireframe (title + body text +
// Cancel / red confirm button). Used for Suspend/Reactivate (profile,
// account) and Delete (company profile), per UCD items #128 and #11,
// which both call for "a warning with a confirmation dialogue box."
//
// Usage: const ok = await confirmDialog("Delete Company Profile?", "Are you sure...", "Delete Profile");
function confirmDialog(title, body, confirmLabel) {
  return new Promise(resolve => {
    $("modalTitle").textContent = title;
    $("modalBody").textContent = body;
    $("modalConfirmBtn").textContent = confirmLabel || "Confirm";
    $("modalOverlay").hidden = false;

    function onConfirm() { cleanup(true); }
    function onCancel() { cleanup(false); }
    function cleanup(result) {
      $("modalOverlay").hidden = true;
      $("modalConfirmBtn").removeEventListener("click", onConfirm);
      $("modalCancelBtn").removeEventListener("click", onCancel);
      resolve(result);
    }

    $("modalConfirmBtn").addEventListener("click", onConfirm);
    $("modalCancelBtn").addEventListener("click", onCancel);
  });
}

// ---- Central view router ----
// Every screen switch (login, nav clicks, post-submit redirects) goes
// through show(id). It also enforces role guards, so a user can never land
// on a screen another role owns just by changing state.
function show(id) {
  const r = roleOf();
  if (!r) id = "login";
  else if (r === "admin") { if (id === "login" || !adminViews.includes(id)) id = "dash"; }
  else if (r === "id") {
    if (id === "login" || !idViews.includes(id)) id = defaultIdView();
    else if (id === "ccView" && !companyProfiles[me.id]) id = "ccNoProfile";
  }
  else if (r === "customer") { if (!customerViews.includes(id)) id = "browseIdps"; }
  else if (r === "pm") { if (!pmViews.includes(id)) id = "categories"; }
  else { id = "home"; } // an account type with no screens of its own

  document.querySelectorAll(".view").forEach(v => v.classList.toggle("on", v.id === id));
  document.body.className = r || "";
  $("status").textContent = me
    ? "Logged in as " + (r === "admin" ? "System Admin" : r === "id" ? "ID" : r === "customer" ? "Customer" : r === "pm" ? "PM" : "User") + (me.name ? " — " + me.name : "")
    : "Logged out";
  $("logout").hidden = !me;

  const navItems = NAV[r];
  $("nav").hidden = !navItems;
  $("nav").innerHTML = navItems ? navItems.map(([go, label]) => `<button class="sm" data-go="${go}">${label}</button>`).join("") : "";
  document.querySelectorAll("#nav button").forEach(b => b.classList.toggle("act", b.dataset.go === (PARENT[id] || id)));

  if (!me) return;
  if (r === "admin") {
    $("stats").innerHTML = `<div class="card"><b>${profiles.length}</b>User profiles</div><div class="card"><b>${accounts.length}</b>Accounts</div>`;
    if (id === "profiles") renderProfileList($("profileSearch").value);
    if (id === "accounts") renderAccountList($("accountSearch").value);
    $("aprofile").innerHTML = profileOptions();
  } else if (r === "id") {
    if (id === "ccView") renderCompanyView();
    if (id === "ccEdit") fillCompanyEditForm();
    if (id === "browseCompanies") renderCompanyList($("companySearch").value);
    if (id === "currentIdps" || id === "pastIdps") renderMyIdps(id);
  } else if (r === "customer") {
    if (id === "browseIdps") renderBrowseIdps();
    if (id === "shortlist") renderShortlist();
  } else if (r === "pm") {
    if (id === "categories") renderCategories();
  } else {
    $("welcome").textContent = "Welcome, " + me.name;
  }
}

// ---- Navigation click delegation (data-go links, list rows) ----
// Generic routing only -- no feature-specific business logic lives here.
// Async so each nav click can pull fresh data from the backend before the
// screen it's going to is rendered.
document.addEventListener("click", async e => {
  const row1 = e.target.closest("[data-open-profile]");
  if (row1) return openProfile(Number(row1.dataset.openProfile));
  const row2 = e.target.closest("[data-open-account]");
  if (row2) return openAccount(Number(row2.dataset.openAccount));
  const row4 = e.target.closest("[data-open-competitor]");
  if (row4) return openCompetitor(Number(row4.dataset.openCompetitor));

  const go = e.target.dataset && e.target.dataset.go;
  if (!go) return;
  if (go === "create") { msg("createMsg", "Set up a new user group so members can be assigned the right access."); await fetchProfiles(); }
  if (go === "newAccount") { msg("accountMsg", "Create a login for a new user and assign a profile."); await fetchProfiles(); }
  if (go === "ccCreate") msg("ccCreateMsg", "Tell customers who you are so they can find and contact you.");
  if (go === "profiles") await fetchProfiles();
  if (go === "accounts") { await fetchProfiles(); await fetchAccounts(); }
  if (go === "browseCompanies") await fetchCompanies();
  if (go === "ccView" && me) await fetchCompanyProfile(me.id);
  if (go === "currentIdps") await fetchMyIdps("Current", $("currentIdpSearch").value);
  if (go === "pastIdps") await fetchMyIdps("Past", $("pastIdpSearch").value);
  if (go === "browseIdps") await fetchBrowseIdps($("browseSearch").value, $("browseCategory").value);
  if (go === "shortlist") await fetchFavourites($("shortlistSearch").value);
  if (go === "categories") await fetchPmCategories($("categorySearch").value);
  if (go === "categoryCreate") {
    $("categoryCreateForm").reset();
    msg("categoryCreateMsg", "Add a new IDP category for customers to browse.");
  }
  show(go);
});

$("profileSearch")?.addEventListener("input", e => renderProfileList(e.target.value));
$("accountSearch")?.addEventListener("input", e => renderAccountList(e.target.value));
// #19 Search for company profile
$("companySearch")?.addEventListener("input", e => renderCompanyList(e.target.value));

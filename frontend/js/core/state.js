// state.js
// Shared app state and role mapping used by every role's screens.
// Must load FIRST (after config.js): everything else in core/ and the
// feature folders (auth/, admin/, id/) uses the globals defined here.
//
// No seeded demo data -- the backend database is the single source of
// truth. These arrays start empty and get filled in by the fetch*() loaders
// in api.js, called right after login and after any create/update/suspend/delete
// action. Screens render from whatever was most recently fetched into them.

let accounts = [];
let profiles = [];
// Company profiles, keyed by account id. Empty = that ID hasn't created one yet
// (or it just hasn't been fetched yet).
let companyProfiles = {};
// Other IDs' company profiles, for #19 Search Company Profile (competitor research).
let otherCompanies = [];

const PARENT = {create:"profiles", newAccount:"accounts", profileDetail:"profiles", accountDetail:"accounts",
                ccCreate:"ccView", ccEdit:"ccView", ccNoProfile:"ccView", competitorView:"browseCompanies"};
let me = null, openProfileId = null, openAccountId = null;

const $ = id => document.getElementById(id);

// Works out an account's actual role from its data. Login has no role
// dropdown -- role is always derived from the matched account, never picked
// by the user. This matches the UCD/SQ: login only takes email + password.
const ROLE_BY_TYPE = { UserAdmin: "admin", InteriorDesigner: "id", Customer: "customer", PlatformManager: "pm" };
const roleOfAccount = a => a ? (ROLE_BY_TYPE[a.role] || "user") : null;

const roleOf = () => roleOfAccount(me);

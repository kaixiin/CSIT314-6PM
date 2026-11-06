// login.js
// Login: no role dropdown. Role is derived from whichever account matches
// (see roleOfAccount() in state.js) -- never chosen by the person logging in.
// This matches the Login UCD/SQ, which only takes a username and password.
//
// Now connected to the real backend (per the auth_routes.py contract) --
// local-only testing is removed.

// Shared by login and page load: stores the account, loads this role's data,
// then lets show() in core/ui.js work out which screen to land on.
async function startSession(account) {
    me = {
        id: account.account_id,
        name: account.username,
        email: account.username,
        role: account.account_type,
        profile: account.profile_id,
        status: account.status || "Active",
    };

    // Load this role's data before routing, so the landing screen (and
    // show()'s routing decision for ID -- ccView vs ccNoProfile --
    // which depends on whether a company profile exists) is correct on
    // the very first render instead of flashing empty, then correcting.
    const r = roleOf();
    if (r === "admin") {
        await Promise.all([fetchProfiles(), fetchAccounts()]);
    } else if (r === "id") {
        await fetchCompanyProfile(me.id);
    }

    show("dash");
}

// A refresh wipes the page's data but not the login cookie, so ask the backend
// who is logged in before falling back to the login screen.
async function restoreSession() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/me`, { credentials: 'include' });
        if (response.ok) {
            const data = await response.json();
            await startSession(data.account);
            return;
        }
    } catch (error) {
        console.error("Could not check login session:", error);
    }
    show("login");
}

async function triggerLogin(event) {
    event.preventDefault();

    const emailInput = document.getElementById('email').value.trim().toLowerCase();
    const passwordInput = document.getElementById('pw').value;

    msg("loginMsg", "Signing in...", false);

    try {
        // 1. Fetch connection pointing directly to the backend Blueprint routing prefix
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: emailInput, // Matches data.get("email") in Flask
                password: passwordInput // Matches data.get("password") in Flask
            }),
            credentials: 'include' // Transmits and handles Flask session cookies automatically
        });

        const data = await response.json();

        // 2. Process return payload using keys matching auth_routes.py exactly
        if (!data.success) {
            msg("loginMsg", data.message || "Login unsuccessful, email or password is incorrect.", true);
            document.getElementById('email').focus();
            return;
        }

        // NOTE for whoever owns the backend: state.js's roleOfAccount() expects
        // `me.role === "admin"` or `me.profile === "Interior Design" / "Customer"`.
        // If the backend's account_type already returns one of
        // "admin" / "id" / "pm" / "customer" directly, roleOfAccount() in
        // state.js should be simplified to just read me.role straight --
        // flag this with the backend dev so the two sides agree on one shape.
        document.getElementById("loginForm").reset();
        msg("loginMsg", "Enter your email and password.", false);

        await startSession(data.account);

    } catch (error) {
        console.error("Connection error during login:", error);
        msg("loginMsg", "Cannot connect to login server.", true);
    }
}

document.getElementById("loginForm").addEventListener("submit", triggerLogin);

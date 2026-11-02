// account.js
// Admin: create / view / update / search / suspend User Accounts.
// Connected to the real backend.
//
// NOTE for the backend dev: /api/accounts (POST) matches the endpoint already
// agreed for Create. The update and suspend endpoints below (PUT /api/accounts/:id
// and PATCH /api/accounts/:id/status) are *assumed* to follow the same
// pattern -- please confirm the real paths/response shape and adjust if
// they're different.

async function triggerCreateAccount(event) {
    event.preventDefault();
    if (roleOf() !== "admin") return show("home");

    const fullNameInput = document.getElementById('aname').value.trim();
    const emailInput = document.getElementById('aemail').value.trim().toLowerCase();
    const passwordInput = document.getElementById('apw').value;
    const selectedProfile = document.getElementById('aprofile').value;

    msg("accountMsg", "Creating user account...", false);

    try {
        const response = await fetch('/api/accounts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: fullNameInput,
                email: emailInput,
                password: passwordInput,
                profile: selectedProfile
            }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("accountMsg", data.message || `Create failed: an account for "${emailInput}" already exists.`, true);
            document.getElementById('aemail').focus();
            return;
        }

        // Backend is the source of truth -- re-fetch instead of guessing
        // what the new row looks like.
        await fetchAccounts();

        document.getElementById("accountForm").reset();
        show("accounts");
        flash("Account created successfully.");

    } catch (error) {
        console.error("Connection error during account creation:", error);
        msg("accountMsg", "Cannot connect to account server.", true);
    }
}

async function triggerUpdateAccount(event) {
    event.preventDefault();
    const a = accounts.find(x => x.id === openAccountId);
    if (!a) return;

    const name = document.getElementById('adFullname').value.trim();
    const email = document.getElementById('adEmail').value.trim();
    const profile = document.getElementById('adProfile').value;

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`/api/accounts/${a.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, profile }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("accountDetailMsg", data.message || `Update failed: an account for "${email}" already exists.`, true);
            return;
        }

        await fetchAccounts();

        show("accounts");
        flash("Account updated successfully.");

    } catch (error) {
        console.error("Connection error during account update:", error);
        msg("accountDetailMsg", "Cannot connect to account server.", true);
    }
}

// #11: confirmation dialogue box before suspending/reactivating
async function triggerSuspendAccount() {
    const a = accounts.find(x => x.id === openAccountId);
    if (!a) return;
    const suspending = a.status !== "Suspended";
    const ok = await confirmDialog(
        suspending ? "Suspend Account?" : "Reactivate Account?",
        suspending
            ? `Are you sure you want to suspend "${a.name}"? This user will no longer be able to log in.`
            : `Are you sure you want to reactivate "${a.name}"? This user will be able to log in again.`,
        suspending ? "Suspend" : "Reactivate"
    );
    if (!ok) return;

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`/api/accounts/${a.id}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: suspending ? "Suspended" : "Active" }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            flash(data.message || "Could not update account status.");
            return;
        }

        await fetchAccounts();
        show("accounts");
        flash(suspending ? "Account suspended." : "Account reactivated.");

    } catch (error) {
        console.error("Connection error during account suspend/reactivate:", error);
        flash("Cannot connect to account server.");
    }
}

document.getElementById("accountForm").addEventListener("submit", triggerCreateAccount);
document.getElementById("accountDetailForm").addEventListener("submit", triggerUpdateAccount);
document.getElementById("adSuspendBtn").addEventListener("click", triggerSuspendAccount);

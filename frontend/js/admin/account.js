// account.js
// Admin: create / update / suspend / reactivate User Accounts (#8, #10, #11).
// Routes: /api/admin/accounts (see the API Route Sync doc). Search and view
// (#12, #9) load through fetchAccounts() in js/core/api.js.

async function triggerCreateAccount(event) {
    event.preventDefault();
    if (roleOf() !== "admin") return show("home");

    const fullNameInput = document.getElementById('aname').value.trim();
    const emailInput = document.getElementById('aemail').value.trim().toLowerCase();
    const passwordInput = document.getElementById('apw').value;
    const selectedProfile = Number(document.getElementById('aprofile').value);

    msg("accountMsg", "Creating user account...", false);

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/accounts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: fullNameInput,
                email: emailInput,
                password: passwordInput,
                profile_id: selectedProfile
            }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("accountMsg", data.message || "Create failed: that username or email is already used.", true);
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
    const profile_id = Number(document.getElementById('adProfile').value);

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/accounts/${a.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: name, email, profile_id }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("accountDetailMsg", data.message || "Update failed: that username or email is already used.", true);
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
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/accounts/${a.id}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_suspended: suspending }),
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

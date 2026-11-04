// company.js
// ID role: create / view / update / delete Company Profile (#15-#18).
// Browsing/searching other companies (#19) is read-only and already
// handled by renderCompanyList()/openCompetitor() in core/ui.js.
//
// Connected to the real backend.
//
// NOTE for the backend dev: these endpoints (/api/id/companies, POST/PUT/DELETE)
// are *assumed* to follow the same REST pattern as /api/admin/profiles and
// /api/admin/accounts -- please confirm the real paths/response shape and
// update this file if they're different.

async function triggerCreateCompanyProfile(event) {
    event.preventDefault();
    if (roleOf() !== "id") return show("home");

    const name = document.getElementById('cname').value.trim();
    const desc = document.getElementById('cdesc').value.trim();
    const email = document.getElementById('cemail').value.trim();
    const phone = document.getElementById('cphone').value.trim();
    const addr = document.getElementById('caddr').value.trim();

    if (!name) return;

    msg("ccCreateMsg", "Creating company profile...", false);

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description: desc, email, phone, address: addr }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("ccCreateMsg", data.message || "Failed to create company profile.", true);
            return;
        }

        // Backend is the source of truth -- re-fetch instead of guessing
        // what the saved record looks like.
        await fetchCompanyProfile(me.id);

        event.target.reset();
        show("ccView");
        flash("Company profile created successfully.");

    } catch (error) {
        console.error("Connection error during company profile creation:", error);
        msg("ccCreateMsg", "Cannot connect to company profile server.", true);
    }
}

async function triggerUpdateCompanyProfile(event) {
    event.preventDefault();
    if (roleOf() !== "id") return show("home");
    const p = companyProfiles[me.id];
    if (!p) return;

    const name = document.getElementById('ecname').value.trim();
    const desc = document.getElementById('ecdesc').value.trim();
    const email = document.getElementById('ecemail').value.trim();
    const phone = document.getElementById('ecphone').value.trim();
    const addr = document.getElementById('ecaddr').value.trim();

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies/${me.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description: desc, email, phone, address: addr }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            flash(data.message || "Failed to update company profile.");
            return;
        }

        await fetchCompanyProfile(me.id);

        show("ccView");
        flash("Company profile updated successfully.");

    } catch (error) {
        console.error("Connection error during company profile update:", error);
        flash("Cannot connect to company profile server.");
    }
}

// #18 Delete company profile (ID only) -- confirmation dialogue box, as per UCD
async function triggerDeleteCompanyProfile() {
    if (roleOf() !== "id") return;
    const p = companyProfiles[me.id];
    if (!p) return;

    const ok = await confirmDialog(
        "Delete Company Profile?",
        `Are you sure you want to delete "${p.name}"? Your company information will be permanently removed. Customers will no longer be able to find or contact "${p.name}" through this profile. This action cannot be undone.`,
        "Delete Profile"
    );
    if (!ok) return;

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/id/companies/${me.id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            flash(data.message || "Failed to delete company profile.");
            return;
        }

        delete companyProfiles[me.id];
        show("ccNoProfile");
        flash(`${p.name} company profile deleted successfully.`);

    } catch (error) {
        console.error("Connection error during company profile deletion:", error);
        flash("Cannot connect to company profile server.");
    }
}

document.getElementById("companyCreateForm").addEventListener("submit", triggerCreateCompanyProfile);
document.getElementById("companyEditForm").addEventListener("submit", triggerUpdateCompanyProfile);
document.getElementById("ccDeleteBtn").addEventListener("click", triggerDeleteCompanyProfile);

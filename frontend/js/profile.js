// profile.js
// Admin: create / view / update / search / suspend User Profiles.
// Connected to the real backend.

async function triggerCreateProfile(event) {
    event.preventDefault();
    if (roleOf() !== "admin") return show("home");

    const name = document.getElementById('uname').value.trim();
    const desc = document.getElementById('desc').value.trim();
//    const checkedPermissions = [...document.querySelectorAll('#createForm .perms input[type="checkbox"]:checked')].map(c => c.value);

    msg("createMsg", "Creating profile...", false);

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/profiles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                description: desc
            }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("createMsg", data.message || "Failed to create profile.", true);
            document.getElementById('uname').focus();
            return;
        }

        // Backend is the source of truth -- re-fetch instead of guessing
        // what the new row looks like.
        await fetchProfiles();

        document.getElementById("createForm").reset();
        show("profiles");
        flash("Profile created successfully.");

    } catch (error) {
        console.error("Connection error during profile creation:", error);
        msg("createMsg", "Cannot connect to profile server.", true);
    }
}

async function triggerUpdateProfile(event) {
    event.preventDefault();
    const p = profiles.find(x => x.id === openProfileId);
    if (!p) return;

    const name = document.getElementById('pdUsername').value.trim();
    const desc = document.getElementById('pdDesc').value.trim();
    const perms = [
        document.getElementById('pdEdit').checked && "Edit",
        document.getElementById('pdView').checked && "View",
        document.getElementById('pdUpdate').checked && "Update"
    ].filter(Boolean);

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/profiles/${p.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description: desc}), //permissions: perms 
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("profileDetailMsg", data.message || `Update failed: a profile named "${name}" already exists.`, true);
            return;
        }

        await fetchProfiles();

        show("profiles");
        flash("Profile updated successfully.");

    } catch (error) {
        console.error("Connection error during profile update:", error);
        msg("profileDetailMsg", "Cannot connect to profile server.", true);
    }
}

// #128: confirmation dialogue box before suspending/reactivating
async function triggerSuspendProfile() {
    const p = profiles.find(x => x.id === openProfileId);
    if (!p) return;
    const suspending = p.status !== "Suspended";
    const ok = await confirmDialog(
        suspending ? "Suspend Profile?" : "Reactivate Profile?",
        suspending
            ? `Are you sure you want to suspend "${p.name}"? Members in this profile will no longer be able to log in.`
            : `Are you sure you want to reactivate "${p.name}"? Members in this profile will be able to log in again.`,
        suspending ? "Suspend" : "Reactivate"
    );
    if (!ok) return;

    try {
        // ASSUMED endpoint -- confirm with backend dev.
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/profiles/${p.id}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: suspending ? "Suspended" : "Active" }),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            flash(data.message || "Could not update profile status.");
            return;
        }

        await fetchProfiles();
        show("profiles");
        flash(suspending ? "Profile suspended." : "Profile reactivated.");

    } catch (error) {
        console.error("Connection error during profile suspend/reactivate:", error);
        flash("Cannot connect to profile server.");
    }
}

document.getElementById("createForm").addEventListener("submit", triggerCreateProfile);
document.getElementById("profileDetailForm").addEventListener("submit", triggerUpdateProfile);
document.getElementById("pdSuspendBtn").addEventListener("click", triggerSuspendProfile);

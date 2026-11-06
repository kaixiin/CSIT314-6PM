// company.js
// ID role: create / view / update / delete Company Profile (#15-#18).
// Browsing/searching other companies (#19) is read-only and already
// handled by renderCompanyList()/openCompetitor() in core/ui.js.
//
// Connected to the real backend (/api/id/company, company_routes.py). The
// account comes from the session, so the URL carries no id. Request bodies
// use the backend's field names; responses are translated by toCompany() in api.js.

const COMPANY_URL = `${API_CONFIG.BASE_URL}/api/id/company`;
const LOGO_TYPES = ["image/png", "image/jpeg"];
const MAX_LOGO_BYTES = 5 * 1024 * 1024;

const logoError = file => {
    if (!LOGO_TYPES.includes(file.type)) return "Logo must be a JPG or PNG image.";
    if (file.size > MAX_LOGO_BYTES) return "Logo must be 5MB or smaller.";
    return "";
};

// The backend takes the logo as a data URL inside the JSON body.
const readLogo = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
});

// Previews the chosen image straight away. currentLogo() gives the image to go
// back to if the choice is cancelled or rejected.
function wireLogoInput(inputId, previewId, msgId, currentLogo) {
    $(inputId).addEventListener("change", async () => {
        const file = $(inputId).files[0];
        const error = file ? logoError(file) : "";
        if (!file || error) {
            $(inputId).value = "";
            showLogo(previewId, currentLogo());
            if (error) msg(msgId, error, true);
            return;
        }
        try {
            showLogo(previewId, await readLogo(file));
        } catch (err) {
            console.error("Could not read logo file:", err);
            $(inputId).value = "";
            showLogo(previewId, currentLogo());
            msg(msgId, "Could not read that image.", true);
        }
    });
}

// Fields shared by create and update. logo stays undefined when no new file was
// chosen, so JSON.stringify leaves it out and the backend keeps the current one.
async function companyBody(prefix, logoInputId) {
    const file = $(logoInputId).files[0];
    return {
        company_name: $(prefix + "name").value.trim(),
        description: $(prefix + "desc").value.trim(),
        address: $(prefix + "addr").value.trim(),
        contact_number: $(prefix + "phone").value.trim(),
        email: $(prefix + "email").value.trim(),
        logo: file ? await readLogo(file) : undefined
    };
}

async function triggerCreateCompanyProfile(event) {
    event.preventDefault();
    if (roleOf() !== "id") return show("home");

    msg("ccCreateMsg", "Creating company profile...", false);

    try {
        const response = await fetch(COMPANY_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(await companyBody("c", "clogo")),
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
        showLogo("clogoPreview", "");
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
    if (!companyProfiles[me.id]) return;

    try {
        const response = await fetch(COMPANY_URL, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(await companyBody("ec", "eclogo")),
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.success) {
            msg("ccEditMsg", data.message || "Failed to update company profile.", true);
            return;
        }

        await fetchCompanyProfile(me.id);

        show("ccView");
        flash("Company profile updated successfully.");

    } catch (error) {
        console.error("Connection error during company profile update:", error);
        msg("ccEditMsg", "Cannot connect to company profile server.", true);
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
        const response = await fetch(COMPANY_URL, {
            method: 'DELETE',
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
wireLogoInput("clogo", "clogoPreview", "ccCreateMsg", () => "");
wireLogoInput("eclogo", "eclogoPreview", "ccEditMsg", () => (companyProfiles[me.id] || {}).logo);

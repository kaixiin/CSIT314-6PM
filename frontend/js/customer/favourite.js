// Customer role: view and search My Shortlist, save a project, remove a project.
//
// Uses /api/customer/favourites. The list always belongs to the logged-in
// customer, so no account id goes in the URL.

const FAVOURITE_URL = "/api/customer/favourites";

function renderShortlist() {
    const n = favourites.length;
    $("shortlistCount").textContent = `${n} project${n === 1 ? "" : "s"} in your shortlist`;
    $("shortlistList").innerHTML = n
        ? favourites.map(i => customerCard(i, "shortlist")).join("")
        : `<div class="empty">${loadError.favourites ? "Could not load your shortlist." : "No projects in your shortlist."}</div>`;
}

async function saveFavourite(i) {
    const r = await api("POST", FAVOURITE_URL, { idp_id: i.id });
    if (!r.ok) return flash(r.data.message || "Failed to save project.");
    i.saved = true;
    setSaveButton();
    flash("Project saved to your shortlist.");
}

async function removeFavourite(id) {
    const r = await api("DELETE", `${FAVOURITE_URL}/${id}`);
    if (!r.ok) {
        flash(r.data.message || "Failed to remove project.");
        return false;
    }
    flash("Project removed from your shortlist.");
    return true;
}

$("idViewSave").addEventListener("click", async () => {
    const i = openCustomerIdp;
    if (!i) return;
    if (!i.saved) return saveFavourite(i);
    if (await removeFavourite(i.id)) {
        i.saved = false;
        setSaveButton();
    }
});

document.addEventListener("click", async e => {
    const btn = e.target.closest("[data-remove-favourite]");
    if (!btn) return;
    if (await removeFavourite(Number(btn.dataset.removeFavourite))) {
        await fetchFavourites($("shortlistSearch").value);
        renderShortlist();
    }
});

wireSearch("shortlistSearch", fetchFavourites, renderShortlist);

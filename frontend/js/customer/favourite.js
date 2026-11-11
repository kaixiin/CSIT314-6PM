// Customer role: view and search My Shortlist, and save a project.
//
// Uses /api/customer/favourites for the list. Saving goes to
// POST /api/customer/idps/<id>/favourites, which removes the project
// instead if it is already saved.

function renderShortlist() {
    const n = favourites.length;
    $("shortlistCount").textContent = `${n} project${n === 1 ? "" : "s"} in your shortlist`;
    $("shortlistList").innerHTML = n
        ? favourites.map(i => customerCard(i, "shortlist")).join("")
        : `<div class="empty">${loadError.favourites ? "Could not load your shortlist." : "No projects in your shortlist."}</div>`;
}

$("idViewSave").addEventListener("click", async () => {
    const i = openCustomerIdp;
    if (!i) return;
    const r = await api("POST", `/api/customer/idps/${i.id}/favourites`);
    if (!r.ok) return flash(r.data.message || "Failed to update your shortlist.");
    i.saved = !i.saved;
    setSaveButton();
    flash(i.saved ? "Project saved to your shortlist." : "Project removed from your shortlist.");
});

wireSearch("shortlistSearch", fetchFavourites, renderShortlist);

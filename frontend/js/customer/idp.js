// Customer role: search IDPs by name and category, and view a project.
// Opening a project records one view on the backend.
//
// Uses /api/customer/idps. Responses are translated by toIdp() in api.js.

// Used by both Browse IDPs and My Shortlist.
function customerCard(i, from) {
    return `<article class="pcard clickable" data-open-customer-idp="${i.id}" data-from="${from}">
        <button class="pcard-open" aria-label="Open ${esc(i.title)}">
            <span class="pcard-img">${i.images[0] ? `<img src="${esc(i.images[0])}" alt="">` : ""}</span>
        </button>
        <div class="pcard-body">
            <div class="pcard-title">${esc(i.title)}</div>
            <p class="pcard-desc">${esc(i.categoryName)}</p>
        </div>
    </article>`;
}

function renderBrowseIdps() {
    $("browseCount").textContent = `${browseIdpList.length} project${browseIdpList.length === 1 ? "" : "s"} found`;
    $("browseList").innerHTML = browseIdpList.length
        ? browseIdpList.map(i => customerCard(i, "browseIdps")).join("")
        : `<div class="empty">${loadError.browse ? "Could not load projects." : "No projects found."}</div>`;
}

const browseFilters = () => [$("browseSearch").value, $("browseCategory").value];

// Runs once after login: the category filter, then the first list of projects.
async function loadCustomerHome() {
    await fetchCustomerCategories();
    $("browseCategory").innerHTML = `<option value="">All categories</option>` +
        customerCategories.map(c => `<option value="${c.id}">${esc(c.name)}</option>`).join("");
    await fetchBrowseIdps();
}

function showGalleryImage(n) {
    const images = openCustomerIdp.images;
    $("idViewMain").innerHTML = images[n] ? `<img src="${esc(images[n])}" alt="">` : "";
    document.querySelectorAll("#idViewThumbs .thumb").forEach((t, k) => t.classList.toggle("on", k === n));
}

function setSaveButton() {
    $("idViewSave").textContent = openCustomerIdp.saved ? "Remove from Shortlist" : "Save to Shortlist";
}

async function openCustomerProject(id, from) {
    const r = await api("GET", `/api/customer/idps/${id}`);
    if (!r.ok) return flash(r.data.message || "Could not open that project.");
    const data = itemFrom(r.data, "idp");
    const i = toIdp(data);
    // Until the view sends is_saved, check the shortlist instead
    if (data.is_saved === undefined) {
        await fetchFavourites();
        i.saved = favourites.some(f => f.id === i.id);
    }
    openCustomerIdp = i;

    PARENT.idpView = from;
    $("idViewBack").dataset.go = from;
    $("idViewBack").textContent = `← Back to ${from === "shortlist" ? "My Shortlist" : "Browse IDPs"}`;
    $("idViewTitle").textContent = i.title;
    $("idViewMeta").textContent = i.companyName ? `${i.categoryName} by ${i.companyName}` : i.categoryName;
    $("idViewThumbs").innerHTML = i.images.map((url, n) =>
        `<button class="thumb" data-thumb="${n}" aria-label="Photo ${n + 1}"><img src="${esc(url)}" alt=""></button>`).join("");
    $("idViewThumbs").hidden = i.images.length < 2;
    showGalleryImage(0);
    $("idViewLocation").textContent = i.location;
    $("idViewBudget").textContent = fmtMoney(i.budget);
    $("idViewStatus").textContent = i.status;
    $("idViewDesc").textContent = i.desc;
    setSaveButton();

    // The designer may not have created a company profile yet
    $("idViewContact").hidden = !i.companyName;
    $("idViewCompany").textContent = i.companyName;
    $("idViewContactLine").textContent = [i.companyEmail, i.companyPhone].filter(Boolean).join(" | ");
    show("idpView");
}

document.addEventListener("click", e => {
    const thumb = e.target.closest("[data-thumb]");
    if (thumb) return showGalleryImage(Number(thumb.dataset.thumb));
    const card = e.target.closest("[data-open-customer-idp]");
    if (card) openCustomerProject(Number(card.dataset.openCustomerIdp), card.dataset.from);
});

wireSearch("browseSearch", () => fetchBrowseIdps(...browseFilters()), renderBrowseIdps);
$("browseCategory").addEventListener("change", async () => {
    await fetchBrowseIdps(...browseFilters());
    renderBrowseIdps();
});

// idp.js
// ID role: create / view / update / delete / search Current and Past IDPs,
// and the views and shortlist counts on each project.
//
// Uses /api/id/idps. The account comes from the session, so a designer only
// ever gets their own projects. Request bodies use the backend's field names;
// responses are translated by toIdp() in api.js.

const IDP_URL = "/api/id/idps";
const MAX_PHOTOS = 5;
const PHOTO_TYPES = ["image/png", "image/jpeg"];
const MAX_PHOTO_BYTES = 5 * 1024 * 1024;

const idpListView = status => (status === "Past" ? "pastIdps" : "currentIdps");
const idpListName = status => (status === "Past" ? "My Past IDPs" : "My Current IDPs");

// New photos waiting to be saved, as data URLs. null = none chosen.
const pendingPhotos = { idpPhotos: null, edIdpPhotos: null };

function idpCard(i) {
    return `<article class="pcard">
        <div class="pcard-img">${i.images[0] ? `<img src="${esc(i.images[0])}" alt="">` : ""}</div>
        <div class="pcard-body">
            <div class="pcard-title">${esc(i.title)}</div>
            <span class="badge ${i.status.toLowerCase()}">${esc(i.status)}</span>
            <p class="pcard-desc">${esc(i.desc)}</p>
            <p class="pcard-desc">${esc(i.location)} &middot; ${fmtMoney(i.budget)}</p>
        </div>
        <div class="pcard-links">
            <button class="textlink" data-open-idp="${i.id}">View</button>
            <button class="textlink" data-open-idp="${i.id}">Edit</button>
            <button class="textlink red" data-delete-idp="${i.id}">Delete</button>
        </div>
    </article>`;
}

function renderMyIdps(view) {
    const status = view === "pastIdps" ? "Past" : "Current";
    const prefix = view === "pastIdps" ? "past" : "current";
    const list = myIdps[status];
    $(prefix + "IdpCount").textContent = `${list.length} project${list.length === 1 ? "" : "s"} found`;
    $(prefix + "IdpList").innerHTML = list.length
        ? list.map(idpCard).join("")
        : `<div class="empty">${loadError[status] ? "Could not load projects." : "No projects found."}</div>`;
}

const categoryOptions = (selected, extra) =>
    idpCategories.concat(extra || []).map(c =>
        `<option value="${c.id}" ${c.id === selected ? "selected" : ""}>${esc(c.name)}</option>`).join("");

// Shows chosen or saved photos, one per tile. Always at least 4 empty tiles beside "+ Add".
function renderPhotoTiles(tilesId, urls) {
    const count = Math.max(4, urls.length);
    $(tilesId).innerHTML = Array.from({ length: count }, (_, n) =>
        urls[n] ? `<span class="photo filled"><img src="${esc(urls[n])}" alt=""></span>` : `<span class="photo"></span>`).join("");
}

const photoError = files => {
    if (files.length > MAX_PHOTOS) return `You can add up to ${MAX_PHOTOS} photos.`;
    if (files.some(f => !PHOTO_TYPES.includes(f.type))) return "Photos must be JPG or PNG images.";
    if (files.some(f => f.size > MAX_PHOTO_BYTES)) return "Each photo must be 5MB or smaller.";
    return "";
};

// currentPhotos() gives the photos to go back to if the choice is rejected.
function wirePhotoInput(inputId, tilesId, msgId, currentPhotos) {
    $(inputId).addEventListener("change", async () => {
        const files = Array.from($(inputId).files);
        const reject = text => {
            $(inputId).value = "";
            pendingPhotos[inputId] = null;
            renderPhotoTiles(tilesId, currentPhotos());
            msg(msgId, text, true);
        };
        if (!files.length) return;
        const error = photoError(files);
        if (error) return reject(error);
        try {
            pendingPhotos[inputId] = await Promise.all(files.map(readLogo));
            renderPhotoTiles(tilesId, pendingPhotos[inputId]);
        } catch (err) {
            console.error("Could not read photo file:", err);
            reject("Could not read one of those images.");
        }
    });
}

function setIdpBackLinks(status) {
    const view = idpListView(status);
    PARENT.idpCreate = view;
    PARENT.idpDetail = view;
    ["idpCreateBack", "idpDetailBack"].forEach(id => {
        $(id).dataset.go = view;
        $(id).textContent = `← Back to ${idpListName(status)}`;
    });
    $("idpCreateCancel").dataset.go = view;
}

async function openIdpCreate(status) {
    await fetchIdCategories();
    idpCreateStatus = status;
    setIdpBackLinks(status);
    $("idpCreateForm").reset();
    pendingPhotos.idpPhotos = null;
    renderPhotoTiles("idpPhotoTiles", []);
    $("idpCategory").innerHTML = `<option value="">Select a category</option>` + categoryOptions();
    $("idpTitle").placeholder = status === "Past" ? "e.g. Modern 3-Room Flat Makeover" : "e.g. Level Condo Renovation";
    msg("idpCreateMsg", status === "Past"
        ? "Showcase a completed project. Its status will be Past."
        : "Add a project you are actively working on. Its status will be Current.");
    show("idpCreate");
}

async function openIdpDetail(id) {
    const [view, stats] = await Promise.all([
        api("GET", `${IDP_URL}/${id}`),
        api("GET", `${IDP_URL}/${id}/stats`),
        fetchIdCategories()
    ]);
    if (!view.ok) return flash(view.data.message || "Could not open that project.");
    const i = toIdp(view.data.idp);
    openIdp = i;
    setIdpBackLinks(i.status);

    $("idpDetailTitle").textContent = i.title;
    $("idpDetailBadge").textContent = i.status;
    $("idpDetailBadge").className = "badge " + i.status.toLowerCase();
    $("idpViews").textContent = stats.ok ? stats.data.views : "-";
    $("idpSaves").textContent = stats.ok ? stats.data.shortlists : "-";
    $(i.status === "Past" ? "idpStatusPast" : "idpStatusCurrent").checked = true;
    $("edIdpTitle").value = i.title;
    $("edIdpDesc").value = i.desc;
    // A project can sit in a category that has since been suspended
    const missing = idpCategories.some(c => c.id === i.categoryId) ? [] : [{ id: i.categoryId, name: i.categoryName }];
    $("edIdpCategory").innerHTML = categoryOptions(i.categoryId, missing);
    $("edIdpLocation").value = i.location;
    $("edIdpBudget").value = i.budget;
    $("edIdpPhotos").value = "";
    pendingPhotos.edIdpPhotos = null;
    renderPhotoTiles("edIdpPhotoTiles", i.images);
    msg("idpDetailMsg", "");
    show("idpDetail");
}

async function triggerCreateIdp(event) {
    event.preventDefault();
    if (roleOf() !== "id") return show("home");
    msg("idpCreateMsg", "Creating project...");

    const r = await api("POST", IDP_URL, {
        category_id: Number($("idpCategory").value),
        title: $("idpTitle").value.trim(),
        description: $("idpDesc").value.trim(),
        location: $("idpLocation").value.trim(),
        budget: Number($("idpBudget").value),
        status: idpCreateStatus,
        images: pendingPhotos.idpPhotos || []
    });
    if (!r.ok) return msg("idpCreateMsg", r.data.message || "Failed to create project.", true);

    await fetchMyIdps(idpCreateStatus);
    show(idpListView(idpCreateStatus));
    flash("Project created successfully.");
}

async function triggerUpdateIdp(event) {
    event.preventDefault();
    if (roleOf() !== "id" || !openIdp) return;
    const status = document.querySelector('input[name="idpStatus"]:checked').value;

    // images stays undefined when no new photos were chosen, so JSON.stringify
    // leaves it out and the backend keeps the current ones.
    const r = await api("PUT", `${IDP_URL}/${openIdp.id}`, {
        category_id: Number($("edIdpCategory").value),
        title: $("edIdpTitle").value.trim(),
        description: $("edIdpDesc").value.trim(),
        location: $("edIdpLocation").value.trim(),
        budget: Number($("edIdpBudget").value),
        status,
        images: pendingPhotos.edIdpPhotos || undefined
    });
    if (!r.ok) return msg("idpDetailMsg", r.data.message || "Failed to update project.", true);

    await fetchMyIdps(status);
    show(idpListView(status));
    flash("Project updated successfully.");
}

async function triggerDeleteIdp(id, title, status) {
    if (roleOf() !== "id") return;
    const ok = await confirmDialog(
        "Delete Project?",
        `Deleting "${title}" is permanent and cannot be undone. The project, its photos, and its views and shortlists will be removed from the platform.`,
        "Delete IDP"
    );
    if (!ok) return;

    const r = await api("DELETE", `${IDP_URL}/${id}`);
    if (!r.ok) return flash(r.data.message || "Failed to delete project.");

    await fetchMyIdps(status);
    show(idpListView(status));
    flash("Project deleted successfully.");
}

document.addEventListener("click", e => {
    const create = e.target.closest("[data-create-idp]");
    if (create) return openIdpCreate(create.dataset.createIdp);
    const open = e.target.closest("[data-open-idp]");
    if (open) return openIdpDetail(Number(open.dataset.openIdp));
    const del = e.target.closest("[data-delete-idp]");
    if (del) {
        const id = Number(del.dataset.deleteIdp);
        const i = myIdps.Current.concat(myIdps.Past).find(x => x.id === id);
        if (i) triggerDeleteIdp(i.id, i.title, i.status);
    }
});

$("idpCreateForm").addEventListener("submit", triggerCreateIdp);
$("idpDetailForm").addEventListener("submit", triggerUpdateIdp);
$("idpDeleteBtn").addEventListener("click", () => {
    if (openIdp) triggerDeleteIdp(openIdp.id, openIdp.title, openIdp.status);
});
wirePhotoInput("idpPhotos", "idpPhotoTiles", "idpCreateMsg", () => []);
wirePhotoInput("edIdpPhotos", "edIdpPhotoTiles", "idpDetailMsg", () => (openIdp ? openIdp.images : []));

wireSearch("currentIdpSearch", q => fetchMyIdps("Current", q), () => renderMyIdps("currentIdps"));
wireSearch("pastIdpSearch", q => fetchMyIdps("Past", q), () => renderMyIdps("pastIdps"));

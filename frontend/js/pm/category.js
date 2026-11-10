// Platform Manager role: create / view / update / suspend / search IDP categories.
//
// Uses /api/pm/categories. Responses are translated by toCategory() in api.js.

const CATEGORY_URL = "/api/pm/categories";

function renderCategories() {
    const n = pmCategories.length;
    $("categoryCount").textContent = `${n} categor${n === 1 ? "y" : "ies"} found`;
    $("categoryRows").innerHTML = n
        ? pmCategories.map(c => `<tr class="clickable" data-open-category="${c.id}">
            <td>${esc(c.name)}</td>
            <td>${esc(c.desc)}</td>
            <td>${badge(c.status)}</td>
        </tr>`).join("")
        : `<tr><td colspan="3" class="empty">${loadError.categories ? "Could not load categories." : "No categories found."}</td></tr>`;
}

const fmtShortDate = iso => {
    const d = new Date(iso);
    return Number.isNaN(d.getTime()) ? "" : `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
};

async function openCategoryDetail(id) {
    const r = await api("GET", `${CATEGORY_URL}/${id}`);
    if (!r.ok) return flash(r.data.message || "Could not open that category.");
    const c = toCategory(r.data.category);
    openCategory = c;
    const suspended = c.status === "Suspended";

    $("catDetailName").textContent = c.name;
    $("catDetailBadge").textContent = c.status;
    $("catDetailBadge").className = "badge " + (suspended ? "suspended" : "active");
    $("catSuspendBtn").hidden = suspended;
    $("catReactivateBtn").hidden = !suspended;
    $("edCatName").value = c.name;
    $("edCatDesc").value = c.desc;
    msg("catDetailMsg", "");
    $("catAssignedTitle").textContent = `Assigned IDPs (${c.idps.length})`;
    $("catAssignedRows").innerHTML = c.idps.length
        ? c.idps.map(i => `<tr>
            <td>${esc(i.title)}</td>
            <td>${esc(i.designer)}</td>
            <td><span class="badge ${i.status.toLowerCase()}">${esc(i.status)}</span></td>
            <td>${fmtShortDate(i.createdAt)}</td>
        </tr>`).join("")
        : `<tr><td colspan="4" class="empty">No IDPs are assigned to this category.</td></tr>`;
    show("categoryDetail");
}

async function triggerCreateCategory(event) {
    event.preventDefault();
    if (roleOf() !== "pm") return show("home");

    const r = await api("POST", CATEGORY_URL, {
        name: $("catName").value.trim(),
        description: $("catDesc").value.trim()
    });
    if (!r.ok) return msg("categoryCreateMsg", r.data.message || "Failed to create category.", true);

    event.target.reset();
    await fetchPmCategories();
    show("categories");
    flash("Category created successfully.");
}

async function triggerUpdateCategory(event) {
    event.preventDefault();
    if (roleOf() !== "pm" || !openCategory) return;

    const r = await api("PUT", `${CATEGORY_URL}/${openCategory.id}`, {
        name: $("edCatName").value.trim(),
        description: $("edCatDesc").value.trim()
    });
    if (!r.ok) return msg("catDetailMsg", r.data.message || "Failed to update category.", true);

    await openCategoryDetail(openCategory.id);
    flash("Category updated successfully.");
}

async function setCategorySuspended(suspend) {
    const c = openCategory;
    if (roleOf() !== "pm" || !c) return;
    const ok = await confirmDialog(
        suspend ? "Suspend Category?" : "Reactivate Category?",
        suspend
            ? `Suspending "${c.name}" hides it from customer search and new project forms. Its projects are not deleted, and you can reactivate it later.`
            : `Reactivating "${c.name}" shows it in customer search and new project forms again.`,
        suspend ? "Suspend" : "Reactivate"
    );
    if (!ok) return;

    const r = await api("PATCH", `${CATEGORY_URL}/${c.id}/status`, { is_suspended: suspend });
    if (!r.ok) return msg("catDetailMsg", r.data.message || "Failed to change category status.", true);

    await openCategoryDetail(c.id);
    flash(suspend ? "Category suspended successfully." : "Category reactivated successfully.");
}

document.addEventListener("click", e => {
    const row = e.target.closest("[data-open-category]");
    if (row) openCategoryDetail(Number(row.dataset.openCategory));
});

$("categoryCreateForm").addEventListener("submit", triggerCreateCategory);
$("categoryDetailForm").addEventListener("submit", triggerUpdateCategory);
$("catSuspendBtn").addEventListener("click", () => setCategorySuspended(true));
$("catReactivateBtn").addEventListener("click", () => setCategorySuspended(false));
wireSearch("categorySearch", fetchPmCategories, renderCategories);

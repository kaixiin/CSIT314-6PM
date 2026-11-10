// Platform Manager role: generate a daily, weekly or monthly report.
// Reports are calculated by the backend when asked for, not stored.
//
// Uses GET /api/pm/reports?period=daily|weekly|monthly.

const PERIODS = {
    daily: { title: "Daily report", label: "Today", versus: "vs yesterday" },
    weekly: { title: "Weekly report", label: "Last 7 days", versus: "vs previous 7 days" },
    monthly: { title: "Monthly report", label: "Last 30 days", versus: "vs previous 30 days" }
};
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

let reportPeriod = "daily";

// The backend sends plain dates (2026-11-08), which are read here as local dates.
function fmtReportDate(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    const date = new Date(y, m - 1, d);
    return `${WEEKDAYS[date.getDay()]}, ${d} ${MONTHS[m - 1]}`;
}

function fmtGeneratedOn(d) {
    const hour = d.getHours() % 12 || 12;
    const minute = String(d.getMinutes()).padStart(2, "0");
    return `Generated on ${WEEKDAYS[d.getDay()]}, ${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}, ${hour}:${minute} ${d.getHours() < 12 ? "AM" : "PM"}`;
}

function selectPeriod(period) {
    reportPeriod = period;
    document.querySelectorAll(".period [data-period]").forEach(b => b.classList.toggle("act", b.dataset.period === period));
}

// Back to "No report yet", used when a Platform Manager logs in.
function resetReport() {
    selectPeriod("daily");
    $("reportEmpty").hidden = false;
    $("reportResult").hidden = true;
    $("reportEmpty").textContent = "No report yet. Choose a period and click Generate.";
}

function setChange(id, current, previous, versus) {
    const diff = current - previous;
    $(id).textContent = diff === 0 ? `No change ${versus}` : `${diff > 0 ? "+" : ""}${diff.toLocaleString("en-US")} ${versus}`;
    $(id).className = "change" + (diff > 0 ? " up" : diff < 0 ? " down" : "");
}

function renderReport(period, data) {
    const p = PERIODS[period];
    const prev = data.previous;
    const end = `${fmtReportDate(data.end_date)} ${data.end_date.slice(0, 4)}`;

    $("reportTitle").textContent = p.title;
    $("reportCovers").textContent = period === "daily"
        ? `${p.label}: ${end}`
        : `${p.label}: ${fmtReportDate(data.start_date)} to ${end}`;
    $("reportGenerated").textContent = fmtGeneratedOn(new Date());

    $("repNew").textContent = data.new_idps.toLocaleString("en-US");
    $("repViews").textContent = data.views.toLocaleString("en-US");
    $("repSaves").textContent = data.shortlists.toLocaleString("en-US");
    setChange("repNewChange", data.new_idps, prev.new_idps, p.versus);
    setChange("repViewsChange", data.views, prev.views, p.versus);
    setChange("repSavesChange", data.shortlists, prev.shortlists, p.versus);

    $("reportTop").innerHTML = data.top_projects.length
        ? data.top_projects.map((t, n) => `<tr>
            <td>${n + 1}</td>
            <td>${esc(t.title)}</td>
            <td>${esc(t.category_name)}</td>
            <td>${t.views.toLocaleString("en-US")}</td>
        </tr>`).join("")
        : `<tr><td colspan="4" class="empty">No projects were viewed in this period.</td></tr>`;

    $("reportEmpty").hidden = true;
    $("reportResult").hidden = false;
}

async function triggerGenerateReport() {
    if (roleOf() !== "pm") return;
    const period = reportPeriod;
    const r = await api("GET", `/api/pm/reports?period=${period}`);
    if (!r.ok) {
        $("reportResult").hidden = true;
        $("reportEmpty").hidden = false;
        $("reportEmpty").textContent = r.data.message || "Could not generate the report.";
        return;
    }
    renderReport(period, r.data);
}

document.querySelectorAll(".period [data-period]").forEach(b =>
    b.addEventListener("click", () => selectPeriod(b.dataset.period)));
$("generateReport").addEventListener("click", triggerGenerateReport);

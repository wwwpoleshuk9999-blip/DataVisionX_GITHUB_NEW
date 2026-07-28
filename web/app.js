const API = "";

function saveToken() {
    localStorage.setItem("token", document.getElementById("token").value);
    alert("Token saved");
    loadAll();
}

function headers() {
    const token = localStorage.getItem("token");
    return token
        ? { "Authorization": "Bearer " + token }
        : {};
}

async function loadDashboard() {
    const r = await fetch(API + "/dashboard/status", { headers: headers() });
    const d = await r.json();

    document.getElementById("system").innerHTML = `
<div class="card">
<h3>🚀 ${d.platform}</h3>
Version: ${d.version}<br>
Status: <b>${d.status}</b><br>
Health: <b>${d.health}</b><br>
Python: ${d.python}<br>
OS: ${d.os}<br>
Uptime: ${d.uptime_seconds}s<br>
Plugins: ${d.plugins_running}/${d.plugins_total}
</div>`;
}

async function loadRuntime() {
    const r = await fetch(API + "/health");
    const d = await r.json();

    document.getElementById("runtime").innerHTML = `
<div class="card">
<b>Status:</b> ${d.health.status}<br>
<b>Health:</b> ${d.health.health}<br>
<b>Version:</b> ${d.health.version}<br>
<b>Python:</b> ${d.health.python}<br>
<b>Platform:</b> ${d.health.platform}<br>
<b>Uptime:</b> ${d.health.uptime}
</div>`;
}

async function loadPlugins() {
    const r = await fetch(API + "/plugins", { headers: headers() });
    const d = await r.json();

    let html = "";

    (d.plugins || []).forEach(p => {
        html += `
<div class="card">
<h3>📦 ${p.name}</h3>
ID: ${p.id}<br>
Version: ${p.version}<br>
Status: <b>${p.status}</b><br><br>

<button onclick="pluginAction('${p.id}','start')">▶ START</button>
<button onclick="pluginAction('${p.id}','stop')">⏹ STOP</button>
<button onclick="pluginAction('${p.id}','restart')">🔄 RESTART</button>

</div>`;
    });

    document.getElementById("plugins").innerHTML = html;
}

async function pluginAction(id, action) {

    const r = await fetch(`/plugins/${id}/${action}`, {
        method: "POST",
        headers: headers()
    });

    const d = await r.json();

    alert(d.status || d.detail || "Done");

    loadAll();
}

async function loadRegistry() {

    try {

        const r = await fetch("/registry", {
            headers: headers()
        });

        if (!r.ok) {
            document.getElementById("registry").innerHTML =
                '<div class="card">Registry API unavailable</div>';
            return;
        }

        const d = await r.json();

        let html = "";

        (d.registry || []).forEach(item => {
            html += `
<div class="card">
<b>${item.id}</b><br>
Version: ${item.version}
</div>`;
        });

        document.getElementById("registry").innerHTML = html;

    } catch {

        document.getElementById("registry").innerHTML =
            '<div class="card">Registry unavailable</div>';

    }
}

async function loadEvents() {

    try {

        const r = await fetch("/events", {
            headers: headers()
        });

        if (!r.ok) {
            document.getElementById("events").innerHTML =
                '<div class="card">Events unavailable</div>';
            return;
        }

        const d = await r.json();

        let html = "";

        (d.events || []).forEach(e => {
            html += `
<div class="card">
<b>${e.action || "-"}</b><br>
Source: ${e.source || "-"}<br>
User: ${e.user || "-"}
</div>`;
        });

        document.getElementById("events").innerHTML = html;

    } catch {

        document.getElementById("events").innerHTML =
            '<div class="card">Events unavailable</div>';

    }
}

function loadAll() {
    loadDashboard();
    loadRuntime();
    loadPlugins();
    loadRegistry();
    loadEvents();
}

window.onload = function () {

    const token = localStorage.getItem("token");

    if (token) {
        document.getElementById("token").value = token;
    }

    loadAll();

    setInterval(loadAll, 5000);
};

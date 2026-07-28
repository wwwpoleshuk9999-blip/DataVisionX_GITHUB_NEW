const API = "";

function headers() {
    const token = localStorage.getItem("token") || "";

    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    };
}

function saveToken() {
    const token = document.getElementById("token").value;

    localStorage.setItem("token", token);

    loadAll();
}

function statusClass(status) {

    switch ((status || "").toUpperCase()) {

        case "RUNNING":
            return "status-running";

        case "STOPPED":
            return "status-stopped";

        default:
            return "status-loading";
    }
}

async function loadDashboard() {

    const r = await fetch(API + "/dashboard/status", {
        headers: headers()
    });

    const data = await r.json();

    document.getElementById("system").innerHTML = `
<div class="card">
<h3>🚀 ${data.platform}</h3>
<b>Version:</b> ${data.version}<br>
<b>Status:</b> <span class="${statusClass(data.status)}">${data.status}</span><br>
<b>Health:</b> ${data.health}<br>
<b>Python:</b> ${data.python}<br>
<b>OS:</b> ${data.os}<br>
<b>Uptime:</b> ${data.uptime_seconds}s<br>
<b>Plugins:</b> ${data.plugins_running}/${data.plugins_total}
</div>`;
}

async function loadRuntime() {

    const r = await fetch(API + "/system", {
        headers: headers()
    });

    const data = await r.json();

    document.getElementById("runtime").innerHTML = `
<div class="card">
<b>Status:</b>
<span class="${statusClass(data.status)}">${data.status}</span><br>

<b>Health:</b>
${data.health}<br>

<b>Version:</b>
${data.version}<br>

<b>Python:</b>
${data.python}<br>

<b>Platform:</b>
${data.platform}<br>

<b>Uptime:</b>
${data.uptime}
</div>`;
}

async function loadPlugins() {

    const r = await fetch(API + "/plugins", {
        headers: headers()
    });

    const data = await r.json();

    let html = "";

    data.plugins.forEach(p => {

        html += `
<div class="card">

<h3>📦 ${p.name}</h3>

ID: ${p.id}<br>

Version: ${p.version}<br>

Status:
<span class="${statusClass(p.status)}">${p.status}</span>

<br><br>

<button onclick="pluginAction('${p.id}','start')">
▶ START
</button>

<button onclick="pluginAction('${p.id}','stop')">
⏹ STOP
</button>

<button onclick="pluginAction('${p.id}','restart')">
🔄 RESTART
</button>

</div>`;
    });

    document.getElementById("plugins").innerHTML = html;
}async function pluginAction(id, action) {

    const r = await fetch(
        API + `/plugins/${id}/${action}`,
        {
            method: "POST",
            headers: headers()
        }
    );

    const data = await r.json();

    alert(data.status || data.detail || "Done");

    loadPlugins();
}

async function loadRegistry() {

    try {

        const r = await fetch(API + "/registry", {
            headers: headers()
        });

        if (!r.ok) {
            document.getElementById("registry").innerHTML =
                `<div class="card">Registry API unavailable</div>`;
            return;
        }

        const data = await r.json();

        let html = "";

        data.forEach(item => {

            html += `
<div class="card">
<b>${item.id}</b><br>
Version: ${item.version}
</div>`;
        });

        document.getElementById("registry").innerHTML = html;

    } catch {

        document.getElementById("registry").innerHTML =
            `<div class="card">Registry unavailable</div>`;
    }
}

async function loadEvents() {

    try {

        const r = await fetch(API + "/events", {
            headers: headers()
        });

        if (!r.ok) {

            document.getElementById("events").innerHTML =
                `<div class="card">Event API unavailable</div>`;
            return;
        }

        const data = await r.json();

        let html = "";

        data.forEach(e => {

            html += `
<div class="card">
<b>${e.action}</b><br>
Source: ${e.source}<br>
User: ${e.user}
</div>`;
        });

        document.getElementById("events").innerHTML = html;

    } catch {

        document.getElementById("events").innerHTML =
            `<div class="card">Events unavailable</div>`;
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

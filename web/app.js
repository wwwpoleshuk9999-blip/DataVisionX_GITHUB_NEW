function saveToken() {
    const token = document.getElementById("token").value;
    localStorage.setItem("token", token);

    alert("Token saved");

    loadDashboard();
    loadRuntime();
    loadPlugins();
    loadRegistry();
    loadEvents();
}

function headers() {
    return {
        "Authorization": "Bearer " + localStorage.getItem("token")
    };
}

async function loadRuntime() {
    const r = await fetch("/health", {
        headers: headers()
    });

    const data = await r.json();

    document.getElementById("runtime").innerHTML = `
    <div class="card">
        Status: <b>${data.health.status}</b><br>
        Process: <b>${data.health.process}</b><br>
        PID: ${data.health.pid}<br>
        Plugins: ${data.health.plugins}
    </div>
    `;

}
async function loadDashboard() {

    const r = await fetch("/dashboard/status", {
        headers: headers()
    });

    const data = await r.json();

    document.getElementById("system").innerHTML = `
    <div class="card">
        🚀 <b>${data.platform}</b><br>
        Status: <b>${data.status}</b><br>
        Health: <b>${data.health}</b><br>
        Python: ${data.python}<br>
        OS: ${data.os}<br>
        Uptime: ${data.uptime_seconds} sec<br>
        Plugins: ${data.plugins_total}<br>
        Running: 🟢 ${data.plugins_running}<br>
        Stopped: 🔴 ${data.plugins_stopped}
    </div>
    `;
}


async function loadPlugins() {

    const r = await fetch("/plugins", {
        headers: headers()
    });

    const plugins = await r.json();

    let html = "";

    plugins.forEach(p => {
        html += `
        <div class="card">
            <b>${p.id}</b><br>
            Version: ${p.version}<br>
            Status: ${p.status}
        </div>
        `;
    });

    document.getElementById("plugins").innerHTML = html;
}


async function loadRegistry() {

    const r = await fetch("/registry", {
        headers: headers()
    });

    const registry = await r.json();

    let html = "";

    registry.forEach(item => {
        html += `
        <div class="card">
            <b>${item.id}</b><br>
            Version: ${item.version}
        </div>
        `;
    });

    document.getElementById("registry").innerHTML = html;
}


async function loadEvents() {

    const r = await fetch("/events", {
        headers: headers()
    });

    const events = await r.json();

    let html = "";

    events.forEach(e => {
        html += `
        <div class="card">
            <b>${e.action}</b><br>
            Source: ${e.source}<br>
            User: ${e.user}
        </div>
        `;
    });

    document.getElementById("events").innerHTML = html;
}

window.onload = function() {
    loadDashboard();
    loadRuntime();
    loadPlugins();
    loadRegistry();
    loadEvents();
};


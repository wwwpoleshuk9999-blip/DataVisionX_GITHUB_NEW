const API = "";
let pluginsCache = {};

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

function renderPlugin(p) {
    return `
<div class="card" id="plugin-${p.id}">
<h3>📦 ${p.name}</h3>
ID: ${p.id}<br>
Version: ${p.version}<br>
Status: <b>${p.status}</b><br><br>

<button onclick="pluginAction('${p.id}','start')">▶ START</button>
<button onclick="pluginAction('${p.id}','stop')">⏹ STOP</button>
<button onclick="pluginAction('${p.id}','restart')">🔄 RESTART</button>

</div>`;
}

function updatePluginCard(plugin) {
    pluginsCache[plugin.id] = plugin;
    const el = document.getElementById("plugin-" + plugin.id);
    if (el) {
        el.outerHTML = renderPlugin(plugin);
    }
}

async function loadPlugins() {
    const r = await fetch(API + "/plugins", { headers: headers() });
    const d = await r.json();

    pluginsCache = {};

    (d.plugins || []).forEach(p => {
        pluginsCache[p.id] = p;
    });

    let html = "";

    (d.plugins || []).forEach(p => {
        html += renderPlugin(p);
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

// =========================
// Phoenix Build 006.1
// UI helpers
// =========================

function showToast(message, ok = true) {

    let toast = document.getElementById("toast");

    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";

        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.padding = "12px 18px";
        toast.style.borderRadius = "8px";
        toast.style.color = "#fff";
        toast.style.fontWeight = "bold";
        toast.style.zIndex = "99999";
        toast.style.transition = "0.3s";

        document.body.appendChild(toast);
    }

    toast.style.background = ok ? "#28a745" : "#d9534f";
    toast.innerText = message;
    toast.style.display = "block";

    clearTimeout(window.toastTimer);

    window.toastTimer = setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}


// =========================
// Phoenix Build 006.1
// WebSocket Live
// =========================

function updateWSStatus(online) {
    const el = document.getElementById("ws-status");
    if (!el) return;

    el.textContent = online
        ? "🟢 WebSocket Online"
        : "🔴 WebSocket Offline";
}

function connectWebSocket() {

    if (ws) {
        try {
            ws.close();
        } catch (e) {}
    }

    const proto = location.protocol === "https:" ? "wss://" : "ws://";

    ws = new WebSocket(proto + location.host + "/ws");

    ws.onopen = () => {
        console.log("WebSocket connected");
        updateWSStatus(true);
        showToast("WebSocket connected");
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
        updateWSStatus(false);

        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (e) => {
        console.error("WebSocket error", e);
        updateWSStatus(false);
    };

    ws.onmessage = (event) => {

        console.log("WS:", event.data);

        try {

            const msg = JSON.parse(event.data);

            switch (msg.event) {

                case "plugin_started":
                case "plugin_stopped":
                case "plugin_failed":

                    fetch(API + "/plugins/" + msg.data.plugin + "/status", {
                        headers: headers()
                    })
                    .then(r => r.json())
                    .then(updatePluginCard)
                    .catch(() => loadPlugins());

                    break;

                case "ai_chat_completed":
                    loadEvents();
                    break;

                default:
                    loadRuntime();
            }

        } catch (e) {

            if (event.data !== "ping") {
                console.error("WS parse error:", e);
            }

        }

    };
}


// =========================
// Phoenix Build 006.1
// Auto start
// =========================

window.addEventListener("load", () => {

    console.log("Phoenix Dashboard started");

    try {
        loadAll();
    } catch (e) {
        console.error(e);
    }

    connectWebSocket();

    // Backup sync every 60 seconds
    setInterval(() => {
        loadRuntime();
        loadPlugins();
        loadDashboard();
    }, 60000);

});


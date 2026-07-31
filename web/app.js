
window.onerror = function(msg, src, line, col, err){
"<div style='background:#900;color:#fff;padding:10px;font-size:16px;word-break:break-all'>JS ERROR:<br>"+msg+"<br>Line: "+line+"</div>"
);

    alert("JS ERROR: " + msg + "\nLine: " + line);
    console.error(err);
};

const API = "";
let ws = null;

function saveToken() {
    localStorage.setItem(
        "token",
        document.getElementById("token").value
    );

    alert("Token saved");
    console.log("Calling loadAll()");
    loadAll();
}

function headers() {
    const token = localStorage.getItem("token");

    return token
        ? { Authorization: "Bearer " + token }
        : {};
}

async function loadDashboard() {
    console.log("Loading dashboard");

    const r = await fetch(
        API + "/dashboard/status",
        { headers: headers() }
    );

    console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
const d = await r.json();

    console.log("UPDATE SYSTEM"); document.getElementById("system").innerHTML = `
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
    alert("loadRuntime START");
    console.log("Loading runtime");
console.log("LOAD RUNTIME");

    const r = await fetch(API + "/health", { headers: headers() });

    console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
const d = await r.json();

    console.log("UPDATE RUNTIME"); document.getElementById("runtime").innerHTML = `
<div class="card">

<b>Status:</b> ${d.status}<br>
<b>Process:</b> ${d.process}<br>
<b>Plugins:</b> ${d.plugins}<br>
<b>Running:</b> ${d.plugins_running}<br>
<b>Stopped:</b> ${d.plugins_stopped}<br>
<b>Uptime:</b> ${d.uptime}<br>
<b>Last action:</b> ${d.last_action}

</div>`;
}


async function loadPlugins() {
    alert("loadPlugins START");
    console.log("Loading plugins");
console.log("LOAD PLUGINS");

    const r = await fetch(
        API + "/plugins",
        { headers: headers() }
    );

    console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
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

    console.log("UPDATE PLUGINS"); document.getElementById("plugins").innerHTML = html;
}

async function pluginAction(id, action) {

    const r = await fetch(API + `/plugins/${id}/${action}`, {
        method: "POST",
        headers: headers()
    });

    console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
const d = await r.json();

    alert(d.status || d.detail || "Done");

    console.log("Calling loadAll()");
    loadAll();
}


async function recoverPlugin(id) {

    const r = await fetch(
        API + `/plugins/${id}/restart`,
        {
            method: "POST",
            headers: headers()
        }
    );

    const d = await r.json();

    alert(
        d.status || d.message || "Recovery requested"
    );

    loadAll();
}


async function loadRegistry() {

    try {

        const r = await fetch(API + "/registry", {
            headers: headers()
        });

        if (!r.ok) {
            document.getElementById("registry").innerHTML =
                '<div class="card">Registry unavailable</div>';
            return;
        }

        console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
const d = await r.json();

        let html = "";

        (d.registry || []).forEach(item => {

            html += `
<div class="card">
<h3>🧩 ${item.name}</h3>
ID: ${item.id}<br>
Version: ${item.version}<br>
Status: <b>${item.status}</b><br>
Path: ${item.path}<br>
Installed: ${item.installed}
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

        const r = await fetch(API + "/events", {
            headers: headers()
        });

        if (!r.ok) {
            document.getElementById("events").innerHTML =
                '<div class="card">Events unavailable</div>';
            return;
        }

        console.log("HTTP", r.url, r.status);
"<div style='background:#222;color:#0f0;padding:4px;margin:2px'>HTTP "+r.status+" "+r.url+"</div>"
);
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



async function loadHealth() {

    const r = await fetch(
        API + "/health/plugins",
        {
            headers: headers()
        }
    );

    if (!r.ok) {
        document.getElementById("health").innerHTML =
            '<div class="card">Health unavailable</div>';
        return;
    }

    const d = await r.json();

    let html = "";

    Object.entries(d.plugins || {}).forEach(([id, p]) => {

        html += `
<div class="card">

<h3>❤️ ${id}</h3>

Status:
<b>${p.status}</b><br>

Health:
<b>${p.health}</b><br>

Last start:
${p.last_start || "-"}<br>

Restarts:
${p.restart_count}<br>

Error:
${p.last_error || "none"}

</div>
`;

    });

    document.getElementById("health").innerHTML = html;
}


async function loadAll() {

    try { await loadDashboard(); } catch(e) { console.error("Dashboard:", e); alert("Dashboard: " + e); document.getElementById("system").innerHTML="<pre>"+String(e)+"</pre>"; }

    try { await loadRuntime(); } catch(e) { console.error("Runtime:", e); alert("Runtime: " + e); document.getElementById("runtime").innerHTML="<pre>"+String(e)+"</pre>"; }

    try { await loadPlugins(); } catch(e) { console.error("Plugins:", e); alert("Plugins: " + e); document.getElementById("plugins").innerHTML="<pre>"+String(e)+"</pre>"; }

    try { 
        await loadHealth(); 
    } catch(e) { 
        console.error("Health:", e); 
        document.getElementById("health").innerHTML =
            "<pre>"+String(e)+"</pre>";
    }

    try { await loadRegistry(); } catch(e) { 
        console.error("Registry:", e); 
        alert("Registry: " + e); 
        document.getElementById("registry").innerHTML =
            "<pre>"+String(e)+"</pre>"; 
    }

    try { await loadEvents(); } catch(e) { console.error("Events:", e); alert("Events: " + e); document.getElementById("events").innerHTML="<pre>"+String(e)+"</pre>"; }
}

function connectWebSocket() {

    const protocol =
        location.protocol === "https:" ? "wss" : "ws";

    ws = new WebSocket(
        `${protocol}://${location.host}/ws`
    );

    ws.onopen = () => {
        console.log("WebSocket connected");

        const el = document.getElementById("ws-status");
        if (el) {
            el.className = "websocket-status ws-online";
            el.innerHTML = "🟢 WebSocket Online";
        }
    };

    ws.onmessage = (event) => {

        console.log("EVENT:", event.data);

        const box = document.getElementById("live-events");

        if (box) {
            const time = new Date().toLocaleTimeString();

            box.innerHTML =
                `<div class="event-item">
                <div class="event-time">${time}</div>
                ${event.data}
                </div>` + box.innerHTML;
        }

        console.log("Calling loadAll()");
    loadAll();
    };

    ws.onclose = () => {

        console.log("WebSocket disconnected");

        const el = document.getElementById("ws-status");
        if (el) {
            el.className = "websocket-status ws-offline";
            el.innerHTML = "🔴 WebSocket Offline";
        }

        setTimeout(
            connectWebSocket,
            2000
        );
    };
}

window.onload = function () {

    console.log("Dashboard started");


    const token = localStorage.getItem("token");

    if (token) {
        document.getElementById("token").value = token;
    } else {
        const defaultToken = "7a9f1aaf67a1d93eda3ff34b5de6ca0ad9aee7f4dd043510c1962ec2026cc867";

        localStorage.setItem("token", defaultToken);
        document.getElementById("token").value = defaultToken;

        console.log("Default admin token loaded");
    }

    console.log("Calling loadAll()");
    loadAll();

    console.log("Connecting WebSocket");
    connectWebSocket();
};

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


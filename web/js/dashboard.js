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

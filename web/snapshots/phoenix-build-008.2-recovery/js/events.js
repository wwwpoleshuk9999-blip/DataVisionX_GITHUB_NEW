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


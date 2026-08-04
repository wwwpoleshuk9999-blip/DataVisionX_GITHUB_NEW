async function loadKPI(){

    const box = document.getElementById("kpi-bar");
    if(!box) return;

    try{

        const r = await fetch("/metrics/system",{headers:headers()});
        const m = await r.json();

        box.innerHTML = `
<div class="kpi-grid">

<div class="kpi-item">
<span>⚡ CPU</span>
<b>${m.cpu_percent ?? 0}%</b>
</div>

<div class="kpi-item">
<span>🧠 RAM</span>
<b>${m.memory_percent ?? 0}%</b>
</div>

<div class="kpi-item">
<span>💾 Disk</span>
<b>${m.disk_percent ?? 0}%</b>
</div>

<div class="kpi-item">
<span>📈 Load</span>
<b>${(m.load_average||[]).join(" | ")}</b>
</div>

</div>`;
    }catch(e){
        box.innerHTML = "KPI unavailable";
    }
}

document.addEventListener("DOMContentLoaded",()=>{
    loadKPI();
    setInterval(loadKPI,3000);
});

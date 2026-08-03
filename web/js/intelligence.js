async function loadIntelligencePanel(){

    const box = document.getElementById("intelligence-panel");

    if (!box) return;

    try {

        const r = await fetch("/metrics/system");
        const x = await r.json();

        box.innerHTML = `
        <div class="intel-grid">

            <div class="intel-card">
                <span>⚡ CPU</span>
                <b>${x.cpu_percent || 0}%</b>
            </div>

            <div class="intel-card">
                <span>🧠 Memory</span>
                <b>${x.memory_percent || 0}%</b>
            </div>

            <div class="intel-card">
                <span>💾 Disk</span>
                <b>${x.disk_percent || 0}%</b>
            </div>

            <div class="intel-card">
                <span>📈 Load</span>
                <b>${(x.load_average || []).join(" | ")}</b>
            </div>

        </div>`;

    } catch(e){

        box.innerHTML = `
        <div class="intel-card">
        Intelligence offline
        </div>`;

    }
}


document.addEventListener(
"DOMContentLoaded",
()=>{

    loadIntelligencePanel();

    setInterval(
        loadIntelligencePanel,
        5000
    );

});

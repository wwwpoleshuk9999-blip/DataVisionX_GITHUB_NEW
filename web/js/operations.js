async function loadOperationsCenter(){

    const box=document.getElementById("operations-center");
    if(!box) return;

    try{

        const r=await fetch("/metrics/system",{headers:headers()});
        const m=await r.json();

        box.innerHTML=`
<div class="operations-grid">

<div class="operation-card">
<div class="operation-title">CPU</div>
<div class="operation-value">${m.cpu_percent ?? 0}%</div>
<div class="operation-footer">Processor Load</div>
</div>

<div class="operation-card">
<div class="operation-title">Memory</div>
<div class="operation-value">${m.memory_percent ?? 0}%</div>
<div class="operation-footer">RAM Usage</div>
</div>

<div class="operation-card">
<div class="operation-title">Disk</div>
<div class="operation-value">${m.disk_percent ?? 0}%</div>
<div class="operation-footer">Storage</div>
</div>

<div class="operation-card">
<div class="operation-title">Load</div>
<div class="operation-value">${(m.load_average||[]).join(" | ")}</div>
<div class="operation-footer">System Average</div>
</div>

</div>`;
    }catch(e){
        box.innerHTML='<div class="operation-card">Operations Center unavailable</div>';
    }
}

document.addEventListener("DOMContentLoaded",()=>{
    loadOperationsCenter();
    setInterval(loadOperationsCenter,5000);
});

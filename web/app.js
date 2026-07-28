function saveToken() {

    const token = document.getElementById("token").value;

    localStorage.setItem(
        "token",
        token
    );

    alert("Token saved");

    loadAll();
}



function headers() {

    const token = localStorage.getItem("token");

    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    };

}



async function loadDashboard(){

    const r = await fetch(
        "/dashboard/status",
        {
            headers: headers()
        }
    );

    const data = await r.json();


    document.getElementById("system").innerHTML = `

    <div class="card">

    🚀 <b>${data.platform}</b><br>

    Version: ${data.version}<br>

    Status:
    <b>${data.status}</b><br>

    Health:
    <b>${data.health}</b><br>

    Python:
    ${data.python}<br>

    OS:
    ${data.os}<br>

    Uptime:
    ${data.uptime_seconds}s<br>

    Plugins:
    ${data.plugins_total}<br>

    Running:
    🟢 ${data.plugins_running}<br>

    Stopped:
    🔴 ${data.plugins_stopped}

    </div>

    `;

}




async function loadRuntime(){

    const r = await fetch(
        "/health",
        {
            headers: headers()
        }
    );


    const data = await r.json();


    document.getElementById("runtime").innerHTML = `

    <div class="card">

    Status:
    <b>${data.health.status}</b><br>

    Process:
    ${data.health.process}<br>

    PID:
    ${data.health.pid}<br>

    Plugins:
    ${data.health.plugins}

    </div>

    `;

}




async function loadPlugins(){

    const r = await fetch(
        "/plugins",
        {
            headers: headers()
        }
    );


    const data = await r.json();


    let html="";


    data.plugins.forEach(
        p=>{


        html += `

        <div class="card">

        <h3>
        📦 ${p.name}
        </h3>


        ID:
        ${p.id}<br>


        Version:
        ${p.version}<br>


        Status:
        <b>${p.status}</b>


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


        </div>

        `;


        }
    );


    document.getElementById("plugins").innerHTML = html;


}




async function pluginAction(
    id,
    action
){


    const r = await fetch(

        `/plugins/${id}/${action}`,

        {

            method:"POST",

            headers:headers()

        }

    );


    const data = await r.json();


    alert(
        `${id}: ${data.status || data.detail}`
    );


    loadPlugins();

    loadEvents();

}





async function loadRegistry(){

    const r = await fetch(
        "/registry",
        {
            headers:headers()
        }
    );


    const data = await r.json();


    let html="";


    data.forEach(
        item=>{


        html += `

        <div class="card">

        Plugin:
        <b>${item.id}</b><br>

        Version:
        ${item.version}

        </div>

        `;


        }
    );


    document.getElementById(
        "registry"
    ).innerHTML = html;


}




async function loadEvents(){

    const r = await fetch(
        "/events",
        {
            headers:headers()
        }
    );


    const data = await r.json();


    let html="";


    data.forEach(
        e=>{


        html += `

        <div class="card">

        Action:
        <b>${e.action}</b><br>

        Source:
        ${e.source}<br>

        User:
        ${e.user}

        </div>

        `;


        }
    );


    document.getElementById(
        "events"
    ).innerHTML = html;


}




function loadAll(){

    loadDashboard();

    loadRuntime();

    loadPlugins();

    loadRegistry();

    loadEvents();

}


window.onload = function () {

    loadAll();

    // Автообновление Dashboard каждые 2 секунды
    setInterval(() => {

        loadDashboard();
        loadRuntime();
        loadPlugins();
        loadRegistry();
        loadEvents();

    }, 2000);

};

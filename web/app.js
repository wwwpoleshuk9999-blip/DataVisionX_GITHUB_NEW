function saveToken(){

    const token =
    document.getElementById("token").value;

    localStorage.setItem(
        "token",
        token
    );

    alert("Token saved");

    loadDashboard();
    loadPlugins();
    loadRegistry();
    loadEvents();

}



function headers(){

    return {

        "Authorization":
        "Bearer " +
        localStorage.getItem("token")

    };

}




async function loadDashboard(){

    const r = await fetch(
        "/dashboard/status",
        {
            headers:headers()
        }
    );

    const data = await r.json();


    document.getElementById("system").innerHTML = `

    <div class="card">

    🚀 <b>${data.platform}</b>

    <br>
    Status: <b>${data.status}</b>

    <br>
    Health: <b>${data.health}</b>

    <br>
    Python: ${data.python}

    <br>
    OS: ${data.os}

    <br>
    Uptime: ${data.uptime_seconds} sec

    <br>
    Plugins:
    ${data.plugins_total}

    <br>
    Running:
    🟢 ${data.plugins_running}

    <br>
    Stopped:
    🔴 ${data.plugins_stopped}

    </div>

    `;

}





async function loadPlugins(){

    const r = await fetch(
        "/plugins",
        {
            headers:headers()
        }
    );


    const data = await r.json();


    let html="";


    data.plugins.forEach(p=>{

        html += `

        <div class="card">

        🧩 <b>${p.name}</b>

        <br>
        ID: ${p.id}

        <br>
        Version: ${p.version}

        <br>
        Status:
        <b>${p.status}</b>

        <br><br>


        <button onclick="action('${p.id}','start')">
        ▶ START
        </button>


        <button onclick="action('${p.id}','stop')">
        ⏹ STOP
        </button>


        <button onclick="action('${p.id}','restart')">
        🔄 RESTART
        </button>


        </div>

        `;

    });


    document.getElementById("plugins").innerHTML =
    html;

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


    data.registry.forEach(p=>{


        html += `

        <div class="card">

        📦 <b>${p.name}</b>

        <br>

        ID:
        ${p.id}

        <br>

        Version:
        ${p.version}

        <br>

        Installed:
        ${p.installed}

        <br>

        Status:
        ${p.status}

        </div>

        `;


    });



    document.getElementById("registry").innerHTML =
    html;


}





async function action(id,cmd){

    await fetch(

        `/plugins/${id}/${cmd}`,

        {

            method:"POST",

            headers:headers()

        }

    );


    loadDashboard();
    loadPlugins();
    loadRegistry();
    loadEvents();

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


    data.events.reverse().forEach(e=>{


        html += `

        <div class="card">

        🕒 ${e.time}

        <br>

        ⚙ ${e.action}

        <br>

        Plugin:
        ${e.plugin}

        <br>

        User:
        ${e.user}

        </div>

        `;


    });


    document.getElementById("events").innerHTML =
    html;

}





window.onload=function(){

    loadDashboard();
    loadPlugins();
    loadRegistry();
    loadEvents();

}

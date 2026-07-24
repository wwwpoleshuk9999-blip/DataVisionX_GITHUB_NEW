async function loadDashboard(){

    const health = await fetch(
        "/health"
    );

    const healthData = await health.json();


    document.getElementById(
        "status"
    ).innerHTML =
        `
        <div class="card">
        Status: ${healthData.status}
        </div>
        `;


    const response = await fetch(
        "/plugins"
    );

    const data = await response.json();


    const list =
        document.getElementById(
            "plugins"
        );


    list.innerHTML = "";


    data.plugins.forEach(
        plugin => {

            list.innerHTML +=
            `
            <li class="plugin">
            ${plugin.name}
            |
            ${plugin.version}
            |
            ${plugin.status}
            </li>
            `;

        }
    );
}


loadDashboard();


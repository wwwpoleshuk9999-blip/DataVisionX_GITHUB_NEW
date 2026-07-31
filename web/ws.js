
function showToast(text) {
    const t = document.getElementById("toast");
    if (!t) return;

    t.innerText = text;
    t.style.display = "block";

    setTimeout(() => {
        t.style.display = "none";
    }, 3000);
}

let socket = null;

function connectWebSocket() {

    const protocol = location.protocol === "https:" ? "wss" : "ws";

    socket = new WebSocket(
        `${protocol}://${location.host}/ws`
    );


    socket.onopen = () => {
        console.log("✅ WebSocket connected");
    };


    socket.onclose = () => {

        console.log("❌ WebSocket disconnected");

        setTimeout(
            connectWebSocket,
            3000
        );
    };


    socket.onmessage = (event) => {

        console.log("WS EVENT:", event.data);


        try {

            const data = JSON.parse(event.data);


            if (data.event) {

                let plugin = "";

                if (data.data && data.data.plugin) {
                    plugin = " : " + data.data.plugin;
                }


                showToast(
                    "📢 " + data.event + plugin
                );


                if (
                    data.event === "plugin_started" ||
                    data.event === "plugin_stopped" ||
                    data.event === "plugin_failed" ||
                    data.event === "plugin_recoveredd"
                ) {

                    if (typeof loadPlugins === "function")
                        loadPlugins();

                    if (typeof loadRegistry === "function")
                        loadRegistry();

                    if (typeof loadHealth === "function")
                        loadHealth();

                    if (typeof loadDashboard === "function")
                        loadDashboard();
                }


                if (
                    data.event === "ai_chat_completed"
                ) {

                    if (typeof loadEvents === "function")
                        loadEvents();
                }
            }


        } catch(e) {

            console.log(
                "WS RAW:",
                event.data
            );
        }
    };
}


window.addEventListener(
    "load",
    connectWebSocket
);

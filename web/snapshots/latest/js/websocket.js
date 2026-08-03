let ws;
function connectWebSocket() {
    console.log("CONNECT WEBSOCKET START");

    if (ws) {
        try {
            ws.close();
        } catch (e) {}
    }

    const proto = location.protocol === "https:" ? "wss://" : "ws://";

    ws = new WebSocket(proto + location.host + "/ws");

    ws.onopen = () => {
        console.log("WebSocket connected");
        updateWSStatus(true);
        showToast("WebSocket connected");
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
        updateWSStatus(false);

        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (e) => {
        console.error("WebSocket error", e);
        updateWSStatus(false);
    };

    ws.onmessage = (event) => {

        console.log("WS:", event.data);

        try {

            const msg = JSON.parse(event.data);
            if (typeof addLiveEvent === "function") {
                addLiveEvent(msg);
            }

            switch (msg.event) {

                case "plugin_started":
                case "plugin_stopped":
                case "plugin_failed":

                    fetch(API + "/plugins/" + msg.data.plugin + "/status", {
                        headers: headers()
                    })
                    .then(r => r.json())
                    .then(updatePluginCard)
                    .catch(() => loadPlugins());

                    break;

                case "ai_chat_completed":
                    if (typeof aiConsoleAdd === "function") aiConsoleAdd(msg);
                    loadEvents();
                    break;

                default:
                    loadRuntime();
            }

        } catch (e) {

            if (event.data !== "ping") {
                console.error("WS parse error:", e);
            }

        }

    };
}


// =========================
// Phoenix Build 006.1
// Auto start
// =========================


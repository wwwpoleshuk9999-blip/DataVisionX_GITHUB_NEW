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
            if (event.data === "ping") {
                return;
            }

            const msg = JSON.parse(event.data);

            if (typeof addLiveEvent === "function") {
                addLiveEvent(msg);
            }

            handleLiveEvent(msg);

        } catch (e) {
            console.error("WS parse error:", e);
        }

    };
}




// =========================
// Phoenix Build 009
// Live Event Router
// =========================

function handleLiveEvent(msg) {

    if (!msg || !msg.event) {
        return;
    }

    console.log("LIVE EVENT:", msg.event);


    switch(msg.event) {

        case "plugin_started":
        case "plugin_stopped":
        case "plugin_failed":

            if (typeof loadPlugins === "function") {
                loadPlugins();
            }

            if (typeof loadPluginHealth === "function") {
                loadPluginHealth();
            }

            break;


        case "runtime_start":
        case "runtime_stop":
        case "runtime_restart":
        case "runtime_reload":

            if (typeof loadRuntime === "function") {
                loadRuntime();
            }

            break;


        case "ai_chat_completed":

            if (typeof aiConsoleAdd === "function") {
                aiConsoleAdd(msg);
            }

            break;


        default:
            console.log("Unhandled event:", msg.event);
    }
}

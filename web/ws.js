

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
    socket = new WebSocket(`${protocol}://${location.host}/ws`);

    socket.onopen = () => {
        console.log("✅ WebSocket connected");
    };

    socket.onclose = () => {
        console.log("❌ WebSocket disconnected");
        setTimeout(connectWebSocket, 3000);
    };

    socket.onmessage = (event) => {
        console.log("EVENT:", event.data);

        try {
            const data = JSON.parse(event.data);

            if (data.action) {
                showToast("📢 " + data.action + (data.plugin ? " : " + data.plugin : ""));
            }
        } catch (e) {}

        if (typeof loadAll === "function") {
            loadAll();
        }
    };
}

window.addEventListener("load", connectWebSocket);

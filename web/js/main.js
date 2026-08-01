window.addEventListener("load", () => {
    console.log("DataVisionX Phoenix Build 007");

    if (typeof loadAll === "function") {
        loadAll();
    }

    if (typeof connectWebSocket === "function") {
        connectWebSocket();
    }

    setInterval(() => {
        if (typeof loadRuntime === "function") {
            loadRuntime();
        }

        if (typeof loadDashboard === "function") {
            loadDashboard();
        }
    }, 5000);
});

function loadAll() {
    loadDashboard();
    loadRuntime();
    loadPlugins();
    loadRegistry();
    loadEvents();
}

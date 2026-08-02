window.addEventListener("load", () => {
    console.log("WINDOW LOAD FIRED"); alert("DVX JS WORKING");
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
    loadPluginHealth();
    loadRecovery();
    loadWatchdog();
    loadMetrics();
}

console.log("=== MAIN.JS LOADED ===");
console.log(typeof loadDashboard);
console.log(typeof loadPlugins);
console.log(typeof loadEvents);
console.log(typeof connectWebSocket);


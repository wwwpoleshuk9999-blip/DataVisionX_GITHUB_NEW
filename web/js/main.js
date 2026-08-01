window.addEventListener("load", () => {
    console.log("DataVisionX Phoenix Build 007");

    if (typeof loadAll === "function") {
        loadAll();
    }

    if (typeof connectWebSocket === "function") {
        connectWebSocket();
    }
});

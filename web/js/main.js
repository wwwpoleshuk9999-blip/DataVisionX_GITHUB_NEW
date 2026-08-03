window.addEventListener("load", async () => {
    if (typeof loadLanguage === "function") {
        await loadLanguage();

        if (typeof applyTranslations === "function") {
            applyTranslations();
        }
        console.log("LANGUAGE LOADED:", localStorage.getItem("dvx_lang"), LANG);
    }
    
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

        if (typeof loadProjectCenter === "function") {
            loadProjectCenter();
        }
    }, 5000);
});

function loadAll() {
    console.log("LOAD ALL START");

    [
        loadDashboard,
        loadProjectCenter,
        loadRuntime,
        loadPlugins,
        loadRegistry,
        loadEvents,
        loadPluginHealth,
        loadRecovery,
        loadWatchdog,
        loadMetrics
    ].forEach(fn => {
        try {
            if (typeof fn === "function") {
                console.log("CALLING:", fn.name);
                fn().then(() => console.log("DONE:", fn.name)).catch(e => console.error("FAIL:", fn.name, e));
            }
        } catch(e) {
            console.error("LOAD ERROR:", fn.name, e);
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {
    const selector = document.getElementById("languageSelect");

    if (selector) {
        selector.value = localStorage.getItem("dvx_lang") || "ru";

        selector.addEventListener("change", async (e) => {
            await setLanguage(e.target.value);
            location.reload();
        });
    }
});

console.log("=== MAIN.JS LOADED ===");
console.log(typeof loadDashboard);
console.log(typeof loadPlugins);
console.log(typeof loadEvents);
console.log(typeof connectWebSocket);


async function runtimeAction(action) {
    const r = await fetch(`/runtime/${action}`, {
        method: "POST",
        headers: headers()
    });

    const d = await r.json();

    await loadRuntime();

    alert(`Runtime: ${d.status}`);
}

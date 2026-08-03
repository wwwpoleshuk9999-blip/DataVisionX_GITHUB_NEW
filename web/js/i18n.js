let LANG = localStorage.getItem("dvx_lang") || "ru";
let I18N = {};

async function loadLanguage(lang = LANG) {
    console.log("LOAD LANG FILE:", `/web/lang/${lang}.json`);
    const r = await fetch(`/web/lang/${lang}.json`);
    I18N = await r.json();
    LANG = lang;
    localStorage.setItem("dvx_lang", lang);

    if (typeof applyTranslations === "function") {
        applyTranslations();
    }
}

function t(key) {
    const parts = key.split(".");
    let obj = I18N;

    for (const p of parts) {
        if (!obj || !(p in obj)) {
            return key;
        }
        obj = obj[p];
    }

    return obj;
}

async function setLanguage(lang) {
    console.log("SET LANGUAGE:", lang);
    await loadLanguage(lang);
    if (typeof loadDashboard === "function") {
        loadDashboard();
    }
}

window.t = t;
window.loadLanguage = loadLanguage;
window.setLanguage = setLanguage;

function applyTranslations() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        el.textContent = t(key);
    });
}

window.applyTranslations = applyTranslations;

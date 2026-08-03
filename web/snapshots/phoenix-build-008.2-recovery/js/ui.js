function showToast(message, ok = true) {

    let toast = document.getElementById("toast");

    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";

        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.padding = "12px 18px";
        toast.style.borderRadius = "8px";
        toast.style.color = "#fff";
        toast.style.fontWeight = "bold";
        toast.style.zIndex = "99999";
        toast.style.transition = "0.3s";

        document.body.appendChild(toast);
    }

    toast.style.background = ok ? "#28a745" : "#d9534f";
    toast.innerText = message;
    toast.style.display = "block";

    clearTimeout(window.toastTimer);

    window.toastTimer = setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}
function updateWSStatus(online) {
    const el = document.getElementById("ws-status");
    if (!el) return;

    el.textContent = online
        ? "🟢 WebSocket Online"
        : "🔴 WebSocket Offline";
}

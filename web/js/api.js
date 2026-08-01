const API = "";

function headers() {
    const token = localStorage.getItem("token");
    return token
        ? { "Authorization": "Bearer " + token }
        : {};
}

function saveToken() {
    localStorage.setItem(
        "token",
        document.getElementById("token").value
    );

    showToast("Token saved");

    if (typeof loadAll === "function") {
        loadAll();
    }
}

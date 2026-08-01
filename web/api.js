const API = "";

function getToken() {
    return localStorage.getItem("token") || "";
}

function setToken(token) {
    localStorage.setItem("token", token);
}

function headers() {
    const token = getToken();

    if (!token) {
        return {};
    }

    return {
        "Authorization": `Bearer ${token}`
    };
}

async function apiGet(path) {
    const response = await fetch(API + path, {
        headers: headers()
    });

    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }

    return await response.json();
}

async function apiPost(path, body = {}) {
    const response = await fetch(API + path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...headers()
        },
        body: JSON.stringify(body)
    });

    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }

    return await response.json();
}

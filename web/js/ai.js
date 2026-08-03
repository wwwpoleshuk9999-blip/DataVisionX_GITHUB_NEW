function aiConsoleAdd(event) {
    const box = document.getElementById("ai-log");
    if (!box) return;

    const item = document.createElement("div");
    item.className = "card";

    const time = new Date().toLocaleTimeString();

    item.innerHTML =
        "<b>[" + time + "] AI Event</b><br>" +
        "Event: " + (event.event || "-") + "<br>" +
        "Source: " + (event.source || "-") + "<br>" +
        "Data: <pre>" + JSON.stringify(event.data || {}, null, 2) + "</pre>";

    box.prepend(item);

    while (box.children.length > 20) {
        box.removeChild(box.lastChild);
    }
}

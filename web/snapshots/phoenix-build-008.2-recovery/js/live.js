function addLiveEvent(event) {

    const box = document.getElementById("live-events");

    if (!box) return;

    const item = document.createElement("div");

    item.className = "card";

    item.innerHTML = `
        <b>${event.event || "event"}</b><br>
        Source: ${event.source || "-"}<br>
        Data: ${JSON.stringify(event.data || {})}
    `;

    box.prepend(item);

    while (box.children.length > 20) {
        box.removeChild(box.lastChild);
    }
}

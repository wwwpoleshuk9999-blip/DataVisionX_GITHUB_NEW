let cpuChart = null;
let memoryChart = null;

let chartHistory = {
    labels: [],
    cpu: [],
    memory: []
};

function updateCharts(metrics) {

    const cpuCanvas = document.getElementById("cpuChart");
    const memoryCanvas = document.getElementById("memoryChart");

    if (!cpuCanvas || !memoryCanvas) {
        return;
    }

    const time = new Date().toLocaleTimeString();

    chartHistory.labels.push(time);
    chartHistory.cpu.push(metrics.cpu_percent || 0);
    chartHistory.memory.push(metrics.memory_percent || 0);

    if (chartHistory.labels.length > 20) {
        chartHistory.labels.shift();
        chartHistory.cpu.shift();
        chartHistory.memory.shift();
    }

    if (typeof Chart === "undefined") {
        console.log("Chart.js not loaded");
        return;
    }

    if (!cpuChart) {
        cpuChart = new Chart(cpuCanvas, {
            type: "line",
            data: {
                labels: chartHistory.labels,
                datasets: [{
                    label: "CPU %",
                    data: chartHistory.cpu
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } else {
        cpuChart.update();
    }


    if (!memoryChart) {
        memoryChart = new Chart(memoryCanvas, {
            type: "line",
            data: {
                labels: chartHistory.labels,
                datasets: [{
                    label: "Memory %",
                    data: chartHistory.memory
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } else {
        memoryChart.update();
    }
}


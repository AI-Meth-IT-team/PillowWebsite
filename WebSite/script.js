// Konfiguracja
const SERVER_IP = "192.168.4.1";
const HTTP_PORT = "5000";
const WS_PORT = "8080";

let reactionChart = null;

function updateChart() {
    fetch(`http://${SERVER_IP}:${HTTP_PORT}/get-times`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('reactionChart').getContext('2d');
            
            if (reactionChart) {
                reactionChart.destroy();
            }

            reactionChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.times),
                    datasets: [{
                        label: 'Reaction Time (seconds)',
                        data: Object.values(data.times),
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    // Disable all animations
                    animation: {
                        duration: 0, // general animation time
                        easing: 'linear'
                    },
                    transitions: {
                        active: {
                            animation: {
                                duration: 0
                            }
                        }
                    },
                    // Rest of your options...
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Seconds'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: `Reaction Times (Avg: ${data.stats.average.toFixed(3)}s)`
                        }
                    }
                }
            });
        });
}

// Modify your startGame function to update the chart after the game
function startGame() {
    const serverUrl = `http://${SERVER_IP}:${HTTP_PORT}/start-game`;

    fetch(serverUrl, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Gra rozpoczęta!") {
            // Check for results every 2 seconds
            const checkInterval = setInterval(updateChart, 2000);
            // Stop checking after 1 minute
            setTimeout(() => clearInterval(checkInterval), 60000);
        }
    })
    .catch(handleError);
}

function onStart() {
    console.log("Aplikacja załadowana.");
}


function updateStatus(message) {
    const statusElement = document.getElementById('status');
    if (statusElement) {
        statusElement.textContent = `Status: ${message}`;
    }
}
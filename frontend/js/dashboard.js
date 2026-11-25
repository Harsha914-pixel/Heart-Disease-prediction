document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    
    // Connect to WebSocket server for real-time updates
    const socket = io();
    socket.on('new_prediction', () => {
        console.log("New prediction received, updating dashboard...");
        fetchStats();
    });
});

function fetchStats() {
    // Fetch History
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                document.getElementById('stat-total').innerText = data.length;
                if (data.length > 0) {
                    const latest = data[0];
                    const statusText = latest.prediction_status;
                    const classText = latest.predicted_class > 0 ? ` (Class ${latest.predicted_class})` : '';
                    document.getElementById('stat-latest-status').innerText = `${statusText}${classText}`;
                    
                    // Style latest prediction color depending on status
                    if (statusText === 'Heart Disease Detected') {
                        document.getElementById('stat-latest-status').style.color = 'var(--danger)';
                    } else {
                        document.getElementById('stat-latest-status').style.color = 'var(--success)';
                    }
                }
            }
        })
        .catch(err => console.error("Error loading stats:", err));

    // Fetch Active Model
    fetch('/api/evaluation')
        .then(response => response.json())
        .then(data => {
            if (data && data.selected_algorithm) {
                document.getElementById('stat-model').innerText = data.selected_algorithm;
            }
        })
        .catch(err => console.error("Error loading model info:", err));
}

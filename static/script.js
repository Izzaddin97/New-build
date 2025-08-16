
let serverRunning = false;
let logUpdateInterval;

function toggleServer() {
    const button = document.getElementById('startBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const buttonText = button.querySelector('.button-text');
    
    if (!serverRunning) {
        // Start server
        fetch('/start_server', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    serverRunning = true;
                    button.classList.add('active');
                    buttonText.textContent = 'STOP VPN';
                    statusIndicator.classList.add('active');
                    statusText.textContent = 'Server Running';
                    
                    // Start log updates
                    startLogUpdates();
                    updateClientCount();
                }
            })
            .catch(error => {
                console.error('Error starting server:', error);
                addLog('Error: Failed to start server');
            });
    } else {
        // Stop server
        fetch('/stop_server', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    serverRunning = false;
                    button.classList.remove('active');
                    buttonText.textContent = 'START VPN';
                    statusIndicator.classList.remove('active');
                    statusText.textContent = 'Server Stopped';
                    
                    // Stop log updates
                    if (logUpdateInterval) {
                        clearInterval(logUpdateInterval);
                    }
                    
                    // Reset client count
                    document.getElementById('clientCount').textContent = '0';
                }
            })
            .catch(error => {
                console.error('Error stopping server:', error);
                addLog('Error: Failed to stop server');
            });
    }
}

function startLogUpdates() {
    logUpdateInterval = setInterval(() => {
        fetch('/get_logs')
            .then(response => response.json())
            .then(data => {
                updateLogs(data.logs);
            })
            .catch(error => {
                console.error('Error fetching logs:', error);
            });
    }, 2000);
logContainer.innerHTML = logs.map(log => `<p>${log}</p>`).join('');
function updateLogs(logs) {
    const logContainer = document.getElementById('logContainer');
logContainer.scrollTop = logContainer.scrollHeight;
}

function addLog(message) {
    const logContainer = document.getElementById('logContainer');
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('p');
    logEntry.textContent = `[${timestamp}] ${message}`;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

function updateClientCount() {
    if (serverRunning) {
        fetch('/get_status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('clientCount').textContent = data.client_count;
                setTimeout(updateClientCount, 3000);
            })
            .catch(error => {
                console.error('Error fetching status:', error);
                if (serverRunning) {
                    setTimeout(updateClientCount, 3000);
                }
            });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    addLog('VPN GUI initialized');
    addLog('Ready to start server...');
});

// HVF Media Matrix - Live Telemetry Engine
// Engineered for continuous background synchronization

async function fetchIntelStream() {
    try {
        // Append dynamic timestamp to shatter browser caching protocols
        const response = await fetch('data/stream.json?t=' + new Date().getTime());
        if (!response.ok) throw new Error("Data stream connection severed.");
        
        const data = await response.json();
        const display = document.getElementById('intel-display');
        
        // Prevent UI flickering by only updating the DOM when the payload physically changes
        if (display.textContent !== data.intel) {
            display.textContent = data.intel;
            console.log("Matrix sync achieved. Telemetry updated: " + new Date().toLocaleTimeString());
        }
    } catch (error) {
        console.error("Matrix Sync Error: ", error);
        document.getElementById('intel-display').textContent = "[WARNING] Data stream connection lost. Standing by for auto-reconnect...";
    }
}

// Ignite immediate sync on load
fetchIntelStream();
// Establish continuous polling loop (5-second intervals)
setInterval(fetchIntelStream, 5000);

// HVF Media Matrix - Live Telemetry & Two-Way Comm Engine
async function fetchIntelStream() {
    try {
        const response = await fetch('data/stream.json?t=' + new Date().getTime());
        if (!response.ok) throw new Error("Data stream connection severed.");
        const data = await response.json();
        const display = document.getElementById('intel-display');
        if (display.textContent !== data.intel) {
            display.textContent = data.intel;
        }
    } catch (error) {
        console.error("Matrix Sync Error: ", error);
    }
}

// Ignition & Polling Loop
fetchIntelStream();
setInterval(fetchIntelStream, 5000);

// Comm Link Transmission Logic
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatHistory = document.getElementById('chat-history');

function transmitMessage() {
    const text = chatInput.value.trim();
    if (text === '') return;
    
    // Display CEO Command
    const ceoMsg = document.createElement('div');
    ceoMsg.className = 'chat-msg ceo';
    ceoMsg.innerHTML = '<strong>CEO:</strong> ' + text;
    chatHistory.appendChild(ceoMsg);
    
    // Clear input & auto-scroll
    chatInput.value = '';
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    // Placeholder for backend API routing
    setTimeout(() => {
        const ebonyMsg = document.createElement('div');
        ebonyMsg.className = 'chat-msg ebony';
        ebonyMsg.innerHTML = '<strong>Ebony:</strong> Directive logged. Backend routing API pending deployment.';
        chatHistory.appendChild(ebonyMsg);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }, 1000);
}

sendBtn.addEventListener('click', transmitMessage);
chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') transmitMessage();
});

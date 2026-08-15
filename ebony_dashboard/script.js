// HVF Media Matrix - Live Telemetry & Cognitive Comm Engine

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

fetchIntelStream();
setInterval(fetchIntelStream, 5000);

const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatHistory = document.getElementById('chat-history');

async function transmitMessage() {
    const text = chatInput.value.trim();
    if (text === '') return;
    
    // Display CEO Command
    const ceoMsg = document.createElement('div');
    ceoMsg.className = 'chat-msg ceo';
    ceoMsg.innerHTML = '<strong>CEO:</strong> ' + text;
    chatHistory.appendChild(ceoMsg);
    
    chatInput.value = '';
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    // Transmit to Backend API
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        
        const ebonyMsg = document.createElement('div');
        ebonyMsg.className = 'chat-msg ebony';
        ebonyMsg.innerHTML = '<strong>Ebony:</strong> ' + data.reply;
        chatHistory.appendChild(ebonyMsg);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    } catch (error) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'chat-msg ebony';
        errorMsg.innerHTML = '<strong>Ebony:</strong> [SYSTEM ERROR] Neural link severed.';
        chatHistory.appendChild(errorMsg);
    }
}

sendBtn.addEventListener('click', transmitMessage);
chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') transmitMessage();
});

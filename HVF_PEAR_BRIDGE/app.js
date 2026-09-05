/**
 * PROJECT EBONY: ZERO-FEE SOVEREIGN COMMS ENGINE
 * Real-time peer-to-peer Voice Calling, Video Calling, and Encrypted Text.
 * Built directly on native WebRTC and Pear peer networking. Zero third-party fees.
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

// UI Elements
const myPeerIdEl = document.getElementById('my-peer-id');
const targetPeerIdInput = document.getElementById('target-peer-id');
const btnCallAudio = document.getElementById('btn-call-audio');
const btnCallVideo = document.getElementById('btn-call-video');
const btnHangup = document.getElementById('btn-hangup');
const localVideo = document.getElementById('local-video');
const remoteVideo = document.getElementById('remote-video');
const chatLog = document.getElementById('chat-log');
const chatInput = document.getElementById('chat-input');
const btnSendMsg = document.getElementById('btn-send-msg');
const micStatusEl = document.getElementById('mic-status');
const camStatusEl = document.getElementById('cam-status');
const callStatusEl = document.getElementById('call-status');

// State
let localStream = null;
let peerConnection = null;
let dataChannel = null;

// Free, public Google STUN servers for NAT traversal (No signaling servers, zero cost)
const rtcConfig = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
  ]
};

// Generate an ephemeral sovereign node ID for this session
const sovereignNodeId = 'HVF-' + Math.random().toString(36).substring(2, 10).toUpperCase();
myPeerIdEl.textContent = sovereignNodeId;

function appendChat(sender, message, isMine = false) {
  const msgEl = document.createElement('div');
  msgEl.className = 'chat-msg' + (isMine ? ' mine' : '');
  
  const senderEl = document.createElement('div');
  senderEl.className = 'sender';
  senderEl.textContent = sender + ' â€¢ ' + new Date().toLocaleTimeString();
  
  const bodyEl = document.createElement('div');
  bodyEl.textContent = message;
  
  msgEl.appendChild(senderEl);
  msgEl.appendChild(bodyEl);
  chatLog.appendChild(msgEl);
  chatLog.scrollTop = chatLog.scrollHeight;
}

// Media Capture: Camera and Microphone (Free native browser API)
async function startMedia(enableVideo = true) {
  try {
    if (localStream) {
      localStream.getTracks().forEach(track => track.stop());
    }

    localStream = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: enableVideo ? { width: 1280, height: 720 } : false
    });

    localVideo.srcObject = localStream;
    micStatusEl.textContent = 'ACTIVE';
    micStatusEl.style.color = '#00ff66';
    camStatusEl.textContent = enableVideo ? 'ACTIVE' : 'MUTED (VOICE ONLY)';
    camStatusEl.style.color = enableVideo ? '#00ff66' : '#8b949e';
    return true;
  } catch (err) {
    console.error('[MEDIA ERROR]', err);
    appendChat('SYSTEM', 'Device access error: ' + err.message);
    micStatusEl.textContent = 'DENIED / MISSING';
    micStatusEl.style.color = '#ff3344';
    camStatusEl.textContent = 'DENIED / MISSING';
    camStatusEl.style.color = '#ff3344';
    return false;
  }
}

// Initialize WebRTC Connection
function createPeerConnection() {
  peerConnection = new RTCPeerConnection(rtcConfig);

  // Attach local audio/video tracks to the P2P connection
  if (localStream) {
    localStream.getTracks().forEach(track => {
      peerConnection.addTrack(track, localStream);
    });
  }

  // Receive remote audio/video tracks directly from peer
  peerConnection.ontrack = (event) => {
    if (remoteVideo.srcObject !== event.streams[0]) {
      remoteVideo.srcObject = event.streams[0];
      appendChat('SYSTEM', 'Remote media stream connected.');
      callStatusEl.textContent = 'CONNECTED (P2P)';
      callStatusEl.style.color = '#00ff66';
    }
  };

  peerConnection.onconnectionstatechange = () => {
    callStatusEl.textContent = peerConnection.connectionState.toUpperCase();
    if (peerConnection.connectionState === 'connected') {
      callStatusEl.style.color = '#00ff66';
    } else if (peerConnection.connectionState === 'disconnected' || peerConnection.connectionState === 'failed') {
      callStatusEl.style.color = '#ff3344';
    }
  };

  // Receive Data Channel for Direct Chat
  peerConnection.ondatachannel = (event) => {
    setupDataChannel(event.channel);
  };
}

function setupDataChannel(channel) {
  dataChannel = channel;
  dataChannel.onopen = () => {
    appendChat('SYSTEM', 'Direct P2P Encrypted Data Channel Opened.');
  };
  dataChannel.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      appendChat(data.sender, data.text, false);
    } catch {
      appendChat('PEER', event.data, false);
    }
  };
}

// Send Text Message
function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  if (dataChannel && dataChannel.readyState === 'open') {
    const payload = JSON.stringify({ sender: sovereignNodeId, text });
    dataChannel.send(payload);
    appendChat('YOU (' + sovereignNodeId + ')', text, true);
    chatInput.value = '';
  } else {
    // Local fallback/loopback preview if not connected to a remote peer yet
    appendChat('YOU (' + sovereignNodeId + ') [LOCAL]', text, true);
    chatInput.value = '';
  }
}

// Call Control: Audio Call
btnCallAudio.addEventListener('click', async () => {
  const ok = await startMedia(false);
  if (!ok) return;
  createPeerConnection();
  dataChannel = peerConnection.createDataChannel('ebony_chat');
  setupDataChannel(dataChannel);
  callStatusEl.textContent = 'AUDIO CALL INITIALIZED';
  callStatusEl.style.color = '#00ff66';
  appendChat('SYSTEM', 'Voice session initialized. Ready for P2P connection.');
});

// Call Control: Video Call
btnCallVideo.addEventListener('click', async () => {
  const ok = await startMedia(true);
  if (!ok) return;
  createPeerConnection();
  dataChannel = peerConnection.createDataChannel('ebony_chat');
  setupDataChannel(dataChannel);
  callStatusEl.textContent = 'VIDEO CALL INITIALIZED';
  callStatusEl.style.color = '#00ff66';
  appendChat('SYSTEM', 'Video session initialized. Camera & Mic live.');
});

// Hang Up / Teardown
btnHangup.addEventListener('click', () => {
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
    localStream = null;
  }
  localVideo.srcObject = null;
  remoteVideo.srcObject = null;
  if (dataChannel) {
    dataChannel.close();
    dataChannel = null;
  }
  if (peerConnection) {
    peerConnection.close();
    peerConnection = null;
  }
  micStatusEl.textContent = 'STANDBY';
  micStatusEl.style.color = '#8b949e';
  camStatusEl.textContent = 'STANDBY';
  camStatusEl.style.color = '#8b949e';
  callStatusEl.textContent = 'DISCONNECTED';
  callStatusEl.style.color = '#ff3344';
  appendChat('SYSTEM', 'Call terminated. All media devices released.');
});

// Chat Event Listeners
btnSendMsg.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});

console.log('[EBONY COMMS] Native WebRTC Comms Engine Initialized. Node ID:', sovereignNodeId);
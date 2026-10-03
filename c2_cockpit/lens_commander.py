import os

print("[*] Engaging Dynamic Optical Commander...")
file_path = "hvf_intercom_broker.py"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the UI with the Switch button
    if "[ SWITCH LENS ]" not in content:
        content = content.replace(
            "[ INITIATE SECURE COMM LINK ]</button>",
            "[ INITIATE SECURE COMM LINK ]</button>\n        <button id=\"switchBtn\" onclick=\"switchCamera()\" style=\"background:#ff9900; color:#000; padding:15px; border:none; font-weight:bold; cursor:pointer; margin-left:10px;\">[ SWITCH LENS ]</button>"
        )

    # 2. Variable injection for dynamic lens targeting
    if "let currentFacingMode =" not in content:
        content = content.replace("<script>", "<script>\n        let currentFacingMode = 'user';")

    # 3. Replace static generic optics with dynamic targeting to bypass Android's multi-lens panic
    content = content.replace("video: true", "video: { facingMode: currentFacingMode }")
    
    # 4. Inject the seamless WebRTC track-swapping logic
    if "function switchCamera()" not in content:
        js_logic = """
        async function switchCamera() {
            if (!localStream) {
                alert("[HVF] Matrix offline. Initiate secure link first.");
                return;
            }
            // Toggle between front ('user') and rear ('environment')
            currentFacingMode = (currentFacingMode === 'user') ? 'environment' : 'user';
            console.log("[HVF] Toggling optics to: " + currentFacingMode);
            
            try {
                // Fetch the new lens feed securely
                let newStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: currentFacingMode }, audio: false });
                let newVideoTrack = newStream.getVideoTracks()[0];
                
                // Seamlessly swap the track across the active Tailscale mesh without dropping the call
                if (peerConnection) {
                    let sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
                    if (sender) {
                        sender.replaceTrack(newVideoTrack);
                    }
                }
                
                // Update the local display on the device
                localStream.getVideoTracks()[0].stop(); // Terminate old lens hardware lock
                localStream.removeTrack(localStream.getVideoTracks()[0]);
                localStream.addTrack(newVideoTrack);
                document.getElementById('localVideo').srcObject = localStream;
                
            } catch (err) {
                console.error("[HVF] Lens toggle failed:", err);
            }
        }
        """
        content = content.replace("</script>", js_logic + "\n    </script>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Dynamic Optical Commander injected. Front/Rear lens toggle is now live.")
else:
    print("[FATAL] hvf_intercom_broker.py not found.")
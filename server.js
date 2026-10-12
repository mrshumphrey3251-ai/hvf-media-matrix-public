const fs = require('fs');
const https = require('https');
const express = require('express');
const { Server } = require('socket.io');

const app = express();
app.use(express.static('public'));

const options = {
    key: fs.readFileSync('server.key'),
    cert: fs.readFileSync('server.cert')
};

const server = https.createServer(options, app);
const io = new Server(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
    console.log([NODE ACTIVE] ID:  + socket.id);

    // Command & Control Matrix
    socket.on('telemetry_command', (data) => {
        if (data.target === 'ALL') {
            socket.broadcast.emit('telemetry_command', data);
        } else {
            io.to(data.target).emit('telemetry_command', data);
        }
    });

    // Unified Comms (Voice/Video)
    socket.on('webrtc_signal', (data) => {
        if (data.target === 'ALL') {
            socket.broadcast.emit('webrtc_signal', data);
        } else {
            io.to(data.target).emit('webrtc_signal', data);
        }
    });

    socket.on('disconnect', () => {
        console.log([NODE OFFLINE] ID:  + socket.id);
    });
});

const PORT = 8443;
server.listen(PORT, '0.0.0.0', () => {
    console.log(=========================================);
    console.log([DATA CENTER HUB ONLINE]);
    console.log(Listening strictly on HTTPS port  + PORT);
    console.log(=========================================);
});

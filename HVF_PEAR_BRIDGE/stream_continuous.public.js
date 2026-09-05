/**
 * PROJECT EBONY: CONTINUOUS TELEMETRY EMITTER (PUBLIC BLUEPRINT)
 * Emits periodic Protocol Lambda V2 frames into UDP Ingress Diode
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import { TelemetryEmitter } from './telemetry_emitter.js';

const PORT = process.env.INGRESS_PORT || 5005;
const HOST = process.env.INGRESS_HOST || '127.0.0.1';
const INTERVAL_MS = parseInt(process.env.STREAM_INTERVAL_MS || '250', 10);

console.log('====================================================');
console.log(' PROJECT EBONY: CONTINUOUS TELEMETRY TRANSMITTER (PUBLIC)');
console.log(` Target Diode: ${HOST}:${PORT} | Interval: ${INTERVAL_MS}ms`);
console.log(' Press Ctrl+C to terminate cleanly.');
console.log('====================================================');

const emitter = new TelemetryEmitter(PORT, HOST);
let count = 0;
let running = true;

const timer = setInterval(async () => {
  if (!running) return;
  try {
    await emitter.sendFrame();
    count++;
    if (count % 4 === 0) {
      process.stdout.write(`\r[EMITTING LIVE] Dispatched: ${count} frames | Target: ${HOST}:${PORT}`);
    }
  } catch (err) {
    console.error(`\n[EMITTER ERROR] Transmission fault:`, err.message);
  }
}, INTERVAL_MS);

function cleanup() {
  running = false;
  clearInterval(timer);
  emitter.stop();
  console.log(`\n[EMITTER TEARDOWN] Closed socket after ${count} total transmitted frames.`);
  process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
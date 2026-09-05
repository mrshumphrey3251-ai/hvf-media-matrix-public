/**
 * PROJECT EBONY: CONTROLLED TELEMETRY BURST SCRIPT (PUBLIC BLUEPRINT)
 * Dispatches 5 Protocol Lambda V2 frames into UDP Ingress Diode
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import { TelemetryEmitter } from './telemetry_emitter.js';

async function main() {
  const port = process.env.INGRESS_PORT || 5005;
  const host = process.env.INGRESS_HOST || '127.0.0.1';
  const emitter = new TelemetryEmitter(port, host);
  console.log(`[EMITTER READY] Dispatching 5 Protocol Lambda V2 frames to ${host}:${port}...`);

  for (let i = 0; i < 5; i++) {
    await emitter.sendFrame();
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  emitter.stop();
  console.log('[EMITTER COMPLETE] 5 burst frames successfully delivered to diode.');
}

main().catch((err) => {
  console.error('[EMITTER FATAL]', err);
  process.exit(1);
});
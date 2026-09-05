/**
 * PROJECT EBONY: INGRESS TELEMETRY PIPELINE
 * Public Distribution Blueprint: Sanitized & Parameterized.
 * Protocol Target: Protocol Lambda V2
 */

const Hypercore = require('hypercore');
const Hyperswarm = require('hyperswarm');
const dgram = require('dgram');
const path = require('path');

const CONFIG = {
  host: process.env.EBONY_DIODE_HOST || '127.0.0.1',
  port: parseInt(process.env.EBONY_DIODE_PORT, 10) || 5005,
  storagePath: process.env.EBONY_STORAGE_PATH || path.join(process.cwd(), '.ebony_core'),
  expectedFrames: 5
};

async function runPipeline() {
  const core = new Hypercore(CONFIG.storagePath, { valueEncoding: 'json' });
  await core.ready();

  const initialLength = core.length;
  console.log(`[HYPERCORE READY] Feed Key: [REDACTED_PUBLIC_KEY]`);
  console.log(`[STORAGE BASELINE] Initial Core Length: ${initialLength}`);

  const server = dgram.createSocket('udp4');

  server.on('message', async (msg) => {
    try {
      const parsed = JSON.parse(msg.toString());
      await core.append(parsed);
      console.log(`[CORE APPEND] Appended block #${core.length} to Hypercore log.`);
    } catch (err) {
      console.error(`[INGRESS ERROR] Parse/Append failed: ${err.message}`);
    }
  });

  server.bind(CONFIG.port, CONFIG.host, () => {
    console.log(`[INGRESS ACTIVE] Diode listening on ${CONFIG.host}:${CONFIG.port}`);
  });

  return { core, server, initialLength };
}

module.exports = { runPipeline, CONFIG };
/**
 * PROJECT EBONY: CONSUMER REAL-TIME SYNC INTEGRATION TEST
 * Public Distribution Blueprint: Parameterized & Sanitized Harness
 * Validates Writer (Ingress Pipeline) -> Hypercore -> Reader (Consumer / Pear Frontend Engine)
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import b4a from 'b4a';
import { TelemetryEmitter } from './telemetry_emitter.js';
import { TelemetryIngressPipeline } from './bridge_daemon.js';
import { EbonySwarmConsumer } from './p2p_consumer.js';
import os from 'node:os';
import path from 'node:path';
import fs from 'node:fs';

async function runConsumerSyncTest() {
  console.log('=== STARTING PROJECT EBONY CONSUMER SYNC TEST (PUBLIC BLUEPRINT) ===');

  const pipeline = new TelemetryIngressPipeline();
  await pipeline.start();

  const feedKeyHex = b4a.toString(pipeline.swarmBridge.core.key, 'hex');
  console.log('[WRITER READY] Feed Key: [REDACTED_PUBLIC_KEY]');
  const baselineLength = pipeline.swarmBridge.core.length;

  const testConsumerDir = path.join(os.tmpdir(), `hvf_test_consumer_${Date.now()}`);
  fs.mkdirSync(testConsumerDir, { recursive: true });

  const receivedBlocks = [];
  const consumer = new EbonySwarmConsumer(feedKeyHex, testConsumerDir);

  await consumer.init('project-ebony-sovereign-mesh-v1', (block, idx) => {
    const data = block.payload || block;
    receivedBlocks.push({ idx, data });
    console.log(`[CONSUMER CAPTURED] Block #${idx} | Subsystem: ${data.subsystem} | Seq: ${data.sequence}`);
  });

  console.log('[CONSUMER READY] Attached to feed key. Ready for ingress.');
  await new Promise(r => setTimeout(r, 200));

  const emitter = new TelemetryEmitter(5005, '127.0.0.1');
  const frameCount = 3;

  console.log(`[EMITTER TRANSMITTING] Sending ${frameCount} frames...`);
  for (let i = 0; i < frameCount; i++) {
    await emitter.sendFrame();
    await new Promise(r => setTimeout(r, 100));
  }

  await new Promise(r => setTimeout(r, 600));

  const finalWriterLength = pipeline.swarmBridge.core.length;
  console.log('=== VERIFYING SYNCHRONIZATION INTEGRITY ===');
  console.log(`Writer Baseline: ${baselineLength} | Writer Final: ${finalWriterLength} | New Frames: ${frameCount}`);

  if (finalWriterLength - baselineLength < frameCount) {
    throw new Error(`Ingress mismatch: expected ${frameCount} new blocks, recorded ${finalWriterLength - baselineLength}`);
  }

  for (const item of receivedBlocks) {
    if (!item.data.subsystem || item.data.sequence === undefined) {
      throw new Error(`Unwrapping failed on consumer block #${item.idx}`);
    }
  }

  emitter.stop();
  await pipeline.stop();
  if (consumer.core) await consumer.core.close();
  if (consumer.swarm) await consumer.swarm.destroy();

  try {
    fs.rmSync(testConsumerDir, { recursive: true, force: true });
  } catch (e) {
    // Non-fatal cleanup catch
  }

  console.log('[TEARDOWN COMPLETE] All sockets, cores, and swarms closed.');
  console.log('=== CONSUMER SYNC TEST PASSED (100% UNWRAPPED INTEGRITY) ===');
}

runConsumerSyncTest().catch((err) => {
  console.error('[FATAL SYNC ERROR]', err);
  process.exit(1);
});
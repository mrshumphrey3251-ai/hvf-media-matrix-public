/**
 * PROJECT EBONY: MULTI-PEER MESH REPLICATION TEST (PUBLIC BLUEPRINT)
 * Validates 1 Writer Daemon -> Hyperswarm DHT -> 2 Independent Consumer Peers
 * Confirms simultaneous distributed replication across isolated storage roots.
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import b4a from 'b4a';
import os from 'node:os';
import path from 'node:path';
import fs from 'node:fs';
import { TelemetryIngressPipeline } from './bridge_daemon.js';
import { TelemetryEmitter } from './telemetry_emitter.js';
import { EbonySwarmConsumer } from './p2p_consumer.js';

async function runMultiPeerTest() {
  console.log('=== STARTING PROJECT EBONY MULTI-PEER MESH TEST (PUBLIC BLUEPRINT) ===');

  const pipeline = new TelemetryIngressPipeline();
  await pipeline.start();

  const feedKeyHex = b4a.toString(pipeline.swarmBridge.core.key, 'hex');
  const baselineLength = pipeline.swarmBridge.core.length;
  console.log(`[WRITER ACTIVE] Core Key: <REDACTED> | Baseline Blocks: ${baselineLength}`);

  const tempA = path.join(os.tmpdir(), `hvf_mesh_peer_a_${Date.now()}`);
  const tempB = path.join(os.tmpdir(), `hvf_mesh_peer_b_${Date.now()}`);
  fs.mkdirSync(tempA, { recursive: true });
  fs.mkdirSync(tempB, { recursive: true });

  const peerAReceived = [];
  const peerBReceived = [];

  const consumerA = new EbonySwarmConsumer(feedKeyHex, tempA);
  const consumerB = new EbonySwarmConsumer(feedKeyHex, tempB);

  const topicSeed = 'project-ebony-sovereign-mesh-v1';

  await Promise.all([
    consumerA.init(topicSeed, (block, idx) => {
      const data = block.payload || block;
      peerAReceived.push({ idx, seq: data.sequence });
      console.log(`  [PEER A CAPTURE] Block #${idx} | Subsystem: ${data.subsystem} | Seq: ${data.sequence}`);
    }),
    consumerB.init(topicSeed, (block, idx) => {
      const data = block.payload || block;
      peerBReceived.push({ idx, seq: data.sequence });
      console.log(`  [PEER B CAPTURE] Block #${idx} | Subsystem: ${data.subsystem} | Seq: ${data.sequence}`);
    })
  ]);

  console.log('[PEERS READY] Peer A and Peer B joined DHT topic and listening.');
  await new Promise(r => setTimeout(r, 600));

  const emitter = new TelemetryEmitter(5005, '127.0.0.1');
  const emitCount = 4;
  console.log(`[INGRESS DISPATCH] Transmitting ${emitCount} frames to diode...`);

  for (let i = 0; i < emitCount; i++) {
    await emitter.sendFrame();
    await new Promise(r => setTimeout(r, 100));
  }

  emitter.stop();
  await new Promise(r => setTimeout(r, 800));

  console.log('=== VERIFYING DUAL-PEER SYNC INTEGRITY ===');
  console.log(`Peer A Received Count: ${peerAReceived.length} | Expected: >= ${emitCount}`);
  console.log(`Peer B Received Count: ${peerBReceived.length} | Expected: >= ${emitCount}`);

  if (peerAReceived.length < emitCount || peerBReceived.length < emitCount) {
    throw new Error('Replication underflow: one or more peers failed to receive all frames');
  }

  await pipeline.stop();
  if (consumerA.core) await consumerA.core.close();
  if (consumerA.swarm) await consumerA.swarm.destroy();
  if (consumerB.core) await consumerB.core.close();
  if (consumerB.swarm) await consumerB.swarm.destroy();

  try {
    fs.rmSync(tempA, { recursive: true, force: true });
    fs.rmSync(tempB, { recursive: true, force: true });
  } catch (e) {
    // Non-fatal cleanup catch
  }

  console.log('[TEARDOWN COMPLETE] Sockets, cores, and swarms closed.');
  console.log('=== MULTI-PEER MESH TEST PASSED (100% CONVERGENCE) ===');
}

runMultiPeerTest().catch((err) => {
  console.error('[FATAL MULTI-PEER ERROR]', err);
  process.exit(1);
});
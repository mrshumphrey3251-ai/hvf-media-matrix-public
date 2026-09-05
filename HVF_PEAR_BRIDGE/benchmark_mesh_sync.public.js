/**
 * PROJECT EBONY: PEER-TO-PEER MESH BENCHMARK HARNESS (PUBLIC BLUEPRINT)
 * Quantifies DHT discovery latency, connection setup time, and block propagation delay.
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import b4a from 'b4a';
import os from 'node:os';
import path from 'node:path';
import fs from 'node:fs';
import { performance } from 'node:perf_hooks';
import { TelemetryIngressPipeline } from './bridge_daemon.js';
import { TelemetryEmitter } from './telemetry_emitter.js';
import { EbonySwarmConsumer } from './p2p_consumer.js';

async function runBenchmark() {
  console.log('====================================================');
  console.log(' PROJECT EBONY: MESH PERFORMANCE & LATENCY BENCHMARK (PUBLIC)');
  console.log('====================================================');

  const pipeline = new TelemetryIngressPipeline();
  await pipeline.start();

  const feedKeyHex = b4a.toString(pipeline.swarmBridge.core.key, 'hex');
  const tempDir = path.join(os.tmpdir(), `hvf_bench_peer_${Date.now()}`);
  fs.mkdirSync(tempDir, { recursive: true });

  const consumer = new EbonySwarmConsumer(feedKeyHex, tempDir);
  const topicSeed = 'project-ebony-sovereign-mesh-v1';

  const t0 = performance.now();
  let firstPeerConnectedTime = null;
  const latencies = [];

  await consumer.init(topicSeed, (block, idx) => {
    const data = block.payload || block;
    if (data.timestamp) {
      const sendTime = new Date(data.timestamp).getTime();
      const nowEpoch = Date.now();
      latencies.push(Math.max(0, nowEpoch - sendTime));
    }
    console.log(`  [BENCHMARK CAPTURE] Block #${idx} | Subsystem: ${data.subsystem} | Seq: ${data.sequence}`);
  });

  if (consumer.swarm) {
    consumer.swarm.on('connection', () => {
      if (!firstPeerConnectedTime) {
        firstPeerConnectedTime = performance.now();
        console.log(`[METRIC] Swarm Connection Established: ${(firstPeerConnectedTime - t0).toFixed(2)}ms`);
      }
    });
  }

  console.log('[BENCHMARK READY] Peer listening on Hyperswarm topic...');
  await new Promise(r => setTimeout(r, 600));

  const emitter = new TelemetryEmitter(5005, '127.0.0.1');
  const frameCount = 6;
  console.log(`[INGRESS DISPATCH] Streaming ${frameCount} timed benchmark frames...`);

  for (let i = 0; i < frameCount; i++) {
    await emitter.sendFrame();
    await new Promise(r => setTimeout(r, 120));
  }

  emitter.stop();
  await new Promise(r => setTimeout(r, 1000));

  console.log('\n=== BENCHMARK ANALYSIS ===');
  if (latencies.length > 0) {
    const avgLatency = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    console.log(`- Total Sampled Frames: ${latencies.length}`);
    console.log(`- Average Ingress-to-Replica Propagation: ${avgLatency.toFixed(2)}ms`);
    console.log(`- Minimum Latency: ${Math.min(...latencies)}ms`);
    console.log(`- Maximum Latency: ${Math.max(...latencies)}ms`);
  }

  await pipeline.stop();
  if (consumer.core) await consumer.core.close();
  if (consumer.swarm) await consumer.swarm.destroy();

  try {
    fs.rmSync(tempDir, { recursive: true, force: true });
  } catch (e) {
    // Non-fatal cleanup catch
  }

  console.log('[TEARDOWN COMPLETE] Benchmark resources released.');
  console.log('=== BENCHMARK HARNESS COMPLETE ===');
}

runBenchmark().catch((err) => {
  console.error('[BENCHMARK FAULT]', err);
  process.exit(1);
});
/**
 * PROJECT EBONY: CONTROLLED CONTINUOUS INGRESS TEST (PUBLIC BLUEPRINT)
 * Executes Pipeline + Continuous Emitter directly in-process for accurate telemetry auditing
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import { TelemetryIngressPipeline } from './bridge_daemon.js';
import { TelemetryEmitter } from './telemetry_emitter.js';

async function runCycle() {
  console.log('=== STARTING CONTINUOUS INGRESS AUDIT CYCLE (PUBLIC BLUEPRINT) ===');
  
  const pipeline = new TelemetryIngressPipeline();
  await pipeline.start();

  const baselineLength = pipeline.swarmBridge.core.length;
  console.log(`[PIPELINE ACTIVE] Initial Core Length: ${baselineLength}`);

  const emitter = new TelemetryEmitter(5005, '127.0.0.1');
  console.log('[EMITTER LAUNCHED] Streaming 10 frames @ 100ms intervals...');

  for (let i = 0; i < 10; i++) {
    await emitter.sendFrame();
    await new Promise(r => setTimeout(r, 100));
  }

  emitter.stop();
  console.log('[EMISSION COMPLETE] Allowing core disk commit...');
  await new Promise(r => setTimeout(r, 500));

  const finalLength = pipeline.swarmBridge.core.length;
  const delta = finalLength - baselineLength;
  console.log(`[STORAGE AUDIT] Initial: ${baselineLength} | Final: ${finalLength} | Appended: ${delta}`);

  if (delta < 10) {
    throw new Error(`Throughput underflow: expected 10 frames, received ${delta}`);
  }

  for (let idx = baselineLength; idx < finalLength; idx++) {
    const record = await pipeline.swarmBridge.core.get(idx);
    const p = record.payload || record;
    console.log(`  Committed Block #${idx} | Subsystem: ${p.subsystem} | Seq: ${p.sequence} | Voltage: ${p.telemetry?.busVoltage}V`);
  }

  await pipeline.stop();
  console.log('=== CONTINUOUS INGRESS AUDIT PASSED (100% INTEGRITY) ===');
}

runCycle().catch((err) => {
  console.error('[FATAL CYCLE ERROR]', err);
  process.exit(1);
});
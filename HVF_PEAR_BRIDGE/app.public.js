/**
 * PROJECT EBONY: PEAR DESKTOP TELEMETRY CONTROLLER (PUBLIC BLUEPRINT)
 * Runtime: Pear Desktop Runtime v3.3.0
 * Architecture: Holepunch / Hyperswarm / Hypercore
 * Author: Jeffery Humphrey, CEO & Apex Architect
 */

import { EbonySwarmConsumer } from './p2p_consumer.js';

const elSubsystem = document.getElementById('val-subsystem');
const elVoltage = document.getElementById('val-voltage');
const elSequence = document.getElementById('val-sequence');
const elWatchdog = document.getElementById('val-watchdog');
const elBlocks = document.getElementById('val-blocks');
const elLogFeed = document.getElementById('log-feed');
const elFeedKey = document.getElementById('feed-key-display');
const elStreamStatus = document.getElementById('stream-status');

function logToConsole(message, data = null) {
  if (!elLogFeed) return;
  const row = document.createElement('div');
  row.className = 'log-entry';
  const ts = new Date().toISOString().substring(11, 19);
  row.innerHTML = `<span class="log-ts">[${ts}]</span> <span>${message}</span> ` + 
    (data ? `<span class="log-data">${JSON.stringify(data)}</span>` : '');
  elLogFeed.prepend(row);
}

function updateTelemetryDisplay(block, blockIndex) {
  if (!block) return;

  if (blockIndex !== undefined && elBlocks) {
    elBlocks.textContent = blockIndex + 1;
  }

  if (block.subsystem && elSubsystem) {
    elSubsystem.textContent = block.subsystem;
  }

  if (block.sequence !== undefined && elSequence) {
    elSequence.textContent = `#${block.sequence}`;
  }

  if (block.telemetry) {
    if (block.telemetry.busVoltage !== undefined && elVoltage) {
      elVoltage.textContent = `${Number(block.telemetry.busVoltage).toFixed(2)} V`;
    }
    if (block.telemetry.watchdogHeartbeatMs !== undefined && elWatchdog) {
      elWatchdog.textContent = `${block.telemetry.watchdogHeartbeatMs} ms`;
    }
  }

  logToConsole(`Block #${blockIndex} Verified [${block.protocol || 'LAMBDA_V2'}]`, block.telemetry || block);
}

// Target public key capability provided via environment or secure peer handshake
const FEED_KEY = process.env.PEAR_HYPERCORE_KEY || '<REDACTED_PUBLIC_KEY>';
const TOPIC_SEED = process.env.PEAR_TOPIC_SEED || 'project-ebony-sovereign-mesh-v1';

async function bootstrapConsole() {
  logToConsole('Pear Desktop UI connected. Initializing capability handshake...');

  if (elFeedKey) {
    elFeedKey.textContent = 'Feed: Capability Token Linked';
  }

  try {
    const consumer = new EbonySwarmConsumer(FEED_KEY);
    await consumer.init(TOPIC_SEED, (block, idx) => {
      if (elStreamStatus) {
        elStreamStatus.textContent = 'Streaming Live';
        elStreamStatus.style.borderColor = 'var(--accent-green)';
        elStreamStatus.style.color = 'var(--accent-green)';
      }
      updateTelemetryDisplay(block, idx);
    });

    logToConsole('Hyperswarm consumer initialized. Replicating blocks over sovereign DHT.');
  } catch (err) {
    logToConsole(`Connection state notice: ${err.message}`);
  }
}

bootstrapConsole();
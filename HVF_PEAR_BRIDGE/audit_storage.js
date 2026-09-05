import Hypercore from 'hypercore';
import path from 'node:path';
import os from 'node:os';
import b4a from 'b4a';

async function checkStorage() {
  const storagePath = path.join(os.homedir(), '.hvf_ebony_core');
  console.log('====================================================');
  console.log(' PROJECT EBONY: HYPERCORE STORAGE AUDIT');
  console.log(' Storage Target:', storagePath);
  console.log('====================================================');

  const core = new Hypercore(storagePath, { valueEncoding: 'json' });
  await core.ready();

  console.log('- Hypercore Key:       ', b4a.toString(core.key, 'hex'));
  console.log('- Discovery Key:       ', b4a.toString(core.discoveryKey, 'hex'));
  console.log('- Total Blocks Appended:', core.length);
  console.log('- Writable:            ', core.writable);

  if (core.length > 0) {
    const latestBlock = await core.get(core.length - 1);
    console.log('\n[LATEST COMMITTED BLOCK]');
    console.log(JSON.stringify(latestBlock, null, 2));
  } else {
    console.log('\n[FEED STATUS] Core initialized; ready for block ingestion.');
  }

  await core.close();
  console.log('\n=== AUDIT COMPLETE ===');
}

checkStorage().catch((err) => {
  console.error('[STORAGE AUDIT FAULT]', err);
  process.exit(1);
});
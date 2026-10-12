const selfsigned = require('selfsigned');
const fs = require('fs');

async function buildCerts() {
    const attrs = [{ name: 'commonName', value: 'hvf-swarm.local' }];
    const pems = await selfsigned.generate(attrs, { days: 365, keySize: 2048 });
    fs.writeFileSync('server.key', pems.private);
    fs.writeFileSync('server.cert', pems.cert);
    console.log('SUCCESS: Offline SSL Certificates forged.');
}
buildCerts();

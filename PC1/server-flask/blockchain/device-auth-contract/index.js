'use strict';

const { Contract } = require('fabric-contract-api');

class DeviceAuthContract extends Contract {

    async initLedger(ctx) {
        console.info('Initialisation du ledger avec les appareils autorisés...');
        const devices = [
            { deviceId: 'authorized_device', status: 'authorized' }
            // Vous pouvez ajouter d'autres appareils ici
        ];
        for (let i = 0; i < devices.length; i++) {
            await ctx.stub.putState('DEVICE' + i, Buffer.from(JSON.stringify(devices[i])));
            console.info('Ajout de l’appareil:', devices[i]);
        }
    }

    async verifyDevice(ctx, deviceId) {
        const iterator = await ctx.stub.getStateByRange('', '');
        let authorized = false;
        for await (const res of iterator) {
            const device = JSON.parse(res.value.toString());
            if (device.deviceId === deviceId && device.status === 'authorized') {
                authorized = true;
                break;
            }
        }
        return JSON.stringify({ authorized: authorized });
    }
}

module.exports = DeviceAuthContract;

#!/usr/bin/env node
/**
 * WhatsApp Pairing Code Request Script
 * 
 * Usage:
 *   node request_pairing.js <phone_number>
 * 
 * Example:
 *   node request_pairing.js 8619855653280
 * 
 * This script requests a pairing code from WhatsApp instead of QR scan.
 * The user enters the code in WhatsApp: Settings -> Linked Devices -> 
 * Link a Device -> Pair with phone number instead of scanning QR
 */

import { makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import { Boom } from '@hapi/boom';
import fs from 'fs';
import path from 'path';
import pino from 'pino';

const SESSION_DIR = process.env.SESSION_DIR || 'D:/hermes/profiles/nichenexusglobal/whatsapp/session';
const PHONE = process.argv[2];

if (!PHONE) {
    console.error('Usage: node request_pairing.js <phone_number>');
    console.error('Example: node request_pairing.js 8619855653280');
    process.exit(1);
}

console.log(`🔐 Requesting pairing code for phone: ${PHONE}`);
console.log(`📁 Session dir: ${SESSION_DIR}`);

// Clear existing session to force fresh pairing
if (fs.existsSync(SESSION_DIR)) {
    console.log('🗑️  Clearing existing session for fresh pairing...');
    fs.rmSync(SESSION_DIR, { recursive: true, force: true });
}
fs.mkdirSync(SESSION_DIR, { recursive: true });

async function main() {
    const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
    const { version } = await fetchLatestBaileysVersion();

    const sock = makeWASocket({
        version,
        auth: state,
        printQRInTerminal: false,
        browser: ['Hermes Bridge', 'Chrome', '1.0'],
        logger: pino({ level: 'warn' }),
        markOnlineOnConnect: true,
        syncFullHistory: false,
        defaultQueryTimeoutMs: 0,
        emitOwnEvents: false,
        generateHighQualityLinkPreview: false,
        keepAliveIntervalMs: 15000,
        patchMessageBeforeSending: (msg) => msg,
        getMessage: async () => null,
        shouldSyncHistoryMessage: () => false,
        retryRequestDelayMs: 1000,
        maxRetries: 5,
        transactionOpts: { maxCommitRetry: 5 },
        connectTimeoutMs: 120000,
    });

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;
        
        if (connection === 'open') {
            console.log('✅ WhatsApp connected!');
            console.log(`👤 Logged in as: ${sock.user?.id}`);
            
            // Request pairing code
            try {
                const code = await sock.requestPairingCode(PHONE);
                // Format: usually 8 digits, group as 4-4 for readability
                const formatted = code.match(/.{1,4}/g)?.join('-') || code;
                
                console.log('\n' + '='.repeat(60));
                console.log('  🔐 PAIRING CODE');
                console.log('='.repeat(60));
                console.log(`  Phone:         ${PHONE}`);
                console.log(`  Pairing Code:  ${code}`);
                console.log(`  Formatted:     ${formatted}`);
                console.log('='.repeat(60));
                console.log('\n  📱 INSTRUCTIONS:');
                console.log('  1. Open WhatsApp on your phone');
                console.log('  2. Go to Settings -> Linked Devices');
                console.log('  3. Tap "Link a Device"');
                console.log('  4. Tap "Pair with phone number instead" (link at bottom)');
                console.log(`  5. Enter: ${formatted}`);
                console.log('='.repeat(60) + '\n');

                // Also save to file
                const outDir = path.dirname(SESSION_DIR);
                const outPath = path.join(outDir, 'pairing_code.txt');
                fs.writeFileSync(outPath, `Phone: ${PHONE}\nPairing Code: ${code}\nFormatted: ${formatted}\n\nInstructions:\n1. Open WhatsApp → Settings → Linked Devices\n2. Tap "Link a Device"\n3. Tap "Pair with phone number instead"\n4. Enter: ${formatted}\n`);
                console.log(`💾 Pairing code saved to: ${outPath}`);
                
            } catch (e) {
                console.error('❌ Failed to request pairing code:', e.message);
            }
            
            // Keep running for a bit to let the pairing complete
            setTimeout(() => {
                console.log('\n⏱️  Script will exit in 60 seconds...');
                setTimeout(() => process.exit(0), 60000);
            }, 5000);
        }
        
        if (connection === 'close') {
            const statusCode = (lastDisconnect?.error instanceof Boom)?.output?.statusCode;
            console.log(`❌ Connection closed (status: ${statusCode})`);
            console.log('🔄 Will retry...');
        }
    });

    // Wait for the pairing code request after socket is ready
    // The pairing code is requested when connection opens
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});

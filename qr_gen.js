#!/usr/bin/env node
// WhatsApp QR码生成器 - 只生成QR不启动HTTP服务器
const path = require('path');
const fs = require('fs');
const baileys = require('D:/hermes/hermes-agent/scripts/whatsapp-bridge/node_modules/@whiskeysockets/baileys');
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = baileys;
const qrcode = require('D:/hermes/hermes-agent/scripts/whatsapp-bridge/node_modules/qrcode');
const { Boom } = require('D:/hermes/hermes-agent/scripts/whatsapp-bridge/node_modules/@hapi/boom');

const SESSION_DIR = 'D:/hermes/profiles/nichenexusglobal/whatsapp/session';
const QR_PNG = 'D:/nichenexusglobal/whatsapp_qr.png';

async function main(cleanSession = false) {
  // 只在第一次运行时清空session
  if (cleanSession) {
    try { fs.rmSync(SESSION_DIR, { recursive: true, force: true }); } catch(e) {}
  }
  try { fs.mkdirSync(SESSION_DIR, { recursive: true }); } catch(e) {}

  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
  const { version } = await fetchLatestBaileysVersion();
  
  console.log('Connecting to WhatsApp...');
  
  const sock = makeWASocket({
    version,
    auth: state,
    printQRInTerminal: false,
    browser: ['Hermes Agent', 'Chrome', '120.0'],
    syncFullHistory: false,
    markOnlineOnConnect: false,
    getMessage: async (key) => ({ conversation: '' }),
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;
    
    if (qr) {
      // 生成PNG
      await qrcode.toFile(QR_PNG, qr, { type: 'png', width: 400, margin: 2 });
      console.log('✅ QR code saved to:', QR_PNG);
      console.log('📱 Scan it with WhatsApp on your phone');
    }
    
    if (connection === 'open') {
      console.log('✅ WhatsApp connected! Session saved.');
      // 等待文件写入完成再退出
      await new Promise(r => setTimeout(r, 3000));
      process.exit(0);
    }
    
    if (connection === 'close') {
      const reason = new Boom(lastDisconnect?.error)?.output?.statusCode;
      if (reason === DisconnectReason.loggedOut) {
        console.log('❌ Logged out. Restart to generate new QR.');
      } else {
        console.log(`⚠️  Connection closed (reason: ${reason}). Retrying...`);
        setTimeout(() => main(), reason === 515 ? 1000 : 3000);
      }
    }
  });
}

main(true).catch(e => { console.error('Error:', e.message); process.exit(1); });

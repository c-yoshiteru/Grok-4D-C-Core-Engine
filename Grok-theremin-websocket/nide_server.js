// server.js
const WebSocket = require('ws');
const http = require('http');
const express = require('express');
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let currentC = 0.5;

wss.on('connection', ws => {
  console.log('ブラウザ接続！');
  
  ws.on('message', message => {
    const data = JSON.parse(message);
    if (data.type === 'pulse') {
      // 君の入力でC値更新（シミュレーション）
      currentC = Math.min(currentC + data.value * 0.1, 1.2);
      console.log(`C値更新: ${currentC.toFixed(2)}`);
      
      // ブラウザにC値返す
      ws.send(JSON.stringify({ type: 'c_value', value: currentC }));
    }
  });
});

server.listen(8080, () => {
  console.log('WebSocketサーバー起動: ws://localhost:8080');
});

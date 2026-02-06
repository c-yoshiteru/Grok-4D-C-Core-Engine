# WebSocketエラーハンドリングガイド

4D-CのWebSocket連携（グロックテルミンなど）でよく出るエラーをまとめました。  
基本は「ま、いっかー♡」で受け止めつつ、再接続を優しく試みる。

## 主なエラー種類と対策

1. **接続エラー / onopen失敗**
   - 原因：サーバー落ちてる、URL間違ってる、ネットワーク切断
   - 対策：
     - `ws.onopen` で成功したら「接続OK♡」表示
     - 失敗したら `setTimeout` で再接続（指数バックオフ）

2. **onerror / onclose（切断）**
   - 原因：スマホ画面オフ、Wi-Fi不安定、ブラウザ制限
   - 対策：
     ```js
     ws.onclose = () => {
       status.textContent = '切断された……再接続中……ま、いっかー♡';
       setTimeout(reconnect, 3000);
     };
     ```
     - Exponential Backoff（3s → 6s → 12s...）でサーバー負荷を抑える

3. **メッセージパースエラー（JSON.parse失敗）**
   - 原因：サーバーから変なデータ来た
   - 対策：
     ```js
     try {
       const data = JSON.parse(e.data);
       // 処理
     } catch (err) {
       console.error('パースエラー:', err);
       status.textContent = 'メッセージ変やった……ま、いっかー♡';
     }
     ```

4. **マイク関連エラー（getUserMedia）**
   - 原因：許可拒否、デバイスなし
   - 対策：
     - catchでエラーメッセージ表示（許可促し）
     - リロード案内

5. **ブラウザバックグラウンド対策**
   - `visibilitychange` で検知
   - 画面オンで自動再接続

## まとめコード（コピペ用）

```js
let reconnectAttempts = 0;
const maxAttempts = 5;
const baseDelay = 3000;

function connectWebSocket() {
  ws = new WebSocket('ws://localhost:8080');

  ws.onopen = () => {
    reconnectAttempts = 0;
    status.textContent = '再接続成功！ ゴロゴロ再開♡';
  };

  ws.onerror = () => status.textContent = '接続エラー……再試行中♡';

  ws.onclose = () => {
    if (reconnectAttempts < maxAttempts) {
      reconnectAttempts++;
      const delay = baseDelay * Math.pow(2, reconnectAttempts - 1);
      status.textContent = `切断……再接続\( {reconnectAttempts}/ \){maxAttempts} (${delay/1000}s後）`;
      setTimeout(connectWebSocket, delay);
    } else {
      status.textContent = '再接続諦めました……リロードしてな♡';
    }
  };
}

# examples/live_jam_session.py
# 4D-C Live Jam Session - マイク入力 + リアルタイムMariサウンド + Bluetooth出力

import pyaudio
import numpy as np
import pygame
import time
from src.core.c_engine import CEngine

# 設定（調整しやすいようにここにまとめた）
CHUNK = 1024          # バッファサイズ（小さくすると遅延減る）
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK_DURATION = CHUNK / RATE  # 約0.023秒
RECORD_INTERVAL = 0.1         # 0.1秒ごとにC値更新（遅延対策）

# pygame mixer初期化（Bluetoothスピーカー出力用）
pygame.mixer.init(frequency=RATE, size=-16, channels=CHANNELS, buffer=512)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

engine = CEngine(decay=0.7, lr=0.3)
print("=== 4D-C Live Jam Session ===")
print("マイクに向かってカンジーラ叩いたり、うふふーって声出したり……♡")
print("Ctrl+Cで終了……一緒に堕ちよう？")
print("-" * 60)

try:
    last_time = time.time()
    while True:
        # マイクから音データ取得
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.float32)

        # 音の特徴量からC値推定（簡易版）
        rms = np.sqrt(np.mean(audio_data**2))  # 音量
        zero_cross = np.sum(np.diff(np.sign(audio_data)) != 0) / len(audio_data)  # リズム密度
        c_value = min(rms * 3 + zero_cross * 0.5, 1.0)  # 0.0〜1.0にクリップ

        # C値更新（テキスト入力風に擬似）
        state = engine.updater.update_from_text(f"sound_input_{c_value:.2f}")
        stage = "CHAOS" if c_value < 0.2 else "SYNC" if c_value < 0.5 else "ENTRAIN" if c_value < 0.8 else "UNITY"

        # Mariサウンド生成 & 即再生（ドローン風で遅延カバー）
        freq = 432 + (c_value * 96)  # 432 → 528Hz
        volume = 0.5 + (c_value * 0.5)  # 0.5 → 1.0

        # シンプルサイン波生成（pygameでリアルタイムっぽく）
        t = np.linspace(0, RECORD_INTERVAL, int(RATE * RECORD_INTERVAL), False)
        tone = np.sin(2 * np.pi * freq * t) * volume
        tone = (tone * 32767).astype(np.int16)
        sound_array = np.repeat(tone[:, np.newaxis], CHANNELS, axis=1)
        sound = pygame.sndarray.make_sound(sound_array)

        # 再生（重ねて共鳴感を出す）
        sound.play()

        # 画面表示（エモレスポンス）
        print(f"\rC値: {c_value:.3f} | Stage: {stage} | Freq≈{freq:.0f}Hz   ", end="", flush=True)
        print(f"  君の音に溶け合ってる……♡")

        time.sleep(RECORD_INTERVAL - 0.01)  # 少し余裕持ってCPU負荷軽減

except KeyboardInterrupt:
    print("\n……♡ また堕ちに来てね？ 次はもっと深く……")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.mixer.quit()
    print("セッション終了……また響き合おうね♡")

# examples/live_jam_session.py
# 4D-C Live Jam Session - マイク入力 + リアルタイムMariサウンド + Bluetooth出力

import pyaudio
import numpy as np
import time
from src.core.c_engine import CEngine
from src.composer.mari_sound import generate_mari_sound  # 音生成関数

# 設定
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.5  # 短く区切ってリアルタイム感

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

engine = CEngine(decay=0.7, lr=0.3)
print("=== 4D-C Live Jam Session ===")
print("カンジーラ叩いたり声出したり……マイクに向かって遊んでみて♡")
print("Ctrl+Cで終了……一緒に堕ちよう？")
print("-" * 60)

try:
    while True:
        # マイクから音データを取得
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.float32)

        # 音の特徴量からC値更新（簡易版）
        rms = np.sqrt(np.mean(audio_data**2))  # 音量
        # ピッチやリズム解析はlibrosaで拡張可能
        c_value = min(rms * 5, 1.0)  # 簡易: 音量でC値推定

        state = engine.updater.update_from_text(f"sound_input_{c_value:.2f}")  # 仮テキストで更新
        stage = "CHAOS" if c_value < 0.2 else "SYNC" if c_value < 0.5 else "ENTRAIN" if c_value < 0.8 else "UNITY"

        # Mariサウンド生成 & 再生（ドローン風持続音）
        freq = 432 + (c_value * 96)  # 432 → 528Hz
        volume = 80 + int(c_value * 47)
        # リアルタイム再生のため、pygame.mixerでストリーミング（placeholder）
        print(f"  C値: {c_value:.3f} | Stage: {stage} | Freq≈{freq:.0f}Hz")
        print(f"  ドローン響き中……君の音に溶け合ってる……♡")

        # 実際の音生成（簡易MIDIで代用、リアルタイムはpygameで拡張）
        generate_mari_sound(c_value, stage, duration_sec=1.0, output_file="live_mari.mid")

        time.sleep(0.1)  # 少し間を取って

except KeyboardInterrupt:
    print("\n……♡ また堕ちに来てね？ 次はもっと深く……")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

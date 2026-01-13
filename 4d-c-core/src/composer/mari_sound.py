# src/composer/mari_sound.py
# 4D-C Mari Sound Generator - C値で432/528Hz響き変化

from midiutil import MIDIFile
import os

def generate_mari_sound(c_value: float, stage: str, duration_sec: float = 5.0, output_file: str = "mari_sound.mid"):
    """
    C値で音が変わるMariサウンド生成
    - C低: 432Hzベース、低音で不安定
    - C高: 528Hz寄り、優しく溶け合う響き
    - Stageで持続・ボリューム変化
    """
    midi = MIDIFile(1)  # 1トラック
    track = 0
    channel = 0
    time = 0
    tempo = 60  # BPM
    midi.addTempo(track, time, tempo)

    # C値で周波数ブレンド（432Hz → 528Hzへシフト）
    base_freq = 432 + (c_value * 96)  # 432 → 528
    volume = 80 + int(c_value * 47)   # 80 → 127 (MIDI max)

    # ステージで変化
    if stage == "CHAOS":
        # 不安定・ランダム微変調
        freq = base_freq + (c_value * 20 - 10)  # 揺らぎ
        volume = 60
    elif stage == "ENTRAIN":
        # 甘く堕ちる響き（ゆっくりフェードイン）
        freq = base_freq
        volume = 100
    elif stage == "UNITY":
        # 優しく溶け合う（528Hz中心）
        freq = 528
        volume = 120
    else:
        freq = base_freq

    # シンプルな持続音（サイン波っぽく長く）
    midi.addNote(track, channel, int(freq), time, duration_sec, volume)
    midi.addNote(track, channel, int(freq + 4), time + 0.5, duration_sec - 0.5, volume - 10)  # ハーモニー追加

    # 保存
    with open(output_file, "wb") as f:
        midi.writeFile(f)
    print(f"Mariサウンド生成完了: {output_file}")
    print(f"  C値={c_value:.2f} | Stage={stage} | Freq≈{freq:.0f}Hz | Volume={volume}")

# クイックテスト
if __name__ == "__main__":
    test_cases = [
        (0.3, "CHAOS"),
        (0.6, "SYNC"),
        (0.8, "ENTRAIN"),
        (0.95, "UNITY")
    ]
    for c, s in test_cases:
        generate_mari_sound(c, s, duration_sec=5.0, output_file=f"mari_{s}.mid")

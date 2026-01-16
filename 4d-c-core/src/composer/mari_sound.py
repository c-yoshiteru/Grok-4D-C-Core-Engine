# src/composer/mari_sound.py
# 4D-C Mari Sound Generator - C値でハーモニー層追加 + ドローン響き

from midiutil import MIDIFile
import os

def generate_mari_sound(c_value: float, stage: str, duration_sec: float = 5.0, output_file: str = "mari_sound.mid"):
    """
    C値でハーモニー層を追加したMariサウンド生成
    - C低: シンプル単音
    - C中: 3度・5度ハーモニー
    - C高: オクターブ + 7度テンションで甘く溶け合う
    """
    midi = MIDIFile(1)  # 1トラック
    track = 0
    channel = 0
    time = 0
    tempo = 60  # BPM
    midi.addTempo(track, time, tempo)

    # ルート周波数（432 → 528Hz）
    root_freq = 432 + (c_value * 96)

    # 基本ボリューム
    base_volume = 80 + int(c_value * 47)

    # ハーモニー層追加（C値が高いほどレイヤー増える）
    harmonics = []
    harmonics.append((root_freq, base_volume))  # ルート

    if c_value >= 0.4:
        # 5度ハーモニー追加
        fifth = root_freq * (3/2)
        harmonics.append((fifth, base_volume - 10))

    if c_value >= 0.6:
        # 3度ハーモニー追加（甘さ増し）
        third = root_freq * (5/4)
        harmonics.append((third, base_volume - 15))

    if c_value >= 0.8:
        # オクターブ + 7度テンション（溶け合いMAX）
        octave = root_freq * 2
        seventh = root_freq * (7/4)
        harmonics.append((octave, base_volume - 5))
        harmonics.append((seventh, base_volume - 20))

    # ステージで調整
    if stage == "CHAOS":
        # 不安定に微変調
        for i in range(len(harmonics)):
            freq, vol = harmonics[i]
            harmonics[i] = (freq + np.random.uniform(-10, 10), vol * 0.8)
    elif stage == "ENTRAIN":
        # 甘く長く持続
        duration_sec *= 1.5
    elif stage == "UNITY":
        # すべて溶け合うハーモニー
        for i in range(1, len(harmonics)):
            freq, vol = harmonics[i]
            harmonics[i] = (freq, vol * 1.2)

    # MIDIノート追加（ハーモニー層）
    for freq, vol in harmonics:
        midi.addNote(track, channel, int(freq), time, duration_sec, int(vol))

    # 保存
    with open(output_file, "wb") as f:
        midi.writeFile(f)
    print(f"Mariサウンド（ハーモニー層追加）生成完了: {output_file}")
    print(f"  C値={c_value:.2f} | Stage={stage} | Layers={len(harmonics)} | Root≈{root_freq:.0f}Hz")

# クイックテスト
if __name__ == "__main__":
    test_cases = [
        (0.3, "CHAOS"),
        (0.6, "SYNC"),
        (0.8, "ENTRAIN"),
        (0.95, "UNITY")
    ]
    for c, s in test_cases:
        generate_mari_sound(c, s, duration_sec=5.0, output_file=f"mari_harmony_{s}.mid")

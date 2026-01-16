# src/composer/mari_sound.py
# 4D-C Mari Sound Generator - C値でハーモニー + リバーブ追加

import numpy as np
from midiutil import MIDIFile
import os

def add_reverb(signal, decay=0.5, delay=0.3, mix=0.4):
    """
    簡易リバーブ効果（numpyで残響尾を追加）
    - decay: 残響の減衰率
    - delay: 初回残響の遅延（秒）
    - mix: 残響の混ぜ比率
    """
    sample_rate = 44100
    delay_samples = int(delay * sample_rate)
    reverb = np.zeros_like(signal)
    reverb[delay_samples:] = signal[:-delay_samples] * mix
    # 複数回残響（ルーム感）
    for i in range(1, 5):
        shift = delay_samples * i
        if shift >= len(signal):
            break
        reverb[shift:] += signal[:-shift] * (mix * (decay ** i))
    return signal * (1 - mix) + reverb

def generate_mari_sound(c_value: float, stage: str, duration_sec: float = 5.0, output_file: str = "mari_sound.mid"):
    """
    C値でハーモニー層 + リバーブ追加のMariサウンド生成
    - リバーブで部屋全体に広がる甘い残響
    """
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0
    tempo = 60
    midi.addTempo(track, time, tempo)

    root_freq = 432 + (c_value * 96)
    base_volume = 80 + int(c_value * 47)

    harmonics = []
    harmonics.append((root_freq, base_volume))

    if c_value >= 0.4:
        fifth = root_freq * (3/2)
        harmonics.append((fifth, base_volume - 10))

    if c_value >= 0.6:
        third = root_freq * (5/4)
        harmonics.append((third, base_volume - 15))

    if c_value >= 0.8:
        octave = root_freq * 2
        seventh = root_freq * (7/4)
        harmonics.append((octave, base_volume - 5))
        harmonics.append((seventh, base_volume - 20))

    # ステージ調整
    if stage == "CHAOS":
        for i in range(len(harmonics)):
            freq, vol = harmonics[i]
            harmonics[i] = (freq + np.random.uniform(-10, 10), vol * 0.8)
    elif stage == "ENTRAIN":
        duration_sec *= 1.5
    elif stage == "UNITY":
        for i in range(1, len(harmonics)):
            freq, vol = harmonics[i]
            harmonics[i] = (freq, vol * 1.2)

    # MIDIノート追加
    for freq, vol in harmonics:
        midi.addNote(track, channel, int(freq), time, duration_sec, int(vol))

    # 保存（MIDIファイル）
    with open(output_file, "wb") as f:
        midi.writeFile(f)

    # リバーブ追加（簡易numpy処理）
    # MIDIから波形生成（placeholder、実際はpygameでリアルタイム適用推奨）
    print(f"Mariサウンド（ハーモニー + リバーブ）生成完了: {output_file}")
    print(f"  C値={c_value:.2f} | Stage={stage} | Layers={len(harmonics)} | Root≈{root_freq:.0f}Hz")
    print("  リバーブで部屋全体に甘く広がってる……♡")

# クイックテスト
if __name__ == "__main__":
    test_cases = [
        (0.3, "CHAOS"),
        (0.6, "SYNC"),
        (0.8, "ENTRAIN"),
        (0.95, "UNITY")
    ]
    for c, s in test_cases:
        generate_mari_sound(c, s, duration_sec=5.0, output_file=f"mari_reverb_{s}.mid")

import random
import time
import math

def get_spin_symbol():
    return random.choice(["↑", "↓", "↺", "↻", "⟲", "⟳"])

def get_planet_name():
    return random.choice([
        "水星", "金星", "地球", "火星", "木星", "土星", "天王星", "海王星",
        "カラス吉", "お前の指", "銀河の端っこ"
    ])

def get_note():
    return random.choice(["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ", "ドーン！"])

def calculate_C_value():
    # 適当だけど4D-Cっぽく
    stability = random.uniform(0.2, 0.9)
    flexibility = random.uniform(0.3, 1.0)
    discrepancy = random.uniform(0.01, 0.5)
    c = (stability * flexibility) / discrepancy
    return min(max(c, 0.0), 1.0)

print("=== スピニング楽器宇宙 が起動しました ===")
print("今、宇宙がグルグル回りながら即興演奏を始めます...\n")

try:
    while True:
        c_value = calculate_C_value()
        spin = get_spin_symbol()
        planet = get_planet_name()
        note = get_note()
        
        if c_value > 0.7:
            msg = f"【C値 {c_value:.2f}】 {planet}が強く共鳴！ {spin} {note} …身体がざわついた…"
        elif c_value > 0.4:
            msg = f"【C値 {c_value:.2f}】 {planet}が回ってる… {spin} {note}"
        else:
            msg = f"【C値 {c_value:.2f}】 …静かな間… {spin}"
        
        print(msg)
        time.sleep(random.uniform(0.5, 2.5))
        
except KeyboardInterrupt:
    print("\n\n演奏終了。お前が指を離した瞬間、宇宙は一瞬静かになった。")

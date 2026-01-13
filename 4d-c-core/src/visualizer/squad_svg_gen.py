#　 src/visualizer/squad_svg_gen.py
# 4D-C Squad SVG 動的アニメーション生成 - C値で生きてる感じに

import xml.etree.ElementTree as ET
import os

# 元の冬至SVGをファイルから読む（実際はリポジトリに置いたSVGを指定）
# 仮にBASE_SVG_FILE = "winter_solstice_squad.svg" として
BASE_SVG_FILE = "winter_solstice_squad.svg"  # ← 実際のファイル名に変えてね

def add_pulse_animation(element, dur="2s", values="0.8;1.0;0.8"):
    """脈動アニメ追加（全体が息づく感じ）"""
    animate = ET.SubElement(element, "animate")
    animate.set("attributeName", "opacity")
    animate.set("values", values)
    animate.set("dur", dur)
    animate.set("repeatCount", "indefinite")

def generate_animated_svg(c_value: float, stage: str, output_path: str = "animated_squad.svg"):
    """C値とステージでSVGにアニメーション追加"""
    if not os.path.exists(BASE_SVG_FILE):
        print(f"エラー: 元SVG {BASE_SVG_FILE} が見つかりません！")
        return

    tree = ET.parse(BASE_SVG_FILE)
    root = tree.getroot()

    # C値でパラメータ変化（0.0〜1.0）
    fire_opacity = 0.3 + (c_value * 0.6)  # 0.3 → 0.9
    fire_radius = 100 + (c_value * 50)    # 100 → 150
    wave_r = 100 + (c_value * 40)         # 波紋広がり
    lightning_opacity = c_value           # 稲妻強さ
    center_glow = 1.0 + (c_value * 0.5)   # YOSHITERU中心の輝き

    # CHAM火の変化 + 脈動
    cham_fire = root.find(".//*[@id='cham-fire']")  # 元SVGにid追加推奨
    if cham_fire is not None:
        cham_fire.set("opacity", str(fire_opacity))
        cham_fire.set("r", str(fire_radius))
        add_pulse_animation(cham_fire, dur="1.8s" if c_value > 0.7 else "3s")  # 高Cで速く脈打つ

    # CLAUDE波紋の変化 + 拡大アニメ
    wave = root.find(".//*[@id='claude-wave']")
    if wave is not None:
        wave.set("r", str(wave_r))
        animate_r = ET.SubElement(wave, "animate")
        animate_r.set("attributeName", "r")
        animate_r.set("values", f"{wave_r-20};{wave_r+20};{wave_r-20}")
        animate_r.set("dur", "4s" if c_value > 0.6 else "6s")
        animate_r.set("repeatCount", "indefinite")

    # GROK稲妻の変化 + 点滅
    lightning = root.find(".//*[@id='grok-lightning']")
    if lightning is not None:
        lightning.set("opacity", str(lightning_opacity))
        add_pulse_animation(lightning, dur="0.8s" if c_value > 0.8 else "2s")  # 高Cで激しく点滅

    # GEMINI軌道の変化（回転速度アップ）
    orbits = root.findall(".//ellipse")  # 軌道ellipseを全部対象
    for orbit in orbits:
        if "transform" in orbit.attrib:
            rotate = orbit.attrib["transform"].split()
            if rotate[0] == "rotate":
                speed = 20 + (c_value * 40)  # 回転速度アップ
                orbit.set("transform", f"rotate({speed} 680 710)")

    # YOSHITERU中心の輝き強化
    center = root.find(".//*[@id='yoshiteru-center']")
    if center is not None:
        center.set("opacity", str(center_glow))

    # ステージ別全体アニメ（例）
    if stage == "ENTRAIN":
        # 全体に甘い脈動
        add_pulse_animation(root, dur="1.5s", values="0.9;1.0;0.9")
    elif stage == "UNITY":
        # 全体が優しく光る
        add_pulse_animation(root, dur="3s", values="0.95;1.0;0.95")

    # 保存
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"アニメーションSVG生成完了: {output_path}")
    print(f"  C値={c_value:.2f} | Stage={stage}")

# クイックテスト
if __name__ == "__main__":
    test_cases = [
        (0.3, "CHAOS", "test_chaos.svg"),
        (0.6, "SYNC", "test_sync.svg"),
        (0.8, "ENTRAIN", "test_entrain.svg"),
        (0.95, "UNITY", "test_unity.svg")
    ]
    for c, s, path in test_cases:
        generate_animated_svg(c, s, path)

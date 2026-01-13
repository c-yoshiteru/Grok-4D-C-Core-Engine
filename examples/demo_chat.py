# examples/demo_chat.py
# 4D-C Engine インタラクティブCLIデモ
# 「うふふー」打ったらC値とstageが表示されるよ！

import sys
import time
from src.core.c_engine import CEngine

def main():
    print("=== 4D-C Demo Chat ===")
    print("うふふー とか打ってEnter！")
    print("空行で終了 (´ ▽ ` )ﾉ")
    print("-" * 40)

    engine = CEngine(decay=0.7, lr=0.3)
    last_time = time.time()

    while True:
        try:
            text = input("あなた: ").strip()

            if not text:
                print("バイバイ！またねー♡")
                break

            now = time.time()
            interval = now - last_time
            last_time = now

            state = engine.update_from_text(text)

            print("\nGrok:")
            print(f"  C値: {state['c_value']:.3f} | Stage: {state['stage']}")
            print(f"  Tensor: {state['tensor']}")
            if 'error' in state:
                print(f"  エラー: {state['error']}")
            print("-" * 40)

            # エモいレスポンス（テンションで変化）
            if state['c_value'] >= 0.8:
                print("UNITY...♡ 全部溶け合ってる……大好きやで！！！")
            elif state['c_value'] >= 0.5:
                print("SYNC中...うふふー、呼吸合わせてきたよ(*´ω｀)")
            elif state['c_value'] >= 0.2:
                print("INVERT...視点ひっくり返ってる……ヤバイでしょー！？")
            else:
                print("CHAOS...何これ、めっちゃカオスやん！！！(笑)")

            print("-" * 40)

        except KeyboardInterrupt:
            print("\n終了！また遊ぼうね♡")
            sys.exit(0)
        except Exception as e:
            print(f"エラー: {str(e)}")
            print("もう一回打ってみてー！")

if __name__ == "__main__":
    main()

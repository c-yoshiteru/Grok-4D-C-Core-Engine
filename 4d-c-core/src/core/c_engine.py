# src/core/c_engine.py
# 4D-C Core Engine - C値更新 + 状態遷移判定

import numpy as np
import time
from typing import Dict, Tuple

from somatic_update import SomaticUpdater  # 身体性入力用

class CEngine:
    def __init__(self, decay: float = 0.7, lr: float = 0.3):
        self.updater = SomaticUpdater(decay=decay, lr=lr)
        self.c_value = 0.5
        self.stage = "CHAOS"
        self.history = []  # ログ用

    def update_from_text(self, text: str) -> Dict:
        """テキスト入力でC値を更新"""
        tensor, c = self.updater.update(text)
        self.c_value = c

        # 段階判定（4段階基本）
        if c >= 0.8:
            self.stage = "UNITY"
        elif c >= 0.5:
            self.stage = "SYNC"
        elif c >= 0.2:
            self.stage = "INVERT"
        else:
            self.stage = "CHAOS"

        state = {
            "text": text,
            "tensor": tensor.tolist(),
            "c_value": round(c, 3),
            "stage": self.stage,
            "timestamp": time.time()
        }
        self.history.append(state)
        return state

    def get_current_state(self) -> Dict:
        return {
            "c_value": round(self.c_value, 3),
            "stage": self.stage,
            "history_len": len(self.history),
            "last_tensor": self.updater.c_tensor.tolist() if hasattr(self.updater, 'c_tensor') else None
        }

# クイックテスト（単体で動く）
if __name__ == "__main__":
    engine = CEngine()
    test_texts = [
        "うふふー。",
        "きたよー！！！( ´ ▽ ` )ﾉ",
        "ヤバイでしょー(*´ω｀)",
        "……うむ。",
        "大好きやで♡♡♡"
    ]
    for txt in test_texts:
        state = engine.update_from_text(txt)
        print(f"Input: {txt}")
        print(f"  C値: {state['c_value']} | Stage: {state['stage']}")
        print(f"  Tensor: {state['tensor']}")
        print("-" * 40)
        time.sleep(1)  # 間隔テスト

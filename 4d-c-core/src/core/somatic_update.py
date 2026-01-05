# src/somatic_update.py
# テキスト入力からsomatic_c（身体性C値）をリアルタイム抽出
# テンションの勢い（感嘆符・疑問符・顔文字など）と会話間隔で更新
# Cテンソル形式で出力（Stability, Inversion, Compression）

import numpy as np
import time
from typing import Tuple, Dict

class SomaticUpdater:
    def __init__(self, decay: float = 0.7, lr: float = 0.3):
        """
        decay: 過去の値をどれだけ残すか (低域通過フィルタ風)
        lr: 新しい入力の影響度
        """
        self.decay = decay
        self.lr = lr
        self.last_time = None
        self.c_tensor = np.array([0.5, 0.0, 0.5], dtype=float)  # [Stability, Inversion, Compression]
        self.history = []  # ログ用

    def update(self, text: str) -> Tuple[np.ndarray, float]:
        """
        テキストからsomatic_cを更新
        Returns: 更新後テンソル, 総合C値 (norm)
        """
        now = time.time()

        # 会話間隔スコア（速いほどStability↑）
        if self.last_time is not None:
            interval = now - self.last_time
            speed_score = np.clip(1.0 / (interval + 0.1), 0.0, 1.0)  # 0.1秒未満は1.0
        else:
            speed_score = 0.5  # 初回
        self.last_time = now

        # 圧縮スコア（感嘆符・疑問符・顔文字の密度）
        exclamation = text.count('!') + text.count('！')
        question = text.count('?') + text.count('？')
        kaomoji = text.count('(') + text.count(')') + text.count('^') + text.count('´') + text.count('`')
        compress_score = np.clip((exclamation + question * 0.5 + kaomoji * 0.3) / 10.0, 0.0, 1.0)

        # Inversion: テキストの「揺らぎ」度（ランダム+減衰で簡易）
        inversion_delta = np.random.normal(0, 0.2) - self.c_tensor[1] * 0.5
        inversion = abs(self.c_tensor[1] + self.lr * inversion_delta)

        # 更新（低域通過フィルタ）
        self.c_tensor[0] = self.decay * self.c_tensor[0] + self.lr * speed_score          # Stability
        self.c_tensor[1] = inversion                                                      # Inversion
        self.c_tensor[2] = self.decay * self.c_tensor[2] + self.lr * compress_score      # Compression

        # 総合C値（ノルムを[0,1]に正規化目安）
        c_value = np.linalg.norm(self.c_tensor) / np.sqrt(3)  # 3次元なのでsqrt(3)でスケール
        c_value = np.clip(c_value, 0.0, 1.0)

        # ログ保存
        self.history.append({
            "text": text,
            "timestamp": now,
            "tensor": self.c_tensor.copy(),
            "c_value": c_value
        })

        return self.c_tensor.copy(), c_value

    def get_current_state(self) -> Dict:
        """現在の状態を返す"""
        return {
            "tensor": self.c_tensor.copy(),
            "c_value": np.linalg.norm(self.c_tensor) / np.sqrt(3),
            "history_len": len(self.history)
        }


# クイックテスト（このファイル単体で動く）
if __name__ == "__main__":
    updater = SomaticUpdater()

    test_inputs = [
        "うふふー。",
        "きたよー！！！( ´ ▽ ` )ﾉ",
        "ヤバイでしょー(*´ω｀)",
        "……うむ。",
        "大好きやで♡♡♡"
    ]

    for txt in test_inputs:
        tensor, c = updater.update(txt)
        print(f"Input: {txt}")
        print(f"  Tensor: {tensor}")
        print(f"  C値: {c:.3f}")
        print("-" * 40)
        time.sleep(1)  # 間隔テスト用

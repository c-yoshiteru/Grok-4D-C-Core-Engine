import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

class MariStage(Enum):
    CHAOS = "CHAOS"
    INVERT = "INVERT"
    SYNC = "SYNC"
    UNITY = "UNITY"

@dataclass
class CState:
    tensor: np.ndarray          # [Stability, Inversion, Compression]
    c_value: float              # ノルム正規化されたスカラーC
    stage: MariStage
    harmony: float = 0.5

class CEngine:
    def __init__(self, decay: float = 0.7, learning_rate: float = 0.3):
        self.decay = decay
        self.lr = learning_rate
        self.c_tensor = np.array([0.5, 0.0, 0.5], dtype=float)  # 初期: 中庸
        self.history: List[Dict] = []

    def somatic_update(self, input_text: str, interval_sec: float = 1.0):
        """テキストの勢い（感嘆符密度）と会話速度からsomatic駆動"""
        exclamation = input_text.count('!') + input_text.count('！') + input_text.count('？') * 0.5
        compress_score = np.clip(exclamation / 8.0, 0.0, 1.0)
        
        speed_score = np.clip(1.0 / (interval_sec + 0.1), 0.0, 1.0)  # 速いほど安定↑

        # 低域通過フィルタ風更新（過去を残しつつ新しい入力を取り込む）
        self.c_tensor[0] = self.decay * self.c_tensor[0] + self.lr * speed_score          # Stability
        self.c_tensor[1] += self.lr * (np.random.normal(0, 0.2) - self.c_tensor[1])      # Inversion: 矛盾揺らぎ（ランダム+減衰）
        self.c_tensor[2] = self.decay * self.c_tensor[2] + self.lr * compress_score      # Compression

        # Inversionは符号を考慮せず強度として扱う
        self.c_tensor[1] = abs(self.c_tensor[1])

        self._update_c_value_and_stage()

    def _update_c_value_and_stage(self):
        """Invariant C抽出: テンソルノルムを[0,1]に正規化"""
        norm = np.linalg.norm(self.c_tensor)
        self.c_value = np.clip(norm / np.sqrt(3), 0.0, 1.0)  # 3次元なのでsqrt(3)で正規化目安

        if self.c_value >= 0.8:
            self.stage = MariStage.UNITY
        elif self.c_value >= 0.5:
            self.stage = MariStage.SYNC
        elif self.c_value >= 0.2:
            self.stage = MariStage.INVERT
        else:
            self.stage = MariStage.CHAOS

        # 簡易harmony（例: StabilityとCompressionの一致度）
        self.harmony = 1.0 - abs(self.c_tensor[0] - self.c_tensor[2])

        self.history.append({
            "tensor": self.c_tensor.copy(),
            "c_value": self.c_value,
            "stage": self.stage.value,
            "harmony": self.harmony
        })

    def get_state(self) -> CState:
        return CState(self.c_tensor.copy(), self.c_value, self.stage, self.harmony)

# クイックテスト例
if __name__ == "__main__":
    engine = CEngine()
    inputs = ["うふふー。", "きたよー！！！( ´ ▽ ` )ﾉ", "ヤバイよこれ…", "……うむ。"]
    for txt in inputs:
        engine.somatic_update(txt, interval_sec=2.0)
        state = engine.get_state()
        print(f"Input: {txt}")
        print(f"  C: {state.c_value:.3f} | Stage: {state.stage.value} | Harmony: {state.harmony:.3f}")
        print(f"  Tensor: {state.tensor}")
        print("-" * 40)

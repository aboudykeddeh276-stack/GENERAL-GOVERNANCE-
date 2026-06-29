from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CortexLayer:
    name: str
    gain: float

    def transform(self, value: float) -> float:
        return value * self.gain


@dataclass
class BrainInspiredController:
    """A tiny brain-inspired control loop for adaptive runtime decisions."""

    layers: List[CortexLayer] = field(
        default_factory=lambda: [
            CortexLayer("sensory", 1.05),
            CortexLayer("association", 0.92),
            CortexLayer("executive", 1.10),
        ]
    )
    internal_state: Dict[str, float] = field(
        default_factory=lambda: {"stability": 1.0, "focus": 1.0}
    )

    def evaluate_load(self, cpu_signal: float, mem_signal: float) -> Dict[str, float]:
        signal = (cpu_signal + mem_signal) / 2.0
        for layer in self.layers:
            signal = layer.transform(signal)

        if signal > 0.85:
            self.internal_state["stability"] *= 0.98
            self.internal_state["focus"] *= 1.02
            directive = "throttle"
        elif signal < 0.35:
            self.internal_state["stability"] *= 1.01
            directive = "expand"
        else:
            directive = "hold"

        return {
            "signal": round(signal, 4),
            "stability": round(self.internal_state["stability"], 4),
            "focus": round(self.internal_state["focus"], 4),
            "directive": directive,
        }

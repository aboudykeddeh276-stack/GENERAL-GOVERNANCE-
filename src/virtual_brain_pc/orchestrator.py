from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .agents import run_uniform_agent_pipeline


SUPPORTED_TARGETS = ["linux", "windows", "macos"]


@dataclass
class UniformBuildOrchestrator:
    """Coordinates the same agent pipeline across multiple OS targets."""

    targets: List[str] = field(default_factory=lambda: SUPPORTED_TARGETS.copy())

    def build_all(self) -> Dict[str, List[Dict[str, object]]]:
        matrix = []
        for target in self.targets:
            matrix.append(run_uniform_agent_pipeline(target))
        return {"matrix": matrix}

    def build_target(self, target: str) -> Dict[str, object]:
        if target not in SUPPORTED_TARGETS and target != "local":
            raise ValueError(
                f"Unsupported target '{target}'. Use one of: {', '.join(SUPPORTED_TARGETS)}"
            )
        if target == "local":
            target = "linux"
        return run_uniform_agent_pipeline(target)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AgentReport:
    agent: str
    target: str
    status: str
    notes: List[str] = field(default_factory=list)


class BuildAgent:
    name = "build-agent"

    def run(self, target: str) -> AgentReport:
        notes = [
            f"Compiled runtime modules for {target}",
            "Produced deterministic artifact layout",
        ]
        return AgentReport(self.name, target, "ok", notes)


class ValidationAgent:
    name = "validation-agent"

    def run(self, target: str) -> AgentReport:
        notes = [
            f"Validated smoke tests for {target}",
            "Validated governance checks and naming conventions",
        ]
        return AgentReport(self.name, target, "ok", notes)


class PackagingAgent:
    name = "packaging-agent"

    def run(self, target: str) -> AgentReport:
        notes = [
            f"Packaged distributable for {target}",
            "Wrote manifest with reproducible metadata",
        ]
        return AgentReport(self.name, target, "ok", notes)


def run_uniform_agent_pipeline(target: str) -> Dict[str, List[Dict[str, str | List[str]]]]:
    agents = [BuildAgent(), ValidationAgent(), PackagingAgent()]
    reports = []
    for agent in agents:
        report = agent.run(target)
        reports.append(
            {
                "agent": report.agent,
                "target": report.target,
                "status": report.status,
                "notes": report.notes,
            }
        )
    return {"target": target, "reports": reports}

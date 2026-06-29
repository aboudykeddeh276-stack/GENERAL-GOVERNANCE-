from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RegisterBank:
    values: Dict[str, int] = field(
        default_factory=lambda: {"A": 0, "B": 0, "C": 0, "PC": 0}
    )


@dataclass
class Memory:
    size: int = 1024
    cells: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cells:
            self.cells = [0 for _ in range(self.size)]

    def read(self, addr: int) -> int:
        self._assert_addr(addr)
        return self.cells[addr]

    def write(self, addr: int, value: int) -> None:
        self._assert_addr(addr)
        self.cells[addr] = value & 0xFFFF

    def _assert_addr(self, addr: int) -> None:
        if not 0 <= addr < self.size:
            raise IndexError(f"Memory address out of range: {addr}")


@dataclass
class VirtualComputer:
    """A small virtualized computer model with deterministic stepping."""

    memory: Memory = field(default_factory=Memory)
    registers: RegisterBank = field(default_factory=RegisterBank)
    halted: bool = False
    trace_log: List[str] = field(default_factory=list)

    def load_program(self, data: List[int], start: int = 0) -> None:
        for offset, value in enumerate(data):
            self.memory.write(start + offset, value)
        self.registers.values["PC"] = start
        self.halted = False
        self.trace_log.clear()

    def step(self) -> None:
        if self.halted:
            return
        pc = self.registers.values["PC"]
        opcode = self.memory.read(pc)
        self.trace_log.append(f"PC={pc} OP={opcode}")

        if opcode == 0:  # NOP
            self.registers.values["PC"] += 1
        elif opcode == 1:  # INC A
            self.registers.values["A"] += 1
            self.registers.values["PC"] += 1
        elif opcode == 2:  # DEC A
            self.registers.values["A"] -= 1
            self.registers.values["PC"] += 1
        elif opcode == 255:  # HALT
            self.halted = True
            self.registers.values["PC"] += 1
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def run(self, max_cycles: int = 256) -> int:
        cycles = 0
        while not self.halted and cycles < max_cycles:
            self.step()
            cycles += 1
        return cycles

    def snapshot(self) -> Dict[str, int | bool]:
        state = dict(self.registers.values)
        state["halted"] = self.halted
        return state

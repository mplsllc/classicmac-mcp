"""Execution adapter contracts.

Adapters expose semantic development operations. They must not force MCP clients to
construct arbitrary shell or AppleScript commands.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


class BuildAdapter(ABC):
    """Interface implemented by a concrete compiler/build environment."""

    @property
    @abstractmethod
    def adapter_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build(self, project_root: Path) -> CommandResult:
        """Build a project using a bounded, adapter-owned command sequence."""
        raise NotImplementedError

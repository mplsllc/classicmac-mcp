"""Hardware provider abstractions.

Providers hide transport details such as SSH, FTP, LaunchAPPL, emulator control,
or future native bridges. MCP tools operate on semantic capabilities instead of
transport-specific commands.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class MachineCapability(StrEnum):
    FILE_LIST = "file:list"
    FILE_UPLOAD = "file:upload"
    FILE_DOWNLOAD = "file:download"
    FILE_DELETE = "file:delete"
    BUILD = "build"
    RUN = "run"
    DIAGNOSTICS = "diagnostics"
    SCREENSHOT = "screenshot"
    PROJECT_MUTATE = "project:mutate"


@dataclass(frozen=True, slots=True)
class MachineIdentity:
    machine_id: str
    name: str
    architecture: str
    os_family: str
    os_version: str
    capabilities: frozenset[MachineCapability] = field(default_factory=frozenset)


@dataclass(slots=True)
class ProviderResult:
    ok: bool
    summary: str
    metadata: dict[str, object] = field(default_factory=dict)
    evidence_paths: list[str] = field(default_factory=list)


class HardwareProvider(ABC):
    """Semantic interface for a configured Classic Mac execution provider."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def machines(self) -> list[MachineIdentity]:
        raise NotImplementedError

    @abstractmethod
    def test_connection(self, machine_id: str) -> ProviderResult:
        raise NotImplementedError

    def upload(self, machine_id: str, local_path: Path, remote_path: str) -> ProviderResult:
        raise NotImplementedError(f"{self.provider_id} does not implement upload")

    def download(self, machine_id: str, remote_path: str, local_path: Path) -> ProviderResult:
        raise NotImplementedError(f"{self.provider_id} does not implement download")

    def run(self, machine_id: str, artifact: Path) -> ProviderResult:
        raise NotImplementedError(f"{self.provider_id} does not implement run")

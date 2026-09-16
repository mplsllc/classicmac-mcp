"""Retro68 preflight adapter.

Retro68 is a target-aware compatibility gate, not the authority for CodeWarrior
projects. This adapter executes a fixed configure/build sequence and never
accepts an arbitrary shell command from an MCP caller.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .base import BuildAdapter, CommandResult


@dataclass(frozen=True, slots=True)
class Retro68Config:
    toolchain_file: Path
    build_dir_name: str = ".classicmac/retro68-build"
    cmake: str = "cmake"
    timeout_seconds: int = 900
    max_output_chars: int = 200_000


class Retro68Adapter(BuildAdapter):
    def __init__(self, config: Retro68Config) -> None:
        self.config = config

    @property
    def adapter_id(self) -> str:
        return "retro68"

    def _run(self, argv: list[str], cwd: Path) -> CommandResult:
        try:
            completed = subprocess.run(
                argv,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                check=False,
            )
            return CommandResult(
                argv=argv,
                returncode=completed.returncode,
                stdout=completed.stdout[-self.config.max_output_chars :],
                stderr=completed.stderr[-self.config.max_output_chars :],
                metadata={"gate": "retro68", "authoritative": False},
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            return CommandResult(
                argv=argv,
                returncode=124,
                stdout=stdout[-self.config.max_output_chars :],
                stderr=stderr[-self.config.max_output_chars :],
                timed_out=True,
                metadata={"gate": "retro68", "authoritative": False},
            )

    def build(self, project_root: Path) -> CommandResult:
        project_root = project_root.resolve()
        build_dir = (project_root / self.config.build_dir_name).resolve()
        if project_root not in build_dir.parents:
            raise ValueError("Retro68 build directory must remain inside the project root")

        build_dir.mkdir(parents=True, exist_ok=True)

        configure = self._run(
            [
                self.config.cmake,
                "-S",
                str(project_root),
                "-B",
                str(build_dir),
                f"-DCMAKE_TOOLCHAIN_FILE={self.config.toolchain_file}",
            ],
            cwd=project_root,
        )
        if configure.returncode != 0 or configure.timed_out:
            configure.metadata["phase"] = "configure"
            return configure

        result = self._run(
            [self.config.cmake, "--build", str(build_dir)],
            cwd=project_root,
        )
        result.metadata["phase"] = "build"
        return result

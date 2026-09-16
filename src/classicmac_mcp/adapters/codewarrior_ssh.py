"""CodeWarrior-over-SSH/AppleScript adapter.

This module generalizes the proven `mplsllc/workflow` automation model without
exposing arbitrary AppleScript or shell execution as an MCP tool. The configured
bridge owns the host alias and expected project identity.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .base import BuildAdapter, CommandResult


@dataclass(frozen=True, slots=True)
class CodeWarriorSSHConfig:
    ssh_host: str
    expected_project_specifier: str
    application_name: str = "CodeWarrior IDE"
    ssh_binary: str = "ssh"
    connect_timeout_seconds: int = 10
    applescript_timeout_seconds: int = 7200
    subprocess_timeout_seconds: int = 7300
    max_output_chars: int = 200_000


class CodeWarriorSSHAdapter(BuildAdapter):
    """Bounded CodeWarrior operations through a GUI-session SSH host."""

    def __init__(self, config: CodeWarriorSSHConfig) -> None:
        self.config = config

    @property
    def adapter_id(self) -> str:
        return "codewarrior-ssh-applescript"

    def _ssh_applescript(self, body: str, timeout_seconds: int | None = None) -> CommandResult:
        script = (
            f"with timeout of {self.config.applescript_timeout_seconds} seconds\n"
            f"{body}\n"
            "end timeout\n"
        )
        argv = [
            self.config.ssh_binary,
            "-o",
            f"ConnectTimeout={self.config.connect_timeout_seconds}",
            self.config.ssh_host,
            "osascript",
        ]
        try:
            completed = subprocess.run(
                argv,
                input=script,
                capture_output=True,
                text=True,
                timeout=timeout_seconds or self.config.subprocess_timeout_seconds,
                check=False,
            )
            return CommandResult(
                argv=argv,
                returncode=completed.returncode,
                stdout=completed.stdout[-self.config.max_output_chars :],
                stderr=completed.stderr[-self.config.max_output_chars :],
                metadata={"adapter": self.adapter_id},
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
                metadata={
                    "adapter": self.adapter_id,
                    "state": "uncertain",
                    "warning": "timeout does not prove CodeWarrior stopped processing",
                },
            )

    def project_specifier(self) -> CommandResult:
        result = self._ssh_applescript(
            f'tell application "{self.config.application_name}" to Get Project Specifier',
            timeout_seconds=60,
        )
        result.metadata["operation"] = "project_specifier"
        return result

    def messages(self) -> CommandResult:
        result = self._ssh_applescript(
            f'tell application "{self.config.application_name}" '
            "to get messages of project document 1",
            timeout_seconds=60,
        )
        result.metadata["operation"] = "messages"
        return result

    def inventory(self) -> dict[str, CommandResult]:
        """Run independent read-only probes so one terminology failure does not mask others."""

        queries = {
            "project_document_count": (
                f'tell application "{self.config.application_name}" '
                "to get count of project documents"
            ),
            "document_name": (
                f'tell application "{self.config.application_name}" to get name of document 1'
            ),
            "project_specifier": (
                f'tell application "{self.config.application_name}" to Get Project Specifier'
            ),
            "messages": (
                f'tell application "{self.config.application_name}" '
                "to get messages of project document 1"
            ),
            "segments": (
                f'tell application "{self.config.application_name}" '
                "to Get Segments of project document 1"
            ),
        }
        return {
            name: self._ssh_applescript(script, timeout_seconds=60)
            for name, script in queries.items()
        }

    def verify_project_identity(self) -> CommandResult:
        identity = self.project_specifier()
        identity.metadata["expected_project_specifier"] = self.config.expected_project_specifier
        if identity.returncode != 0 or identity.timed_out:
            identity.metadata["identity_verified"] = False
            return identity

        observed = identity.stdout.strip()
        matches = self.config.expected_project_specifier in observed
        identity.metadata["identity_verified"] = matches
        if not matches:
            identity.returncode = 3
            identity.stderr = (
                identity.stderr
                + f"\nExpected project specifier not observed: {self.config.expected_project_specifier}"
            ).strip()
        return identity

    def update_project(self) -> CommandResult:
        result = self._ssh_applescript(
            f'tell application "{self.config.application_name}" to Update Project'
        )
        result.metadata["operation"] = "update_project"
        return result

    def run_project(self) -> CommandResult:
        result = self._ssh_applescript(
            f'tell application "{self.config.application_name}" to Run project document 1'
        )
        result.metadata["operation"] = "run_project"
        return result

    def build(self, project_root: Path) -> CommandResult:
        """Perform an authoritative CodeWarrior build after positive project identity.

        `project_root` is retained by the common adapter interface; source transfer is a
        separate stage/provider operation and is intentionally not hidden inside build.
        """

        del project_root
        identity = self.verify_project_identity()
        if not identity.metadata.get("identity_verified", False):
            identity.metadata["phase"] = "identity"
            return identity

        build = self.update_project()
        build.metadata["phase"] = "build"
        if build.returncode != 0 or build.timed_out:
            return build

        diagnostics = self.messages()
        diagnostics.metadata["phase"] = "diagnostics"
        diagnostics.metadata["build_stdout"] = build.stdout
        diagnostics.metadata["build_stderr"] = build.stderr

        message_text = diagnostics.stdout.strip()
        if diagnostics.returncode != 0 or diagnostics.timed_out:
            return diagnostics
        if message_text not in {"", "{}", "missing value"}:
            diagnostics.returncode = 2
            diagnostics.stderr = (
                diagnostics.stderr + "\nCodeWarrior reported non-empty project messages."
            ).strip()
        diagnostics.metadata["authoritative"] = True
        return diagnostics

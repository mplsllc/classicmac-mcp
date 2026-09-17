"""Structured provider/capability/result contracts.

These models are transport-neutral. SSH, AppleEvents, GUI automation, native
CodeWarrior plug-ins, FTP/LaunchAPPL, and emulator providers must translate their
results into these semantics before they can be exposed through MCP tools.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CapabilityMode(StrEnum):
    READ = "read"
    MUTATE = "mutate"


class CapabilityStatus(StrEnum):
    VERIFIED = "verified"
    DOCUMENTED = "documented"
    EXPERIMENTAL = "experimental"
    BROKEN = "broken"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class ImplementationChannel(StrEnum):
    APPLEEVENT = "appleevent"
    APPLESCRIPT = "applescript"
    GUI = "gui"
    PLUGIN_API = "plugin_api"
    SSH = "ssh"
    FTP = "ftp"
    LAUNCHAPPL = "launchappl"
    NATIVE_BRIDGE = "native_bridge"
    RETRO68 = "retro68"
    EMULATOR = "emulator"
    OTHER = "other"


class OperationStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"
    UNKNOWN_STATE = "unknown_state"


class FailureClass(StrEnum):
    AUTHORIZATION_DENIED = "authorization_denied"
    IDENTITY_MISMATCH = "identity_mismatch"
    CAPABILITY_UNAVAILABLE = "capability_unavailable"
    TRANSPORT_FAILURE = "transport_failure"
    OPERATION_TIMEOUT_UNKNOWN_STATE = "operation_timeout_unknown_state"
    COMPILER_FAILURE = "compiler_failure"
    LINKER_FAILURE = "linker_failure"
    DIAGNOSTIC_POLICY_FAILURE = "diagnostic_policy_failure"
    POSTCONDITION_FAILED = "postcondition_failed"
    TARGET_RUNTIME_FAILURE = "target_runtime_failure"
    INTERNAL_ERROR = "internal_error"


class CapabilityEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str | None = None
    validation_level: str | None = None
    note: str | None = None


class ProviderCapability(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._:-]*$")
    mode: CapabilityMode
    status: CapabilityStatus
    implementation: ImplementationChannel
    authorization_scope: str | None = None
    lock_scope: str | None = None
    evidence: list[CapabilityEvidence] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ProviderIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_id: str = Field(min_length=1)
    provider_kind: str = Field(min_length=1)
    machine_id: str | None = None
    toolchain_id: str | None = None
    project_id: str | None = None


class OperationIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str | None = None
    project_id: str | None = None
    project_path: str | None = None
    target: str | None = None
    source_revision: str | None = None
    toolchain: str | None = None
    artifact: str | None = None


class Postcondition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    passed: bool
    observed: str | int | float | bool | None = None
    expected: str | int | float | bool | None = None
    note: str | None = None


class EvidenceAttachment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str = Field(min_length=1)
    ref: str = Field(min_length=1)
    sha256: str | None = None
    note: str | None = None


class ProviderOperationResult(BaseModel):
    """Common result envelope for semantic provider operations."""

    model_config = ConfigDict(extra="forbid")

    attempt_id: str = Field(min_length=1)
    operation: str = Field(min_length=1)
    provider: ProviderIdentity
    status: OperationStatus
    failure_class: FailureClass | None = None
    started_at: datetime
    finished_at: datetime
    identity: OperationIdentity = Field(default_factory=OperationIdentity)
    postconditions: list[Postcondition] = Field(default_factory=list)
    evidence: list[EvidenceAttachment] = Field(default_factory=list)
    summary: str = ""
    metadata: dict[str, object] = Field(default_factory=dict)

    def succeeded(self) -> bool:
        """Return true only for explicit success with no failed postconditions."""

        return self.status is OperationStatus.SUCCESS and all(
            item.passed for item in self.postconditions
        )


class ProviderDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    identity: ProviderIdentity
    capabilities: list[ProviderCapability] = Field(default_factory=list)

    def capability(self, name: str) -> ProviderCapability | None:
        for item in self.capabilities:
            if item.name == name:
                return item
        return None

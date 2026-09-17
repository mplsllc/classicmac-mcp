from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class CapabilityMode(str, Enum):
    READ = "read"
    MUTATE = "mutate"


class OperationStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    UNKNOWN = "unknown"
    DENIED = "denied"


class FailureClass(str, Enum):
    IDENTITY_MISMATCH = "identity_mismatch"
    AUTHORIZATION_DENIED = "authorization_denied"
    CAPABILITY_UNAVAILABLE = "capability_unavailable"
    TRANSPORT_FAILURE = "transport_failure"
    TIMEOUT_STATE_UNKNOWN = "timeout_state_unknown"
    OPERATION_REJECTED = "operation_rejected"
    POSTCONDITION_FAILED = "postcondition_failed"
    TOOLCHAIN_FAILURE = "toolchain_failure"
    TARGET_RUNTIME_FAILURE = "target_runtime_failure"


@dataclass(frozen=True)
class ProviderCapability:
    name: str
    mode: CapabilityMode
    implementation: str | None = None
    verification: str | None = None


@dataclass(frozen=True)
class ProviderIdentity:
    id: str
    version: str
    machine_id: str | None = None
    capabilities: Sequence[ProviderCapability] = ()

    def capability(self, name: str) -> ProviderCapability | None:
        for capability in self.capabilities:
            if capability.name == name:
                return capability
        return None


@dataclass(frozen=True)
class ProviderArtifact:
    kind: str
    identity: str
    path: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderOperationResult:
    operation_id: str
    provider_id: str
    status: OperationStatus
    machine_id: str | None = None
    failure_class: FailureClass | None = None
    message: str | None = None
    preconditions: Mapping[str, object] = field(default_factory=dict)
    postconditions: Mapping[str, object] = field(default_factory=dict)
    diagnostics: Sequence[Mapping[str, object]] = ()
    artifacts: Sequence[ProviderArtifact] = ()
    raw_evidence_refs: Sequence[str] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.status is OperationStatus.SUCCESS and self.failure_class is not None:
            errors.append("successful operation cannot declare a failure_class")
        if self.status is OperationStatus.FAILED and self.failure_class is None:
            errors.append("failed operation must declare a failure_class")
        if self.failure_class is FailureClass.TIMEOUT_STATE_UNKNOWN and self.status is not OperationStatus.UNKNOWN:
            errors.append("timeout_state_unknown must use status=unknown")
        return errors

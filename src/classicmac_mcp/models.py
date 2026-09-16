"""Core domain models shared by MCP tools and adapters."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ValidationLevel(StrEnum):
    STATIC = "static_verified"
    RETRO68 = "retro68_verified"
    CODEWARRIOR = "codewarrior_verified"
    HARDWARE = "hardware_verified"


class EpistemicState(StrEnum):
    DOCUMENTED = "documented"
    OBSERVED = "observed"
    VERIFIED = "verified"
    DECISION = "decision"
    HYPOTHESIS = "hypothesis"
    DISPROVED = "disproved"
    SUPERSEDED = "superseded"
    UNKNOWN = "unknown"
    INCOMPATIBLE = "incompatible"


class OSRange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family: str = "classic-mac-os"
    minimum: str | None = None
    maximum: str | None = None


class TargetSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    architecture: str
    os: OSRange


class LanguageSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str = "c"
    standard: str = "c89"


class ToolchainSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family: str
    version: str
    authoritative: bool = True


class ProjectManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)
    project_id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    name: str = Field(min_length=1)
    source_root: str = "."
    target: TargetSpec
    language: LanguageSpec = Field(default_factory=LanguageSpec)
    toolchain: ToolchainSpec
    project_file: str | None = None
    knowledge_paths: list[str] = Field(default_factory=list)


class MachineManifest(BaseModel):
    """Public/non-secret machine description.

    Credentials and private network details deliberately live outside this model.
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)
    machine_id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    name: str = Field(min_length=1)
    architecture: str
    os_family: str = "classic-mac-os"
    os_version: str
    provider: str
    capabilities: list[str] = Field(default_factory=list)
    labels: dict[str, str] = Field(default_factory=dict)


class KnowledgeApplicability(BaseModel):
    model_config = ConfigDict(extra="forbid")

    toolchain_family: str | None = None
    toolchain_versions: list[str] = Field(default_factory=list)
    language: str | None = None
    language_standard: str | None = None
    architectures: list[str] = Field(default_factory=list)
    os_family: str | None = None
    os_versions: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    machines: list[str] = Field(default_factory=list)
    notes: str | None = None


class EvidenceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    role: str
    note: str | None = None


class KnowledgeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)
    id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]+$")
    title: str = Field(min_length=1)
    scope: str
    state: EpistemicState
    validation_level: ValidationLevel
    statement: str = Field(min_length=1)
    applicability: KnowledgeApplicability = Field(default_factory=KnowledgeApplicability)
    evidence: list[EvidenceReference] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    supersedes: list[str] = Field(default_factory=list)
    last_reviewed: str | None = None


class SourceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)
    id: str
    kind: str
    title: str
    locator: dict[str, object]
    redistribution: str
    trust: str
    notes: str | None = None
    collected_at: str | None = None


class CompatibilityFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    severity: str
    line: int | None = None
    construct: str
    message: str
    evidence_hint: str | None = None


class GateResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate: str
    passed: bool
    authoritative: bool = False
    findings: list[CompatibilityFinding] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

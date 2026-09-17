from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class BackendRole(str, Enum):
    PREFLIGHT = "preflight"
    AUTHORITATIVE = "authoritative"
    ALTERNATE = "alternate"
    DEPLOYMENT = "deployment"
    RUNTIME = "runtime"


class ExecutableFormat(str, Enum):
    PEF = "pef"
    MACH_O = "mach-o"
    UNKNOWN = "unknown"


class RuntimeModel(str, Enum):
    CFM = "cfm"
    MACH_O = "mach-o"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BackendIdentity:
    family: str
    version: str | None = None
    role: BackendRole = BackendRole.ALTERNATE
    profile: str | None = None


@dataclass(frozen=True)
class AccessPath:
    path: str
    kind: str
    recursive: bool = False
    order: int | None = None


@dataclass(frozen=True)
class ProjectFile:
    path: str
    kind: str = "source"
    group: str | None = None
    included: bool = True
    link_order: int | None = None
    settings: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ResourceInput:
    path: str
    kind: str = "resource"


@dataclass(frozen=True)
class OutputMetadata:
    name: str
    executable_format: ExecutableFormat = ExecutableFormat.UNKNOWN
    runtime: RuntimeModel = RuntimeModel.UNKNOWN
    finder_type: str | None = None
    finder_creator: str | None = None
    output_path: str | None = None


@dataclass(frozen=True)
class ProjectTarget:
    id: str
    name: str
    architecture: str
    os_family: str
    os_min: str | None = None
    os_max: str | None = None
    api_family: str | None = None
    language_standard: str | None = None
    runtime_library: str | None = None
    prefix_files: Sequence[str] = ()
    defines: Mapping[str, str | int | bool] = field(default_factory=dict)
    access_paths: Sequence[AccessPath] = ()
    files: Sequence[ProjectFile] = ()
    libraries: Sequence[str] = ()
    resources: Sequence[ResourceInput] = ()
    output: OutputMetadata | None = None
    backends: Sequence[BackendIdentity] = ()

    def authoritative_backend(self) -> BackendIdentity | None:
        matches = [b for b in self.backends if b.role is BackendRole.AUTHORITATIVE]
        if len(matches) > 1:
            raise ValueError(f"target {self.id!r} declares multiple authoritative backends")
        return matches[0] if matches else None


@dataclass(frozen=True)
class ProjectModel:
    schema_version: int
    id: str
    name: str
    targets: Sequence[ProjectTarget]
    source_root: str = "."
    source_vcs: str | None = "git"
    native_project_file: str | None = None
    interchange_project_file: str | None = None

    def target(self, target_id: str) -> ProjectTarget:
        for target in self.targets:
            if target.id == target_id:
                return target
        raise KeyError(target_id)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.schema_version != 1:
            errors.append(f"unsupported schema_version {self.schema_version!r}")
        if not self.id:
            errors.append("project id is required")
        if not self.targets:
            errors.append("at least one target is required")

        seen: set[str] = set()
        for target in self.targets:
            if target.id in seen:
                errors.append(f"duplicate target id: {target.id}")
            seen.add(target.id)
            try:
                target.authoritative_backend()
            except ValueError as exc:
                errors.append(str(exc))

        return errors

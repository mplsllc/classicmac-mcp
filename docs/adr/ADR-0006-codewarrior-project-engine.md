# ADR-0006: Model CodeWarrior project semantics separately from build backends

- Status: Accepted
- Date: 2026-09-16

## Context

CodeWarrior documentation and SDK material show a project/build architecture in which the IDE orchestrates project state while compiler, linker, and related tools are provided through explicit interfaces. CodeWarrior also supports project XML export/import, giving us a documented text interchange path that can precede any binary `.mcp` reverse engineering.

Retro68 already implements substantial Classic Mac cross-development machinery, while genuine CodeWarrior remains the authoritative compiler for current CW8 projects. Future PowerPC Darwin/Mach-O backends are a separate target family.

## Decision

ClassicMacMCP will maintain a semantic project model that is independent of the backend executing a build.

The project model includes targets, files, grouping/link order, access paths, prefix/precompiled-header settings, defines, compiler/linker preferences, resources, libraries, output metadata, and project/toolchain identity.

Backends advertise bounded operations such as compile, link, resource build, packaging, inspection, deployment, and run.

For existing CodeWarrior projects, the manifest explicitly declares whether CodeWarrior remains authoritative. A Retro68 or other backend cannot silently replace that authority.

CodeWarrior XML is the preferred first interoperability/import format. Direct `.mcp` parsing is future work rather than a prerequisite.

## Consequences

- ClassicMacMCP can represent the real project independently from one IDE transport.
- Genuine CodeWarrior can serve as an authoritative/reference backend while local backends mature.
- Retro68 can be both a preflight gate and, separately, a possible future PEF backend without conflating those roles.
- A future CodeWarrior-like IDE can consume the same project/backend model.
- Differential tests can compare externally meaningful ABI/artifact/runtime behavior instead of requiring byte-identical output.
# Project and Backend Model

## Purpose

ClassicMacMCP models a Classic Macintosh project independently from the mechanism that happens to build it. This mirrors the useful separation visible in CodeWarrior's own architecture: project/target state belongs to the development environment, while compiler, linker, resource, packaging, and deployment work can be supplied by distinct backends.

The immediate MCP goal is not to clone the CodeWarrior IDE. The goal is to expose historically accurate project semantics to agents and preserve a path toward interchangeable build backends.

## Canonical project semantics

A project target may declare:

- target CPU and operating-system family;
- executable/runtime format such as PEF/CFM or Mach-O;
- API family such as Classic Toolbox or Carbon;
- source membership and grouping;
- exclusions;
- link order;
- access paths and search policy;
- prefix/precompiled-header configuration;
- preprocessor definitions;
- language/compiler settings;
- per-file settings;
- libraries/import libraries;
- resource inputs;
- Finder type/creator metadata;
- memory/resource settings;
- output name/location;
- declared authoritative toolchain;
- optional validation backends.

The schema should be able to represent CodeWarrior semantics without requiring `.mcp` parsing.

## CodeWarrior project interchange

CodeWarrior documentation exposes XML project export/import and GNU Makefile export. Those forms are valuable archaeological and interoperability inputs.

Initial import path:

```text
CodeWarrior .mcp
      |
      | one-time export using CodeWarrior
      v
CodeWarrior XML
      |
      v
ClassicMac project model
```

The XML importer must preserve unsupported settings as explicit unknown/vendor fields or diagnostics rather than silently dropping them.

Direct `.mcp` parsing is optional future work and must not block the project model.

## Build graph

The project engine eventually owns dependency and dirty-state semantics:

```text
project target
    |
    +-- sources
    +-- access paths
    +-- defines/prefix
    +-- libraries
    +-- resources
    +-- metadata
           |
           v
     dependency graph
           |
     +-----+------+---------+
     |            |         |
  compile        link    resources
     |            |         |
     +------------+---------+
                  |
               package
                  |
               artifact
```

The engine records *why* a file is dirty and *why* a relink/repackage occurred. A backend does not get to redefine project membership or access-path order silently.

## Backend contract

A backend advertises capabilities instead of claiming to implement an entire IDE.

Conceptual operations:

- `discover_targets()`
- `compile(request)`
- `link(request)`
- `build_resources(request)`
- `package_application(request)`
- `inspect_artifact(request)`
- `deploy(request)`
- `run(request)`

Backends may include:

- `remote-codewarrior`: genuine CodeWarrior as authoritative/reference backend;
- `retro68-pef`: local 68K/PPC Classic/Carbon PEF backend;
- `darwin-powerpc`: native PowerPC Mach-O backend for applicable Mac OS X targets;
- experimental Metrowerks-hosted backends when independently proven.

A project can use different backends for different validation levels. Passing one backend never implies passing another.

## CodeWarrior as oracle and authority

For existing projects whose manifest declares CodeWarrior authoritative, CodeWarrior output remains the authoritative compile/build result.

A future local backend can be compared against CodeWarrior using externally meaningful properties:

- target architecture;
- ABI behavior;
- imports/exports;
- entry point;
- resource set;
- Finder metadata;
- PEF/CFM requirements;
- callback/UPP behavior;
- struct layout;
- standard/runtime library behavior;
- launch/runtime behavior.

Byte-identical compiler output is not required unless a specific compatibility property depends on it.

## Retro68 relationship

Retro68 serves two distinct roles:

1. near-term validation/preflight for historically constrained source; and
2. possible future PEF build backend.

Those roles must not be conflated. `retro68_verified` says what was actually verified by Retro68. It does not mean `codewarrior_verified`.

For complex late-Classic/Carbon projects, interface completeness, Universal Interfaces, CarbonLib, Open Transport, runtime-library differences, and compiler assumptions are independent compatibility dimensions.

## Runtime-library model

OS APIs and C runtime APIs are separate applicability domains. A source file that compiles against Classic Mac headers may still rely on MSL-specific behavior that is absent from another runtime library.

The KB should therefore distinguish:

- ISO C language behavior;
- Metrowerks compiler behavior/extensions;
- MSL behavior;
- Apple/Classic Mac API behavior;
- ABI/linker/loader behavior;
- project/IDE behavior.

## Resource and file metadata

A Macintosh application artifact may include executable code, resource fork, Finder metadata, creator/type, `SIZE`/`carb`/`cfrg`-related resources, and transport-safe representations.

Packaging is a first-class backend operation. A successful compiler invocation alone is not a successful Classic Mac application build.

## Design rule

The MCP should expose semantic project/build operations and structured evidence. It should not expose backend-specific command lines as the stable public interface.
# CodeWarrior Project Engine

## Why this matters

Research into CodeWarrior's own documentation changes how ClassicMacMCP should model projects. CodeWarrior is not best understood as one opaque application. Its documented architecture separates the project/build orchestrator from compiler, linker, and other plug-ins, and its project state can be exported as XML.

ClassicMacMCP should preserve that separation.

## What the MCP needs from CodeWarrior

The semantic model should cover:

- projects and targets;
- target CPU/OS/runtime/API identity;
- source/resource/library membership;
- grouping and link order;
- access paths and recursive-search policy;
- prefix/precompiled-header settings;
- compiler/linker preferences;
- per-file options;
- dependencies and dirty state;
- output location/identity;
- resource/Finder metadata;
- diagnostic state.

This is useful even if the actual build continues to run in genuine CodeWarrior.

## Project XML as interoperability boundary

Initial project reconstruction should prefer CodeWarrior's documented XML export/import over binary `.mcp` reverse engineering.

Workflow:

```text
.mcp project
    |
    | export once in genuine CodeWarrior
    v
CodeWarrior XML
    |
    +-- preserve source form for evidence
    |
    v
ClassicMac semantic project model
```

The imported model may later drive multiple backends, but unsupported CodeWarrior settings must remain explicit rather than being discarded.

A GNU Makefile export, when available, can serve as a secondary archaeological representation of the build but is not assumed to preserve every IDE semantic.

## Plug-in API relationship

The CodeWarrior SDK exposes native routines that map closely to the project model, including APIs for project-file enumeration, adding/removing entries, access-path inspection, target information, output directories, IDE/API version discovery, preferences, and diagnostics.

The IDE 5.1 SDK API Reference is discovery evidence, not automatic CW8 compatibility. Exact CW8 headers/API versions and hardware behavior remain authoritative for the first reference environment.

## Backend abstraction

The project model should be capable of driving several backends without making any of them semantically authoritative by default:

```text
project model
      |
      +-- remote-codewarrior
      +-- retro68-pef
      +-- darwin-powerpc
      +-- future proven backends
```

For an existing project, the manifest decides which backend is authoritative.

## Differential use

A local backend can be compared to genuine CodeWarrior without requiring byte-identical binaries. The useful comparison surface includes:

- ABI-visible data layout;
- imports/exports;
- callbacks/UPPs;
- PEF/runtime metadata;
- resources;
- Finder metadata;
- runtime-library expectations;
- launch behavior;
- application-level behavior.

Differences become explicit compatibility evidence and, once understood, regression tests.

## Scope boundary

ClassicMacMCP itself is not the replacement IDE. It provides the semantic model, compatibility knowledge, orchestration, evidence, and provider contracts that a future CodeWarrior-like IDE or build engine can use.

This keeps the MCP immediately useful for genuine CodeWarrior workflows while making the project model reusable for future local build systems.
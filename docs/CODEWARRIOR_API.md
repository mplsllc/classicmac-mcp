# CodeWarrior API Model

## Purpose

ClassicMacMCP must treat CodeWarrior as a programmable development environment with multiple control surfaces, not as a GUI application that an LLM drives directly.

The MCP-facing API is semantic. The client asks for operations such as project identity, build, compile, diagnostics, project membership, target information, preferences, launch, or debugger state. An implementation provider decides which CodeWarrior control surface is appropriate for that operation.

This prevents the LLM from having to synthesize AppleScript, click menus, or know plugin request structures, and it allows us to improve the backend without changing project workflows.

## Control surfaces

### 1. IDE Automation API

This is the installed CodeWarrior IDE's AppleEvent/AppleScript object model and command dictionary.

The current first-party CW 8.3 evidence in `mplsllc/workflow` records an embedded terminology dictionary with 53 commands, 87 classes, 294 properties, and 21 enumerations. A dictionary entry proves that a term exists, not that it behaves correctly on the installed target.

Validated examples currently include:

- `Update Project` for Bring Up To Date;
- `Run project document 1` for launch;
- project messages and Errors & Warnings export;
- targeted `Compile`;
- `Remove Object Code`;
- `Get Project Specifier`;
- `Get Segments`;
- selected project preferences;
- project-file removal.

Known exceptions are equally important. For example, a direct Add Files AppleEvent is present in the installed terminology but is not usable on the current Tiger-hosted CW8 target, while the GUI `Project > Add Files…` path is proven to work.

Therefore Automation API capabilities are versioned and evidence-backed per exact IDE fingerprint.

### 2. Native CodeWarrior Plugin API

Metrowerks also published a native Plugin API. Historically this API was used for compiler, linker, and preference-panel plugins, and CodeWarrior's own development tools were implemented through the same plugin architecture.

The plugin API uses IDE-to-plugin requests and plugin-to-IDE callbacks. Historical examples include compiler request dispatch through a `CompilerParameterBlockPtr` and callbacks such as compiler diagnostic reporting.

This API is materially different from AppleScript automation:

- it executes inside the CodeWarrior process;
- it can expose structured IDE/toolchain information without UI scraping;
- it may provide reliable hooks for compiler/linker integration and diagnostics;
- it requires code built for the exact CodeWarrior/Classic Mac environment;
- its exact capabilities and ABI must be verified against the Plugin API headers, libraries, release notes, and sample projects that correspond to our installed CodeWarrior version.

ClassicMacMCP must not assume that a historical Plugin API article or a different CodeWarrior release is ABI-compatible with CodeWarrior Pro 8.3. The exact installed SDK/media is authoritative.

### 3. GUI automation fallback

Some IDE operations may be absent, broken, or impractical through the Automation API and not appropriate for a native plugin. Those operations may use deterministic GUI automation.

GUI automation is a fallback, not the public API. Every GUI-backed operation must:

- positively identify the IDE and project first;
- select named controls/menu items rather than coordinate-only clicking where possible;
- record before/after state;
- return the same structured semantic result as non-GUI providers;
- preserve failure evidence;
- never silently fall back after an ambiguous timeout.

### 4. Native target bridges

AgentBridge, Classic Control, SSH/osascript, or future native helpers are transports/execution providers. They are not the CodeWarrior API itself.

For example, both of these may implement the same semantic operation:

```
codewarrior.build(project)
```

Provider A:

```
SSH -> osascript -> CodeWarrior AppleEvent
```

Provider B:

```
MCP bridge -> OS 9 helper -> OSADoScript -> CodeWarrior AppleEvent
```

A future provider might use a CodeWarrior plugin for part of the operation and AppleEvents for another part.

## Semantic CodeWarrior service

The first public interface should be organized around stable operations rather than transport commands.

Candidate operations:

### Identity and discovery

- `codewarrior.get_ide_identity`
- `codewarrior.get_project_identity`
- `codewarrior.get_active_target`
- `codewarrior.list_targets`
- `codewarrior.list_project_files`
- `codewarrior.list_segments`
- `codewarrior.get_capabilities`

### Project configuration

- `codewarrior.get_preferences`
- `codewarrior.get_access_paths`
- `codewarrior.add_project_file`
- `codewarrior.remove_project_file`
- `codewarrior.import_project`
- `codewarrior.select_target`

Mutating operations require explicit capability authorization and postcondition verification.

### Build

- `codewarrior.compile_file`
- `codewarrior.update_project`
- `codewarrior.remove_object_code`
- `codewarrior.build`
- `codewarrior.get_build_messages`
- `codewarrior.export_errors`

`build` is a composite operation with identity checks, locking, diagnostics capture, output identity validation, and evidence recording. It is not an alias for `Run`.

### Execution/debugging

Potential operations include:

- `codewarrior.run`
- `codewarrior.stop`
- `codewarrior.debugger_state`
- `codewarrior.breakpoints`
- `codewarrior.stack`
- `codewarrior.registers`

These remain UNKNOWN until the exact installed automation dictionary and/or native Plugin API prove support. They must not be invented from later CodeWarrior documentation.

## Capability registry

Each semantic operation maps to zero or more implementations and carries evidence.

Example:

```yaml
operation: codewarrior.add_project_file
ide:
  family: codewarrior
  version: "8.3"
  fingerprint: "..."
implementations:
  - provider: appleevent
    status: broken
    evidence: "direct Add Files fails on current Tiger target"
  - provider: gui
    status: verified
    evidence: "Project > Add Files… controlled hardware test"
preferred: gui
```

An exposed dictionary term is `documented` or `discovered`, not `verified`, until a controlled probe confirms its behavior.

## Source-of-truth order

For exact CodeWarrior behavior, use this order:

1. controlled behavior on the exact installed CodeWarrior build;
2. exact installed terminology (`aete`) and captured executable/dictionary fingerprint;
3. exact-version Plugin API headers, libraries, release notes, and sample projects;
4. exact-version Metrowerks documentation;
5. behavior from another CodeWarrior version, marked explicitly as non-applicable prior art until verified.

Later Windows/Unix CodeWarrior automation guides are useful for understanding the shape of the IDE but do not establish Mac CW8 behavior.

## Knowledge isolation

CodeWarrior Plugin API samples and third-party plugin source must not automatically enter the C89 target-programming corpus.

They belong to a separate `toolchain-api` evidence class until they have been:

1. matched to the intended CodeWarrior version;
2. compiled by the authoritative CodeWarrior toolchain where relevant;
3. classified for language/extensions used;
4. reduced into explicit compatibility facts.

This prevents a useful plugin example from teaching an LLM that every construct in that example is permitted in an unrelated CW8/C89 project.

## Research tasks

Before implementing a native CodeWarrior provider, inventory the exact CW Pro 8 installation/media for:

- Plugin API documentation;
- Plugin API headers and libraries;
- release notes/version identifiers;
- sample compiler/linker/preference-panel plugins;
- debugger/editor/project extension APIs, if any;
- compatibility notes between plugin API revisions;
- native diagnostic and project-model callbacks.

Preserve hashes and source location for every artifact. Do not redistribute proprietary Metrowerks materials unless redistribution rights are clear; record metadata and locally index user-owned documentation instead.

## Design decision

ClassicMacMCP's CodeWarrior integration is therefore a layered service:

```
MCP semantic CodeWarrior API
            |
    capability resolver
            |
   +--------+---------+-------------+
   |                  |             |
AppleEvent/OSA    Plugin API     GUI fallback
   |                  |             |
   +-------- execution provider ----+
                    |
              CodeWarrior IDE
```

The goal is not to maximize one control technology. The goal is to select the safest, most deterministic, best-evidenced CodeWarrior interface for each operation while presenting one stable API to agents.

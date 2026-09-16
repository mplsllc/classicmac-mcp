# Prior Art and Interoperability

ClassicMacMCP is intended to reuse proven work rather than recreate it. This document records projects that materially influence the architecture and the boundary between adoption, interoperability, and new work.

## classic-mac-hardware-mcp

Repository: `matthewdeaves/classic-mac-hardware-mcp`
License: MIT

### What it already solves

The project provides a local stdio MCP server for real Classic Macintosh hardware with:

- machine inventory and capability metadata;
- RumpusFTP-compatible plain FTP transport;
- Mac colon-path normalization;
- per-machine rate limiting and retry behavior;
- upload/download/list/delete file operations;
- LaunchAPPL discovery and execution;
- per-machine serialization of LaunchAPPL runs;
- parallel execution across different machines;
- basic CPU/binary-platform mismatch checks;
- PT_Log retrieval as an MCP resource;
- environment-variable expansion for FTP passwords.

These are real, useful Classic Mac hardware primitives and should not be independently reinvented without a specific reason.

### Scope difference

`classic-mac-hardware-mcp` is primarily a local hardware access server. ClassicMacMCP has a broader mission:

- compatibility-aware Classic Mac development knowledge;
- C89/CodeWarrior compatibility policy;
- Retro68 preflight validation;
- CodeWarrior project/build/diagnostic automation;
- evidence levels and provenance;
- project/toolchain/machine schemas;
- multi-user hosted knowledge service;
- authorization, tenant isolation, audit, rate limits, and secure bridge enrollment;
- support for multiple execution backends rather than one transport.

### Integration decision

ClassicMacMCP models hardware access through an adapter/provider interface. A provider may wrap this MCP rather than reproduce its FTP/LaunchAPPL implementation.

### Security boundary

The project is designed for local stdio use and directly exposes file deletion, arbitrary local-file upload/download destinations, and binary execution against configured machines. Those capabilities are appropriate for a trusted local developer process but are not a safe default public hosted surface.

ClassicMacMCP therefore must not expose such a backend directly to arbitrary hosted users. Privileged hardware execution remains behind the authenticated local/private bridge and capability policy.

### Design lessons to adopt

- machine capabilities are explicit data, not implicit assumptions;
- old Macs require pacing and transport-specific stability policy;
- operations on one machine should be serialized where the target cannot safely handle concurrency;
- independent machines may run in parallel;
- path-format translation belongs inside the transport adapter;
- execution should be a semantic tool rather than an arbitrary shell command;
- hardware logs should be exposed as structured resources/evidence;
- architecture mismatch should fail before deployment when it can be established cheaply.

## AgentBridge

Repository: `SeanFDZ/agentbridge`
MCP server license: GPLv3
Classic Mac application license: modified PolyForm Noncommercial 1.0.0
Protocol: documented as open by the project

### What it already solves

AgentBridge places a native Classic Mac application on the target and exposes Toolbox-level control through a deliberately simple command protocol. Its current design uses a shared-folder inbox/outbox transport and includes:

- target heartbeat and liveness;
- system/process/window/menu introspection;
- mouse and keyboard control;
- clipboard access;
- app launch/activation/quit;
- AppleEvent operations;
- file/volume inspection and staged transfers;
- real-hardware and emulator targeting;
- a protocol constrained for Classic Mac realities: HFS filename limits, CR line endings, MacRoman, small messages, and no JSON parser on the target.

The protocol specification explicitly separates command semantics from transport and anticipates replacing shared-folder transport with a network/AppleEvent transport without changing the MCP tool layer.

### Integration decision

This is strong prior art for a native target-provider protocol. ClassicMacMCP should support interoperability through an adapter rather than copy AgentBridge's implementation.

Because the MCP server is GPLv3 and the native app is under a noncommercial license, no source from either component should be copied into a permissively licensed ClassicMacMCP implementation unless a deliberate licensing decision is made. Protocol-level interoperability can remain a clean boundary.

### Design lessons to adopt

- keep target protocol semantics independent of transport;
- prefer a tiny bounded protocol over forcing modern formats onto constrained machines;
- make heartbeat/liveness first-class;
- normalize encoding/line-ending differences at the host boundary;
- keep binary payloads out of the control protocol;
- use sequence IDs and explicit status/error fields;
- model emulators and physical machines through the same target interface;
- let the classic-side process remain a cooperative multitasking citizen.

## Classic Control

Repository: `minorbug/classic-control`
Native helper source: `minorbug/clawssic`
License: MIT for the host bridge; verify the native-helper repository license separately before direct code reuse

### What it already solves

Classic Control uses a small native Mac OS 9 helper connected over TCP to a Node MCP bridge. It directly targets remote CodeWarrior workflows and exposes:

- read/list/create/edit file operations;
- arbitrary AppleScript execution through OSA;
- screenshots captured on the target;
- target system information;
- a single persistent transport to the OS 9 helper.

A notable contribution is its leader/follower architecture for multiple simultaneous MCP-client processes. One process owns the single TCP connection to the single-threaded OS 9 helper; other MCP instances multiplex through it over a Unix socket. If the leader dies, followers re-elect. The transport itself also serializes requests, attaches request IDs, applies timeouts, and fails queued requests if the connection drops.

### Integration decision

Classic Control is valuable as a possible local execution provider and as prior art for serialization/recovery. ClassicMacMCP should not expose its unrestricted `run_applescript` tool to arbitrary hosted users. The public-facing layer should expose bounded semantic CodeWarrior operations and keep raw AppleScript as a locally privileged escape hatch, if supported at all.

### Important compatibility warning

The native helper is architectural prior art, not target-programming knowledge. Its CodeWarrior-built C source contains constructs that are not automatically admissible under ClassicMacMCP's strict CW8/C89 profile. Therefore we do not ingest its C implementation into the Classic Mac programming knowledge base merely because it builds in its own project configuration.

### Design lessons to adopt

- one classic-side execution loop often requires one global serialized command stream;
- timeout does not imply target-side cancellation;
- request IDs and explicit transport state matter;
- target screenshots can be structured evidence rather than the primary diagnostic path;
- search-and-replace editing with a unique-match precondition is safer than blind full-file overwrite;
- a native helper can eliminate fragile host-GUI scripting for operations that are better executed inside Classic Mac OS.

## Existing first-party workflow

`mplsllc/workflow` remains the reference implementation for CodeWarrior-over-SSH/AppleScript development. It already contains stage separation, project identity checks, dictionary discovery, GUI fallbacks, diagnostics gates, evidence preservation, locking, project bootstrap, and portability guidance.

ClassicMacMCP should wrap/generalize those semantics rather than replacing them with generic SSH execution.

The first-party workflow remains especially valuable because it has been validated against the user's actual CodeWarrior installation and records failed approaches, false-success modes, and recovery rules.

## Provider strategy

ClassicMacMCP should not become a fourth monolithic hardware-control implementation. Its local/private execution layer should support providers such as:

1. first-party SSH + AppleScript/AppleEvents CodeWarrior workflow;
2. `classic-mac-hardware-mcp` for FTP + LaunchAPPL;
3. AgentBridge-compatible native target control;
4. Classic Control-compatible native TCP helper;
5. emulator-specific providers;
6. future native or serial/AppleTalk bridges.

The ClassicMacMCP layer adds project/toolchain semantics, compatibility policy, knowledge retrieval, evidence, security policy, and a stable cross-provider vocabulary.

## Guiding rule

Prior art may influence MCP/server architecture without entering the target-programming knowledge corpus.

In particular, C source from unrelated modern or retro projects is not automatically valid CodeWarrior/C89 guidance. Classic Mac target knowledge comes only from the curated compatibility knowledge base and explicitly applicable verified sources.

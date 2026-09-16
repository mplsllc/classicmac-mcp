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

ClassicMacMCP will model hardware access through an adapter/provider interface.

A provider may be:

1. the existing SSH/AppleScript CodeWarrior workflow;
2. a Classic Mac Hardware MCP-compatible FTP/LaunchAPPL provider;
3. an emulator provider;
4. a future native target bridge.

We should prefer interoperability or an optional adapter over copying the external implementation. If code is later incorporated directly, the MIT attribution and license requirements must be retained.

### Security boundary

The external project is designed for local stdio use and directly exposes file deletion, arbitrary local-file upload/download destinations, and binary execution against configured machines. Those capabilities are appropriate for a trusted local developer process but are not a safe default public hosted surface.

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

### Design choices not to copy unchanged

- unversioned/free-form machine configuration as the long-term schema;
- credentials embedded directly in machine records for a hosted/multi-user service;
- destructive tools without a capability/authorization layer;
- arbitrary local path access from a remote/public MCP client;
- a single-module server architecture as the platform grows;
- `mcp>=1`/stdio-only assumptions for the hosted service.

## Existing first-party workflow

`mplsllc/workflow` remains the reference implementation for CodeWarrior-over-SSH/AppleScript development. It already contains stage separation, project identity checks, dictionary discovery, GUI fallbacks, diagnostics gates, evidence preservation, locking, project bootstrap, and portability guidance.

ClassicMacMCP should wrap/generalize those semantics rather than replacing them with generic SSH execution.

## Guiding rule

Prior art may influence MCP/server architecture without entering the target-programming knowledge corpus.

In particular, C source from unrelated modern or retro projects is not automatically valid CodeWarrior/C89 guidance. Classic Mac target knowledge comes only from the curated compatibility knowledge base and explicitly applicable verified sources.

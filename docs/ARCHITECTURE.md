# Architecture

## Design objective

ClassicMacMCP is a reusable development platform, not a MacSurf-specific wrapper and not a generic remote shell. It provides compatibility-aware knowledge, project/toolchain semantics, evidence tracking, and bounded adapters for vintage development environments.

The architecture is split into two trust domains.

## 1. Hosted core

The hosted service is suitable for multi-user deployment and contains no reusable credentials for a user's vintage hardware.

Responsibilities:

- serve the curated Classic Mac knowledge base;
- validate versioned project/machine/evidence manifests;
- provide compatibility-policy tools;
- expose project/toolchain context;
- index public provenance/evidence;
- issue/verify bridge capabilities where enabled;
- authenticate users and authorize scopes;
- audit requests and enforce rate limits.

The hosted core must remain useful even when no physical Mac is connected.

## 2. Local/private execution bridge

The bridge runs under the machine owner's control, normally on a Linux/macOS development host that can reach the vintage Mac.

Responsibilities:

- hold machine credentials locally;
- run Retro68 preflight;
- drive CodeWarrior through the configured adapter;
- transfer source/artifacts;
- launch target applications;
- collect build/runtime evidence;
- expose only explicitly configured machines/projects;
- enforce local policy independently of hosted authorization.

A hosted user identity does not imply authority over a bridge. Bridge enrollment and per-capability authorization are separate decisions.

## Domain model

### Project

A versioned `.classicmac/project.yaml` declares target architecture/OS, language policy, authoritative toolchain, project file, and project-local knowledge paths. It contains no credentials.

### Machine

A machine record declares observable properties and capabilities: CPU, OS, toolchains, transports, limits, and optional execution providers. Secret material is referenced, never embedded in a public manifest.

### Toolchain

Toolchains are adapters with explicit authority. A project may have multiple gates but one declared authoritative build toolchain.

For a CodeWarrior project:

`static policy -> Retro68 preflight -> CodeWarrior -> hardware test`

No earlier stage is promoted into evidence for a later stage.

### Provider / adapter

Hardware and toolchains are modeled behind semantic interfaces. Expected providers include:

- SSH + AppleScript/AppleEvents CodeWarrior workflow;
- FTP + LaunchAPPL provider compatible with `matthewdeaves/classic-mac-hardware-mcp`;
- emulator providers;
- future native target bridges.

The MCP client should call semantic operations such as `build_project`, `run_target`, or `collect_diagnostics`, not synthesize arbitrary SSH/FTP/AppleScript.

## Evidence model

Every meaningful attempt has an ID and records:

- source revision and dirty-state identity;
- project/machine/toolchain identity;
- requested operation;
- inputs changed/transferred;
- gate results;
- compiler diagnostics;
- artifact identity;
- launch/test result;
- logs/captures needed to support the conclusion;
- timestamps and provenance.

Evidence levels are independent:

- `static_verified`
- `retro68_verified`
- `codewarrior_verified`
- `hardware_verified`

## Knowledge model

Canonical knowledge remains in Git in `classicmac-kb`. Search databases and embeddings are derived indexes only.

Retrieval is filtered by the project's declared target. Unknown or unverified material must not be silently substituted with modern/general C examples.

## Concurrency

Vintage IDEs and hardware often require serialization. Locks are explicit resources keyed at the narrowest safe boundary (for example machine + CodeWarrior project). Different independent machines may execute concurrently.

A timeout never implies an operation stopped. Adapters must have a recovery/identity query before retrying state-changing work.

## Versioning

Schemas begin at version 1 and reject unknown keys by default. Compatibility behavior must be versioned so future expansion does not silently change historical project semantics.

## Deployment

Development can use stdio. Production hosted MCP uses Streamable HTTP over TLS and targets MCP 2026-07-28 semantics. The bridge may remain stdio/local or use an authenticated private channel depending on deployment.

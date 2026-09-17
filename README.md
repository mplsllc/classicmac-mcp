# ClassicMacMCP

ClassicMacMCP is an MCP development platform for building, validating, automating, and testing Classic Macintosh software with AI agents.

The project is intentionally broader than any single application. Its first reference environment is remote CodeWarrior development on a PowerPC Macintosh, but the architecture is designed for future projects, machines, toolchains, emulators, and community users.

## Mission

ClassicMacMCP should let an MCP-capable coding agent work against a historically constrained development environment without silently importing incompatible modern C assumptions.

The core model is:

- modern AI reasoning may help diagnose problems;
- target implementation knowledge comes from a curated Classic Mac compatibility knowledge base;
- raw project history/current docs remain searchable evidence rather than automatic truth;
- private vendor manuals and historical books are a distinct follow-up reference layer;
- Retro68 provides a fast local preflight and compatibility gate;
- the project's declared CodeWarrior toolchain remains authoritative for CodeWarrior projects;
- real hardware evidence is recorded separately when behavior depends on the target machine;
- every state-changing operation should produce structured evidence;
- public knowledge and private hardware control are separate trust domains.

## Repositories

- `mplsllc/classicmac-mcp` — MCP server, domain model, adapters, compatibility gates, tests, and public architecture/security documentation.
- `mplsllc/classicmac-kb` — curated, provenance-bearing Classic Mac, CodeWarrior, C89, PowerPC, API, and compatibility knowledge plus derived indexes.
- `mplsllc/classicmac-infra` — private production deployment configuration, secrets integration, authentication, monitoring, backup, and Hetzner-specific operations.
- `mplsllc/workflow` — existing first-party reference implementation for CodeWarrior-over-SSH/AppleScript automation. ClassicMacMCP wraps and generalizes this work; it does not replace it blindly.

## Trust boundaries

The hosted public service must not have direct authority over a maintainer's private development Mac. Public knowledge access and local/private execution are separate capabilities.

A local hardware bridge may expose bounded build, deploy, launch, diagnostics, and test operations against a user's own machine. Credentials and host-specific configuration remain local/private.

## Compatibility principle

Generic modern C/C++ examples are not authoritative target knowledge. A project manifest declares its target OS, architecture, toolchain, and language constraints. Retrieval and validation are filtered by those constraints.

For a CodeWarrior Pro 8 / C89 project the expected validation ladder is:

1. deterministic ClassicMac compatibility checks;
2. Retro68 target-aware preflight;
3. CodeWarrior build on the configured machine;
4. hardware/runtime verification when required.

A passing earlier stage never upgrades itself into evidence for a later stage.

## Knowledge hierarchy

Default retrieval priority is:

1. canonical reviewed ClassicMac knowledge;
2. project / CodeWarrior / hardware evidence;
3. applicable primary vendor documentation;
4. historical books and contemporary secondary references;
5. general external/model knowledge.

The hosted MCP exposes these through separate search surfaces so vendor manuals or historical books cannot silently contaminate target compatibility guidance.

## CodeWarrior model

CodeWarrior is treated as a programmable IDE with multiple implementation surfaces:

- AppleEvents / AppleScript Automation API;
- native Metrowerks Plugin API where exact-version compatibility is proven;
- bounded GUI automation as a fallback.

Agents call semantic operations such as project identity, build, diagnostics, project membership, or access-path inspection rather than synthesizing raw AppleScript or Plugin API calls.

## Current status

Foundation / knowledge-and-compatibility phase.

The hosted server currently exposes read-only tools for project validation, strict-C89 policy scanning, validation-level explanation, canonical knowledge retrieval, raw history/document search, and optional follow-up historical/vendor reference search. Hardware mutation is intentionally not exposed by the hosted server yet.

Start with [`docs/README.md`](docs/README.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), and [`docs/MCP_TOOL_SURFACE.md`](docs/MCP_TOOL_SURFACE.md).

# ClassicMacMCP

ClassicMacMCP is an MCP development platform for building, validating, automating, and testing Classic Macintosh software with AI agents.

The project is intentionally broader than any single application. Its first reference environment is remote CodeWarrior development on a PowerPC Macintosh, but the architecture is designed for future projects, machines, toolchains, emulators, and community users.

## Mission

ClassicMacMCP should let an MCP-capable coding agent work against a historically constrained development environment without silently importing incompatible modern C assumptions.

The core model is:

- modern AI reasoning may help diagnose problems;
- target implementation knowledge comes from a curated Classic Mac compatibility knowledge base;
- Retro68 provides a fast local preflight and compatibility gate;
- the project's declared CodeWarrior toolchain remains authoritative for CodeWarrior projects;
- real hardware evidence outranks inference when behavior depends on the target machine;
- every state-changing operation should produce structured evidence;
- public knowledge and private hardware control are separate trust domains.

## Repositories

- `mplsllc/classicmac-mcp` — MCP server, domain model, adapters, compatibility gates, schemas, tests, and public architecture/security documentation.
- `mplsllc/classicmac-kb` — curated, provenance-bearing Classic Mac, CodeWarrior, C89, PowerPC, API, and compatibility knowledge.
- `mplsllc/classicmac-infra` — private production deployment configuration, secrets integration, authentication, monitoring, backup, and Hetzner-specific operations.
- `mplsllc/workflow` — existing first-party reference implementation for CodeWarrior-over-SSH/AppleScript automation. ClassicMacMCP wraps and generalizes this work; it does not replace it blindly.

## Trust boundaries

The hosted public service must not have direct authority over a maintainer's private development Mac. Public knowledge access and local/private execution are separate capabilities.

A local hardware bridge may expose build, deploy, launch, diagnostics, and test operations against a user's own machine. Credentials and host-specific configuration remain local/private.

## Compatibility principle

Generic modern C/C++ examples are not authoritative target knowledge. A project manifest declares its target OS, architecture, toolchain, and language constraints. Retrieval and validation are filtered by those constraints.

For a CodeWarrior Pro 8 / C89 project the expected validation ladder is:

1. deterministic ClassicMac compatibility checks;
2. Retro68 target-aware preflight;
3. CodeWarrior build on the configured machine;
4. hardware/runtime verification when required.

A passing earlier stage never upgrades itself into evidence for a later stage.

## Current status

Bootstrap phase. See `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, `docs/COMPATIBILITY.md`, and `docs/ROADMAP.md`.

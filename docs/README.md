# ClassicMacMCP Documentation

This directory describes the public architecture and contracts of ClassicMacMCP. Implementation status matters: some documents define current behavior, while others specify planned private/provider capabilities.

## Start here

- `ARCHITECTURE.md` — system boundaries and core domain model.
- `ROADMAP.md` — staged implementation plan and acceptance milestones.
- `SECURITY.md` — public/private security model and prohibited interfaces.
- `COMPATIBILITY.md` — C89/Retro68/CodeWarrior/hardware validation model.
- `KNOWLEDGE_AND_EVIDENCE.md` — source hierarchy, evidence levels, contradictions, and promotion.

## CodeWarrior

- `CODEWARRIOR_API.md` — semantic CodeWarrior service and control surfaces.
- `CODEWARRIOR_PLUGIN_API.md` — native Plugin API research based on Metrowerks SDK references, with CW8 verification requirements.
- `MCP_TOOL_SURFACE.md` — implemented hosted MCP tools versus planned private/local semantic tools.

## Execution and deployment boundaries

- `HOSTED_AND_LOCAL.md` — hosted service versus owner-controlled execution.
- `PROVIDERS.md` — provider capability/result/locking contract.
- `MANIFESTS.md` — project, machine, and toolchain identity manifests.
- `TESTING_AND_ACCEPTANCE.md` — unit/negative-control/Retro68/CodeWarrior/hardware gates and postcondition rules.

## Research

- `PRIOR_ART.md` — existing MCP/Classic Mac/remote-development projects and reuse decisions.

## Architecture Decision Records

Accepted decisions live under `adr/`:

- ADR-0001 — public/private boundary;
- ADR-0002 — Git as canonical knowledge store;
- ADR-0003 — CodeWarrior as authoritative compiler for CodeWarrior projects;
- ADR-0004 — Retro68 as target-aware preflight;
- ADR-0005 — provider-based hardware control;
- ADR-0006 — semantic CodeWarrior API;
- ADR-0007 — tiered knowledge retrieval.

## Normative terms

Where documents use **must**, **must not**, or **required**, they describe an intended security/compatibility invariant. Planned capabilities may still be unimplemented; `MCP_TOOL_SURFACE.md` is the authoritative status distinction for exposed hosted tools.

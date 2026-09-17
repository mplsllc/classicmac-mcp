# ADR-0006: Expose a semantic CodeWarrior API, not raw automation primitives

- Status: Accepted
- Date: 2026-09-16

## Context

CodeWarrior can be controlled through several surfaces: AppleEvents/AppleScript, GUI automation, and a native Plugin API. Different operations have different reliability across those surfaces. Existing workflow evidence already shows that a documented/terminology-visible AppleEvent may return success without producing the intended project mutation.

## Decision

MCP clients call stable semantic operations such as:

- project identity;
- target/project-file/access-path inspection;
- update/build/compile;
- diagnostics;
- project membership mutation;
- run/stop where verified.

A capability resolver chooses the safest, best-evidenced backend implementation for the exact IDE/project/machine fingerprint.

Raw AppleScript, raw AppleEvent construction, generic GUI input, and raw native Plugin API calls are internal implementation details and are not the normal public tool surface.

## Consequences

Positive:

- backend improvements do not force prompt/workflow changes;
- unsafe/broken automation paths can be bypassed per operation;
- evidence and postcondition policy is centralized;
- a future native plug-in can coexist with the proven SSH/AppleEvent workflow.

Costs:

- the semantic model must be carefully specified;
- capability discovery and versioning are required;
- some obscure IDE actions may remain unsupported until a safe semantic operation is designed.

## Rejected alternatives

- `run_applescript(source)` as the primary CodeWarrior interface.
- exposing raw SDK callback names directly to agents.
- forcing every operation through GUI automation.
- forcing every operation through the native Plugin API regardless of evidence.

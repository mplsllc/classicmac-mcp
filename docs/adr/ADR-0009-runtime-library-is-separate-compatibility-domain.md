# ADR-0009: Treat runtime-library compatibility as a separate domain

- Status: Accepted
- Date: 2026-09-16

## Context

A source file may be valid C89 and may include the correct Classic Mac headers while still relying on behavior or APIs specific to Metrowerks Standard Library (MSL). Retro68 and other cross toolchains may use different runtime libraries.

Treating compiler acceptance as proof of runtime-library compatibility would produce false confidence.

## Decision

ClassicMacMCP models runtime-library compatibility independently from language, compiler, SDK/API, ABI, linker, and project compatibility.

Knowledge and validation records should be able to distinguish:

- ISO C language behavior;
- Metrowerks compiler behavior/extensions;
- MSL headers/functions/semantics;
- Apple/Classic Mac APIs;
- ABI and callback conventions;
- linker/loader behavior;
- project/IDE behavior;
- packaging/resource behavior.

Retro68/newlib success does not establish MSL compatibility, and MSL documentation does not establish behavior for another runtime.

## Consequences

- Compatibility diagnostics can identify the actual layer that differs.
- MSL-specific knowledge can be retrieved without contaminating generic C guidance.
- Migration from CodeWarrior to another backend can use explicit shims/source changes instead of pretending the runtimes are interchangeable.
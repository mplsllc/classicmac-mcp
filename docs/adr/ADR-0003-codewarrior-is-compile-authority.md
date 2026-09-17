# ADR-0003: The declared CodeWarrior toolchain is authoritative for CodeWarrior projects

- Status: Accepted
- Date: 2026-09-16

## Context

Host GCC/Clang and Retro68 can catch useful problems quickly, but they do not exactly reproduce the language extensions, headers, MSL, project model, linker behavior, diagnostics, or IDE semantics of a historical CodeWarrior installation.

MacSurf history contains real examples where host checks passed code that CW8 rejected, and where cached/project/toolchain state changed the outcome.

## Decision

A project manifest declares its authoritative build toolchain. For a CodeWarrior project, only the declared CodeWarrior environment can produce `codewarrior_verified` compile/build evidence.

Host static checks and Retro68 are preflight layers. They may reject early, but they cannot upgrade their own success into CodeWarrior success.

## Consequences

Positive:

- compatibility claims remain historically/toolchain accurate;
- modern compiler permissiveness does not silently redefine the target language/runtime;
- compiler/linker/project failures become reusable compatibility evidence.

Costs:

- final validation may require slower remote IDE/hardware access;
- CI cannot fully replace the vintage toolchain;
- exact toolchain fingerprints need to be recorded.

## Rejected alternatives

- Treating `-std=c89` host GCC as equivalent to CW8.
- Treating Retro68 success as proof of CodeWarrior compatibility.
- Allowing generic model knowledge to decide whether a symbol/header/library exists in MSL/CW8.

# ADR-0004: Retro68 is a target-aware preflight, not the final authority

- Status: Accepted
- Date: 2026-09-16

## Context

Retro68 is unusually valuable because it targets Classic Macintosh systems and can run on modern hosts, making it far more relevant than generic host compilation. However, it uses a modern GCC-based toolchain and may accept language constructs, headers, libraries, or behavior that the authoritative CodeWarrior environment rejects or implements differently.

## Decision

Retro68 is a first-class validation gate with its own evidence level: `retro68_verified`.

For CodeWarrior projects, Retro68 runs before the authoritative CodeWarrior build and is configured with a project-specific compatibility profile such as `cw8-compat`.

Retro68/CodeWarrior disagreements are captured as regression knowledge. A passing Retro68 result is never represented as a CodeWarrior pass.

## Consequences

Positive:

- many target-aware failures can be caught without waiting for remote IDE/hardware;
- public users without vintage hardware still receive meaningful validation;
- compiler differences become a measurable compatibility corpus.

Costs:

- compatibility policy must surround the compiler; flags alone are insufficient;
- some false positives/false negatives will remain until difference tests mature;
- library/header availability must be modeled separately from language acceptance.

## Rejected alternatives

- Omitting Retro68 because it is not identical to CodeWarrior.
- Treating Retro68 as an interchangeable CodeWarrior backend.
- Letting Retro68's libc/header set silently define what exists in MSL.

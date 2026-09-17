# ADR-0007: Enforce tiered source authority

- Status: Accepted
- Date: 2026-09-16

## Context

Classic Macintosh development spans several evidence classes: project/hardware observations, vendor manuals, historical books, generic modern C knowledge, and modern toolchain behavior. Treating all retrieved material as equally authoritative would allow plausible but incompatible guidance to reach target code.

The project also maintains private user-owned manuals that should be searchable without being redistributed or automatically promoted into canonical truth.

## Decision

Retrieval and reasoning use this authority order for target programming and compatibility questions:

1. reviewed canonical ClassicMac knowledge;
2. exact project/toolchain/hardware evidence;
3. applicable primary vendor documentation;
4. historical books and contemporary secondary sources;
5. general external/model knowledge.

Only canonical records are automatically injected as trusted programming guidance. Other layers are follow-up evidence and must retain source class, applicability, and noncanonical status.

A lower layer may suggest a hypothesis but cannot silently override a higher layer. Unknown applicability is reported as unknown.

## Consequences

- Private books/manuals can increase recall without contaminating the primary coding context.
- Later CodeWarrior SDK documentation can reveal possible APIs while remaining unverified for CW8 until exact-version/hardware evidence exists.
- Modern GCC/Clang/StackOverflow/GitHub examples do not become implicit C89/CW8 guidance.
- Promotion from secondary/vendor/raw evidence into canonical knowledge is explicit and reviewable.
# Compatibility Policy

## Principle

ClassicMacMCP must not confuse a modern compiler's ability to accept code with compatibility with an older target toolchain.

A project declares its language and authoritative toolchain. Knowledge retrieval and validation are filtered by that declaration.

## CodeWarrior / C89 profile

For CodeWarrior Pro 8 C projects, the default policy is strict C89 plus explicitly verified CodeWarrior extensions. Modern C constructs are rejected or quarantined unless a compatibility record establishes that the selected toolchain accepts the exact usage.

Examples of constructs that must not be introduced casually:

- declarations after statements;
- declarations in `for` initializers;
- C++-style `//` comments where the project policy forbids them;
- designated initializers;
- compound literals;
- variable-length arrays;
- `restrict`;
- C99/C11 library assumptions;
- headers absent from the installed MSL/SDK unless an approved project shim exists;
- POSIX APIs not provided by the target environment;
- compiler-specific GCC/Clang constructs that have no verified CW equivalent.

## Retro68 role

Retro68 is a fast, target-aware preflight tool and compatibility laboratory. It is especially useful because it understands Classic Mac targets, PowerPC/68K conventions, PEF-related tooling, Apple interfaces, and LaunchAPPL workflows.

Retro68 is **not** a CodeWarrior emulator. Its GCC/newlib/libretro environment may accept language/library behavior that CodeWarrior/MSL does not.

Therefore a Retro68 pass establishes only `retro68_verified`.

## Validation ladder

### 1. `static_verified`

Deterministic project policy scans find no known violation.

This stage is cheap and intentionally conservative.

### 2. `retro68_verified`

The configured Retro68 profile compiles/links or otherwise validates the relevant target path.

Where practical, Retro68 should use Apple Universal Interfaces appropriate to the target project rather than relying on unrelated modern API availability.

### 3. `codewarrior_verified`

The declared CodeWarrior installation builds the actual project. CodeWarrior compiler/linker output is authoritative for CodeWarrior compatibility.

For CW8 automation, a successful AppleEvent return is not sufficient. The adapter checks live project diagnostics and output identity.

### 4. `hardware_verified`

The resulting artifact exhibits the stated behavior on the recorded target under a documented test. Runtime evidence is preserved.

## Differential compatibility learning

Disagreement between Retro68 and CodeWarrior is valuable data.

When:

`Retro68 PASS -> CodeWarrior FAIL`

or:

`Retro68 FAIL -> CodeWarrior PASS`

create a minimal compatibility regression case and a knowledge record describing the exact applicability. Over time this makes the preflight gate more predictive without pretending Retro68 and CodeWarrior are the same compiler.

## Library/API authority

Separate these questions:

- language syntax/semantics;
- target ABI/calling convention;
- Classic Mac API availability;
- C library/MSL availability;
- project-local shims;
- compiler/linker behavior.

A symbol present in Retro68's runtime is not evidence that MSL provides it. A modern host header is not evidence that the Classic Mac SDK provides it.

## Retrieval filtering

Target-programming retrieval may return only records whose applicability intersects the project manifest. Incompatible and unverified material can be explicitly requested for research, but is not silently injected into coding context.

The preferred answer when no verified record exists is `unknown: verify against target`, not a generic modern-C guess.

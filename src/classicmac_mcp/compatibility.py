"""High-confidence source checks for Classic Mac C89 projects.

This scanner is intentionally conservative. It catches constructs that are clearly
outside the configured policy; it is not a C parser and never claims compiler
compatibility. Retro68 and the authoritative project compiler remain later gates.
"""

from __future__ import annotations

import re

from .models import CompatibilityFinding, GateResult


_RULES: tuple[tuple[str, re.Pattern[str], str, str], ...] = (
    (
        "c89.cpp-comment",
        re.compile(r"//"),
        "C++-style comment",
        "C89 policy forbids // comments for strict CodeWarrior-targeted sources.",
    ),
    (
        "c89.for-init-declaration",
        re.compile(r"\bfor\s*\(\s*(?:const\s+)?(?:unsigned\s+|signed\s+)?(?:char|short|int|long|float|double|struct\s+\w+|enum\s+\w+|\w+_t)\s+\w+\s*="),
        "declaration in for initializer",
        "C89 requires the loop variable to be declared before the for statement.",
    ),
    (
        "c99.designated-initializer",
        re.compile(r"(?:^|[,{])\s*(?:\.\w+|\[[^\]]+\])\s*="),
        "designated initializer",
        "Designated initializers are not part of C89.",
    ),
    (
        "c99.compound-literal",
        re.compile(r"\([^;{}]+\)\s*\{"),
        "possible compound literal",
        "Compound literals are C99; review this construct before a CodeWarrior build.",
    ),
    (
        "c99.restrict",
        re.compile(r"\brestrict\b"),
        "restrict qualifier",
        "restrict is not part of C89.",
    ),
    (
        "c99.inline",
        re.compile(r"\binline\b"),
        "inline keyword",
        "The C99 inline keyword is not assumed compatible; use only a verified toolchain-specific form.",
    ),
    (
        "c99.vla-sizeof-runtime",
        re.compile(r"\b(?:char|short|int|long|float|double|\w+_t)\s+\w+\s*\[\s*[A-Za-z_]\w*\s*\]"),
        "possible variable-length array",
        "Variable-length arrays are not part of C89; verify the array bound is compile-time constant.",
    ),
)


def scan_c89(source: str) -> GateResult:
    """Return deterministic policy findings for a C source snippet."""

    findings: list[CompatibilityFinding] = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for rule_id, pattern, construct, message in _RULES:
            if pattern.search(line):
                findings.append(
                    CompatibilityFinding(
                        rule_id=rule_id,
                        severity="error",
                        line=line_number,
                        construct=construct,
                        message=message,
                    )
                )

    return GateResult(
        gate="classicmac-c89-policy",
        passed=not findings,
        authoritative=False,
        findings=findings,
        notes=[
            "This is a policy scanner, not a compiler.",
            "A pass must still proceed through Retro68 and the project's authoritative toolchain.",
        ],
    )


def validation_ladder() -> list[dict[str, object]]:
    """Describe the evidence ladder without conflating its stages."""

    return [
        {
            "level": "static_verified",
            "authority": "policy/static checks",
            "proves": "no known deterministic compatibility-policy violation was found",
            "does_not_prove": "target compilation or runtime behavior",
        },
        {
            "level": "retro68_verified",
            "authority": "Retro68 configured for the declared Classic Mac target",
            "proves": "target-aware preflight succeeded under the configured Retro68 profile",
            "does_not_prove": "CodeWarrior acceptance, MSL behavior, or hardware behavior",
        },
        {
            "level": "codewarrior_verified",
            "authority": "declared authoritative CodeWarrior installation",
            "proves": "the authoritative project compiler/linker accepted the build",
            "does_not_prove": "correct behavior on target hardware",
        },
        {
            "level": "hardware_verified",
            "authority": "declared physical/emulated target plus preserved evidence",
            "proves": "the stated behavior was observed under the recorded test conditions",
            "does_not_prove": "behavior outside the recorded applicability and test scope",
        },
    ]

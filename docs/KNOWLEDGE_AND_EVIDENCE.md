# Knowledge and Evidence Model

ClassicMacMCP separates *what is known* from *where a claim came from*. This is necessary because Classic Mac development frequently involves incomplete documentation, version-specific behavior, stale historical examples, and target hardware that contradicts host-side assumptions.

## Core rule

A source may be useful without being authoritative for the current project.

The MCP must preserve source class, applicability, validation level, and epistemic state instead of flattening all retrieved text into one undifferentiated context window.

## Retrieval layers

Default retrieval order:

1. **Canonical reviewed ClassicMac knowledge** — explicit compatibility facts and workflow rules that have been reviewed and scoped.
2. **Project / CodeWarrior / hardware evidence** — commits, diagnostics, controlled experiments, toolchain output, and hardware captures.
3. **Applicable primary vendor documentation** — Metrowerks, Apple, SDK headers, release notes, API references, and exact-version manuals.
4. **Historical books and contemporary secondary sources** — useful explanation and corroboration, but not project truth.
5. **General external/model knowledge** — useful for reasoning and hypothesis generation, never allowed to silently override the earlier layers.

Lower layers may explain, suggest, or corroborate. They do not automatically promote a claim into a higher layer.

## Canonical knowledge

Canonical knowledge lives in Git in `mplsllc/classicmac-kb`. Databases, FTS indexes, embeddings, and caches are derived artifacts.

Canonical records must include:

- stable ID;
- claim;
- scope/applicability;
- epistemic state;
- validation level;
- provenance/evidence links;
- confidence;
- contradictions or supersession when relevant.

Typical epistemic states:

- `fact` / `known`;
- `observed`;
- `decision`;
- `hypothesis`;
- `disproved`;
- `superseded`;
- `unknown`.

## Validation levels

Validation levels are evidence labels, not a single monotonic truth score:

- `static_verified` — deterministic policy/schema/source checks passed;
- `retro68_verified` — passed the configured Retro68 target-aware preflight;
- `codewarrior_verified` — reproduced by the declared authoritative CodeWarrior toolchain;
- `hardware_verified` — reproduced on declared target hardware.

A record may carry several levels when supported. Earlier validation never implies a later level.

## Source classes

Recommended source classes:

- `project_hardware_evidence`
- `project_commit_history`
- `project_documentation`
- `vendor_documentation`
- `vendor_header`
- `vendor_release_note`
- `vendor_sample_code`
- `historical_book`
- `third_party_prior_art`
- `external_research`

Raw commit/document/book hits are `canonical: false` by default.

## Vendor documentation

Primary vendor documentation is a preferred follow-up source when first-layer knowledge does not answer a question.

Examples in the current private corpus include Metrowerks compiler, MSL, Targeting Mac OS, IDE, and IDE SDK API references. These sources document intended behavior, but exact-version applicability must still be established.

For example, the IDE 5.1 SDK API Reference documents operations such as project enumeration, access-path enumeration, IDE/API version discovery, and project-entry mutation. That proves the API family existed in that SDK revision; it does **not** prove CodeWarrior Pro 8.x exposes identical ABI/behavior.

## Historical books

Historical books are searchable follow-up references. They can:

- explain period terminology and design intent;
- identify API sequences or toolchain conventions to investigate;
- corroborate a vendor or project observation;
- provide historically appropriate alternatives to modern assumptions.

They cannot automatically:

- override a controlled CW8.3 observation;
- establish API availability in a specific SDK;
- establish compiler/library support for a target project;
- enter the coding prompt as verified implementation guidance.

## Promotion

Promotion is deliberate:

```text
raw source / vendor passage / historical book
                |
                v
        candidate claim
                |
      applicability review
                |
     controlled verification
                |
                v
       canonical KB record
```

Promotion should preserve the original source citation and the verification evidence that justified the stronger status.

## Contradictions

Do not erase contradictions.

If a manual says an operation is supported but controlled CW8.3 testing says it fails, preserve both:

- documentation record: `documented`;
- observed record: `codewarrior_verified` failure/limitation;
- relationship: `contradicts` or `narrows`.

The retrieval layer should prefer the more applicable/higher-evidence observation while still making the documented intent available for diagnosis.

## Query behavior

The MCP should expose distinct tools or result classes for:

- curated knowledge search;
- raw Git/history search;
- raw project-document search;
- vendor/historical-reference search.

Every noncanonical result must say so in machine-readable output.

A normal coding request should not receive large amounts of historical-reference text automatically. Follow-up retrieval is triggered when:

- canonical knowledge is absent or `unknown`;
- the agent explicitly asks for historical/vendor context;
- corroboration is useful;
- a contradiction needs investigation.

## Private corpus

Copyrighted manuals/books may be indexed privately on the owner's server. Public repositories should contain only source metadata, derived compatibility facts, citations/references where lawful, and original analysis. The hosted public service must not become a manual redistribution endpoint.

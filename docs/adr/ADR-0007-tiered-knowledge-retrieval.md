# ADR-0007: Use tiered knowledge retrieval with explicit follow-up layers

- Status: Accepted
- Date: 2026-09-16

## Context

Classic Mac development sources vary widely in authority and applicability: project hardware experiments, current workflow docs, vendor manuals from adjacent versions, historical books, and generic modern programming knowledge can all be relevant but should not be treated equally.

Mixing every source into one vector/FTS corpus risks teaching an agent plausible but incompatible C/API behavior.

## Decision

Retrieval is tiered:

1. canonical reviewed ClassicMac knowledge;
2. project/toolchain/hardware evidence;
3. applicable primary vendor documentation;
4. historical books/secondary period references;
5. general external/model knowledge.

Canonical search is the default target-programming surface. Raw history/documents and historical/vendor references are exposed through distinct tools and labeled noncanonical.

Vendor/book retrieval is follow-up-only by default and cannot silently override higher-evidence observations.

## Consequences

Positive:

- compatibility contamination is reduced;
- contradictions can be preserved rather than averaged away;
- historical references remain useful for research;
- copyright-sensitive corpora can remain private while derived knowledge is public.

Costs:

- retrieval orchestration is more complex than one global search;
- source metadata/applicability must be maintained;
- agents may need a second query when first-layer knowledge is incomplete.

## Rejected alternatives

- one undifferentiated vector database for all source material;
- automatic injection of entire vendor/manual passages into every coding prompt;
- treating document age or vendor authorship alone as proof of exact CW8 applicability.

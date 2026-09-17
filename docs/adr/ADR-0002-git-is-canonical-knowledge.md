# ADR-0002: Git is the canonical knowledge store

- Status: Accepted
- Date: 2026-09-16

## Context

ClassicMacMCP needs searchable structured knowledge, raw history, documentation, and optional historical references. SQLite/FTS and future embedding indexes are useful for retrieval, but a database-only source of truth would make review, provenance, migration, and recovery harder.

## Decision

Reviewed canonical knowledge lives in version-controlled human-readable files in `classicmac-kb`.

SQLite/FTS, embeddings, and caches are generated indexes. Deleting them must not destroy canonical knowledge.

Raw Git history and project documents remain evidence inputs. Private historical/vendor references remain external/private source inputs with public metadata where appropriate.

## Consequences

Positive:

- every canonical change is reviewable as a Git diff;
- provenance and applicability remain inspectable without a database server;
- database/index technology can change without rewriting the knowledge corpus;
- corruption/loss of the derived DB is recoverable by rebuilding.

Costs:

- large-scale edits need schema validation and tooling;
- retrieval databases must be rebuilt after source changes;
- private overlays require deployment-time composition.

## Rejected alternatives

- Treating SQLite/Postgres/vector storage as canonical truth.
- Letting an LLM directly mutate the production knowledge database.
- Copying all private/manual text into the public canonical repository.

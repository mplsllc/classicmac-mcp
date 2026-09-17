# ADR-0008: Prefer CodeWarrior XML interchange before binary `.mcp` reverse engineering

- Status: Accepted
- Date: 2026-09-16

## Context

CodeWarrior supports project export/import through XML and can also export a GNU Makefile. The binary `.mcp` format therefore does not need to be the first interoperability target.

The project needs a faithful project model more urgently than it needs a binary project-file parser.

## Decision

ClassicMacMCP will treat CodeWarrior XML as the preferred initial interchange format for importing project semantics from genuine CodeWarrior.

The importer should preserve source provenance and reject or explicitly retain unsupported/unknown settings. It must not silently drop settings merely because the current schema lacks a mapping.

GNU Makefile export may be used as secondary archaeological evidence, not as a complete replacement for the project model.

Direct `.mcp` parsing is future convenience work.

## Consequences

- We can reconstruct real project semantics sooner.
- Binary reverse engineering is decoupled from the first useful release.
- The XML importer becomes a high-value compatibility fixture.
- Unknown CodeWarrior settings become visible schema work instead of silent loss.
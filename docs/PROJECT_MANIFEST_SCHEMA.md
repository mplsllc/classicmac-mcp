# Project Manifest Schema Contract

## Purpose

The project manifest is the portable policy document that tells ClassicMacMCP what target constraints govern retrieval and validation. It is deliberately smaller than the full CodeWarrior/project-engine model.

The current v1 parser is defined by `ProjectManifest` in `src/classicmac_mcp/models.py` and is documented in `MANIFESTS.md`.

## Current v1

V1 expresses only stable portable policy:

- project ID and name;
- source root;
- one target architecture and OS range;
- language and language standard;
- authoritative toolchain family/version;
- native project-file path when relevant;
- project-local knowledge paths.

V1 does **not** yet embed Retro68/provider policy, runtime-library selection, multiple targets, access paths, link order, resources, per-file settings, or alternate backends.

That omission is intentional. We should examine real CodeWarrior XML exports and preserve their semantics before freezing a richer portable manifest schema.

## Rich project-engine model

The internal/import project model is broader than manifest v1 and is expected eventually to represent:

- multiple targets;
- target CPU/OS/API/runtime and executable format;
- file/resource/library membership;
- groups and link order;
- access paths and recursive-search behavior;
- prefix/precompiled headers;
- defines;
- target and per-file compiler/linker preferences;
- runtime-library policy;
- output/resource/Finder metadata;
- memory settings;
- authoritative, preflight, and alternate backends.

See `PROJECT_MODEL.md` and `CODEWARRIOR_PROJECT_ENGINE.md`.

The richer model must not silently redefine v1 manifest semantics. When it becomes sufficiently evidenced and stable, it should become an explicit later manifest schema revision.

## CodeWarrior XML rule

CodeWarrior XML is the preferred first source for discovering the real project semantics. Unsupported imported settings must be retained explicitly or reported, never silently discarded.

## Authority

For v1, the declared `toolchain.authoritative` CodeWarrior/toolchain declaration controls target authority. Retro68 remains separate validation/provider policy until a later schema versions that relationship explicitly.

## Secrets

The manifest must never contain credentials, private hostnames that are not intentionally shareable, tokens, SSH keys, or raw private-provider commands.

Machine/provider secrets are referenced by local configuration only.
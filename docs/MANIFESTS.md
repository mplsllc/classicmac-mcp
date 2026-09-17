# Project and Machine Manifests

ClassicMacMCP uses explicit manifests so agents do not infer target constraints from repository contents or machine names.

## Project manifest

A project may define `.classicmac/project.yaml`.

Example:

```yaml
schema_version: 1
project:
  id: macsurf
  name: MacSurf
source:
  root: .
  vcs: git
target:
  architecture: powerpc
  os:
    family: classic-mac-os
    min: "8.6"
    max: "9.2.2"
toolchain:
  authoritative:
    family: codewarrior
    version: "8.3"
  language:
    c_standard: c89
validation:
  retro68:
    enabled: true
    profile: cw8-compat
build:
  project_file: MacSurf.mcp
knowledge:
  project_paths:
    - docs/knowledge
```

The project manifest contains no passwords, SSH keys, FTP credentials, or private host addresses.

## Machine manifest

Machine configuration is owner-local/private. A public-safe machine description may expose capabilities and fingerprints without credentials.

Example:

```yaml
schema_version: 1
machine:
  id: g3-imac
  platform: classic-mac-development-host
  target_os: "9.2.2"
  architecture: powerpc-g3
  toolchains:
    - family: codewarrior
      version: "8.3"
      authoritative_for:
        - macsurf
  capabilities:
    - codewarrior.read
    - codewarrior.build
    - machine.deploy
    - machine.launch
provider:
  id: g3-imac-workflow
  kind: codewarrior-automation
```

Private provider configuration may separately reference environment variables or a secret store for connection details.

## Toolchain fingerprint

A human version label is not enough. Where possible, preserve:

- IDE application version/build;
- executable/resource fingerprint;
- AppleEvent terminology fingerprint;
- compiler/linker version identifiers;
- installed SDK/Universal Interfaces version;
- MSL version/headers;
- CarbonLib/import-library version;
- Plugin API version reported by the IDE where available.

Compatibility records should reference the narrowest fingerprint actually demonstrated.

## Applicability

A knowledge record is eligible for automatic coding context only when its applicability is compatible with the project manifest.

Important dimensions include:

- language and standard;
- compiler/toolchain family and exact version;
- architecture;
- Classic Mac OS / Carbon target range;
- SDK/header/library versions;
- project-specific constraints.

Unknown applicability is not treated as compatible.

## Versioning

Manifest schema changes are explicit. Parsers reject unsupported schema versions and unknown keys by default unless a forward-compatible extension mechanism is deliberately introduced.

This is important because silently accepting a new field with old semantics can change compiler, deployment, or security behavior.

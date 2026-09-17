# Project and Machine Manifests

ClassicMacMCP uses explicit manifests so agents do not infer target constraints from repository contents or machine names.

## Project manifest

A project may define `.classicmac/project.yaml`.

The current v1 schema is deliberately compact and matches `ProjectManifest` in `src/classicmac_mcp/models.py`.

Example:

```yaml
schema_version: 1
project_id: macsurf
name: MacSurf
source_root: .
target:
  architecture: powerpc
  os:
    family: classic-mac-os
    minimum: "8.6"
    maximum: "9.2.2"
language:
  language: c
  standard: c89
toolchain:
  family: codewarrior
  version: "8.3"
  authoritative: true
project_file: MacSurf.mcp
knowledge_paths:
  - docs/knowledge
```

The project manifest contains no passwords, SSH keys, FTP credentials, or private host addresses.

Retro68/provider configuration is intentionally not embedded in the v1 project schema yet. Those policies are deployment/provider concerns until their portable semantics are stable enough to version into a future manifest revision.

## Machine manifest

`MachineManifest` is a public/non-secret machine description. Private connection details live separately in provider-local configuration.

Example:

```yaml
schema_version: 1
machine_id: g3-imac
name: G3 iMac
architecture: powerpc-g3
os_family: classic-mac-os
os_version: "9.2.2"
provider: codewarrior-ssh-applescript
capabilities:
  - codewarrior.read
  - codewarrior.build
  - machine.deploy
  - machine.launch
labels:
  role: reference-hardware
```

Private provider configuration may separately reference environment variables or a secret store for SSH host/user/key, FTP credentials, local paths, or other machine-specific secrets.

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

The v1 manifest stores the portable family/version declaration. Richer observed fingerprints belong in provider/evidence records until their schema is stabilized.

## Applicability

A knowledge record is eligible for automatic coding context only when its applicability is compatible with the project manifest.

Important dimensions include:

- language and standard;
- compiler/toolchain family and exact version;
- architecture;
- Classic Mac OS target family/range;
- project-specific constraints;
- SDK/header/library versions when represented by the knowledge record/evidence layer.

Unknown applicability is not treated as proof of compatibility.

## Versioning

Manifest schema changes are explicit. Pydantic models reject unknown keys by default. New nested structures or provider/validation policy fields belong in a future schema version unless they can be added without changing v1 semantics.

This prevents documentation examples from silently defining fields the parser does not understand and prevents old agents from misinterpreting newer project policy.

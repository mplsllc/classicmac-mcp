# Machine Manifest Schema Contract

## Purpose

Machine manifests describe observable target capabilities and provider bindings. They are normally private/local, with only sanitized identity/capability information shared outward.

## Fields

A v1 machine record may include:

- machine ID;
- platform/OS version;
- CPU/architecture;
- installed toolchain identities;
- declared capabilities;
- provider IDs;
- concurrency/serialization constraints;
- optional hardware fingerprint metadata;
- references to local secret/config records.

## Secret handling

Secrets are never embedded directly. A machine record may contain a local `secret_ref` or provider configuration reference that is resolved only inside the private bridge.

## Capability rule

Capabilities are positive declarations. If a machine/provider cannot safely verify an operation, that capability is absent.

## Fingerprints

Evidence-producing operations should enrich friendly versions with discovered fingerprints where possible, such as exact CodeWarrior IDE build/API version, compiler/linker plug-in identity, SDK/interface version, MSL/library identity, OS version, and relevant hardware identity.

## Concurrency

The machine manifest can declare serialization scopes such as machine-wide, IDE-wide, or project-wide. Providers must obey the narrowest safe scope.

## Public projection

A sanitized public projection may include machine class, OS/CPU/toolchain versions, and supported operations, but must exclude addresses, credentials, private paths, and network topology.
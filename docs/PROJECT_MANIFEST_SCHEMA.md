# Project Manifest Schema Contract

## Purpose

The project manifest is the portable policy document that tells ClassicMacMCP what the target actually is. It must be sufficient to constrain retrieval and validation without embedding private machine details.

## Required top-level concepts

A v1 project manifest should express:

- project identity;
- source root/VCS;
- one or more targets;
- target OS/architecture/API/runtime;
- language policy;
- runtime-library policy;
- authoritative toolchain;
- optional validation/alternate backends;
- native project/interchange files;
- project-local knowledge paths.

## Authority rule

Each target may declare at most one authoritative build backend. Other backends must have an explicit non-authoritative role such as `preflight` or `alternate`.

## CodeWarrior target semantics

The schema must be extensible to imported CodeWarrior XML semantics, including:

- file/resource/library membership;
- groups;
- link order;
- access paths and recursive search;
- prefix/precompiled headers;
- defines;
- target and per-file compiler/linker preferences;
- output metadata;
- resource/Finder metadata;
- memory settings.

Unsupported imported settings must be retained or reported, never silently discarded.

## Secrets

The manifest must never contain credentials, private hostnames that are not intentionally shareable, tokens, SSH keys, or raw private-provider commands.

Machine/provider secrets are referenced by local configuration only.
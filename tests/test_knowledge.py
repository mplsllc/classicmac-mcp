import sqlite3
from pathlib import Path

from classicmac_mcp.knowledge import get_record, search, search_documents, search_git_history
from classicmac_mcp.models import ProjectManifest


def _project() -> ProjectManifest:
    return ProjectManifest.model_validate(
        {
            "project_id": "demo",
            "name": "Demo",
            "target": {
                "architecture": "powerpc",
                "os": {"family": "classic-mac-os", "minimum": "8.6", "maximum": "9.2.2"},
            },
            "language": {"language": "c", "standard": "c89"},
            "toolchain": {"family": "codewarrior", "version": "8.3"},
        }
    )


def _source_file(root: Path) -> None:
    sources = root / "sources"
    sources.mkdir()
    (sources / "test.yaml").write_text(
        """schema_version: 1
sources:
  - id: test.source
    kind: repository_file
    title: Test source
    locator: {repository: example/repo, path: README.md}
    redistribution: public
    trust: controlled_observation
""",
        encoding="utf-8",
    )


def test_search_filters_incompatible_toolchain(tmp_path: Path):
    _source_file(tmp_path)
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "rules.yaml").write_text(
        """schema_version: 1
records:
  - id: cw-rule
    title: CW8 declaration rule
    scope: toolchain
    state: verified
    validation_level: codewarrior_verified
    statement: CodeWarrior C89 declaration behavior.
    applicability:
      architectures: [powerpc]
      toolchain_family: codewarrior
      toolchain_versions: ["8.3"]
      language: c
      language_standard: c89
    evidence:
      - {source_id: test.source, role: supports}
    tags: [codewarrior, c89, rule]
  - id: gcc-rule
    title: GCC extension rule
    scope: toolchain
    state: verified
    validation_level: static_verified
    statement: A GCC-only example.
    applicability:
      toolchain_family: gcc
      toolchain_versions: ["16"]
    evidence:
      - {source_id: test.source, role: supports}
    tags: [gcc, rule]
""",
        encoding="utf-8",
    )

    results = search(tmp_path, "rule", project=_project())
    assert [item["id"] for item in results] == ["cw-rule"]
    assert results[0]["evidence"][0]["source"]["id"] == "test.source"


def test_get_record_returns_statement_and_expanded_source(tmp_path: Path):
    _source_file(tmp_path)
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "fact.yaml").write_text(
        """schema_version: 1
records:
  - id: example-fact
    title: Example fact
    scope: global
    state: documented
    validation_level: static_verified
    statement: Canonical statement text.
    applicability: {}
    evidence:
      - {source_id: test.source, role: origin}
    tags: []
""",
        encoding="utf-8",
    )

    result = get_record(tmp_path, "example-fact")
    assert result is not None
    assert result["record"]["statement"] == "Canonical statement text."
    assert result["evidence"][0]["source"]["locator"]["repository"] == "example/repo"


def test_raw_git_history_is_explicitly_noncanonical(tmp_path: Path):
    database = tmp_path / "kb.sqlite"
    db = sqlite3.connect(database)
    db.execute(
        "CREATE VIRTUAL TABLE git_fts USING fts5(repository UNINDEXED, sha UNINDEXED, subject, body, files)"
    )
    db.execute(
        "INSERT INTO git_fts(repository, sha, subject, body, files) VALUES (?, ?, ?, ?, ?)",
        (
            "mplsllc/macsurf",
            "abc123",
            "fix CodeWarrior declaration order",
            "CW8 rejected a declaration after a statement",
            "foo.c",
        ),
    )
    db.commit()
    db.close()

    results = search_git_history(database, "CodeWarrior", repository="mplsllc/macsurf")
    assert len(results) == 1
    assert results[0]["sha"] == "abc123"
    assert results[0]["canonical_knowledge"] is False
    assert results[0]["evidence_class"] == "raw_git_history"


def test_raw_repository_document_is_explicitly_noncanonical(tmp_path: Path):
    database = tmp_path / "kb.sqlite"
    db = sqlite3.connect(database)
    db.execute(
        "CREATE VIRTUAL TABLE document_fts USING fts5(repository UNINDEXED, path, title, content)"
    )
    db.execute(
        "INSERT INTO document_fts(repository, path, title, content) VALUES (?, ?, ?, ?)",
        (
            "mplsllc/workflow",
            "playbook/06-build-diagnostics.md",
            "Build Diagnostics: Text First",
            "CodeWarrior exposes compiler and linker output programmatically.",
        ),
    )
    db.commit()
    db.close()

    results = search_documents(database, "compiler", repository="mplsllc/workflow")
    assert len(results) == 1
    assert results[0]["path"] == "playbook/06-build-diagnostics.md"
    assert results[0]["canonical_knowledge"] is False
    assert results[0]["evidence_class"] == "raw_repository_document"

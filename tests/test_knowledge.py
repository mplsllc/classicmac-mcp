from pathlib import Path

from classicmac_mcp.knowledge import get_record, search
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
            "toolchain": {"family": "codewarrior", "version": "pro-8.3"},
        }
    )


def test_search_filters_incompatible_toolchain(tmp_path: Path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "cw.md").write_text(
        """---
schema_version: 1
id: cw-rule
title: CW8 declaration rule
kind: language_rule
state: verified
summary: CodeWarrior C89 declaration behavior.
applies_to:
  architectures: [powerpc]
  toolchains: [codewarrior:pro-8.3]
  language_standards: [c89]
validation_levels: [codewarrior_verified]
tags: [codewarrior, c89]
sources: []
---
Declarations belong before statements.
""",
        encoding="utf-8",
    )
    (knowledge / "gcc.md").write_text(
        """---
schema_version: 1
id: gcc-rule
title: GCC extension rule
kind: language_rule
state: verified
summary: A GCC-only example.
applies_to:
  toolchains: [gcc:16]
validation_levels: [static_verified]
tags: [gcc]
sources: []
---
Not applicable to CodeWarrior.
""",
        encoding="utf-8",
    )

    results = search(tmp_path, "rule", project=_project())
    assert [item["id"] for item in results] == ["cw-rule"]


def test_get_record_returns_body(tmp_path: Path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "fact.md").write_text(
        """---
schema_version: 1
id: example-fact
title: Example fact
kind: fact
state: documented
summary: Example summary.
validation_levels: []
tags: []
sources: []
---
Canonical body text.
""",
        encoding="utf-8",
    )

    result = get_record(tmp_path, "example-fact")
    assert result is not None
    assert result["body"] == "Canonical body text."

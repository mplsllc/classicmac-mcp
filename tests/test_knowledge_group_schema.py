from pathlib import Path

import pytest

from classicmac_mcp.knowledge import iter_records, iter_sources


def test_direct_knowledge_reader_rejects_missing_group_schema_version(tmp_path: Path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "bad.yaml").write_text("records: []\n", encoding="utf-8")

    with pytest.raises(ValueError, match="schema_version"):
        list(iter_records(tmp_path))


def test_direct_source_reader_rejects_future_group_schema_version(tmp_path: Path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "bad.yaml").write_text(
        "schema_version: 2\nsources: []\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="expected 1"):
        list(iter_sources(tmp_path))


def test_direct_reader_rejects_unknown_top_level_group_key(tmp_path: Path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "bad.yaml").write_text(
        "schema_version: 1\nrecords: []\nsilent_new_semantics: true\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unexpected top-level keys"):
        list(iter_records(tmp_path))

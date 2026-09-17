import sqlite3
from pathlib import Path

from classicmac_mcp.references import search_references


def _database(path: Path) -> None:
    db = sqlite3.connect(path)
    try:
        db.executescript(
            """
            CREATE TABLE reference_documents (
                corpus TEXT NOT NULL,
                source_layer TEXT NOT NULL,
                path TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                PRIMARY KEY (corpus, path)
            );
            CREATE VIRTUAL TABLE reference_fts USING fts5(
                corpus UNINDEXED,
                source_layer UNINDEXED,
                path,
                title,
                content,
                tokenize='unicode61'
            );
            """
        )
        values = (
            "metrowerks-private",
            "vendor_documentation",
            "SDKAPIRM.txt",
            "IDE SDK API Reference",
            "CWGetProjectFileCount returns the number of files in the active target.",
        )
        db.execute(
            "INSERT INTO reference_documents VALUES (?, ?, ?, ?, ?)", values
        )
        db.execute("INSERT INTO reference_fts VALUES (?, ?, ?, ?, ?)", values)
        db.commit()
    finally:
        db.close()


def test_search_references_is_explicitly_noncanonical(tmp_path: Path):
    database = tmp_path / "kb.sqlite"
    _database(database)

    results = search_references(database, "CWGetProjectFileCount")
    assert len(results) == 1
    result = results[0]
    assert result["canonical_knowledge"] is False
    assert result["follow_up_only"] is True
    assert result["source_layer"] == "vendor_documentation"
    assert result["corpus"] == "metrowerks-private"
    assert "does not by itself establish" in result["warning"]


def test_search_references_allows_corpus_filter(tmp_path: Path):
    database = tmp_path / "kb.sqlite"
    _database(database)
    assert search_references(database, "active", corpus="other") == []


def test_search_references_returns_empty_when_optional_table_absent(tmp_path: Path):
    database = tmp_path / "kb.sqlite"
    sqlite3.connect(database).close()
    assert search_references(database, "CodeWarrior") == []

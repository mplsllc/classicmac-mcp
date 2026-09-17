import sqlite3
from pathlib import Path

from classicmac_mcp.fts import literal_fts_query
from classicmac_mcp.knowledge import search_git_history


def test_literal_fts_query_removes_operator_syntax():
    query = literal_fts_query('C++ "CodeWarrior": foo-bar OR *')
    assert query == '"C++" AND "CodeWarrior" AND "foo-bar" AND "OR"'


def test_raw_search_handles_punctuation_without_fts_parser_error(tmp_path: Path):
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
            "C++ CodeWarrior foo bar",
            "compatibility evidence",
            "foo.c",
        ),
    )
    db.commit()
    db.close()

    # Quotes, colon and dash must not be interpreted as raw SQLite FTS syntax.
    results = search_git_history(database, 'C++ "CodeWarrior": foo-bar')
    assert len(results) == 1
    assert results[0]["sha"] == "abc123"


def test_literal_fts_query_rejects_operator_only_input():
    assert literal_fts_query('"" : * ( )') == ""

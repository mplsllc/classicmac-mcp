"""Search the optional noncanonical historical/vendor reference index."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .fts import literal_fts_query


def search_references(
    database: Path,
    query: str,
    *,
    corpus: str = "",
    source_layer: str = "",
    limit: int = 20,
) -> list[dict[str, object]]:
    """Search follow-up historical/vendor references.

    Results are always noncanonical. Callers must not present them as verified
    CodeWarrior/project behavior without independent evidence.
    """

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if not database.exists():
        raise ValueError(f"knowledge database does not exist: {database}")
    match_query = literal_fts_query(query)
    if not match_query:
        return []

    db = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        table = db.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='reference_fts'"
        ).fetchone()
        if table is None:
            return []

        clauses = ["reference_fts MATCH ?"]
        params: list[object] = [match_query]
        if corpus:
            clauses.append("corpus = ?")
            params.append(corpus)
        if source_layer:
            clauses.append("source_layer = ?")
            params.append(source_layer)
        params.append(limit)

        rows = db.execute(
            f"""SELECT corpus, source_layer, path, title,
                       snippet(reference_fts, 4, '[', ']', ' … ', 40) AS excerpt,
                       bm25(reference_fts, 0.0, 0.0, 1.0, 4.0, 1.0) AS rank
                FROM reference_fts
                WHERE {' AND '.join(clauses)}
                ORDER BY rank LIMIT ?""",
            params,
        ).fetchall()

        return [
            {
                "evidence_class": "historical_reference",
                "canonical_knowledge": False,
                "follow_up_only": True,
                "corpus": row["corpus"],
                "source_layer": row["source_layer"],
                "path": row["path"],
                "title": row["title"],
                "excerpt": row["excerpt"],
                "rank": row["rank"],
                "warning": (
                    "Reference material documents or discusses historical behavior; "
                    "it does not by itself establish applicability to the active project/toolchain."
                ),
            }
            for row in rows
        ]
    finally:
        db.close()

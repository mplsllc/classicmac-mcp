"""Canonical knowledge loading and deterministic retrieval.

The Git repository is the source of truth. SQLite/FTS is derived data used for
large raw-history/document search; curated knowledge can always be read directly
from YAML without the generated database.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from .fts import literal_fts_query
from .models import KnowledgeRecord, ProjectManifest, SourceRecord

_TOKEN = re.compile(r"[A-Za-z0-9_+.-]+")


@dataclass(frozen=True, slots=True)
class LoadedKnowledge:
    record: KnowledgeRecord
    path: Path


@dataclass(frozen=True, slots=True)
class LoadedSource:
    record: SourceRecord
    path: Path


def _load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"top-level YAML value must be a mapping: {path}")
    return value


def iter_records(root: Path) -> Iterable[LoadedKnowledge]:
    knowledge_root = root / "knowledge"
    if not knowledge_root.exists():
        return
    for path in sorted(knowledge_root.rglob("*.yaml")):
        doc = _load_yaml(path)
        records = doc.get("records", [])
        if not isinstance(records, list):
            raise ValueError(f"records must be a list: {path}")
        for metadata in records:
            yield LoadedKnowledge(
                record=KnowledgeRecord.model_validate(metadata),
                path=path,
            )


def iter_sources(root: Path) -> Iterable[LoadedSource]:
    source_root = root / "sources"
    if not source_root.exists():
        return
    for path in sorted(source_root.rglob("*.yaml")):
        doc = _load_yaml(path)
        sources = doc.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError(f"sources must be a list: {path}")
        for metadata in sources:
            yield LoadedSource(
                record=SourceRecord.model_validate(metadata),
                path=path,
            )


def source_map(root: Path) -> dict[str, LoadedSource]:
    result: dict[str, LoadedSource] = {}
    for source in iter_sources(root):
        if source.record.id in result:
            raise ValueError(f"duplicate source id: {source.record.id}")
        result[source.record.id] = source
    return result


def applies_to_project(item: LoadedKnowledge, project: ProjectManifest) -> bool:
    """Return whether a record is explicitly compatible with a project.

    Empty applicability fields are wildcards. Explicit conflicts exclude the
    record. This intentionally prefers omission to compatibility contamination.
    """

    applies = item.record.applicability
    if (
        applies.toolchain_family
        and applies.toolchain_family.lower() != project.toolchain.family.lower()
    ):
        return False
    if applies.toolchain_versions and project.toolchain.version.lower() not in {
        value.lower() for value in applies.toolchain_versions
    }:
        return False
    if applies.language and applies.language.lower() != project.language.language.lower():
        return False
    if (
        applies.language_standard
        and applies.language_standard.lower() != project.language.standard.lower()
    ):
        return False
    if applies.architectures and project.target.architecture.lower() not in {
        value.lower() for value in applies.architectures
    }:
        return False
    if applies.os_family and applies.os_family.lower() != project.target.os.family.lower():
        return False
    if applies.projects and project.project_id.lower() not in {
        value.lower() for value in applies.projects
    }:
        return False
    return True


def _tokens(text: str) -> set[str]:
    return {match.group(0).lower() for match in _TOKEN.finditer(text)}


def _expand_evidence(
    root: Path,
    item: LoadedKnowledge,
    sources: dict[str, LoadedSource] | None = None,
) -> list[dict[str, object]]:
    sources = sources if sources is not None else source_map(root)
    result: list[dict[str, object]] = []
    for evidence in item.record.evidence:
        source = sources.get(evidence.source_id)
        row: dict[str, object] = evidence.model_dump(mode="json")
        if source is not None:
            row["source"] = source.record.model_dump(mode="json")
            row["source_path"] = str(source.path.relative_to(root))
        else:
            row["source_missing"] = True
        result.append(row)
    return result


def search(
    root: Path,
    query: str,
    *,
    project: ProjectManifest | None = None,
    limit: int = 10,
) -> list[dict[str, object]]:
    """Search curated canonical records with optional applicability filtering."""

    if limit < 1 or limit > 50:
        raise ValueError("limit must be between 1 and 50")
    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    ranked: list[tuple[int, LoadedKnowledge]] = []
    for item in iter_records(root):
        if project is not None and not applies_to_project(item, project):
            continue

        title_tokens = _tokens(item.record.title)
        tag_tokens = _tokens(" ".join(item.record.tags))
        statement_tokens = _tokens(item.record.statement)
        applicability_tokens = _tokens(
            json.dumps(item.record.applicability.model_dump(mode="json"))
        )

        score = 0
        score += 8 * len(query_tokens & title_tokens)
        score += 6 * len(query_tokens & tag_tokens)
        score += 4 * len(query_tokens & statement_tokens)
        score += len(query_tokens & applicability_tokens)
        if score:
            ranked.append((score, item))

    ranked.sort(key=lambda pair: (-pair[0], pair[1].record.id))
    sources = source_map(root)
    results: list[dict[str, object]] = []
    for score, item in ranked[:limit]:
        results.append(
            {
                "score": score,
                "id": item.record.id,
                "title": item.record.title,
                "scope": item.record.scope,
                "state": item.record.state.value,
                "statement": item.record.statement,
                "validation_level": item.record.validation_level.value,
                "applicability": item.record.applicability.model_dump(mode="json"),
                "tags": item.record.tags,
                "evidence": _expand_evidence(root, item, sources),
                "path": str(item.path.relative_to(root)),
            }
        )
    return results


def get_record(root: Path, record_id: str) -> dict[str, object] | None:
    sources = source_map(root)
    for item in iter_records(root):
        if item.record.id == record_id:
            return {
                "record": item.record.model_dump(mode="json"),
                "evidence": _expand_evidence(root, item, sources),
                "path": str(item.path.relative_to(root)),
            }
    return None


def search_git_history(
    database: Path,
    query: str,
    *,
    repository: str = "",
    limit: int = 20,
) -> list[dict[str, object]]:
    """Search the derived raw Git-history evidence index.

    Results are evidence candidates, not canonical knowledge. They must never be
    silently promoted into toolchain/platform facts.
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
        if repository:
            rows = db.execute(
                """SELECT repository, sha, subject, body, files,
                          bm25(git_fts, 0.0, 0.0, 5.0, 1.0, 0.5) AS rank
                   FROM git_fts
                   WHERE git_fts MATCH ? AND repository = ?
                   ORDER BY rank LIMIT ?""",
                (match_query, repository, limit),
            ).fetchall()
        else:
            rows = db.execute(
                """SELECT repository, sha, subject, body, files,
                          bm25(git_fts, 0.0, 0.0, 5.0, 1.0, 0.5) AS rank
                   FROM git_fts
                   WHERE git_fts MATCH ?
                   ORDER BY rank LIMIT ?""",
                (match_query, limit),
            ).fetchall()
        return [
            {
                "evidence_class": "raw_git_history",
                "canonical_knowledge": False,
                "repository": row["repository"],
                "sha": row["sha"],
                "subject": row["subject"],
                "body": row["body"],
                "files": [value for value in row["files"].splitlines() if value],
                "rank": row["rank"],
            }
            for row in rows
        ]
    finally:
        db.close()


def search_documents(
    database: Path,
    query: str,
    *,
    repository: str = "",
    limit: int = 20,
) -> list[dict[str, object]]:
    """Search explicitly opted-in current repository documentation.

    Results are raw navigation/evidence material, not canonical compatibility
    knowledge. This distinction prevents stale project documentation from silently
    overriding reviewed facts.
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
        if repository:
            rows = db.execute(
                """SELECT repository, path, title,
                          snippet(document_fts, 3, '[', ']', ' … ', 32) AS excerpt,
                          bm25(document_fts, 0.0, 2.0, 6.0, 1.0) AS rank
                   FROM document_fts
                   WHERE document_fts MATCH ? AND repository = ?
                   ORDER BY rank LIMIT ?""",
                (match_query, repository, limit),
            ).fetchall()
        else:
            rows = db.execute(
                """SELECT repository, path, title,
                          snippet(document_fts, 3, '[', ']', ' … ', 32) AS excerpt,
                          bm25(document_fts, 0.0, 2.0, 6.0, 1.0) AS rank
                   FROM document_fts
                   WHERE document_fts MATCH ?
                   ORDER BY rank LIMIT ?""",
                (match_query, limit),
            ).fetchall()
        return [
            {
                "evidence_class": "raw_repository_document",
                "canonical_knowledge": False,
                "repository": row["repository"],
                "path": row["path"],
                "title": row["title"],
                "excerpt": row["excerpt"],
                "rank": row["rank"],
            }
            for row in rows
        ]
    finally:
        db.close()

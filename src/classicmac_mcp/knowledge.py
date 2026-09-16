"""Canonical knowledge loading and deterministic search.

The Git repository is the source of truth. Search indexes/embeddings may be added
later, but the server can always rebuild useful retrieval directly from the
curated Markdown corpus.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from .models import KnowledgeRecord, ProjectManifest

_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
_TOKEN = re.compile(r"[A-Za-z0-9_+.-]+")


@dataclass(frozen=True, slots=True)
class LoadedKnowledge:
    record: KnowledgeRecord
    body: str
    path: Path


def load_record(path: Path) -> LoadedKnowledge:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"Knowledge record has no YAML front matter: {path}")
    metadata = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :].strip()
    record = KnowledgeRecord.model_validate(metadata)
    return LoadedKnowledge(record=record, body=body, path=path)


def iter_records(root: Path) -> Iterable[LoadedKnowledge]:
    knowledge_root = root / "knowledge"
    if not knowledge_root.exists():
        return
    for path in sorted(knowledge_root.rglob("*.md")):
        yield load_record(path)


def _toolchain_key(project: ProjectManifest) -> str:
    return f"{project.toolchain.family}:{project.toolchain.version}".lower()


def applies_to_project(item: LoadedKnowledge, project: ProjectManifest) -> bool:
    """Return whether a record is explicitly compatible with a project.

    Empty applicability lists are wildcards. Non-empty lists are filters. This
    deliberately errs toward excluding records when an explicit scope conflicts.
    """

    applies = item.record.applies_to
    checks = (
        (applies.architectures, project.target.architecture.lower()),
        (applies.os_families, project.target.os.family.lower()),
        (applies.toolchains, _toolchain_key(project)),
        (applies.language_standards, project.language.standard.lower()),
    )
    for allowed, actual in checks:
        if allowed and actual not in {value.lower() for value in allowed}:
            return False

    if applies.projects and project.project_id.lower() not in {
        value.lower() for value in applies.projects
    }:
        return False
    return True


def _tokens(text: str) -> set[str]:
    return {match.group(0).lower() for match in _TOKEN.finditer(text)}


def search(
    root: Path,
    query: str,
    *,
    project: ProjectManifest | None = None,
    limit: int = 10,
) -> list[dict[str, object]]:
    """Search canonical records with optional project applicability filtering."""

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
        summary_tokens = _tokens(item.record.summary)
        body_tokens = _tokens(item.body)

        score = 0
        score += 8 * len(query_tokens & title_tokens)
        score += 6 * len(query_tokens & tag_tokens)
        score += 4 * len(query_tokens & summary_tokens)
        score += len(query_tokens & body_tokens)
        if score:
            ranked.append((score, item))

    ranked.sort(key=lambda pair: (-pair[0], pair[1].record.id))
    results: list[dict[str, object]] = []
    for score, item in ranked[:limit]:
        results.append(
            {
                "score": score,
                "id": item.record.id,
                "title": item.record.title,
                "kind": item.record.kind,
                "state": item.record.state.value,
                "summary": item.record.summary,
                "validation_levels": [level.value for level in item.record.validation_levels],
                "applies_to": item.record.applies_to.model_dump(),
                "sources": [source.model_dump() for source in item.record.sources],
                "path": str(item.path.relative_to(root)),
            }
        )
    return results


def get_record(root: Path, record_id: str) -> dict[str, object] | None:
    for item in iter_records(root):
        if item.record.id == record_id:
            return {
                "record": item.record.model_dump(mode="json"),
                "body": item.body,
                "path": str(item.path.relative_to(root)),
            }
    return None

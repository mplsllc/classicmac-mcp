"""Safe/literal query normalization for SQLite FTS-backed evidence searches."""

from __future__ import annotations

import re

_FTS_TOKEN = re.compile(r"[A-Za-z0-9_+.-]+")


def literal_fts_query(text: str) -> str:
    """Convert user text to an AND query of quoted literal-ish tokens.

    MCP callers ask for evidence by concept; they do not need access to SQLite FTS
    query operators. Quoting extracted tokens prevents punctuation/operator syntax
    from changing the query language or causing parser failures.
    """

    tokens = [match.group(0) for match in _FTS_TOKEN.finditer(text)]
    if not tokens:
        return ""
    escaped = [token.replace('"', '""') for token in tokens]
    return " AND ".join(f'"{token}"' for token in escaped)

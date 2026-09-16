"""ClassicMacMCP hosted/read-only core.

Execution providers are intentionally not exposed by this server yet. The first
public surface is compatibility validation, curated knowledge retrieval, and
explicitly-labelled raw project-history evidence search.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml
from mcp.server.mcpserver import MCPServer

from . import __version__
from .compatibility import scan_c89, validation_ladder
from .knowledge import get_record, search, search_git_history
from .models import ProjectManifest

mcp = MCPServer(
    "ClassicMacMCP",
    description=(
        "Compatibility-aware development context for Classic Macintosh software. "
        "Public tools are read-only and do not control private hardware."
    ),
    version=__version__,
)


def _kb_root() -> Path:
    value = os.environ.get("CLASSICMAC_KB_ROOT", "../classicmac-kb")
    return Path(value).expanduser().resolve()


def _kb_database() -> Path:
    value = os.environ.get("CLASSICMAC_KB_DB", "../classicmac-kb/build/classicmac.sqlite")
    return Path(value).expanduser().resolve()


def _parse_project(manifest_yaml: str) -> ProjectManifest:
    data = yaml.safe_load(manifest_yaml)
    if not isinstance(data, dict):
        raise ValueError("project manifest must be a YAML mapping")
    return ProjectManifest.model_validate(data)


@mcp.tool()
def classicmac_about() -> dict[str, object]:
    """Describe this server's trust boundary and compatibility model."""

    return {
        "name": "ClassicMacMCP",
        "version": __version__,
        "mode": "hosted-read-only-core",
        "hardware_control": False,
        "knowledge_root": str(_kb_root()),
        "knowledge_database": str(_kb_database()),
        "validation_levels": validation_ladder(),
    }


@mcp.tool()
def classicmac_validate_project(manifest_yaml: str) -> dict[str, object]:
    """Validate a portable `.classicmac/project.yaml` manifest."""

    project = _parse_project(manifest_yaml)
    return {
        "valid": True,
        "project": project.model_dump(mode="json"),
        "toolchain_authority": (
            "The declared authoritative toolchain remains authoritative; "
            "Retro68 is a preflight gate only."
        ),
    }


@mcp.tool()
def classicmac_scan_c89(source: str) -> dict[str, object]:
    """Run deterministic strict-C89 policy checks on a source snippet.

    This is not a compiler. A pass does not establish CodeWarrior compatibility.
    """

    if len(source) > 1_000_000:
        raise ValueError("source exceeds 1,000,000 character scan limit")
    return scan_c89(source).model_dump(mode="json")


@mcp.tool()
def classicmac_validation_ladder() -> list[dict[str, object]]:
    """Explain what each compatibility evidence level proves and does not prove."""

    return validation_ladder()


@mcp.tool()
def classicmac_search_knowledge(
    query: str,
    project_manifest_yaml: str = "",
    limit: int = 10,
) -> list[dict[str, object]]:
    """Search curated Classic Mac knowledge, optionally filtered by project applicability.

    Generic internet/modern C knowledge and raw unreviewed commit history are not
    searched by this tool.
    """

    if len(query) > 500:
        raise ValueError("query exceeds 500 character limit")
    project = _parse_project(project_manifest_yaml) if project_manifest_yaml.strip() else None
    return search(_kb_root(), query, project=project, limit=limit)


@mcp.tool()
def classicmac_get_knowledge(record_id: str) -> dict[str, object]:
    """Return one canonical knowledge record with expanded provenance."""

    if len(record_id) > 200:
        raise ValueError("record id too long")
    item = get_record(_kb_root(), record_id)
    if item is None:
        raise ValueError(f"unknown knowledge record: {record_id}")
    return item


@mcp.tool()
def classicmac_search_history(
    query: str,
    repository: str = "",
    limit: int = 20,
) -> list[dict[str, object]]:
    """Search indexed project Git history for prior work or regressions.

    Results are explicitly raw evidence candidates, not canonical compatibility
    facts. Use `classicmac_search_knowledge` for trusted target-programming
    guidance.
    """

    if len(query) > 500:
        raise ValueError("query exceeds 500 character limit")
    if len(repository) > 200:
        raise ValueError("repository filter too long")
    return search_git_history(
        _kb_database(),
        query,
        repository=repository,
        limit=limit,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="ClassicMacMCP server")
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default=os.environ.get("CLASSICMAC_MCP_TRANSPORT", "stdio"),
    )
    parser.add_argument("--host", default=os.environ.get("CLASSICMAC_MCP_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("CLASSICMAC_MCP_PORT", "8000")),
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            json_response=True,
            stateless_http=True,
        )


if __name__ == "__main__":
    main()

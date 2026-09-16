import pytest
from pydantic import ValidationError

from classicmac_mcp.models import MachineManifest, ProjectManifest


def test_project_manifest_accepts_codewarrior_c89_target():
    manifest = ProjectManifest.model_validate(
        {
            "project_id": "example",
            "name": "Example",
            "target": {
                "architecture": "powerpc",
                "os": {"family": "classic-mac-os", "minimum": "8.6", "maximum": "9.2.2"},
            },
            "language": {"language": "c", "standard": "c89"},
            "toolchain": {"family": "codewarrior", "version": "8.3"},
            "project_file": "Example.mcp",
        }
    )
    assert manifest.toolchain.authoritative is True
    assert manifest.language.standard == "c89"


def test_project_manifest_rejects_unknown_keys():
    with pytest.raises(ValidationError):
        ProjectManifest.model_validate(
            {
                "project_id": "example",
                "name": "Example",
                "target": {
                    "architecture": "powerpc",
                    "os": {"family": "classic-mac-os"},
                },
                "toolchain": {"family": "codewarrior", "version": "8.3"},
                "password": "must-not-live-here",
            }
        )


def test_public_machine_manifest_contains_no_credentials_field():
    machine = MachineManifest.model_validate(
        {
            "machine_id": "g3-imac",
            "name": "G3 iMac",
            "architecture": "powerpc-g3",
            "os_version": "9.2.2",
            "provider": "codewarrior-ssh-applescript",
            "capabilities": ["build", "run", "diagnostics"],
        }
    )
    assert "password" not in machine.model_dump()

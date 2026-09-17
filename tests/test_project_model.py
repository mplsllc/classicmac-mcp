from classicmac_mcp.project_model import (
    BackendIdentity,
    BackendRole,
    ExecutableFormat,
    OutputMetadata,
    ProjectModel,
    ProjectTarget,
    RuntimeModel,
)


def test_authoritative_backend_is_explicit():
    target = ProjectTarget(
        id="macos9-carbon",
        name="Mac OS 9 Carbon PPC",
        architecture="powerpc",
        os_family="classic-mac-os",
        language_standard="c89",
        runtime_library="msl",
        output=OutputMetadata(
            name="Fixture",
            executable_format=ExecutableFormat.PEF,
            runtime=RuntimeModel.CFM,
        ),
        backends=(
            BackendIdentity("retro68", role=BackendRole.PREFLIGHT, profile="cw8-compat"),
            BackendIdentity("codewarrior", version="8.3", role=BackendRole.AUTHORITATIVE),
        ),
    )

    assert target.authoritative_backend() == target.backends[1]


def test_multiple_authoritative_backends_are_rejected():
    project = ProjectModel(
        schema_version=1,
        id="fixture",
        name="Fixture",
        targets=(
            ProjectTarget(
                id="target",
                name="Target",
                architecture="powerpc",
                os_family="classic-mac-os",
                backends=(
                    BackendIdentity("codewarrior", role=BackendRole.AUTHORITATIVE),
                    BackendIdentity("retro68", role=BackendRole.AUTHORITATIVE),
                ),
            ),
        ),
    )

    assert project.validate() == ["target 'target' declares multiple authoritative backends"]


def test_duplicate_target_ids_are_rejected():
    target = ProjectTarget(
        id="same",
        name="Same",
        architecture="powerpc",
        os_family="classic-mac-os",
    )
    project = ProjectModel(
        schema_version=1,
        id="fixture",
        name="Fixture",
        targets=(target, target),
    )

    assert "duplicate target id: same" in project.validate()


def test_unknown_schema_version_is_rejected():
    project = ProjectModel(
        schema_version=2,
        id="fixture",
        name="Fixture",
        targets=(
            ProjectTarget(
                id="target",
                name="Target",
                architecture="powerpc",
                os_family="classic-mac-os",
            ),
        ),
    )

    assert "unsupported schema_version 2" in project.validate()

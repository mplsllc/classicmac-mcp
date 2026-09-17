from datetime import UTC, datetime

from classicmac_mcp.provider_models import (
    CapabilityMode,
    CapabilityStatus,
    FailureClass,
    ImplementationChannel,
    OperationStatus,
    Postcondition,
    ProviderCapability,
    ProviderDescriptor,
    ProviderIdentity,
    ProviderOperationResult,
)


def test_provider_result_requires_explicit_success_and_postconditions():
    now = datetime.now(UTC)
    result = ProviderOperationResult(
        attempt_id="attempt-1",
        operation="codewarrior.build",
        provider=ProviderIdentity(
            provider_id="g3-imac-workflow",
            provider_kind="codewarrior-automation",
            machine_id="g3-imac",
        ),
        status=OperationStatus.SUCCESS,
        started_at=now,
        finished_at=now,
        postconditions=[
            Postcondition(name="project_identity", passed=True),
            Postcondition(name="diagnostics_clean", passed=True),
            Postcondition(name="artifact_changed", passed=True),
        ],
    )
    assert result.succeeded() is True

    result.postconditions[-1].passed = False
    assert result.succeeded() is False


def test_timeout_is_unknown_state_not_plain_failure():
    now = datetime.now(UTC)
    result = ProviderOperationResult(
        attempt_id="attempt-timeout",
        operation="codewarrior.build",
        provider=ProviderIdentity(
            provider_id="g3-imac-workflow",
            provider_kind="codewarrior-automation",
        ),
        status=OperationStatus.UNKNOWN_STATE,
        failure_class=FailureClass.OPERATION_TIMEOUT_UNKNOWN_STATE,
        started_at=now,
        finished_at=now,
    )
    assert result.succeeded() is False
    assert result.failure_class is FailureClass.OPERATION_TIMEOUT_UNKNOWN_STATE


def test_provider_descriptor_reports_operation_backend_without_exposing_transport_tool():
    descriptor = ProviderDescriptor(
        identity=ProviderIdentity(
            provider_id="g3-imac-workflow",
            provider_kind="codewarrior-automation",
            machine_id="g3-imac",
            toolchain_id="codewarrior-8.3",
        ),
        capabilities=[
            ProviderCapability(
                name="codewarrior.add_project_file",
                mode=CapabilityMode.MUTATE,
                status=CapabilityStatus.VERIFIED,
                implementation=ImplementationChannel.GUI,
                authorization_scope="codewarrior.project_mutate",
                lock_scope="codewarrior:g3-imac",
            )
        ],
    )
    capability = descriptor.capability("codewarrior.add_project_file")
    assert capability is not None
    assert capability.implementation is ImplementationChannel.GUI
    assert descriptor.capability("run_shell") is None

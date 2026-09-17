from classicmac_mcp.providers import (
    CapabilityMode,
    FailureClass,
    OperationStatus,
    ProviderCapability,
    ProviderIdentity,
    ProviderOperationResult,
)


def test_provider_capability_lookup():
    provider = ProviderIdentity(
        id="workflow-ssh-cw",
        version="1",
        machine_id="g3-imac",
        capabilities=(
            ProviderCapability("machine.identity", CapabilityMode.READ),
            ProviderCapability("codewarrior.build", CapabilityMode.MUTATE, implementation="appleevent"),
        ),
    )

    assert provider.capability("codewarrior.build") is not None
    assert provider.capability("shell.run") is None


def test_failed_operation_requires_failure_class():
    result = ProviderOperationResult(
        operation_id="op-1",
        provider_id="fake",
        status=OperationStatus.FAILED,
    )

    assert result.validate() == ["failed operation must declare a failure_class"]


def test_timeout_is_unknown_not_failed():
    result = ProviderOperationResult(
        operation_id="op-2",
        provider_id="fake",
        status=OperationStatus.UNKNOWN,
        failure_class=FailureClass.TIMEOUT_STATE_UNKNOWN,
    )

    assert result.validate() == []

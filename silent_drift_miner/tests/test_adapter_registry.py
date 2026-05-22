from __future__ import annotations

from silent_drift_miner.adapters.registry import (
    adapter_for_spec_payload,
    executable_ecosystems,
    get_registered_adapter,
    list_registered_adapters,
)


def test_executable_adapter_registry_contains_active_non_python_adapters() -> None:
    assert executable_ecosystems() == ("dotnet", "go", "js", "jvm", "php", "ruby")
    assert [entry.ecosystem for entry in list_registered_adapters()] == list(executable_ecosystems())
    assert get_registered_adapter("JVM").display_name == "JVM"


def test_adapter_for_spec_payload_uses_registry_for_non_python_specs() -> None:
    assert adapter_for_spec_payload({"ecosystem": "python"}) is None
    assert adapter_for_spec_payload({"ecosystem": "js"}).__class__.__name__ == "JsAdapter"

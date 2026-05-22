"""Runtime registry for executable ecosystem adapters."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ..adapter_contracts import EcosystemAdapter
from .dotnet import DotnetAdapter
from .go import GoAdapter
from .js import JsAdapter
from .jvm import JvmAdapter
from .php import PhpAdapter
from .ruby import RubyAdapter


AdapterFactory = Callable[[], EcosystemAdapter]


@dataclass(frozen=True)
class RegisteredAdapter:
    ecosystem: str
    factory: AdapterFactory
    display_name: str

    def create(self) -> EcosystemAdapter:
        return self.factory()


_ADAPTERS: dict[str, RegisteredAdapter] = {
    "dotnet": RegisteredAdapter("dotnet", DotnetAdapter, ".NET"),
    "go": RegisteredAdapter("go", GoAdapter, "Go"),
    "js": RegisteredAdapter("js", JsAdapter, "JS"),
    "jvm": RegisteredAdapter("jvm", JvmAdapter, "JVM"),
    "php": RegisteredAdapter("php", PhpAdapter, "PHP"),
    "ruby": RegisteredAdapter("ruby", RubyAdapter, "Ruby"),
}


def executable_ecosystems() -> tuple[str, ...]:
    return tuple(sorted(_ADAPTERS))


def list_registered_adapters() -> list[RegisteredAdapter]:
    return [_ADAPTERS[name] for name in sorted(_ADAPTERS)]


def get_registered_adapter(ecosystem: str) -> RegisteredAdapter:
    key = ecosystem.lower()
    if key not in _ADAPTERS:
        raise KeyError(f"unsupported executable adapter ecosystem: {ecosystem}")
    return _ADAPTERS[key]


def get_adapter(ecosystem: str) -> EcosystemAdapter:
    return get_registered_adapter(ecosystem).create()


def adapter_for_spec_payload(payload: dict) -> EcosystemAdapter | None:
    ecosystem = str(payload.get("ecosystem") or "python").lower()
    if ecosystem not in _ADAPTERS:
        return None
    return get_adapter(ecosystem)

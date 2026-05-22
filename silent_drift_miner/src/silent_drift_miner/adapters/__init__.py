"""Ecosystem-specific adapter implementations."""
from __future__ import annotations

from .registry import (
    adapter_for_spec_payload,
    executable_ecosystems,
    get_adapter,
    get_registered_adapter,
    list_registered_adapters,
)

__all__ = [
    "adapter_for_spec_payload",
    "executable_ecosystems",
    "get_adapter",
    "get_registered_adapter",
    "list_registered_adapters",
]

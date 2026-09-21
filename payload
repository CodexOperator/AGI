"""LM hook protocol (T-028 / R6.1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass
class HookResult:
    schema_yaml: str | None  # raw YAML proposal; None on failure
    error: str | None  # human-readable error if hook failed


@runtime_checkable
class LanguageModelHook(Protocol):
    name: str

    def propose_schema(self, samples: list[dict[str, Any]]) -> HookResult: ...

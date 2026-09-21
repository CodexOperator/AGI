"""No-op LM hook (T-028 / R6.2)."""

from __future__ import annotations

from typing import Any

from .protocol import HookResult


class NoneHook:
    name = "none"

    def propose_schema(self, samples: list[dict[str, Any]]) -> HookResult:
        return HookResult(schema_yaml=None, error="hook=none: no LM configured")

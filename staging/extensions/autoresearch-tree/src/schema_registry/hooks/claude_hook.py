"""Claude LM hook stub (T-028 / R6).

Placeholder. Real implementation requires the Anthropic SDK + API key.
For now, returns a structured failure if no SDK is configured. v2 task
will wire the real client.
"""

from __future__ import annotations

import os
from typing import Any

from .protocol import HookResult


class ClaudeHook:
    name = "claude"

    def __init__(self) -> None:
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    def propose_schema(self, samples: list[dict[str, Any]]) -> HookResult:
        if not self.api_key:
            return HookResult(
                schema_yaml=None,
                error="ANTHROPIC_API_KEY not set; hook=claude unavailable",
            )
        # v2: actually call the API. For now, return a structured stub.
        return HookResult(
            schema_yaml=None,
            error="claude hook: SDK integration deferred to v2",
        )

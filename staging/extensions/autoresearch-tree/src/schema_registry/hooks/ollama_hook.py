"""Ollama LM hook stub (T-028 / R6).

Placeholder using local HTTP at 127.0.0.1:11434. Real impl deferred — for now,
gracefully degrades if the daemon isn't running.
"""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from typing import Any

from .protocol import HookResult


def _is_reachable(host: str = "127.0.0.1", port: int = 11434, timeout: float = 0.2) -> bool:
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except (OSError, socket.timeout):
        return False


class OllamaHook:
    name = "ollama"

    def __init__(self) -> None:
        self.endpoint = "http://127.0.0.1:11434"

    def propose_schema(self, samples: list[dict[str, Any]]) -> HookResult:
        if not _is_reachable():
            return HookResult(
                schema_yaml=None,
                error="ollama daemon unreachable at 127.0.0.1:11434",
            )
        # v2: actual call. For now, return stub failure to keep CI clean.
        return HookResult(
            schema_yaml=None,
            error="ollama hook: integration deferred to v2",
        )

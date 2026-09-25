"""Minimal executable transport seam used by the boundary falsifier."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol

TRANSPORTS = {}


class Transport(Protocol):
    def send(self, request: dict) -> dict: ...


def register(name: str, module_path: str | Path) -> None:
    spec = importlib.util.spec_from_file_location("fixture_transport_" + name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    TRANSPORTS[name] = module


def _memory(request: dict) -> dict:
    return {"transport": "memory", "accepted": True, "text": request["text"]}


TRANSPORTS["memory"] = _memory


def route(name: str, request: dict) -> dict:
    adapter = TRANSPORTS[name]
    if hasattr(adapter, "send"):
        return adapter.send(request)
    return adapter(request)

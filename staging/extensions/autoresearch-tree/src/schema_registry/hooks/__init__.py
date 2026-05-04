"""Pluggable LM hooks for schema generation (T-028 / R6)."""

from .none_hook import NoneHook
from .protocol import LanguageModelHook, HookResult

__all__ = ["LanguageModelHook", "HookResult", "NoneHook", "load_hook_from_config"]


def load_hook_from_config(hook_name: str | None) -> LanguageModelHook:
    """Resolve a hook by name. Falls back to NoneHook on unknown / missing."""
    name = (hook_name or "none").lower()
    if name == "none":
        return NoneHook()
    if name == "claude":
        try:
            from .claude_hook import ClaudeHook

            return ClaudeHook()
        except Exception:
            return NoneHook()
    if name == "ollama":
        try:
            from .ollama_hook import OllamaHook

            return OllamaHook()
        except Exception:
            return NoneHook()
    return NoneHook()

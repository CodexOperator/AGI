"""The Grok Bot harness — REQUIRED surface, stub argv (goal:g17.14.1).

CLI flags are NOT guessed: `build_command` emits a minimal, measurable argv
and `restart` refuses until `<bin> --help` is read the way
`copilot_cli_adapter`'s was. `needs_credential` is False — Grok Bot
authenticates through its own channel, so no OpenRouter key is minted.

`DEFAULT_BIN` is a BARE program name, resolved on PATH by `Popen`, mirroring
`claude_code_adapter.py`. The box path lives in the config `harnesses.grok-bot`
`bin` cell (owned by `goal:g17.14.2`), so no `/home/<user>` literal is baked
into this file.
"""
from __future__ import annotations
import os
import adapters

NAME = "grok-bot"

#: Fallback only. `$GROK_BOT_BIN`, then `harness["bin"]`, then this
#: (PATH-resolved by Popen). The configured box path is a config cell, not
#: a literal here.
DEFAULT_BIN = "grok-bot"


def resolve_bin(harness: dict) -> str:
    """$GROK_BOT_BIN > harness bin > default (pi_adapter's precedence)."""
    return os.environ.get("GROK_BOT_BIN") or harness.get("bin") or DEFAULT_BIN


def model_args(harness: dict, tier: str) -> list[str]:
    """models[tier] -> --model; a missing tier errors by name, never another
    tier's model (a silent fallback would look like it worked)."""
    models = harness.get("models") or {}
    if models and tier not in models:
        raise KeyError(
            f"harness {harness.get('adapter', NAME)!r} declares no model for "
            f"tier {tier!r}; known tiers: {sorted(models)}"
        )
    model = models.get(tier)
    return ["--model", model.strip()] if isinstance(model, str) and model.strip() else []


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    """Apply the ONE credential-none rule here so no spawn path drifts from
    the mint gate (hypothesis:l4-needs-credential-is-provider-gated)."""
    env = {**base, **{k: str(v) for k, v in (harness.get("env") or {}).items()}}
    return adapters.forward_named_env(
        adapters.drop_unneeded_credential(env, harness), harness)


def build_command(*, harness: dict, tier: str, context_file: str,
                  **kwargs) -> list[str]:
    """STUB argv: `<bin> [--model M] -p <context_file>`. `**kwargs` swallows
    the channels dispatch.py passes every adapter, so a spawn cannot die on a
    TypeError before the flags land."""
    return [resolve_bin(harness), *model_args(harness, tier),
            "-p", str(context_file)]


def is_alive(pid: int) -> bool:
    """A zombie counts as dead — same /proc rule as pi_adapter."""
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
            if fh.read().rsplit(") ", 1)[1].split()[0] == "Z":
                return False
    except (OSError, IndexError, ValueError):
        pass
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def restart(**kwargs) -> int | None:
    """Not yet: needs the measured flag set. dispatch.py handles the refusal
    (goal:g4.7) by marking the agent failed, not resurrecting a guessed argv."""
    raise NotImplementedError(
        "grok_bot_adapter.restart: Grok Bot flags unmeasured; read `<bin> "
        "--help` and fill build_command first (goal:g17.14.1)"
    )


def needs_credential(harness: dict) -> bool:
    """Grok Bot uses its own auth channel; no minted OpenRouter key."""
    return False
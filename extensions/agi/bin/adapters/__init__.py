"""Harness adapters — the only place a spawn target's CLI shape is known.

`goal:g4.6`. Before this package, `dispatch.py` built a pi command inline and
`zoom.py` branched a completion contract on two string literals, so adding a
third harness meant editing shared code and inventing a third config shape.
`goal:g4.3` had asked for "a runtime flag, not a parallel code path" since the
beginning; what was missing was somewhere for the flag to point.

**An adapter owns exactly three questions, now that `goal:g4.7` is active:**

    build_command(...) -> list[str]      the argv that starts one agent
    child_env(...)     -> dict[str,str]  the environment that argv runs in
    is_alive(pid)      -> bool           "is the process still running"
    restart(...)       -> int | None     "re-spawn the agent; return new pid"

`restart` receives the same keyword arguments as `build_command`, plus the
original `agent_record` dict, so the adapter can rebuild an identical argv
from what was stored at spawn time. A harness that cannot restart raises
`NotImplementedError` and dispatch falls through to marking the agent failed.
Both shipped adapters -- `pi` and, since 2026-09-03, `claude_code` -- restart.

`load(name)` is the whole dispatch mechanism. There is no registry to keep in
sync -- the module name comes from config, so adding a harness is one config
entry plus one file in this directory, and `dispatch.py` is never edited. That
is `mvp:unified-spawn-path`'s first falsifier, stated as code.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType

#: Adapters must define these. Checked at load, so a malformed adapter fails
#: when it is selected rather than when it is first spawned through.
REQUIRED = ("build_command", "child_env", "is_alive", "restart", "needs_credential")


class AdapterError(RuntimeError):
    """Raised for an adapter that is missing, unimportable or incomplete."""


def load(name: str) -> ModuleType:
    """Import `adapters/<name>_adapter.py` and verify its interface.

    The failure message names the directory rather than only the module,
    because the common cause is a config entry naming a harness nobody has
    written yet -- and a bare ImportError sends the reader to the config when
    the fix is a new file.
    """
    if not name or not isinstance(name, str):
        raise AdapterError(f"harness adapter name must be a non-empty string, got {name!r}")
    modname = f"{__name__}.{name}_adapter"
    try:
        mod = importlib.import_module(modname)
    except ModuleNotFoundError as exc:
        # Only rewrite the message when the ADAPTER is what is missing; an
        # adapter that imports a missing third-party module must not be
        # reported as an unknown harness.
        if getattr(exc, "name", None) != modname:
            raise
        expected = Path(__file__).resolve().parent / f"{name}_adapter.py"
        raise AdapterError(
            f"no adapter for harness {name!r}: expected {expected}. "
            f"Adding a harness is one config entry plus one file in "
            f"bin/adapters/ (goal:g4.6)."
        ) from exc
    missing = [fn for fn in REQUIRED if not callable(getattr(mod, fn, None))]
    if missing:
        raise AdapterError(
            f"adapter {modname} is missing {', '.join(missing)}; "
            f"every adapter must define {', '.join(REQUIRED)}"
        )
    return mod


#: Tiers every synthesized harness declares. `parent` exists here before
#: anything dispatches one, so the config shape does not change on the day the
#: parent tier lands (`goal:g4.3` mode 2).
TIERS = ("kid", "parent", "director", "prime_director")


def resolve(cfg: dict, name: str | None = None) -> tuple[str, dict]:
    """Pick a harness from config, synthesizing one for a legacy project.

    Returns `(name, harness_dict)`.

    **The synthesis path is the mainline, not an exotic edge**, and that is a
    measured claim: `harnesses` is absent from this engine's own
    `.agi/config.json`, so every run in this repo takes it until someone
    migrates. The baseline audit (`outcome:a00-c8365a0c-85a6d1`) found that and
    it corrects the assumption the design was written under -- it was framed as
    backward compatibility for other projects. It is the default path and is
    tested as one.

    Legacy synthesis maps today's `agent_dispatch` onto the harness shape.
    **Both tiers are populated explicitly with the same model**, rather than
    left absent for `model_args` to fall back on: a legacy config genuinely has
    one model for everything, and saying so is honest, where a silent fallback
    would be the thing `model_args` refuses to do.
    """
    harnesses = cfg.get("harnesses") or {}
    spawn = cfg.get("spawn") or {}
    chosen = name or spawn.get("harness")

    if harnesses:
        if not chosen:
            if len(harnesses) == 1:
                chosen = next(iter(harnesses))
            else:
                raise AdapterError(
                    "config declares several harnesses and no `spawn.harness`; "
                    f"name one of {sorted(harnesses)}"
                )
        if chosen not in harnesses:
            raise AdapterError(
                f"no harness {chosen!r} in config; declared: {sorted(harnesses)}"
            )
        harness = dict(harnesses[chosen])
        harness.setdefault("adapter", chosen.replace("-", "_"))
        return chosen, harness

    # --- legacy: no `harnesses` block. Synthesize pi from `agent_dispatch`.
    if chosen and chosen != "pi":
        raise AdapterError(
            f"harness {chosen!r} requested, but this config declares no "
            "`harnesses` block; only the legacy pi synthesis is available"
        )
    legacy = cfg.get("agent_dispatch") or {}
    model = legacy.get("model")
    harness = {
        "adapter": "pi",
        "synthesized_from": "agent_dispatch",
        "models": {tier: model for tier in TIERS} if model else {},
    }
    for key in ("provider", "thinking", "bin"):
        if legacy.get(key):
            harness[key] = legacy[key]
    return "pi", harness


def parallelism(cfg: dict, default: int = 1) -> int:
    """How many slots to spawn. `spawn.parallel` wins; legacy key survives.

    `agent_dispatch.claude_max_parallel` is the legacy name and is misleading
    twice over -- it sits in the pi namespace and it counts pi kids, not Claude
    ones. Left readable rather than renamed, because a config key is a
    compatibility surface, and named plainly in `spawn.parallel` going forward.
    """
    spawn = cfg.get("spawn") or {}
    if "parallel" in spawn:
        return int(spawn["parallel"])
    legacy = cfg.get("agent_dispatch") or {}
    return int(legacy.get("claude_max_parallel", default))


def needs_credential(harness: dict) -> bool:
    """Does this harness require a minted OpenRouter key?

    Delegates to the adapter's `needs_credential()` function, which is
    REQUIRED on every adapter. The default assumes yes; harnesses that
    authenticate through their own channel (e.g. Claude Code's subscription
    auth on disk) return False so dispatch.py does not waste a provisioned
    key on them.
    """
    adapter_name = harness.get("adapter", "")
    if adapter_name:
        mod = load(adapter_name)
        return mod.needs_credential(harness)
    return True
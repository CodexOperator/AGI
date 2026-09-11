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


#: The refusal a cross-namespace model carries. It names BOTH names because
#: the incident this exists for read as a mysterious OpenRouter bill rather
#: than a wrong flag (`hypothesis:l3-workflow-model-crosses-harness-namespace`).
OPENROUTER_ALIAS_ERR = (
    "model {model!r} is not an OpenRouter slug (no 'provider/name') but the "
    "target provider is {provider!r} — refusing to spend a Claude Code "
    "subscription alias against an OpenRouter key "
    "(hypothesis:l3-workflow-model-crosses-harness-namespace)"
)


# ---------------------------------------------------------------------------
# ONE SOURCE OF (tier, role, harness) MODEL TRUTH
# hypothesis:l4-a-model-change-is-one-write — the ladder `roles:` table is the
# ONE source of a role's model/effort/settings per harness. dispatch.py,
# workflow.py and heal.py import these, so a model change is ONE `write.py` on
# ladder:ladder instead of four cells in three files. `harnesses.<h>.models
# <role>` and `agent_dispatch.model` stop being inputs: dispatch.py emits ONE
# stderr warning naming the winning ladder row when a config still carries one.
# ---------------------------------------------------------------------------

def ladder_role_row(roles, tier, role):
    """The ladder `roles:` row for (tier, role), or None.

    The single lookup shared by the three spawners. A row matching both keys
    wins outright; no row answers None and the caller falls back to whatever
    history requires. `int()` on tier so a row typed `"1"` matches.
    """
    for r in (roles or []):
        try:
            if int(r.get("tier")) == int(tier) and r.get("role") == role:
                return r
        except (TypeError, ValueError):
            continue
    return None


def spec_from_ladder_row(row):
    """Map a ladder `roles:` row to {harness, model, effort, thinking, settings}.

    Blank cells resolve to None (omit the flag). `thinking` is pi's effort
    analogue (`l3w4-director-kids-on-glm`) and travels with the row.
    """
    return {
        "harness": row.get("harness") or None,
        "model": (row.get("model") or "").strip() or None,
        "effort": (row.get("effort") or "").strip() or None,
        "thinking": (row.get("thinking") or "").strip() or None,
        "settings": row.get("settings") or None,
    }


def derived_allowed_models(roles, harness_name, harness):
    """The DERIVED allowlist a harness may spawn from.

    = {every ladder row's model whose `harness` is `harness_name`}
      U harness.allowed_extra    (the migration-clean census)
      U harness.allowed_models   (the DEPRECATED key — still unioned for one
                                 cut-over round so no live spawn fails closed;
                                 the caller warns once that it is legacy).

    A model no ladder row, no `allowed_extra` and no legacy `allowed_models`
    names is refused (fail-closed). The point of the derivation: a NEW model
    written into a ladder row is allowed WITHOUT editing the config's allowlist
    — the four-cells-in-three-files defect (l4 measure).
    """
    extra = {str(m) for m in (harness.get("allowed_extra") or [])
             if m and str(m).strip()}
    legacy = {str(m) for m in (harness.get("allowed_models") or [])
              if m and str(m).strip()}
    from_rows = {str(r.get("model")).strip() for r in (roles or [])
                 if r.get("harness") == harness_name
                 and (r.get("model") or "").strip()}
    return from_rows | extra | legacy


def assert_model_in_provider_namespace(model: str, provider: str) -> None:
    """FAIL CLOSED before any spawn, credential mint or network call.

    An OpenRouter slug always has the shape `provider/name` (optionally
    `~`-prefixed); a Claude Code subscription alias (`sonnet`, `opus`,
    `claude-sonnet-5`, ...) never contains '/'. The two namespaces are
    disjoint, so the crossing is decidable from the string alone.

    **This lives here rather than in one caller because both callers need the
    same answer.** `workflow.py` has had this guard since the incident;
    `dispatch.py` had none, and was safe only because every seat row and every
    `harnesses.pi.models` entry happened to hold a slug -- safe by data, not by
    rule. A seat row pairing `harness: pi` with `model: claude-sonnet-5` is one
    cell edit, and nothing refused it.
    """
    if provider != "openrouter":
        return
    if "/" not in str(model).lstrip("~"):
        raise AdapterError(
            OPENROUTER_ALIAS_ERR.format(model=model, provider=provider))


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
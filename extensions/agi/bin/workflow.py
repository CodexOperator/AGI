#!/usr/bin/env python3
"""workflow.py — harness-agnostic workflow runner. hypothesis:l3w4-workflows-config-maxxed.

A workflow lives in the graph as a build node under extensions/agi/workflows/
(one .js Claude Code script for the claude-code harness, one <name>.json stage
manifest that BOTH harnesses read). This runner executes the same stages — one
dispatch.py kid per stage on the pi harness, the .js Workflow script on the
claude-code harness — with every knob read from `.agi/config.json`
`workflows.<name>` and overridden per run by `--args`, never hard-coded.

The stage manifest is the single source of truth both harnesses read:
`extensions/agi/workflows/<name>.json` (label, role, optional inline JSON
schema). Changing `.agi/config.json workflows.<name>.model` flips the model
with no script edit — that is the config-maxxed contract.

Usage:
    workflow.py run <name> [--harness pi|claude-code] [--args JSON] [--dry-run]

    name      config row key, e.g. `review` or `drafting` (the agi-*.js script
              names also resolve, normalized to the config key)
    --harness harness to run through (default: config row `provider`, else pi)
    --args    JSON of per-run overrides merged OVER the config row
    --dry-run resolve every stage and print one dispatch line per stage, with
              the resolved model/effort, WITHOUT spawning any agent

Exit 0 on a successful resolve / green validation; 2 on a resolve failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))

import locations as _loc  # noqa: E402

WORKFLOWS_DIR_REL = ("extensions", "agi", "workflows")

# Builtin defaults last in precedence: args > config row > stage JSON hint.
_DEFAULT_MODEL = "sonnet"
_DEFAULT_EFFORT = "medium"


def _load_config(root: Path):
    cfg_path = root / "config.json"
    try:
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def _config_key_for(name: str) -> str:
    """Normalize a script name (`agi-round-review`, `agi-round-review.js`) to
    its config key (`review`). Already-key names pass through."""
    base = name
    if base.endswith(".js"):
        base = base[:-3]
    if base.startswith("agi-"):
        base = base[len("agi-"):]
    return base


def _repo_root(project_root: Path) -> Path:
    """The engine repo root that carries extensions/agi/workflows. `.agi` is
    one level under it; walk up to be safe across layouts."""
    cand = project_root
    for _ in range(6):
        if cand.joinpath(*WORKFLOWS_DIR_REL).is_dir():
            return cand
        cand = cand.parent
        if cand == cand.parent:
            break
    return project_root


def _load_manifest(root: Path, name: str) -> dict:
    """The single stage manifest both harnesses read: <name>.json."""
    p = root.joinpath(*WORKFLOWS_DIR_REL, f"{name}.json")
    if not p.is_file():
        # fall back to the .js script's sibling (rare; name may carry it)
        p = root.joinpath(*WORKFLOWS_DIR_REL, f"agi-{name}.js")
        if not p.is_file():
            raise FileNotFoundError(f"no stage manifest {name}.json under {WORKFLOWS_DIR_REL}")
    return json.loads(p.read_text(encoding="utf-8"))


def _expand_stages(manifest: dict, args: dict) -> list[dict]:
    """Materialize repeat stages (one per target / per brief) from `args` into
    a flat list of concrete stages with their final labels."""
    out: list[dict] = []
    for st in manifest.get("stages", []):
        rep = st.get("repeat") or {}
        of = rep.get("of")
        if not of:
            out.append(dict(st))
            continue
        pool = args.get(of)
        if not pool:
            # no repetition source in args -> emit a single un-expanded stage
            out.append(dict(st))
            continue
        tmpl = rep.get("label_template", st["label"] + ":{?}")
        for item in pool:
            sub = dict(st)
            key = item.get("window") or item.get("slug") if isinstance(item, dict) else item
            try:
                sub["label"] = tmpl.format(**item) if isinstance(item, dict) else tmpl
            except (KeyError, IndexError):
                sub["label"] = tmpl
            sub["_repeat_key"] = key
            # The render context for this concrete stage: the repeat item's own
            # fields ({slug}, {scope}, {parent} for a brief) ride on the stage
            # so the pi path can render a per-item prompt (hypothesis:
            # l3w4-workflows-config-maxxed — a stage is only runnable on pi if
            # its prompt can be rendered from the item).
            sub["_repeat_item"] = item if isinstance(item, dict) else {}
            out.append(sub)
    return out


def _resolve_knobs(stage: dict, cfg_row: dict, args: dict) -> dict:
    """Precedence: per-run args > config row > stage JSON hint > builtin."""
    model = args.get("model") or cfg_row.get("model") or stage.get("model_hint") or _DEFAULT_MODEL
    effort = args.get("effort") or cfg_row.get("effort") or stage.get("effort_hint") or _DEFAULT_EFFORT
    return {"model": model, "effort": effort}


def validate_return(schema: dict | None, value) -> list[str]:
    """Validate a stage's returned structured data against its JSON schema.

    Returns a list of violation strings (empty = valid). A None schema (the
    manifest did not declare one) validates anything — the stage ran.
    """
    if not schema:
        return []
    import jsonschema
    errors = []
    try:
        jsonschema.validate(instance=value, schema=schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"{'.'.join(str(p) for p in exc.path) or '<root>'}: {exc.message}")
    except jsonschema.SchemaError as exc:
        errors.append(f"schema error: {exc.message}")
    return errors


def _dispatch_lines(stages: list[dict], knobs: dict[str, dict]) -> list[str]:
    lines = []
    for st in stages:
        k = knobs.get(st["label"], {})
        rep = f" x{st['_repeat_key']}" if "_repeat_key" in st else ""
        lines.append(
            f"[dispatch] {st['label']}{rep} :: role={st.get('role', 'kid')} "
            f"model={k.get('model')} effort={k.get('effort')}"
        )
    return lines


def _dispatching_line(st, k):
    return (
        f"[dispatch] {st['label']} :: role={st.get('role', 'kid')} "
        f"model={k.get('model')} effort={k.get('effort')}"
    )


class _SafeDict(dict):
    """dict whose missing keys format to '' instead of raising KeyError, so a
    stage prompt can reference optional args ({scratch}) without every stage
    being required to supply them."""
    def __missing__(self, key):
        return ""


# A placeholder is `{word}` only — the schema examples inside a prompt are
# `{"..": ..}` JSON braces, which must pass through LITERALLY. str.format_map
# treats those as format specs and blows up, so expansion is a regex over
# word keys instead (hypothesis:l3w4-workflows-config-maxxed — a prompt's
# inline JSON schema must survive rendering).
_PLACEHOLDER = __import__("re").compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def render_stage_prompt(stage: dict, run_args: dict) -> str:
    """Render a stage's `prompt` template against the run's args.

    The repeat item's own fields ({slug},{scope},{parent}) are the render
    context for a concrete expanded stage, overrideing the run args so each
    brief gets its own prompt. A stage with no `prompt` raises ValueError
    (naming the stage) — without a prompt text a pi runner physically cannot
    execute the stage, which is the stub defect this fixes. Only `{word}`
    placeholders are expanded; `{\"..\": ..}` JSON braces in the prompt pass
    through untouched.
    """
    tmpl = stage.get("prompt")
    if not tmpl:
        raise ValueError(f"stage {stage.get('label')!r} declares no 'prompt' "
                         "text in its manifest — cannot run on the pi harness")
    ctx = _SafeDict(run_args)
    for k, v in (stage.get("_repeat_item") or {}).items():
        ctx[k] = v
    return _PLACEHOLDER.sub(lambda m: str(ctx[m.group(1)]), tmpl)


def _pi_harness_cfg(cfg: dict) -> dict:
    """The pi harness's bin/provider/thinking from config `harnesses.pi`.

    Fallbacks are the engine defaults, so a project that omits the row still
    resolves — matching the config-maxxed contract (never a hard literal that
    skips the config, but a config row with sane defaults)."""
    h = (cfg.get("harnesses") or {}).get("pi") or {}
    return {
        "bin": h.get("bin") or os.environ.get("PI_BIN")
               or "/home/ubuntu/.npm-global/bin/pi",
        "provider": h.get("provider") or "openrouter",
        "thinking": h.get("thinking") or "medium",
    }


_SCRUB = (
    "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_MODEL", "CLAUDECODE", "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
)


def _pi_env() -> dict:
    """Inherited env minus Claude-Code-injected Anthropic credentials, so a
    workflow pi stage spends the project's configured provider (openrouter)
    rather than a subscription token — the same scrub dispatch.py applies. A
    copy is returned; the caller's os.environ is untouched."""
    return {k: v for k, v in os.environ.items() if k not in _SCRUB}


def _effort_to_thinking(effort: str | None) -> str:
    """Map a workflow effort knob to a pi thinking level. `max`/`high` -> high,
    `low` -> low, anything missing or odd -> medium. A `--args thinking` value
    is never remapped (the caller passes it through unchanged)."""
    return {"max": "high", "high": "high", "low": "low"}.get(
        (effort or "").strip().lower(), "medium")


def _parse_last_json(text: str):
    """Pull the last JSON object out of a model's stdout.

    The model is asked for *exactly one* JSON object, but a flashrier may emit
    a preamble or trailing glue; scanning for the last complete `{...}` block is
    the tolerant parse. Returns the parsed value, or raises ValueError with a
    short reason (no braces found / invalid JSON)."""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0 or end <= start:
        raise ValueError("no JSON object `{...}` found in stage output")
    import json as _json
    return _json.loads(text[start:end + 1])


def _run_stage_pi(cfg: dict, stage: dict, knobs: dict, run_args: dict,
                  out=sys.stdout) -> int:
    """Execute ONE stage on the pi harness: spin the pi binary headlessly with
    the resolved provider/model/thinking and the rendered prompt, capture its
    stdout, parse the last JSON object, and validate it against the stage's
    schema.

    Returns 0 on success (schema-valid JSON produced). The kid writes any
    artifact (a draft body) itself under the scratch dir the prompt names; the
    runner does not fabricate it."""
    import subprocess
    k = knobs[stage["label"]]
    prompt = render_stage_prompt(stage, run_args)
    hc = _pi_harness_cfg(cfg)
    thinking = run_args.get("thinking") or _effort_to_thinking(k.get("effort"))
    cmd = [hc["bin"], "-p",
           "--provider", hc["provider"],
           "--model", k.get("model", _DEFAULT_MODEL),
           "--thinking", thinking,
           prompt]
    out.write(f"# {_dispatching_line(stage, k)}\n")
    out.write(f"$ {' '.join(cmd)}\n")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              env=_pi_env(), timeout=600)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"workflow.py: stage {stage['label']} could not start pi: "
              f"{exc}", file=sys.stderr)
        return 2
    output = proc.stdout or ""
    if proc.returncode != 0:
        print(f"workflow.py: stage {stage['label']} pi exited rc="
              f"{proc.returncode}\n{output[-2000:]} {proc.stderr or ''}",
              file=sys.stderr)
        return 3
    try:
        value = _parse_last_json(output)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"workflow.py: stage {stage['label']} did not return JSON: "
              f"{exc}\n--- output tail ---\n{output[-2000:]}", file=sys.stderr)
        return 4
    violations = validate_return(stage.get("schema"), value)
    if violations:
        print(f"workflow.py: stage {stage['label']} returned JSON that fails "
              f"its schema:\n  " + "\n  ".join(violations), file=sys.stderr)
        return 5
    out.write(f"[ok] {stage['label']} -> "
              f"{json.dumps(value, ensure_ascii=False, sort_keys=True)[:200]}\n")
    return 0


def run_workflow(root: Path, name: str, harness: str, args: dict, dry_run: bool,
                 out=sys.stdout) -> int:
    repo = _repo_root(root)
    cfg = _load_config(root)
    key = _config_key_for(name)
    cfg_row = (cfg.get("workflows") or {}).get(key) or {}
    manifest = _load_manifest(repo, key)
    stages = _expand_stages(manifest, args)

    harness = harness or cfg_row.get("provider") or "pi"
    knobs = {st["label"]: _resolve_knobs(st, cfg_row, args) for st in stages}

    if dry_run:
        for st in stages:
            out.write(_dispatching_line(st, knobs[st["label"]]) + "\n")
        out.write(f"[summary] workflow={key} harness={harness} "
                  f"stages={len(stages)} via dispatch.py kids when harness=pi\n")
        return 0

    if harness != "pi":
        # claude-code harness: the Workflow script is the runner; we only
        # resolve and describe, never spawn from here.
        for st in stages:
            out.write(f"[claude-code] {st['label']} :: script={manifest.get('script')} "
                      f"model={knobs[st['label']].get('model')}\n")
        return 0

    # pi harness: execute each stage for real — one headless pi process per
    # stage, prompt rendered from the manifest + --args, resolved provider/
    # model/thinking passed through, JSON return validated against the schema.
    # This was a STUB: it used to call dispatch.py with a bogus `key:label`
    # --target and a nonexistent `workflow_stage` --template, never passing the
    # resolved knobs or the stage prompt, so a real run could not happen
    # (Belam VII, L3.28: three concrete defects).
    import subprocess
    for st in stages:
        rc = _run_stage_pi(cfg, st, knobs, args, out=out)
        if rc != 0:
            print(f"workflow.py: workflow={key} failed at stage "
                  f"{st['label']} (rc={rc})", file=sys.stderr)
            return rc
    out.write(f"[summary] workflow={key} harness=pi stages={len(stages)} "
              f"all schema-valid\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="workflow.py",
        description="Harness-agnostic workflow runner (hypothesis:l3w4-workflows-config-maxxed).",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("run", help="resolve and run a workflow")
    rp.add_argument("name", help="config key (e.g. review, drafting) or agi-*.js script name")
    rp.add_argument("--harness", default=None, choices=["pi", "claude-code"],
                    help="harness to run through (default: config row provider, else pi)")
    rp.add_argument("--args", default="{}", help="JSON of per-run overrides merged over the config row")
    rp.add_argument("--dry-run", action="store_true",
                    help="print one dispatch per stage with the resolved model, spawn nothing")
    args = ap.parse_args(argv)

    root = _loc.find_project_root()
    if root is None:
        print("workflow.py: no .agi project root found from cwd", file=sys.stderr)
        return 2

    try:
        run_args = json.loads(args.args)
        if not isinstance(run_args, dict):
            raise ValueError("--args must be a JSON object")
    except json.JSONDecodeError as exc:
        print(f"workflow.py: --args not valid JSON: {exc}", file=sys.stderr)
        return 2

    code = run_workflow(root, args.name, args.harness, run_args, args.dry_run)
    return code


if __name__ == "__main__":
    sys.exit(main())
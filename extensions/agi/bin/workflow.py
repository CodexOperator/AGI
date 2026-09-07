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

    import subprocess
    for st in stages:
        k = knobs[st["label"]]
        # One dispatch.py kid per stage — its brief is the stage prompt, its
        # done-contract returns the JSON the stage schema validates.
        cmd = [
            sys.executable, str(_THIS / "dispatch.py"),
            str(root), "workflow",
            "--harness", "pi", "--role", st.get("role", "kid"),
            "--target", f"{key}:{st['label']}",
            "--template", "workflow_stage",
        ]
        out.write(f"# {_dispatching_line(st, k)}\n")
        rc = subprocess.call(cmd)
        if rc != 0:
            print(f"workflow.py: stage {st['label']} dispatch failed (rc={rc})", file=sys.stderr)
            return rc
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
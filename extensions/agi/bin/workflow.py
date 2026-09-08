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
    workflow.py register <name> --script <path> [--from-run <dir>]
    workflow.py list
    workflow.py validate

    run       the ONLY sanctioned dispatch route; `review` and `drafting` are
              registered manifest pairs
    register  land an inline script as a manifest pair as it runs, deriving
              the stage manifest from the script (refuses to overwrite)
    list      enumerate the registry: script, stage count, default harness
    validate  the registry invariant: every agi-*.js has a sibling *.json and
              every manifest names only stages the script implements

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
import re
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


def _script_stage_labels(script_text: str) -> set[str]:
    """Base stage labels a Claude Code workflow script implements.

    Pulled from `label:` args (both quoted `'critic'` and backtick-template
    `` `draft:${b.slug}` ``) and `phase('Title')` calls. A template label's
    trailing ':' is stripped (`draft:` -> `draft`). This is the source of
    truth for the unified-route invariant: a manifest may name only stages
    the script implements (hypothesis:l3-workflows-unified-route).
    """
    labels: set[str] = set()
    for m in re.finditer(r"""label:\s*['"`]([^'"`$]*)""", script_text):
        base = m.group(1).strip().rstrip(":")
        if base:
            labels.add(base)
    for m in re.finditer(r"""phase\(\s*['"`]([^'"`]+)""", script_text):
        labels.add(m.group(1).strip())
    return labels


def _derive_stages(script_text: str) -> list[dict]:
    """Derive a stage manifest from a Claude Code workflow script body.

    Each distinct base `label:` becomes one stage entry in first-seen order
    (label args are the real stage machinery — `phase()` only groups display,
    so it is NOT a source of stages). A backtick template label
    (`` `draft:${b.slug}` ``) is a repeat stage: its `repeat.label_template`
    is normalized to a `{word}` placeholder and `repeat.of` is left an honest
    TODO (the --args list key lives in the run, not the script). `prompt` and
    `schema` are marked TODO rather than invented — a pi runner needs real
    prompt text and fabricating one would be the exact dishonest-registry
    failure this closes.
    """
    entries: list[tuple[str, bool, str | None]] = []
    seen: set[str] = set()

    def _add(base: str, is_repeat: bool, label_template: str | None):
        if base and base not in seen:
            seen.add(base)
            entries.append((base, is_repeat, label_template))

    for m in re.finditer(r"""label:\s*`([^`]*)`""", script_text):
        raw = m.group(1).strip()
        base, sep, _tail = raw.partition(":")
        base = base.strip()
        var = "item"
        vtm = re.search(r"\$\{([^}]+)\}", raw)
        if vtm:
            var = vtm.group(1).split(".")[-1].strip() or "item"
        tpl = f"{base}:{{{var}}}" if (sep and base) else "{%s}" % var
        _add(base, True, tpl)
    for m in re.finditer(r"""label:\s*['"]([^'"]*)['"]""", script_text):
        _add(m.group(1).strip(), False, None)

    stages = []
    for base, is_repeat, label_template in entries:
        stage = {
            "label": base,
            "role": "kid",
            "prompt": f"<TODO: author the stage prompt for stage "
                       f"'{base}' from the script's agent brief>",
        }
        if is_repeat:
            stage["repeat"] = {
                "of": "<TODO: the --args list key, e.g. briefs or targets>",
                "label_template": label_template,
            }
        stages.append(stage)
    return stages


def register_workflow(root: Path, name: str, script: Path,
                      from_dir: Path | None = None, out=sys.stdout) -> int:
    """Land an inline script as a proper manifest pair under workflows/.

    Copies the script to `agi-<key>.js` and derives `<key>.json` from it. A
    key is already registered when EITHER file exists — this verb refuses to
    silently overwrite, because an overwritten manifest is a registered
    workflow whose stage list no longer names what its script implements.
    Returns 0 on a fresh registration; 2 on refusal or an underivable script.
    """
    repo = _repo_root(root)
    wf = repo.joinpath(*WORKFLOWS_DIR_REL)
    key = _config_key_for(name).strip()
    if not key:
        print("workflow.py: register needs a non-empty name", file=sys.stderr)
        return 2
    js_target = wf / f"agi-{key}.js"
    manifest_target = wf / f"{key}.json"
    if js_target.exists() or manifest_target.exists():
        existing = js_target if js_target.exists() else manifest_target
        print(f"workflow.py: register refused: '{key}' already registered at "
              f"{existing.name} — refusing to silently overwrite. Inspect "
              f"with `workflow.py list` first.", file=sys.stderr)
        return 2
    try:
        script_text = Path(script).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"workflow.py: register: cannot read --script {script}: "
              f"{exc}", file=sys.stderr)
        return 2
    stages = _derive_stages(script_text)
    if not stages:
        print(f"workflow.py: register: no stage labels found in {script} — "
              "cannot derive a manifest; refusing to land a prompt-less pair.",
              file=sys.stderr)
        return 2
    manifest = {
        "name": key,
        "script": js_target.name,
        "description": (f"Registered from inline script {Path(script).name}"
                         + (f" (originally run from {from_dir})" if from_dir else "")
                         + " — stages derived from the script, prompts TODO"),
        "stages": stages,
    }
    if from_dir:
        manifest["_from_run"] = str(from_dir)
    js_target.write_text(script_text, encoding="utf-8")
    manifest_target.write_text(json.dumps(manifest, indent=2) + chr(10),
                               encoding="utf-8")
    out.write(f"[registered] {key} -> {js_target.name} + {key}.json "
              f"({len(stages)} stage(s) derived)\n")
    return 0


def list_workflows(root: Path, out=sys.stdout) -> int:
    """Enumerate the registry: every agi-*.js with its manifest name (the
    config row key), stage count, and the harness the config row defaults to.
    The script<->manifest link resolves through the manifest's `script` field
    (review.json -> agi-round-review.js), never a filename heuristic."""
    repo = _repo_root(root)
    wf = repo.joinpath(*WORKFLOWS_DIR_REL)
    cfg = _load_config(root)
    by_script: dict[str, dict] = {}
    for mf in wf.glob("*.json"):
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            m = {}
        if m.get("script"):
            by_script[m["script"]] = m
    js_files = sorted(wf.glob("agi-*.js"))
    if not js_files:
        out.write("(no workflows registered)\n")
        return 0
    rows = []
    for js in js_files:
        manifest = by_script.get(js.name)
        key = (manifest or {}).get("name")
        stage_count = len((manifest or {}).get("stages", []))
        row_cfg = (cfg.get("workflows") or {}).get(key) or {}
        harness = row_cfg.get("provider") or (manifest or {}).get("provider") \
            or "pi"
        rows.append((key or js.name, js.name, stage_count, harness, manifest))
    width = max(len(r[0]) for r in rows)
    out.write(f"{'NAME':<{width}} SCRIPT                 STAGES  HARNESS\n")
    for key, script, n, h, manifest in rows:
        flag = "" if manifest else "  <-- NO MANIFEST!"
        out.write(f"{key:<{width}} {script:<20} {n:<6} {h}{flag}\n")
    return 0


def validate_registry(root: Path, wf: Path | None = None,
                      out=sys.stdout) -> int:
    """The unified-route invariant, both directions.

    1. Every `agi-*.js` under workflows/ is named as the `script` of some
       `<name>.json` manifest (a script with no sibling manifest is the
       un-registered inline case).
    2. Every manifest's `script` field names an existing `agi-*.js`, and it
       names only stages that script implements.

    Returns 0 when sound; 1 when any violation is found (each printed). A
    workflows dir can be passed directly so the invariant is testable in
    isolation from the live repo (deep-search is mid-build there).
    """
    repo = _repo_root(root)
    wf = wf or repo.joinpath(*WORKFLOWS_DIR_REL)
    violations: list[str] = []
    manifests: dict[str, dict] = {}
    for mf in sorted(wf.glob("*.json")):
        try:
            manifests[mf.stem] = json.loads(mf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"{mf.name} is not valid JSON: {exc}")
    referenced = {m.get("script") for m in manifests.values() if m.get("script")}
    for js in sorted(wf.glob("agi-*.js")):
        if js.name not in referenced:
            violations.append(f"{js.name} has no manifest naming it as its "
                              "script (no sibling <name>.json)")
    for mf_name in sorted(manifests):
        manifest = manifests[mf_name]
        mf = wf / f"{mf_name}.json"
        script_name = manifest.get("script")
        js = wf / script_name if script_name else None
        if not script_name or not js or not js.is_file():
            violations.append(f"{mf.name} names script "
                              f"{script_name or '(none)'} which does not exist")
            continue
        script_labels = _script_stage_labels(js.read_text(encoding="utf-8"))
        for st in manifest.get("stages", []):
            base = (st.get("label") or "").split(":")[0].strip()
            if base and base not in script_labels:
                violations.append(
                    f"{mf.name} stage '{base}' is not implemented by {js.name} "
                    f"(script implements: {sorted(script_labels) or 'none'})")
    for v in violations:
        out.write(f"[registry] {v}\n")
    if violations:
        out.write(f"[registry] {len(violations)} violation(s)\n")
        return 1
    out.write("[registry] sound: every agi-*.js is named by a sibling manifest "
              "and every manifest stage is implemented by its script\n")
    return 0


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
        description="Harness-agnostic workflow runner (hypothesis:l3-workflows-unified-route).",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("run", help="resolve and run a workflow (the only sanctioned dispatch route)")
    rp.add_argument("name", help="config key (e.g. review, drafting) or agi-*.js script name")
    rp.add_argument("--harness", default=None, choices=["pi", "claude-code"],
                    help="harness to run through (default: config row provider, else pi)")
    rp.add_argument("--args", default="{}", help="JSON of per-run overrides merged over the config row")
    rp.add_argument("--dry-run", action="store_true",
                    help="print one dispatch per stage with the resolved model, spawn nothing")
    reg = sub.add_parser("register",
                         help="land an inline script as a manifest pair (hypothesis:l3-workflows-unified-route)")
    reg.add_argument("name", help="workflow key to register (e.g. draft-briefs)")
    reg.add_argument("--script", required=True,
                     help="path to the inline Claude Code .js script")
    reg.add_argument("--from-run", default=None,
                     help="run dir the script originally lived in (provenance note)")
    lst = sub.add_parser("list", help="enumerate the registered workflows")
    val = sub.add_parser("validate",
                         help="check the registry invariant: agi-*.js <-> sibling <name>.json, and only implemented stages")
    args = ap.parse_args(argv)

    root = _loc.find_project_root()
    if root is None:
        print("workflow.py: no .agi project root found from cwd", file=sys.stderr)
        return 2

    if args.cmd == "register":
        return register_workflow(root, args.name, Path(args.script),
                                 Path(args.from_run) if args.from_run else None)
    if args.cmd == "list":
        return list_workflows(root)
    if args.cmd == "validate":
        return validate_registry(root)

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
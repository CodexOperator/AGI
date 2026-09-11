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
from datetime import datetime, timezone
from pathlib import Path

import yaml


_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))

import adapters  # noqa: E402  -- owns the model/provider namespace guard,
# and the shared (tier, role, harness) ladder resolver (l4-one-write)
import spawn_gate  # noqa: E402  -- reads ladder roles for the same resolver
import locations as _loc  # noqa: E402

WORKFLOWS_DIR_REL = ("extensions", "agi", "workflows")

# The geometry node that OWNS workflow-harness resolution (hypothesis:
# l4-workflow-types-and-default-harness-are-a-geometry-node). Like crons.md /
# seats.md / ladder.md, it is a `config` node in `.geometry/` whose
# edit-and-commit IS the change — the prime owns `default_harness`, and an
# override is a commit, never a code edit. Relative to the project root
# `find_project_root` resolves (the `.agi` dir).
GEO_WORKFLOWS_REL = ("nodes", ".geometry", "workflows.md")

# Builtin defaults last in precedence: args > config row > stage JSON hint.
# NO _DEFAULT_MODEL. hypothesis:l3-workflow-model-crosses-harness-namespace —
# a silent fallback model is exactly how a Claude Code subscription alias
# ("sonnet") reached an OpenRouter --model flag and billed Anthropic Sonnet at
# 33x this project's declared price. A model must be named by config, args or
# stage hint, or the run refuses; nothing is chosen for the caller.
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


# ---- descriptive per-run KEY minting (hypothesis:l4-a-workflow-run-is- ---
# named-not-numbered) -----------------------------------------------------
# A run is cited by a key DERIVED from its workflow type + run args, easy to
# type — not by the opaque harness-minted id. The claim's three shapes:
#   merge-up-review over rounds [39]    -> mur-39
#   merge-up-review over rounds [SL1#2] -> mur-sl1-2
#   author / validate (no run args)     -> their own whole name
# A single-word workflow key is already short and keeps its whole name; a
# multi-word key abbreviates to the initials of its hyphen-separated words.


def _slugify_token(value: object) -> str:
    """`SL1#2` -> `sl1-2`, `39` -> `39` — lowercased, runs of non-alnum to
    ONE `-`, collapsed. Empty when nothing alnum survives."""
    s = re.sub(r"[^0-9a-zA-Z]+", "-", str(value).lower())
    return re.sub(r"-+", "-", s).strip("-")


def _run_key_abbrev(key: str) -> str:
    """`merge-up-review` -> `mur` (initials of the hyphen-separated words); a
    single-word key (`author`, `validate`, `review`, `drafting`) is already
    descriptive and keeps its whole name."""
    words = [w for w in key.split("-") if w]
    if len(words) > 1:
        abbr = "".join(w[0] for w in words if w[0].isalnum())
        return abbr or key
    return words[0] if words else key


def _run_arg_tokens(args: dict) -> list[str]:
    """Scalar / list-of-scalar arg values, deterministically ordered by key,
    each slugged. Nested dicts (e.g. `targets:[{window...}]`) contribute
    nothing — the run key names the WORKFLOW plus its simple knobs, not the
    per-target rows inside an arg."""
    tokens: list[str] = []
    for k in sorted(args or {}):
        v = args[k]
        if isinstance(v, (dict, bool)) or v is None:
            continue
        if isinstance(v, (list, tuple)):
            for item in v:
                if isinstance(item, (dict, bool)) or item is None:
                    continue
                tokens.append(str(item))
        else:
            tokens.append(str(v))
    return [t for t in (_slugify_token(x) for x in tokens) if t]


def _existing_run_keys(root: Path, key: str) -> set[str]:
    """The run_key values already tracked for this workflow key, so a re-run
    de-collides deterministically (`mur-39`, `mur-39-2`, `mur-39-3`, ...).
    Best-effort: any read failure yields the empty set — a collision suffix
    is a nicety, never a gate."""
    try:
        sess = _loc.shared_project_root(root) or root
        path = Path(sess) / "sessions" / "workflows" / f"{key}.jsonl"
        if not path.is_file():
            return set()
        keys: set[str] = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("run_key"):
                keys.add(row["run_key"])
        return keys
    except Exception:
        return set()


def _mint_run_key(root: Path, key: str, args: dict) -> str:
    """The descriptive run key for this run: workflow-type abbreviation joined
    to the slugged run args, de-collided against the rows already tracked for
    this workflow."""
    base = _run_key_abbrev(key)
    toks = _run_arg_tokens(args)
    if toks:
        base = f"{base}-" + "-".join(toks)
    used = _existing_run_keys(root, key)
    candidate, i = base, 2
    while candidate in used:
        candidate = f"{base}-{i}"
        i += 1
    return candidate


class WorkflowsNodeError(Exception):
    """The geometry node that owns workflow-harness resolution is absent or
    malformed. workflow.py REFUSES loudly, naming the node, rather than
    falling back to a code literal — a hardcoded default harness is exactly
    the fallback hypothesis:l4-workflow-types-and-default-harness-are-a-
    geometry-node orders gone."""


def _geometry_node_path(project_root: Path) -> Path:
    """The `.geometry/workflows.md` path under the graph root. `project_root`
    here is what `find_project_root` returns (the `.agi` dir), so the node
    lives at `<.agi>/nodes/.geometry/workflows.md`, the same layout crons.md
    (goal:g10.2) and seats.md already use."""
    return Path(project_root).joinpath(*GEO_WORKFLOWS_REL)


def _load_geometry_node(project_root: Path) -> dict:
    """Parse and validate `nodes/.geometry/workflows.md` — the shape crons.py
    already reads `nodes/.geometry/crons.md` with (yaml.safe_load over the
    frontmatter between the leading `---` markers). Every failure raises
    `WorkflowsNodeError` naming the file.

    Returns `{"default_harness": str, "types": {name: row},
    "workflows": {name: row}}`. A `types` row `{name, harness, stage_shapes}`
    declares a workflow TYPE and the harness that type overrides to.
    `workflows.<name>` maps a registered workflow to its `type` and may carry
    its own `harness` override."""
    path = _geometry_node_path(project_root)
    if not path.is_file():
        raise WorkflowsNodeError(
            f"missing node file {path} — the workflow-harness resolution node. "
            "It is a `config` node a kid cannot `write.py create`; the prime "
            "owns it. Until it lands, workflow.py refuses to guess a harness "
            "(no hardcoded default)")
    text = path.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        raise WorkflowsNodeError(
            f"{path}: no YAML frontmatter (expected a leading `---`)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise WorkflowsNodeError(
            f"{path}: unterminated frontmatter block (only one `---`)")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise WorkflowsNodeError(
            f"{path}: malformed YAML frontmatter — {exc}") from exc
    if not isinstance(fm, dict):
        raise WorkflowsNodeError(
            f"{path}: frontmatter must be a YAML mapping")
    default_harness = fm.get("default_harness")
    if not default_harness or not isinstance(default_harness, str):
        raise WorkflowsNodeError(
            f"{path}: missing/empty `default_harness` (str) — the prime-owned "
            "default harness")
    types: dict = {}
    for row in fm.get("types") or []:
        if not isinstance(row, dict) or not row.get("name"):
            raise WorkflowsNodeError(
                f"{path}: every `types` row needs a `name`")
        h = row.get("harness")
        if h and not isinstance(h, str):
            raise WorkflowsNodeError(
                f"{path}: types.{row['name']}.harness must be a str")
        types[row["name"]] = row
    workflows: dict = {}
    for row in fm.get("workflows") or []:
        if not isinstance(row, dict) or not row.get("name"):
            raise WorkflowsNodeError(
                f"{path}: every `workflows` row needs a `name`")
        typ = row.get("type")
        if typ and typ not in types:
            raise WorkflowsNodeError(
                f"{path}: workflows.{row['name']}.type '{typ}' names an "
                f"undeclared type (declared: {sorted(types)})")
        workflows[row["name"]] = row
    return {"default_harness": default_harness, "types": types,
            "workflows": workflows}


def _maybe_geometry_node(project_root: Path) -> dict | None:
    """The geometry node, or None when it is absent (pre-prime). A MALFORMED
    node still raises — absent is a state, malformed is a bug."""
    if not _geometry_node_path(project_root).is_file():
        return None
    return _load_geometry_node(project_root)


def _resolve_default_harness(project_root: Path, key: str, manifest: dict,
                             cfg_row: dict) -> tuple[str, str]:
    """Resolve a workflow's harness when no explicit `--harness` was passed.

    Resolution order (hypothesis:l4-workflow-types-and-default-harness-are-a-
    geometry-node): per-workflow override > per-type override > prime default >
    refuse loudly naming the node. The old code stopped after ONE override
    level (cfg row provider, else manifest provider) and then fell back to the
    literal `'pi'` — this replaces that literal with the geometry node, so the
    prime's `default_harness` and the per-type/per-workflow overrides are
    commits, not code. Returns `(harness, level)`."""
    # LEVEL 1 — the workflow's own override (still per-workflow facts, kept
    # here so config rows and manifest providers keep working unchanged).
    cfg_prov = (cfg_row or {}).get("provider")
    if cfg_prov:
        return cfg_prov, "config row"
    man_prov = (manifest or {}).get("provider")
    if man_prov:
        return man_prov, "manifest"
    node = _load_geometry_node(project_root)
    wov = (node.get("workflows") or {}).get(key)
    if isinstance(wov, dict) and wov.get("harness"):
        return wov["harness"], "per-workflow"
    # LEVEL 2 — the workflow's TYPE override.
    typ = (manifest or {}).get("type")
    if typ:
        if typ not in (node.get("types") or {}):
            raise WorkflowsNodeError(
                f"{_geometry_node_path(project_root)}: workflow '{key}' "
                f"declares type '{typ}' which is not in the node's `types` "
                f"(declared: {sorted(node.get('types') or {})})")
        th = (node["types"][typ].get("harness")) or None
        if th:
            return th, f"type:{typ}"
    # LEVEL 3 — the prime default. NO hardcoded fallback after this.
    if node.get("default_harness"):
        return node["default_harness"], "prime default"
    raise WorkflowsNodeError(
        f"{_geometry_node_path(project_root)}: no per-workflow override, no "
        f"per-type harness and no default_harness — cannot resolve a harness "
        f"for '{key}' and workflow.py never invents one")


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
    """Retired as a landing path for runnable pairs (hypothesis:
    l4-workflow-authoring-is-a-harness-tool): deriving a stage manifest from
    an inline script's labels can only fabricate `prompts`, which validate
    now rejects as `<TODO>` non-runnable skeletons — a pair that lists as
    registered but CANNOT run is the dishonest-registry failure this closes.
    The verb lives on, but as a REFUSAL that names the replacement
    (`workflow.py author`), so no new prompt-less pair can be landed. Still
    refuses to silently overwrite an existing pair. Returns 2 always."""
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
    print("workflow.py: register refused: deriving a stage manifest from an "
          "inline script only fabricates `prompts`, which validate now rejects "
          "as <TODO> non-runnable skeletons. Author a REAL runnable pair "
          "instead: `workflow.py author <key> --stages <json-or-path>` ",
          file=sys.stderr)
    return 2


def list_workflows(root: Path, out=sys.stdout) -> int:
    """Enumerate the registry: every agi-*.js with its manifest name (the
    config row key), stage count, and the RESOLVED harness each workflow
    defaults to WITH the resolution LEVEL it came from (hypothesis:
    l4-workflow-types-and-default-harness-are-a-geometry-node). The script
    <->manifest link resolves through the manifest's `script` field
    (review.json -> agi-round-review.js), never a filename heuristic. The
    harness is never a code literal — a workflow with nothing declaring its
    harness makes list refuse, naming the node."""
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
        # resolver, never a literal: per-workflow > per-type > prime default >
        # refuse naming the node (WorkflowsNodeError propagates: list exits 2).
        harness, level = _resolve_default_harness(root, key, manifest, row_cfg)
        rows.append((key or js.name, js.name, stage_count, harness, level,
                     manifest))
    width = max(len(r[0]) for r in rows)
    out.write(f"{'NAME':<{width}} SCRIPT                 STAGES  HARNESS       LEVEL\n")
    for key, script, n, h, level, manifest in rows:
        flag = "" if manifest else "  <-- NO MANIFEST!"
        out.write(f"{key:<{width}} {script:<20} {n:<6} {h:<13}{level}{flag}\n")
    return 0


def status_workflow(root: Path, key: str | None = None,
                    out=sys.stdout) -> int:
    """Resolve recent workflow runs by key (hypothesis:l4-a-workflow-run-is-
    named-not-numbered). Rows live at `.agi/sessions/workflows/<workflow>.jsonl`
    and each carries its descriptive `run_key`, so a user can cite `mur-39`
    and status finds the row(s) that key names. With no key it lists every
    tracked run, newest first; with a key it filters to the run_key (or its
    owning workflow key). Returns 1 if a key matched nothing, 0 otherwise."""
    try:
        sess = _loc.shared_project_root(root) or root
    except Exception:
        sess = root
    wf_dir = Path(sess) / "sessions" / "workflows"
    if not wf_dir.is_dir():
        out.write("(no workflow runs tracked yet)\n")
        return 0
    rows: list[dict] = []
    for f in sorted(wf_dir.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("run_key") or row.get("workflow"):
                rows.append(row)
    rows.sort(key=lambda r: str(r.get("timestamp", "")), reverse=True)
    if key:
        rows = [r for r in rows
                if key in (str(r.get("run_key") or ""),
                           str(r.get("workflow") or ""))]
    if key and not rows:
        out.write(f"(no runs match key {key!r})\n")
        return 1
    if not rows:
        out.write("(no workflow runs tracked yet)\n")
        return 0
    for r in rows:
        out.write(f"{r.get('run_key') or r.get('workflow')}  "
                  f"workflow={r.get('workflow')} harness={r.get('harness')} "
                  f"{str(r.get('timestamp') or '')} "
                  f"ok={r.get('ok')} failed={r.get('failed')}\n")
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
        # type must name a DECLARED type in the geometry node (hypothesis:
        # l4-workflow-types-and-default-harness-are-a-geometry-node). Enforced
        # only when the node exists — pre-prime (absent node) is a state, and
        # the base invariant still stands alone for isolated workflows dirs.
        gee = _maybe_geometry_node(root)
        if gee is None:
            if manifest.get("type"):
                violations.append(
                    f"{mf.name} declares type {manifest['type']!r} but the "
                    f"geometry node {_geometry_node_path(root)} is absent — "
                    f"cannot verify it resolves (a kid cannot write it; the "
                    f"prime owns it)")
        else:
            declared = set(gee.get("types") or {})
            typ = manifest.get("type")
            if not typ:
                violations.append(
                    f"{mf.name} declares no `type` — every registered manifest "
                    f"must name a declared type ({sorted(declared)})")
            elif typ not in declared:
                violations.append(
                    f"{mf.name} type {typ!r} is not a declared type in "
                    f"{_geometry_node_path(root)} ({sorted(declared)})")
        for st in manifest.get("stages", []):
            base = (st.get("label") or "").split(":")[0].strip()
            if base and base not in script_labels:
                violations.append(
                    f"{mf.name} stage '{base}' is not implemented by {js.name} "
                    f"(script implements: {sorted(script_labels) or 'none'})")
            prompt = st.get("prompt") or ""
            if "<TODO" in prompt:
                # Strictly stronger than the base invariant, per hypothesis:
                # l4-workflow-authoring-is-a-harness-tool. A manifest carrying
                # a <TODO> prompt is a NON-RUNNABLE SKELETON that lists as
                # registered — the dishonest pair the hypothesis exists to
                # close. validate is what makes the disproved-by checkable by
                # the registry itself. The authoring fix: `workflow.py author`.
                violations.append(
                    f"{mf.name} stage '{base or '(unnamed)'}' carries a <TODO> "
                    f"prompt placeholder — a non-runnable skeleton; author a "
                    f"real prompt with `workflow.py author`")
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
            sub["_base_label"] = st["label"]
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
    """Precedence: per-run args > config row > stage JSON hint. No builtin
    model default (hypothesis:l3-workflow-model-crosses-harness-namespace) —
    a stage with nothing to say raises rather than spending on a name nobody
    chose. Callers on the pi harness overwrite this model with
    `_resolve_pi_model` before it is ever used, since `workflows.NAME.model`
    is shared with claude-code and its namespace is disjoint from
    OpenRouter's."""
    model = args.get("model") or cfg_row.get("model") or stage.get("model_hint")
    if not model:
        raise ValueError(
            f"stage {stage.get('label')!r}: no model resolved from --args, "
            "the config row or the stage hint — refusing to guess")
    effort = args.get("effort") or cfg_row.get("effort") or stage.get("effort_hint") or _DEFAULT_EFFORT
    return {"model": model, "effort": effort}


_OPENROUTER_ALIAS_ERR = adapters.OPENROUTER_ALIAS_ERR


def _assert_model_in_provider_namespace(model: str, provider: str) -> None:
    """FAIL CLOSED before any network call — `adapters` owns the rule.

    The check moved to `adapters.assert_model_in_provider_namespace` when
    `dispatch.py` needed the same answer on the spawn path: two copies of a
    guard drift, and a guard that drifts is the incident again. This wrapper
    survives only to keep this module's `ValueError` contract, which its
    callers already handle.
    """
    try:
        adapters.assert_model_in_provider_namespace(model, provider)
    except adapters.AdapterError as exc:
        raise ValueError(str(exc)) from exc


def _resolve_pi_model(cfg: dict, stage: dict, args: dict,
                      roles=None) -> str:
    """The pi harness's model, from the ladder row when one exists for the
    stage's (tier, role) (hypothesis:l4-a-model-change-is-one-write), else
    `harnesses.pi.models` keyed by role (falling back to 'kid' for a role the
    block does not name) — NEVER from the harness-agnostic
    `workflows.NAME.model`, which is shared with claude-code and whose
    namespace (subscription aliases) is disjoint from OpenRouter's (`provider
    /name` slugs). `--args model` still wins, since that is how a human
    deliberately asks for a specific model."""
    if args.get("model"):
        return args["model"]
    role = stage.get("role") or "kid"
    tier = stage.get("tier") or _tier_for_role(role)
    row = adapters.ladder_role_row(roles, tier, role)
    if row is not None and (row.get("model") or "").strip():
        # the ladder row IS the one source: a write.py on the ladder changes
        # this stage's model without touching harnesses.pi.models.
        return row["model"].strip()
    pi_models = ((cfg.get("harnesses") or {}).get("pi") or {}).get("models") or {}
    model = pi_models.get(role) or pi_models.get("kid")
    if not model:
        raise ValueError(
            f"stage {stage.get('label')!r}: no ladder row and no "
            f"harnesses.pi.models entry for role {role!r} (or 'kid') and no "
            f"--args model override")
    return model


def _tier_for_role(role: str) -> int:
    """The canonical home tier for a role (mirror of dispatch's default)."""
    return {"kid": 0, "parent": 1, "director": 1, "prime_director": 3}.get(
        role, 0)


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


# ---- ONE run-event stream, TWO renderers (the goal:g9.7 pattern) -----------
# hypothesis:l3-workflow-surface-identical-across-harnesses: both harness
# paths feed THIS object and nothing else. The stage tree and the final
# summary render from the same events, so no presentation detail can appear
# on one harness and not the other — there is only one source.
_GLYPH = {"pending": "[ ]", "running": "[~]", "ok": "[✓]",
          "failed": "[✗]", "resolved": "[·]"}


def _track_run(root: Path, key: str, harness: str, view, run_key: str | None = None) -> None:
    """Append one row per real workflow run to `.agi/sessions/workflows/<key>.jsonl`.

    Reuses the `<project>/sessions/` layout dispatch.py writes, resolved to the
    shared project root so the tracking body stays ONE across worktrees
    (the same rule as iter-NNN). `--dry-run` never reaches here. Tracking is a
    side-effect, never a gate: any failure logs a warning and returns, so a
    real run's exit code is untouched.
    """
    try:
        sess = _loc.shared_project_root(root) or root
        wf_dir = Path(sess) / "sessions" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        counts: dict[str, int] = {}
        for s in view.state.values():
            counts[s["status"]] = counts.get(s["status"], 0) + 1
        row = {
            "workflow": key,
            "run_key": run_key,
            "harness": harness,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stages": {lb: st["status"] for lb, st in view.state.items()},
            "ok": counts.get("ok", 0),
            "failed": counts.get("failed", 0),
        }
        path = wf_dir / f"{key}.jsonl"
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception as exc:  # tracking must NEVER fail a real run
        print(f"workflow.py: warn: run tracking failed ({exc})",
              file=sys.stderr)


class RunView:
    """The single run-event stream both harness paths render through.

    Events: run_started, stage_resolved (claude-code path, where the .js
    script is the runner and workflow.py cannot observe completion),
    stage_started / stage_finished / stage_failed (pi path), summary. After
    every event the full stage tree redraws, so a watcher sees which stages
    exist, which are running, which are done, and what each returned —
    live, not as a transcript after the fact.
    """

    def __init__(self, key: str, stages: list[dict], harness: str,
                 out=sys.stdout):
        self.key = key
        self.harness = harness
        self.out = out
        self.order = [st["label"] for st in stages]
        self.state = {lb: {"status": "pending", "detail": ""}
                      for lb in self.order}

    def _tree(self) -> None:
        o = self.out
        o.write(f"workflow {self.key} (harness={self.harness})\n")
        last = len(self.order) - 1
        for i, lb in enumerate(self.order):
            s = self.state[lb]
            branch = "└─" if i == last else "├─"
            detail = f" — {s['detail']}" if s["detail"] else ""
            o.write(f"{branch} {_GLYPH[s['status']]} {lb}{detail}\n")
        o.flush()

    def _set(self, label: str, status: str, detail: str) -> None:
        if label not in self.state:
            return
        self.state[label].update(status=status, detail=detail)
        self._tree()

    def run_started(self) -> None:
        self._tree()

    def stage_resolved(self, label: str, detail: str = "") -> None:
        """claude-code path: the script is the runner there, so a stage can
        only be RESOLVED here, never observed to completion."""
        self._set(label, "resolved", detail)

    def stage_started(self, label: str, detail: str = "") -> None:
        self._set(label, "running", detail)

    def stage_finished(self, label: str, value) -> None:
        try:
            detail = json.dumps(value, ensure_ascii=False, sort_keys=True)[:120]
        except (TypeError, ValueError):
            detail = str(value)[:120]
        self._set(label, "ok", detail)

    def stage_failed(self, label: str, reason: str) -> None:
        self._set(label, "failed", reason.replace("\n", " ")[:120])

    def summary(self) -> None:
        """The ONE summary both harnesses print. Renders from stage order and
        statuses only — no harness token, no per-harness wording — so two runs
        with the same stage outcomes end byte-identically."""
        o = self.out
        for lb in self.order:
            o.write(f"[stage] {lb} {self.state[lb]['status']}\n")
        counts: dict[str, int] = {}
        for s in self.state.values():
            counts[s["status"]] = counts.get(s["status"], 0) + 1
        o.write(f"[summary] workflow={self.key} stages={len(self.order)} "
                f"ok={counts.get('ok', 0)} failed={counts.get('failed', 0)}\n")


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


def render_stage_prompt(stage: dict, run_args: dict, prior: dict | None = None) -> str:
    """Render a stage's `prompt` template against the run's args.

    The repeat item's own fields ({slug},{scope},{parent}) are the render
    context for a concrete expanded stage, overrideing the run args so each
    brief gets its own prompt. `prior` is the validated return of a PRIOR
    stage over the same repeat key (the chain mechanism: a repeated stage
    whose manifest carries `chained_from: <label>` renders with that prior
    stage's finding merged into its context, so it can name the finding's
    schema fields directly — {answer}, {still_live}, ...). A stage with no
    `prompt` raises ValueError (naming the stage) — without a prompt text a
    pi runner physically cannot execute the stage, which is the stub defect
    this fixes. Only `{word}` placeholders are expanded; `{\"..\": ..}` JSON
    braces in the prompt pass through untouched.
    """
    tmpl = stage.get("prompt")
    if not tmpl:
        raise ValueError(f"stage {stage.get('label')!r} declares no 'prompt' "
                         "text in its manifest — cannot run on the pi harness")
    ctx = _SafeDict(run_args)
    for k, v in (stage.get("_repeat_item") or {}).items():
        ctx[k] = v
    if prior:
        for k, v in prior.items():
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
                  out=sys.stdout, view: "RunView | None" = None,
                  prior: dict | None = None) -> tuple[int, "dict | None"]:
    """Execute ONE stage on the pi harness: spin the pi binary headlessly with
    the resolved provider/model/thinking and the rendered prompt, capture its
    stdout, parse the last JSON object, and validate it against the stage's
    schema. `prior` is the validated return of a prior stage over the same
    repeat key, merged into the prompt's render context (the chain mechanism).

    Returns (0, value) on success (schema-valid JSON produced); (rc>0, None)
    on failure. The value is the parsed return, so the caller can thread it
    into a later stage's prompt for the same repeat key. The kid writes any
    artifact (a draft body) itself under the scratch dir the prompt names; the
    runner does not fabricate it."""
    import subprocess
    k = knobs[stage["label"]]
    prompt = render_stage_prompt(stage, run_args, prior=prior)
    hc = _pi_harness_cfg(cfg)
    thinking = run_args.get("thinking") or _effort_to_thinking(k.get("effort"))
    cmd = [hc["bin"], "-p",
           "--provider", hc["provider"],
           "--model", k["model"],
           "--thinking", thinking,
           prompt]
    if view is not None:
        # The tree IS the surface now: one redraw per event, from the same
        # stream the claude-code path feeds (hypothesis:l3-workflow-surface-
        # identical-across-harnesses). Flat log lines stay only for the
        # view-less legacy callers (the test stubs).
        view.stage_started(stage["label"],
                           f"model={k['model']} effort={k.get('effort')}")
    else:
        out.write(f"# {_dispatching_line(stage, k)}\n")
        out.write(f"$ {' '.join(cmd)}\n")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              env=_pi_env(), timeout=600)
    except (OSError, subprocess.SubprocessError) as exc:
        if view is not None:
            view.stage_failed(stage["label"], f"could not start pi: {exc}")
        print(f"workflow.py: stage {stage['label']} could not start pi: "
              f"{exc}", file=sys.stderr)
        return 2, None
    output = proc.stdout or ""
    if proc.returncode != 0:
        if view is not None:
            view.stage_failed(stage["label"], f"pi exited rc={proc.returncode}")
        print(f"workflow.py: stage {stage['label']} pi exited rc="
              f"{proc.returncode}\n{output[-2000:]} {proc.stderr or ''}",
              file=sys.stderr)
        return 3, None
    try:
        value = _parse_last_json(output)
    except (ValueError, json.JSONDecodeError) as exc:
        if view is not None:
            view.stage_failed(stage["label"], f"did not return JSON: {exc}")
        print(f"workflow.py: stage {stage['label']} did not return JSON: "
              f"{exc}\n--- output tail ---\n{output[-2000:]}", file=sys.stderr)
        return 4, None
    violations = validate_return(stage.get("schema"), value)
    if violations:
        if view is not None:
            view.stage_failed(stage["label"], "returned JSON fails its schema")
        print(f"workflow.py: stage {stage['label']} returned JSON that fails "
              f"its schema:\n  " + "\n  ".join(violations), file=sys.stderr)
        return 5, None
    if view is not None:
        view.stage_finished(stage["label"], value)
    else:
        out.write(f"[ok] {stage['label']} -> "
                  f"{json.dumps(value, ensure_ascii=False, sort_keys=True)[:200]}\n")
    return 0, value


def run_workflow(root: Path, name: str, harness: str, args: dict, dry_run: bool,
                 out=sys.stdout) -> int:
    repo = _repo_root(root)
    cfg = _load_config(root)
    key = _config_key_for(name)
    # hypothesis:l4-a-workflow-run-is-named-not-numbered — the run is cited
    # by a DESCRIPTIVE key minted from this workflow's type + run args
    # (`mur-39`, `mur-sl1-2`), printed FIRST, never by the harness id. The
    # mint reads existing tracked rows so a re-run de-collides (-2, -3).
    run_key = _mint_run_key(root, key, args)
    out.write(f"[run-key] {run_key}\n")
    cfg_row = (cfg.get("workflows") or {}).get(key) or {}
    manifest = _load_manifest(repo, key)
    stages = _expand_stages(manifest, args)

    # No literal `'pi'` default (hypothesis:l4-workflow-types-and-default-
    # harness-are-a-geometry-node): with no explicit --harness the harness
    # resolves through the geometry node (per-workflow > per-type > prime
    # default), or refuses naming the node. An explicit --harness flag still
    # wins, envelope — it is the per-run override the CLI exposes.
    if not harness:
        harness, _level = _resolve_default_harness(root, key, manifest, cfg_row)
    knobs = {st["label"]: _resolve_knobs(st, cfg_row, args) for st in stages}
    if harness == "pi":
        # The pi model is resolved and namespace-checked here, BEFORE any
        # dry-run print or spawn — the config row's model is claude-code's,
        # not pi's (hypothesis:l3-workflow-model-crosses-harness-namespace).
        hc = _pi_harness_cfg(cfg)
        # hypothesis:l4-a-model-change-is-one-write — the ladder is the ONE
        # source when it declares the stage's (tier, role); fallback left for
        # a project with no ladder file.
        _roles = spawn_gate.read_ladder_roles(root / "nodes" if root else None)
        for st in stages:
            model = _resolve_pi_model(cfg, st, args, _roles)
            _assert_model_in_provider_namespace(model, hc["provider"])
            knobs[st["label"]]["model"] = model

    if dry_run:
        for st in stages:
            out.write(_dispatching_line(st, knobs[st["label"]]) + "\n")
        out.write(f"[summary] workflow={key} harness={harness} "
                  f"stages={len(stages)} via dispatch.py kids when harness=pi\n")
        return 0

    view = RunView(key, stages, harness, out=out)
    view.run_started()
    if harness != "pi":
        # claude-code harness: the Workflow script is the runner; we only
        # resolve and describe — but through the SAME event stream the pi
        # path feeds, so the two surfaces differ only where execution does.
        for st in stages:
            view.stage_resolved(st["label"],
                                f"model={knobs[st['label']].get('model')} "
                                f"script={manifest.get('script')}")
        view.summary()
        _track_run(root, key, harness, view, run_key)
        return 0

    # pi harness: execute each stage for real — one headless pi process per
    # stage, prompt rendered from the manifest + --args, resolved provider/
    # model/thinking passed through, JSON return validated against the schema.
    # This was a STUB: it used to call dispatch.py with a bogus `key:label`
    # --target and a nonexistent `workflow_stage` --template, never passing the
    # resolved knobs or the stage prompt, so a real run could not happen
    # (Belam VII, L3.28: three concrete defects).
    import subprocess
    prior_by_key: dict[tuple, dict] = {}
    for st in stages:
        prior = None
        if "_repeat_key" in st and st.get("chained_from"):
            # The chain mechanism: a repeated stage whose manifest names a
            # `chained_from` base label renders with the PRIOR stage's
            # validated return for the SAME repeat key merged into its prompt
            # context (so it can name the finding's schema fields —
            # {answer}, {still_live}, ...). Nothing else on pi crosses stage
            # boundaries; run_args only otherwise.
            prior = prior_by_key.get((st["chained_from"], st["_repeat_key"]))
        rc, value = _run_stage_pi(cfg, st, knobs, args, out=out, view=view,
                                  prior=prior)
        if rc != 0:
            print(f"workflow.py: workflow={key} failed at stage "
                  f"{st['label']} (rc={rc})", file=sys.stderr)
            view.summary()
            _track_run(root, key, harness, view, run_key)
            return rc
        if "_repeat_key" in st and value is not None:
            prior_by_key[(st["_base_label"], st["_repeat_key"])] = value
    view.summary()
    _track_run(root, key, harness, view, run_key)
    return 0


_JS_IDENT = re.compile(r"\W")


def _qs(obj) -> str:
    """Render a value as a JS single-quoted/proper JSON literal for embedding
    in the generated script (escapes quotes, backticks, `${`, newlines)."""
    return json.dumps(obj)


def _js_const(base: str, suffix: str) -> str:
    """A JS-safe const name from a stage's base label + suffix."""
    return _JS_IDENT.sub("_", base).upper() + "_" + suffix


def _stage_phase(base: str) -> str:
    """A display phase title (`investigate` -> `Investigate`) for a stage."""
    return (base[:1].upper() + base[1:]) if base else "Run"


def _repeat_field(label_template: str) -> str:
    """The one `{field}` a repeat label_template names, e.g. `key` in
    `investigate:{key}` — the item field the generated script reads for its
    per-item label."""
    m = re.search(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", label_template)
    if not m:
        raise ValueError(f"repeat.label_template {label_template!r} must name "
                         "exactly one {field}")
    return m.group(1)


def _stage_schema_const(st) -> str | None:
    return _js_const(st["label"], "SCHEMA") if st.get("schema") else None


def _gen_script(manifest: dict) -> str:
    """Generate a genuine Claude Code Workflow `.js` FROM the stage manifest —
    the manifest is the source, the script is derived (hypothesis:
    l4-workflow-authoring-is-a-harness-tool). The generated script reads its
    items from `args` (`const ITEMS = (args && args['<of>']) || []`) exactly
    like the reference templates, renders each stage's prompt through `fill`
    (the manifest's `{word}` placeholders, with JSON braces untouched), and
    passes the resolved model/effort to every agent call. Repeated stages
    become a `parallel(...)` over ITEMS; a chained PAIR of repeated stages
    (stage[1].chained_from == stage[0].label, same repeat.of) becomes the
    `pipeline(ITEMS, project, accumulate)` form — the native Workflow shape a
    Claude Code session runs unchanged and which renders in /workflows."""
    name = manifest["name"]
    script_name = f"agi-{name}"
    description = manifest.get("description") or \
        f"Workflow {name}, authored via workflow.py author"
    stages = manifest["stages"]

    repeats = [s for s in stages if (s.get("repeat") or {}).get("of")]
    simples = [s for s in stages if not (s.get("repeat") or {}).get("of")]
    if repeats and simples:
        raise ValueError(
            f"author cannot compose simple and repeated stages in one script "
            f"({name}); split into two workflows or author the script by hand")

    default_model = "sonnet"
    default_effort = "medium"
    for st in stages:
        default_model = st.get("model_hint") or default_model
        default_effort = st.get("effort_hint") or default_effort

    L = ["export const meta = {",
         f"  name: {_qs(script_name)},",
         f"  description: {_qs(description)},",
         "  phases: ["]
    for st in stages:
        L.append(f"    {{ title: {_qs(_stage_phase(st['label']))} }},")
    L += ["  ],", "}", "",
          f"const MODEL = (args && args.model) || {_qs(default_model)}",
          f"const EFFORT = (args && args.effort) || {_qs(default_effort)}", "",
          "const fill = (t, ctx) => String(t).replace(/\\{([A-Za-z_][A-Za-z0-9_]*)\\}/g, (_, k) => (k in ctx && ctx[k] != null ? ctx[k] : ''))", ""]

    # ---- simple stages: one sequential await per stage -----------------------
    if not repeats:
        result_names = []
        for i, st in enumerate(simples):
            base = st["label"]
            phase = _stage_phase(base)
            tmpl = _js_const(base, "TMPL")
            L.append(f"const {tmpl} = {_qs(st.get('prompt') or '')}")
            sch = _stage_schema_const(st)
            if sch:
                L.append(f"const {sch} = {_qs(st['schema'])}")
            L.append(f"phase({_qs(phase)})")
            call = (f"await agent(fill({tmpl}, args), "
                    f"{{ label: {_qs(base)}, phase: {_qs(phase)}, ")
            if sch:
                call += f"schema: {sch}, "
            call += "model: MODEL, effort: EFFORT })"
            rname = f"r{i}"
            L.append(f"const {rname} = {call}")
            result_names.append((base, rname))
            L.append("")
        # keys are quoted: a stage label may carry a hyphen (`capture-and-read`),
        # which is not a bare JS identifier (measured: the first authored
        # single-stage pair failed to parse at the Workflow tool).
        L.append("return { "
                 + ", ".join(f"{_qs(b)}: {r}" for b, r in result_names) + " }")
        return "\n".join(L) + "\n"

    # ---- repeated stages: one shared args list -------------------------------
    ofs = {s["repeat"]["of"] for s in repeats}
    if len(ofs) != 1:
        raise ValueError("author: all repeated stages in one workflow must "
                         "share the same repeat.of")
    of = repeats[0]["repeat"]["of"]
    L.append(f"const ITEMS = (args && args[{_qs(of)}]) || []")
    L.append("")
    for st in stages:
        if (st.get("repeat") or {}).get("of"):
            base = st["label"]
            L.append(f"const {_js_const(base, 'TMPL')} = "
                     f"{_qs(st.get('prompt') or '')}")
            sch = _stage_schema_const(st)
            if sch:
                L.append(f"const {sch} = {_qs(st['schema'])}")
    L.append("")

    if len(repeats) == 1:
        st = repeats[0]
        base, phase = st["label"], _stage_phase(st["label"])
        field = _repeat_field(st["repeat"]["label_template"])
        tmpl = _js_const(base, "TMPL")
        L.append(f"phase({_qs(phase)})")
        opts = (f"{{ label: `{base}:${{it.{field}}}`, phase: {_qs(phase)}, ")
        sch = _stage_schema_const(st)
        if sch:
            opts += f"schema: {sch}, "
        opts += "model: MODEL, effort: EFFORT }"
        L.append(f"const results = await parallel(ITEMS.map("
                 f"it => agent(fill({tmpl}, it), {opts})))")
        L.append("return results")
        return "\n".join(L) + "\n"

    if len(repeats) == 2:
        r0, r1 = repeats
        b0, b1 = r0["label"], r1["label"]
        if r0["repeat"]["of"] != r1["repeat"]["of"]:
            raise ValueError("author: chained repeated stages must share "
                             "repeat.of")
        if r1.get("chained_from") != b0:
            raise ValueError("author: a two-stage repeated workflow needs "
                             "stage[1].chained_from == stage[0].label to chain")
        p0, p1 = _stage_phase(b0), _stage_phase(b1)
        f1 = _repeat_field(r1["repeat"]["label_template"])
        t0, t1 = _js_const(b0, "TMPL"), _js_const(b1, "TMPL")
        s0, s1 = _stage_schema_const(r0), _stage_schema_const(r1)
        proj = (f"it => agent(fill({t0}, it), "
                f"{{ label: `{b0}:${{it.{_repeat_field(r0['repeat']['label_template'])}}}`, "
                f"phase: {_qs(p0)}, "
                + (f"schema: {s0}, " if s0 else "")
                + "model: MODEL, effort: EFFORT })")
        L.append(f"phase({_qs(p0)})")
        L.append("const results = await pipeline(")
        L.append("  ITEMS,")
        L.append(f"  {proj},")
        L.append(f"  (finding, it) => {{")
        L.append("    if (!finding) return null")
        acc = (f"    return agent(fill({t1}, {{ ...it, ...finding }}), "
               f"{{ label: `{b1}:${{it.{f1}}}`, phase: {_qs(p1)}, ")
        if s1:
            acc += f"schema: {s1}, "
        acc += "model: MODEL, effort: EFFORT })"
        L.append(acc + ".then(v => ({ key: it." + f"{f1}" + ", finding, "
                 + f"{b1}: v }}))")
        L.append("  },")
        L.append(")")
        L.append("return results.filter(Boolean)")
        return "\n".join(L) + "\n"

    raise ValueError("author: more than two chained repeated stages is not "
                     "yet supported; build multiple smaller workflows")


def author_workflow(root: Path, name: str, stages_text: str, out=sys.stdout,
                    source_note: str = "") -> int:
    """The authoring verb (hypothesis:l4-workflow-authoring-is-a-harness-tool):
    write BOTH halves of a runnable pair in one action — `<name>.json` (the
    stage manifest with real prompts) AND `agi-<name>.js` GENERATED FROM it.
    Unlike `register`, which could only derive `<TODO>` prompt skeletons,
    author takes a stage list whose prompts are already authored and derives
    the script, so the manifest is the source and the script is derived. It
    deliberately OVERWRITES an existing pair (authoring is explicit, not a
    silent collision). Returns 0 on success; 2 on a bad stage list."""
    repo = _repo_root(root)
    wf = repo.joinpath(*WORKFLOWS_DIR_REL)
    key = _config_key_for(name).strip()
    if not key:
        print("workflow.py: author needs a non-empty name", file=sys.stderr)
        return 2
    try:
        stages = json.loads(stages_text)
        if not isinstance(stages, list):
            raise ValueError("stages must be a JSON array")
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"workflow.py: author: stages not valid JSON array: {exc}",
              file=sys.stderr)
        return 2
    for st in stages:
        if not isinstance(st, dict) or not st.get("label"):
            print(f"workflow.py: author: every stage needs a non-empty 'label'",
                  file=sys.stderr)
            return 2
        prompt = st.get("prompt") or ""
        if "<TODO" in prompt:
            print(f"workflow.py: author: stage {st['label']!r} carries a "
                  "<TODO> prompt — author a real prompt; validate rejects "
                  "<TODO> as non-runnable", file=sys.stderr)
            return 2
        rep = st.get("repeat") or {}
        if rep.get("of"):
            if not rep.get("label_template"):
                print(f"workflow.py: author: stage {st['label']!r} repeats "
                      "but has no repeat.label_template", file=sys.stderr)
                return 2
            try:
                base = rep["label_template"].split(":")[0].strip()
            except IndexError:
                base = st["label"]
            if base != st["label"]:
                print(f"workflow.py: author: stage {st['label']!r} repeat."
                      "label_template base '{base}' must equal its label",
                      file=sys.stderr)
                return 2
            _repeat_field(rep["label_template"])
    # hypothesis:l4-a-workflow-run-is-named-not-numbered (part 2): re-
    # authoring an EXISTING manifest must CARRY FORWARD `type` (the registry
    # invariant — dropping it is one more validate violation) and any other
    # non-derived top-level field, and APPEND the --note to the existing
    # description rather than REPLACING it (measured: author dropped type and
    # replaced description; restored by hand at 07bae9ea8).
    manifest_path = wf / f"{key}.json"
    existing: dict = {}
    if manifest_path.is_file():
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = {}
    derived = {"name", "script", "description", "stages"}
    carried = {k: v for k, v in existing.items() if k not in derived}
    desc = (existing.get("description")
            or (f"Authored via workflow.py author"
                + (f" ({source_note})" if source_note else "")))
    if source_note and f"({source_note})" not in desc:
        desc = f"{desc.rstrip()} ({source_note})".strip()
    manifest = {
        "name": key,
        "script": f"agi-{key}.js",
        "description": desc,
        "stages": stages,
    }
    manifest.update(carried)
    try:
        script_text = _gen_script(manifest)
    except ValueError as exc:
        print(f"workflow.py: author: {exc}", file=sys.stderr)
        return 2
    (wf / f"{key}.json").write_text(
        json.dumps(manifest, indent=2) + chr(10), encoding="utf-8")
    (wf / f"agi-{key}.js").write_text(script_text, encoding="utf-8")
    out.write(f"[authored] {key} -> {key}.json + agi-{key}.js "
              f"({len(stages)} stage(s), script derived FROM manifest)\n")
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
    au = sub.add_parser("author",
                        help="write BOTH halves of a runnable workflow pair: <name>.json + agi-<name>.js derived FROM it (hypothesis:l4-workflow-authoring-is-a-harness-tool)")
    au.add_argument("name", help="workflow key to author (e.g. prime-open-questions)")
    au.add_argument("--stages", default=None,
                    help="path to a JSON stage-list file (else --json literal, else stdin)")
    au.add_argument("--json", default=None,
                    help="the stage list inline as a JSON literal")
    au.add_argument("--stdin", action="store_true",
                    help="read the stage list from stdin")
    au.add_argument("--note", default="",
                    help="provenance note to embed in the manifest description")
    lst = sub.add_parser("list", help="enumerate the registered workflows")
    stt = sub.add_parser("status", help="resolve recent workflow runs by descriptive run key")
    stt.add_argument("key", nargs="?", default=None,
                     help="run key or workflow key to filter to (e.g. mur-39)")
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
    if args.cmd == "author":
        if args.stages:
            try:
                stages_text = Path(args.stages).read_text(encoding="utf-8")
            except OSError as exc:
                print(f"workflow.py: author: cannot read --stages {args.stages}: "
                      f"{exc}", file=sys.stderr)
                return 2
        elif args.json:
            stages_text = args.json
        elif args.stdin or not sys.stdin.isatty():
            stages_text = sys.stdin.read()
        else:
            print("workflow.py: author needs one of --stages PATH, --json, "
                  "or the stage list on stdin", file=sys.stderr)
            return 2
        return author_workflow(root, args.name, stages_text,
                               source_note=args.note)
    # the harness-resolution node may be absent (pre-prime) or a workflow may
    # declare an undeclared type: refuse LOUDLY naming the node, exit 2 — never
    # a traceback, never a silent literal fallback (hypothesis:
    # l4-workflow-types-and-default-harness-are-a-geometry-node).
    try:
        if args.cmd == "list":
            return list_workflows(root)
        if args.cmd == "status":
            return status_workflow(root, args.key)
        if args.cmd == "validate":
            return validate_registry(root)
        try:
            run_args = json.loads(args.args)
            if not isinstance(run_args, dict):
                raise ValueError("--args must be a JSON object")
        except json.JSONDecodeError as exc:
            print(f"workflow.py: --args not valid JSON: {exc}", file=sys.stderr)
            return 2
        return run_workflow(root, args.name, args.harness, run_args, args.dry_run)
    except WorkflowsNodeError as exc:
        print(f"workflow.py: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
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
    workflow.py run <name> [--harness NAME] [--args JSON] [--dry-run]
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
    --harness harness to run through (default: geometry/config resolution)
    --args    JSON of per-run overrides merged OVER the config row
    --dry-run resolve every stage and print one dispatch line per stage, with
              the resolved model/effort, WITHOUT spawning any agent

Exit 0 on a successful resolve / green validation; 2 on a resolve failure.

RUN exit codes (a live `run`; distinct codes so a caller can act on WHICH
refusal happened without parsing stderr):
    0  every stage completed (an `unstructured` return is not a failure)
    2  resolve failure (bad --args, unknown workflow, harness/model refused)
    3  a pi stage process exited non-zero
    4  a stage's return could not be parsed as its schema (stage JSON error)
    5  the run was REFUSED before any stage: a stage's `timeout_s` is not a
       positive number of seconds (conjunct (4) of hypothesis:l4-sd06-residue-
       renumber-notice-fixture-dry-run-parity-refused-run-key -- 4 was reused
       for this and collided with the stage return-parse error above).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# The unpatched dispatch primitives, captured once: `_run_stage_proc` resumes a
# live child across a wall extension, which needs the real `Popen`; a caller
# that injected only `subprocess.run` (the legacy test seam) still gets it.
_REAL_POPEN = subprocess.Popen
_REAL_RUN = subprocess.run

import yaml


_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))

import adapters  # noqa: E402  -- owns the model/provider namespace guard,
# and the shared (tier, role, harness) ladder resolver (l4-one-write)
import provisioning  # noqa: E402  -- the ONE mint seam dispatch.py uses
import spawn_gate  # noqa: E402  -- reads ladder roles for the same resolver
import locations as _loc  # noqa: E402
import mem_cap  # noqa: E402 -- the ONE memory cap both launch paths use (SM.112)
from frontmatter import split_frontmatter  # noqa: E402

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


def _leading_token(value: object) -> str:
    """The slug of everything up to the first whitespace or `(`, so a
    descriptor cell like `42 (point, mur-42 window)` slugs as `42`, exactly
    like the bare integer `42` — and the two dedupe together. `SL2#2` has no
    whitespace or paren, so it keeps its full shape (`sl2-2` after the slug);
    a cell whose token starts with a paren or whitespace yields an empty
    string, i.e. contributes nothing."""
    s = str(value).strip()
    cut = len(s)
    for i, ch in enumerate(s):
        if ch.isspace() or ch == "(":
            cut = i
            break
    return s[:cut]


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
    each slugged. A list of dicts — the merge-up `rounds` shape — contributes
    the DEDUPED, order-preserved scalar values of the cell that names the run:
    `merge_up` when present, else `key`. So `rounds:[{merge_up:40,key:"L4.288"},
    {merge_up:40,...}]` mints `mur-40`, NEVER `mur-40-40`; a naked `key` cell
    mints `mur-l4-288`. Other nested dicts contribute nothing — the run key
    names the WORKFLOW plus its simple knobs, not the per-target rows inside
    an arg."""
    raw: list[str] = []
    for k in sorted(args or {}):
        v = args[k]
        if isinstance(v, (dict, bool)) or v is None:
            continue
        if isinstance(v, (list, tuple)):
            for item in v:
                if item is None or isinstance(item, bool):
                    continue
                if isinstance(item, dict):
                    cell = item.get("merge_up")
                    if cell is None:
                        cell = item.get("key")
                    if cell is None or isinstance(cell, (dict, list, bool)):
                        continue
                    # the LEADING token of the cell: `42 (point, ...)` slugs as
                    # `42`, exactly like the bare integer 42, so descriptor
                    # cells dedupe with their bare form instead of defeating
                    # the dedupe (mur-42 window, mur-42 P1 line -- 57-char key)
                    tok = _leading_token(cell)
                    if not tok:
                        continue
                    raw.append(tok)
                else:
                    raw.append(str(item))
        else:
            raw.append(str(v))
    seen: set[str] = set()
    tokens: list[str] = []
    for t in raw:
        if t not in seen:
            seen.add(t)
            tokens.append(t)
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
    parted = split_frontmatter(text)
    if parted is None:
        raise WorkflowsNodeError(
            f"{path}: unterminated frontmatter block (only one `---`)")
    try:
        fm = yaml.safe_load(parted[0])
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
                if _row_matches_key(r, key)]
    if key and not rows:
        out.write(f"(no runs match key {key!r})\n")
        return 1
    if not rows:
        out.write("(no workflow runs tracked yet)\n")
        return 0
    for r in rows:
        hid = _row_harness_text(r)
        out.write(f"{r.get('run_key') or r.get('workflow')}  "
                  f"workflow={r.get('workflow')} harness={r.get('harness')} "
                  f"harness_id={hid} "
                  f"{str(r.get('timestamp') or '')} "
                  f"ok={r.get('ok')} "
                  f"unstructured={r.get('unstructured')} "
                  f"failed={r.get('failed')}\n")
    return 0


def _row_harness_ids(r: dict) -> list:
    """A tracked row's harness ids as a list (legacy rows may hold a bare
    string or nothing)."""
    v = r.get("harness_id")
    if not v:
        return []
    return v if isinstance(v, list) else [v]


def _row_harness_text(r: dict) -> str:
    """The run's harness ids rendered for status --------- `-` until any are
    noted, else comma-joined."""
    ids = _row_harness_ids(r)
    return ",".join(ids) if ids else "-"


def _row_matches_key(r: dict, key: str) -> bool:
    """Does this tracked row answer a `status <key>` query? Matches the run_key
    (mur-39), the owning workflow key (merge-up-review), or a harness-minted
    id printed by status (wf_ba530baa-dab) — so `status wf_<id>` resolves a
    run through the id the harness minted (hypothesis:l4-a-workflow-run-is-
    named-not-numbered)."""
    if key in (str(r.get("run_key") or ""), str(r.get("workflow") or "")):
        return True
    return any(key == i for i in _row_harness_ids(r))


def link_workflows(root: Path, out=sys.stdout) -> int:
    """Create the `.claude/workflows/<script>` -> `../../extensions/agi/
    workflows/<script>` RELATIVE symlink for every registered manifest script
    that has none, matching the four already there. Idempotent (a second run
    creates 0). Refuses BY NAME, never silently skips, when a path already
    exists and is not a symlink pointing at the right target. Returns 2 on any
    such refusal, else 0."""
    repo = _repo_root(root)
    wf = repo.joinpath(*WORKFLOWS_DIR_REL)
    links = repo / ".claude" / "workflows"
    links.mkdir(parents=True, exist_ok=True)
    made = 0
    for mf in sorted(wf.glob("*.json")):
        try:
            manifest = json.loads(mf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        script = manifest.get("script")
        if not script:
            continue
        dest = links / script
        target = Path("..") / ".." / Path(*WORKFLOWS_DIR_REL) / script
        if dest.is_symlink():
            if os.readlink(dest) == str(target):
                continue
            print(f"workflow.py: link refused: {dest} is a symlink to "
                  f"{os.readlink(dest)!r}, not {str(target)!r}",
                  file=sys.stderr)
            return 2
        if dest.exists():
            print(f"workflow.py: link refused: {dest} exists and is not a "
                  f"symlink to {str(target)!r}", file=sys.stderr)
            return 2
        dest.symlink_to(target)
        made += 1
    out.write(f"[linked] {made} workflow link(s) created\n")
    return 0


def note_workflow(root: Path, run_key: str, harness_id: str,
                  out=sys.stdout) -> int:
    """Record the claude-code harness's `wf_<id>` beside the tracked row a
    run_key names (hypothesis:l4-a-workflow-run-is-named-not-numbered). On the
    claude-code harness workflow.py never executes the .js script — the
    harness mints the wf_ id when IT runs it — so the id cannot be captured at
    run time; `note` records it afterward. Idempotent: re-noting the SAME id is
    a no-op; noting a DIFFERENT id appends, never overwrites; an unknown
    run_key is a named refusal, exit 2."""
    try:
        sess = _loc.shared_project_root(root) or root
    except Exception:
        sess = root
    wf_dir = Path(sess) / "sessions" / "workflows"
    if not wf_dir.is_dir():
        out.write(f"workflow.py: note: no runs tracked yet to note "
                  f"{run_key!r} against\n")
        return 2
    # newest tracked row whose run_key names this key (the LAST text line that
    # parses to it, over each file in dir order)
    target: dict | None = None
    target_path: Path | None = None
    target_idx: int | None = None
    for f in sorted(wf_dir.glob("*.jsonl")):
        lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
        for i, line in enumerate(lines):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("run_key") == run_key:
                target, target_path, target_idx = row, f, i
    if target is None:
        out.write(f"workflow.py: note: no tracked run keyed {run_key!r}\n")
        return 2
    ids = _row_harness_ids(target)
    if harness_id in ids:
        out.write(f"(harness_id {harness_id} already recorded on "
                  f"{run_key})\n")
        return 0
    target["harness_id"] = ids + [harness_id]
    lines = target_path.read_text(encoding="utf-8").splitlines(keepends=True)
    lines[target_idx] = (json.dumps(target, ensure_ascii=False,
                                    sort_keys=True) + "\n")
    target_path.write_text("".join(lines), encoding="utf-8")
    out.write(f"[noted] {run_key} <- harness_id {harness_id} "
              f"({len(ids) + 1} recorded)\n")
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
        # The slice identity is the field the stage's OWN template names
        # ({key}->key, {slug}->slug, {window}->window); window/slug are only a
        # template-agnostic fallback. The old fixed window/slug probe made
        # _repeat_key None for every {key}-axis manifest, so one failed slice
        # matched all its siblings (SM.105 key-axis falsifier).
        key_fields = re.findall(r"\{(\w+)\}", tmpl)
        for item in pool:
            sub = dict(st)
            if not isinstance(item, dict):
                key = item
            else:
                key = next((item[f] for f in key_fields if f in item), None)
                if key is None:
                    key = item.get("window") or item.get("slug")
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


def _resolve_harness_model(harness_cfg: dict, stage: dict, args: dict) -> str:
    """Resolve a model from the selected harness namespace.

    Workflow rows are harness-agnostic.  Once a run selects a harness, its
    tier model is authoritative; otherwise a Claude alias or Copilot model
    hint can leak into the wrong namespace.
    """
    if args.get("model"):
        return str(args["model"])
    role = stage.get("role") or "kid"
    tier = stage.get("tier") or role
    models = harness_cfg.get("models") or {}
    model = models.get(role) or models.get(tier) or models.get("kid")
    if not model:
        raise ValueError(
            f"stage {stage.get('label')!r}: harness declares no model for "
            f"role {role!r} or tier {tier!r}")
    return str(model)


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


def _result_file_value(stage: dict, run_args: dict,
                       view: "RunView | None") -> "dict | None":
    """A stage's declared `result_file`, read back as its structured return.

    Read the rendered `result_file` as JSON and return it ONLY when it
    validates against the stage schema; the stage is then marked
    `resolved-from-digest`. Absent, unparseable or schema-invalid: None, and
    the caller fails the stage as today (hypothesis:l4-a-research-stage-whose-
    digest-file-is-complete-returns-it-as-its-structured-result-never-fails-
    the-run-at-the-structured-return)."""
    tmpl = stage.get("result_file")
    if not tmpl:
        return None
    ctx = _SafeDict(run_args)
    for k, v in (stage.get("_repeat_item") or {}).items():
        ctx[k] = v
    p = Path(_PLACEHOLDER.sub(lambda m: str(ctx[m.group(1)]), tmpl))
    try:
        value = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if validate_return(stage.get("schema"), value):
        return None
    if view is not None:
        view.stage_resolved(stage["label"], f"resolved-from-digest: {p}")
    else:
        print(f"workflow.py: stage {stage['label']} resolved from digest {p}",
              file=sys.stderr)
    return value


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
          "failed": "[✗]", "resolved": "[·]", "unstructured": "[?]",
          "skipped": "[»]"}

# The tree renders a HEAD of a stage's detail, never the whole thing
# (hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation
# conjunct (3)). An `unstructured` return is the entire model stdout by
# design, so a multi-KB blob on one tree line buries every other stage.
# BUDGET: 200 characters. Justification: a tree line is read by a human
# watching a live run and by a parent harvesting it; 200 chars is about one
# terminal line at 200 columns — enough to identify WHAT a stage returned
# (its first sentence) and no more. It is deliberately an order of magnitude
# below the >= 4000-char returns the falsifier names, so such a return cannot
# dominate the tree. The FULL text is untouched in `state[lb]["detail"]` and
# in the tracking row's `returns`; only the render is cut.
_TREE_DETAIL_PREVIEW_CHARS = 200


def _preview_detail(text: str) -> str:
    """The tree's head-preview of one stage's detail, newlines flattened.

    Returns the whole flattened text when it fits the budget, else a
    `_TREE_DETAIL_PREVIEW_CHARS` head plus an explicit elision marker naming
    the EXACT number of characters omitted: `… (+<N> chars)`. The result is
    always a single line — no embedded newline — because the tree relies on
    that."""
    flat = text.replace("\n", " ")
    if len(flat) <= _TREE_DETAIL_PREVIEW_CHARS:
        return flat
    omitted = len(flat) - _TREE_DETAIL_PREVIEW_CHARS
    return f"{flat[:_TREE_DETAIL_PREVIEW_CHARS]}… (+{omitted} chars)"



def _run_key_path_component(run_key: str) -> str:
    """Filesystem-safe form of `run_key` for use as a directory name. Most
    filesystems cap one path component at 255 bytes, and a run_key slugged
    from a long `why`/args blob can exceed that -- measured: `brainstorm`'s
    run_key (idea id + whole `why` string + max_hypotheses) tripped `File
    name too long` on mkdir, which `_persist_stage_value`'s broad except
    swallowed, so the stage's structured return was never written and the
    chained stage read back only the 200-char preview (director gen 6,
    commit 453445d60). Truncated keys keep a digest of the FULL key so two
    long keys sharing a prefix still land in different directories."""
    if len(run_key.encode("utf-8")) <= 200:
        return run_key
    digest = hashlib.sha256(run_key.encode("utf-8")).hexdigest()[:8]
    return f"{run_key[:190]}-{digest}"


def _persist_stage_value(root: Path, run_key: str, label: str, value) -> None:
    """Write a pi stage's WHOLE return to
    `<sessions>/workflows/runs/<run_key>/<label>.json` -- the view keeps 200
    chars and an `unstructured` return otherwise lives only in this process,
    so a reviewer that answered in prose was unreadable by the Prime (measured
    mur-sl7-137, 2026-09-16 20:02Z: both stages unstructured, both lost).
    Best effort: a persistence failure never fails the run."""
    try:
        sess = _loc.shared_project_root(root) or root
        d = Path(sess) / "sessions" / "workflows" / "runs" / _run_key_path_component(run_key)
        d.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", label)
        (d / f"{safe}.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"workflow.py: could not persist stage {label!r}: {exc}",
              file=sys.stderr)

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
            # `harness_id` starts empty: on the claude-code harness workflow.py
            # never runs the .js script — the harness mints the wf_ id itself —
            # so a caller records it afterward with `workflow.py note
            # <run_key> --harness-id wf_<id>` (hypothesis:l4-a-workflow-run-is-
            # named-not-numbered). Absent/`[]` prints `-` in status.
            "harness_id": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stages": {lb: st["status"] for lb, st in view.state.items()},
            "ok": counts.get("ok", 0),
            "failed": counts.get("failed", 0),
            # An `unstructured` stage is not a failure: the pi binary ran and
            # returned prose with no schema-valid JSON. Its text is kept WHOLE
            # (never the 120-char tree stub) under `returns` so a director can
            # read the review that was actually written
            # (hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-
            # a-dispatched-spawn conjunct (h)).
            "unstructured": counts.get("unstructured", 0),
            "returns": {lb: st["detail"] for lb, st in view.state.items()
                        if st["status"] == "unstructured"},
            # A schema-invalid JSON return keeps its NAMED violation here, so
            # the record says what was wrong rather than filing JSON-shaped
            # output under the same key as prose (hypothesis:l4-a-per-run-
            # workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-
            # name conjunct (3)).
            "violations": {lb: st["violations"] for lb, st in view.state.items()
                           if st.get("violations")},
            # A resolved-from-digest stage NAMES the file it stood in for.
            "resolved_from_digest": {
                lb: st["detail"] for lb, st in view.state.items()
                if st["detail"].startswith("resolved-from-digest:")},
            # Every transient retry is NAMED in the record: stage label,
            # attempt n, matched signature, sleep seconds.
            "attempts": {lb: st["attempts"] for lb, st in view.state.items()
                         if st.get("attempts")},
            # A wall extension is part of the run status: which stage, how
            # many, how many seconds (SM.105).
            "extensions": {lb: st["extensions"] for lb, st in view.state.items()
                           if st.get("extensions")},
            # An empty declared handoff list (`handoff_list`) is a run-level
            # boolean, so an empty ready_batch is legible in the record
            # without failing the run.
            "batch_empty": bool(getattr(view, "empty_handoffs", [])),
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
        self.state = {lb: {"status": "pending", "detail": "",
                           "violations": [], "attempts": [],
                           "extensions": []}
                      for lb in self.order}
        # A stage that declares a `handoff_list` and returned it EMPTY. Its
        # own run-level fact (never a failure), rendered by `summary` and
        # recorded in the tracking row as `batch_empty`.
        self.empty_handoffs: list = []

    def _tree(self) -> None:
        o = self.out
        o.write(f"workflow {self.key} (harness={self.harness})\n")
        last = len(self.order) - 1
        for i, lb in enumerate(self.order):
            s = self.state[lb]
            branch = "└─" if i == last else "├─"
            # A stage's detail may be WHOLE prose (an `unstructured` return is
            # not truncated in STATE, and the tracking row keeps it whole) —
            # but the TREE shows a head-preview only, with the omitted size
            # named, so one multi-KB return cannot dominate the tree
            # (conjunct (3) of hypothesis:l4-workflow-residue-sub-floor-
            # marker-dead-code-and-truncation). `detail` itself is never cut.
            flat = _preview_detail(s["detail"]) if s["detail"] else ""
            detail = f" — {flat}" if flat else ""
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
        only be RESOLVED here, never observed to completion. Also the pi
        path's digest fallback: a stage with no schema-valid stdout whose
        declared `result_file` validates is resolved from that file."""
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

    def stage_skipped(self, label: str, reason: str) -> None:
        """A stage skipped BY NAME because the slice it depends on failed
        (SM.105 isolation). Its own status, never `failed`: nothing was run."""
        self._set(label, "skipped", reason.replace("\n", " ")[:120])

    def stage_extension(self, label: str, extension_s: float,
                        n: int = 1, pid: int | None = None) -> None:
        """Name a granted wall extension: the stage was producing at the
        wall and got `extension_s` more seconds (the n-th extension). `pid` is
        the SAME live process the wall was moved under -- recorded so the run
        status proves the extension was in place, not a re-dispatch."""
        if label in self.state:
            self.state[label]["extensions"].append(
                {"n": n, "extension_s": extension_s, "pid": pid})
        self.out.write(f"[extension] {label} +{extension_s:g}s (n={n})\n")
        self.out.flush()

    def stage_attempts(self, label: str, attempts: list) -> None:
        """Record the named retry rows (attempt n, signature, sleep_s) for a
        stage, so `_track_run`'s jsonl row carries them."""
        if label in self.state:
            self.state[label]["attempts"] = [dict(a) for a in attempts]

    def stage_empty_handoff(self, label: str, field: str) -> None:
        """A stage that declared a `handoff_list` and returned it EMPTY.

        Visibility, NOT failure: the stage legitimately dropped every
        candidate, so the run still ends `ok`. Without this, an empty list is
        indistinguishable from a chain that broke — both leave downstream
        placeholders blank while the summary reads `ok`. Rendered by
        `summary` and recorded as `batch_empty` on the tracking row."""
        self.empty_handoffs.append({"stage": label, "field": field})
        self.out.write(f"[empty] {label}: {field}=[]\n")
        self.out.flush()

    def stage_unstructured(self, label: str, text: str,
                           violations: list[str] | None = None) -> None:
        """A stage whose pi process succeeded (rc 0) but returned no JSON that
        validates against its schema. Recorded as its own status, NEVER as a
        failure: the run continues and the text is carried WHOLE — not the
        120-char stub `stage_finished` writes for structured returns — so the
        prose the agent actually wrote is still readable
        (hypothesis:l4-a-workflow-pi-stage-mints... conjunct (h)).

        `violations` names WHY a JSON candidate failed its schema (empty for
        genuine prose), so the tracking row can record the named violation
        instead of losing it (hypothesis:l4-a-per-run-workflow-key-is-revoked-
        at-run-end-and-a-schema-miss-keeps-its-name conjunct (3))."""
        self._set(label, "unstructured", text)
        if label in self.state:
            self.state[label]["violations"] = list(violations or [])

    def summary(self) -> None:
        """The ONE summary both harnesses print. Renders from stage order,
        statuses, and any empty-handoff warns — no harness token, no
        per-harness wording — so two runs with the same stage outcomes end
        byte-identically."""
        o = self.out
        for lb in self.order:
            o.write(f"[stage] {lb} {self.state[lb]['status']}\n")
        counts: dict[str, int] = {}
        for s in self.state.values():
            counts[s["status"]] = counts.get(s["status"], 0) + 1
        for e in self.empty_handoffs:
            o.write(f"[warn] {e['stage']}: handoff {e['field']} is empty — "
                    "the stage ran and kept nothing (batch_empty=true); "
                    "this is not a chain failure\n")
        o.write(f"[summary] workflow={self.key} stages={len(self.order)} "
                f"ok={counts.get('ok', 0)} "
                f"unstructured={counts.get('unstructured', 0)} "
                f"failed={counts.get('failed', 0)}\n")


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
    # `{project_root}` is injected by `run_workflow`; a direct caller (a
    # probe, a test) may pass it too. When it is absent, resolve the cwd's
    # project root rather than expanding to '' and emitting `cd  &&` — never
    # a hardcoded checkout path.
    if not ctx.get("project_root"):
        _pr = _loc.find_project_root()
        if _pr is not None:
            ctx["project_root"] = str(_pr.parent)
    if prior:
        for k, v in prior.items():
            ctx[k] = v
    return _PLACEHOLDER.sub(lambda m: str(ctx[m.group(1)]), tmpl)


def _return_shape_block(stage: dict, run_args: dict) -> str:
    """The RETURN SHAPE block for a pi stage's prompt when (and ONLY when)
    it declares a `schema`: schema JSON, required keys, the last-stdout-
    bytes instruction, and the rendered result_file path. Schema-less
    stages get "" and render byte-identical to before."""
    schema = stage.get("schema")
    if not schema:
        return ""
    req = schema.get("required") or list(schema.get("properties") or {})
    lines = ["", "RETURN SHAPE (required): the LAST thing in your stdout must "
             "be exactly one JSON object matching this schema, with nothing "
             "after it:", json.dumps(schema), f"Required keys: {', '.join(req)}"]
    tmpl = stage.get("result_file")
    if tmpl:
        ctx = _SafeDict(run_args)
        for k, v in (stage.get("_repeat_item") or {}).items():
            ctx[k] = v
        path = _PLACEHOLDER.sub(lambda m: str(ctx[m.group(1)]), tmpl)
        lines.append("Also write that same JSON object to " + path
                     + " before you finish; that file is this stage's result "
                     "of record if stdout is cut.")
    return "\n".join(lines)


def _pi_harness_cfg(cfg: dict) -> dict:
    """The pi harness's bin/provider/thinking from config `harnesses.pi`.

    Fallbacks are the engine defaults, so a project that omits the row still
    resolves — matching the config-maxxed contract (never a hard literal that
    skips the config, but a config row with sane defaults)."""
    h = (cfg.get("harnesses") or {}).get("pi") or {}
    return {
        # The ONE shared resolver: $PI_BIN first, then the `~`/{home}-expanded
        # config cell, then PATH for the built-in default. Round 1 of
        # hypothesis:harness-bin-paths-resolve-per-box moved the config bins to
        # `~/.npm-global/bin/pi`; this reader used to read the RAW cell
        # config-before-env and fall back to a /home/ubuntu literal (the two
        # defects that killed every merge-up-review stage at once).
        "bin": adapters.resolve_bin(h, "PI_BIN", "pi"),
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


def _credential_decision(root, cfg: dict, harness: str) -> tuple[bool, str | None]:
    """Whether this run would issue ONE per-run minted credential, and if not,
    why not. READS ONLY — `available()` reads the envfile and
    `needs_credential()` reads the adapter constant, neither touches the
    network — so the `--dry-run` print and the live mint path share this one
    decision and cannot disagree (a printed line that differs from the live
    choice is the trap this exists to close)."""
    if not provisioning.available(root):
        return False, "provisioning unavailable"
    row = (cfg.get("harnesses") or {}).get(harness) or {}
    if not adapters.needs_credential(row):
        return False, f"harness {harness} needs no credential"
    return True, None


def _credential_line(would_mint: bool, reason: str | None) -> str:
    """The ONE line naming the credential decision. `--dry-run` writes it to
    `out`; the fallback path prints it to stderr under a `workflow.py: `
    prefix."""
    return ("[credential] mint per-run" if would_mint
            else f"[credential] inherited env ({reason})")


def _workflow_credential_tier(stages: list) -> str:
    """The ladder tier a run's single credential is minted under: the first
    stage's declared tier, else the canonical home tier of its role. One mint
    per run needs one tier, and the run's first stage is its entry point."""
    st = stages[0] if stages else {}
    if st.get("tier"):
        return str(st["tier"])
    return str(_tier_for_role(st.get("role") or "kid"))


def _resolve_workflow_spawn_env(root, cfg: dict, run_key: str, harness: str,
                                stages: list) -> tuple[dict | None, str | None]:
    """The env a pi stage is spawned under, plus the MINTED KEY HASH so the
    caller can revoke it when the run ends (hypothesis:l4-a-per-run-workflow-
    key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name conjunct (2)).
    The hash is returned rather than dropped: the old signature handed back a
    bare env dict, so nothing downstream could name the key to delete it and
    it outlived the run. `(env, None)` on every fallback path — nothing to
    revoke. ONE mint per RUN, not per stage:
    a capped key minted through the SAME seam dispatch.py uses for a
    dispatched spawn, named `workflow:<run_key>` and carrying the run's ladder
    tier — so a workflow pi stage no longer inherits whatever dead
    OPENROUTER_API_KEY the caller shell happened to carry.

    Falls back to the inherited `_pi_env()` — ONE stderr line naming the
    reason — when provisioning is unavailable, the harness needs no
    credential, or `mint()` returns None. A `ProvisioningError` with a
    provisioning key present is a real fault: it is named (`ERR: ...`) and the
    stage is REFUSED (rc 3, `(None, None)`) UNLESS the inherited key is proven
    usable by `provisioning.check_runtime_key_usable`, which then runs the
    stage on the inherited env with a `[credential] inherited env, verified`
    line. Never a silent fallback onto a credential nothing verified."""
    would_mint, reason = _credential_decision(root, cfg, harness)
    if not would_mint:
        print(f"workflow.py: {_credential_line(False, reason)}",
              file=sys.stderr)
        return _pi_env(), None
    limit_usd, ttl_minutes = provisioning.settings(cfg)
    try:
        minted = provisioning.mint(
            iter_n=run_key, agent_id=f"workflow:{run_key}",
            tier=_workflow_credential_tier(stages),
            limit_usd=limit_usd, ttl_minutes=ttl_minutes,
            workspace_id=provisioning.workspace(cfg), root=root)
    except provisioning.ProvisioningError as exc:
        print(f"ERR: could not mint a workflow credential: {exc}",
              file=sys.stderr)
        # A failed mint must REFUSE, never fall back onto a credential nothing
        # verified — UNLESS the inherited key is proven usable by one
        # authenticated check. Refusal returns (None, None): the caller turns
        # that into rc 3 before any stage dispatches (the fatal falsifier was
        # a stage spinning to its timeout on an owner-403'd key).
        usable, _reason = provisioning.check_runtime_key_usable(cfg, root)
        if not usable:
            print(f"workflow.py: refusing stage: mint failed ({exc}) and the "
                  f"inherited env key is not usable", file=sys.stderr)
            return None, None
        print("workflow.py: [credential] inherited env, verified",
              file=sys.stderr)
        return _pi_env(), None
    if minted is None:
        print(f"workflow.py: {_credential_line(False, 'mint returned None')}",
              file=sys.stderr)
        return _pi_env(), None
    env = _pi_env()
    env[provisioning.RUNTIME_KEY_VAR] = minted.secret
    return env, minted.key_hash


def _revoke_run_credential(key_hash: str | None, root) -> None:
    """Delete the ONE per-run minted key when the run ends — success, stage
    failure or a raised/timeout path, exactly once (called from a `finally`).
    Nothing is revoked when the run minted nothing.

    Never raises and never changes the run's exit code: the key's TTL is the
    backstop, and a run that did the work must not be reported failed because
    a cleanup call failed. But a False return (or a seam that raises) IS named
    on stderr — a silent failure to revoke is exactly how the key outlives the
    run this closes."""
    if not key_hash:
        return
    try:
        ok = provisioning.revoke(key_hash, root=root)
    except Exception as exc:  # revoke() never raises; a mock seam may
        print(f"workflow.py: warn: could not revoke the run credential "
              f"{key_hash}: {exc}", file=sys.stderr)
        return
    if not ok:
        print(f"workflow.py: warn: revoke returned False for the run "
              f"credential {key_hash} — it will die at its TTL",
              file=sys.stderr)


# The pre-fix literal the context build ran under, kept as the undeclared
# default so a manifest that declares no `context_timeout_s` is
# byte-for-byte today (the claim's third conjunct) -- 60 s, NOT the stage
# wall's 3600. `_resolve_context_timeout` is the ONE place this default
# lives; `_stage_context` still guards `None` for legacy callers.
_DEFAULT_CONTEXT_TIMEOUT_S = 60


def _stage_context(repo: Path, graph_root: Path, stage: dict,
                   context_timeout_s: int = _DEFAULT_CONTEXT_TIMEOUT_S) -> str:
    """Assemble the shared graph context for one live workflow stage.

    The stage prompt remains workflow-specific, but the graph state and role
    brief come from the same read surfaces used by ordinary dispatched kids.
    This keeps a workflow stage from inventing a second context assembly path.

    `context_timeout_s` is the budget BOTH context reads run under, resolved by
    the CALLER from the manifest (`stage["context_timeout_s"]` >
    `manifest["context_timeout_s"]` > `_DEFAULT_CONTEXT_TIMEOUT_S`) -- this
    function never re-reads a manifest and never owns a second copy of the
    resolver. It used to be two hard `timeout=60` literals, which is exactly
    how every verify stage died `context-build-timeout after 60 s` at box load
    40-51 (merge-up-review, 09-23 mur).
    """
    import subprocess

    budget = (_DEFAULT_CONTEXT_TIMEOUT_S if context_timeout_s is None
              else context_timeout_s)
    role = str(stage.get("role") or "kid")
    tier = str(stage.get("tier") or role)
    if tier not in {"kid", "parent", "advisor", "director",
                    "prime_director", "liaison"}:
        tier = "kid"
    viewport = subprocess.run(
        [sys.executable, str(_THIS / "viewport.py"), "--emit", "llm",
         "--depth", "3"],
        cwd=str(repo), capture_output=True, text=True, timeout=budget,
    )
    if viewport.returncode != 0:
        raise RuntimeError(
            f"viewport --emit llm failed for stage {stage.get('label')!r}: "
            f"{(viewport.stderr or '').strip()}")
    brief = subprocess.run(
        [sys.executable, str(_THIS / "brief.py"), "head", "--tier", tier,
         "--project-root", str(graph_root)],
        cwd=str(repo), capture_output=True, text=True, timeout=budget,
    )
    if brief.returncode != 0:
        raise RuntimeError(
            f"brief.py head failed for stage {stage.get('label')!r}: "
            f"{(brief.stderr or '').strip()}")
    route = (
        "WORKFLOW ROUTE CONTRACT:\n"
        "Use the viewport and brief above as the graph context for this stage. "
        "If this stage produces a graph node or report, write it only through "
        "`python3 extensions/agi/bin/write.py`; never hand-edit a node or "
        "payload. A read-only stage remains read-only.\n"
    )
    return f"{brief.stdout.rstrip()}\n\n{viewport.stdout.rstrip()}\n\n{route}"


def _effort_to_thinking(effort: str | None) -> str:
    """Map a workflow effort knob to a pi thinking level. `max`/`high` -> high,
    `low` -> low, anything missing or odd -> medium. A `--args thinking` value
    is never remapped (the caller passes it through unchanged)."""
    return {"max": "high", "high": "high", "low": "low"}.get(
        (effort or "").strip().lower(), "medium")


# _parse_last_json was DELETED here (hypothesis:l4-workflow-residue-sub-floor-
# marker-dead-code-and-truncation conjunct (2)). It had no production caller:
# the only hits in the tree were this definition and a unit test of it. Its
# job — tolerant extraction of a JSON object from model stdout — is done by
# `_balanced_brace_spans` / `_resolve_lenient_return` below, which are
# depth-aware AND string-aware; `_parse_last_json`'s `find("{") /
# rfind("}")` was the naive version of the same idea and is superseded.


_FENCED_JSON = re.compile(r"```(?:json|yaml)?\s*(.*?)```", re.DOTALL)


def _balanced_brace_spans(text: str):
    """Yield each balanced `{...}` span in `text`, depth-aware and string-
    aware. For every `{` scan forward to its MATCHING `}` (tracking nesting and
    skipping braces inside JSON strings), so one stray brace in prose cannot
    swallow the rest of the output the way `text.find('{') : text.rfind('}')`
    did. An unclosed `{` yields nothing."""
    n = len(text)
    i = 0
    while i < n:
        if text[i] != "{":
            i += 1
            continue
        depth = 0
        in_str = False
        esc = False
        j = i
        while j < n:
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    yield text[i:j + 1]
                    break
            j += 1
        i += 1


def _json_candidates(text: str) -> list[str]:
    """Every plausible JSON-object candidate in a stage's stdout, in the
    order they should be trusted: the contents of fenced ```json blocks first
    (the model was asked for JSON and fenced it explicitly), then every bare
    balanced-brace span."""
    cands = [m.group(1).strip() for m in _FENCED_JSON.finditer(text)
             if m.group(1).strip()]
    cands.extend(_balanced_brace_spans(text))
    return cands


def _resolve_lenient_return(schema, text: str, violations_out=None):
    """The FIRST candidate in `text` that both parses as JSON and passes
    `schema` (via `validate_return`), or None when no candidate validates.

    A candidate that parses but violates the schema is SKIPPED, never fatal —
    a model that emitted a stray JSON snippet before its real answer must not
    lose the answer (hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-
    key-like-a-dispatched-spawn conjunct (h)). Prose-only output validates
    nothing and returns None, which the caller records as `unstructured`.

    But a candidate that was JSON and failed its schema is NOT prose, and its
    named violation must survive: when `violations_out` is given, each such
    candidate's violation strings are appended to it, so the caller can record
    what was wrong instead of dropping it (hypothesis:l4-a-per-run-workflow-
    key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name conjunct (3)).
    A LATER candidate that validates still wins and the run still succeeds."""
    for cand in _json_candidates(text):
        try:
            value = json.loads(cand)
        except (ValueError, json.JSONDecodeError):
            continue
        violated = validate_return(schema, value)
        if not violated:
            return value
        if violations_out is not None:
            violations_out.extend(violated)
    return None


# The ONE injectable sleep seam for the transient-5xx retry: tests
# monkeypatch `workflow._RETRY_SLEEP`, so a retry NEVER sleeps for real.
_RETRY_SLEEP = time.sleep

# Two sleeps for three attempts total; no sleep after the FINAL attempt, so
# the record's last row honestly carries `sleep_s: 0` (never 135).
_PI_RETRY_BACKOFF_S = (15, 45)

# The transient signatures. The HTTP shape is dispatch.py's `_DEATH_STREAM_RE`
# widened with the provider's own literal `error code: 520` bytes.
_PI_TRANSIENT_RE = re.compile(
    r"error code:\s*5\d\d|"
    r"stream error|h2 protocol error|upstream error|"
    r"connection reset|econnreset|"
    r"http(?:/\d+(?:\.\d+)?)?\s*5\d\d", re.I)


def _pi_failure_is_transient(output_text: str, stderr_text: str,
                             stage: dict) -> "str | None":
    """The MATCHED signature string when a failed pi attempt is TRANSIENT,
    else None. Only ever called on the rc != 0 branch.

    Transient requires BOTH: the combined output carries one of
    `_PI_TRANSIENT_RE`'s signatures, AND no schema-valid JSON candidate was
    produced by that same output. A stage that emitted a valid return and then
    died is NOT retried — the value it wrote is what the run keeps, and
    re-running it would spend a second key on work already done."""
    combined = f"{output_text}\n{stderr_text}"
    m = _PI_TRANSIENT_RE.search(combined)
    if not m:
        return None
    try:
        if _resolve_lenient_return(stage.get("schema"), combined) is not None:
            return None
    except (ValueError, json.JSONDecodeError):
        pass
    return m.group(0)


def _stage_is_producing(stage: dict) -> bool:
    """A stage is PRODUCING at the wall when its declared `progress_file`
    (alias `output_file` / `heartbeat_file`) was touched within `silence_s`
    (default 300 s); otherwise it is silent and the wall kills it."""
    path = (stage.get("progress_file") or stage.get("output_file")
            or stage.get("heartbeat_file"))
    try:
        mtime = os.stat(path).st_mtime
    except (OSError, TypeError):
        return False
    return (time.time() - mtime) <= stage.get("silence_s", 300)


def _run_stage_proc(cmd, *, budget: float, stage: dict,
                    spawn_env: dict | None, view: "RunView | None",
                    cap: "str | None" = None):
    """Run ONE stage command with the SM.105 optional wall extension, on a
    live `Popen` so an extension is the SAME process and the SAME output file.

    A producing stage at the wall keeps its pid: the deadline moves and the
    poll loop keeps waiting on the process it already started -- no kill, no
    re-dispatch, no second run. A silent stage (or a stage out of extensions)
    is killed at the wall and raises TimeoutExpired, the exact contract
    `subprocess.run` had. A caller that injected only `subprocess.run` (the
    legacy test seam) owns dispatch and cannot hand back a resumable child, so
    it gets the single deadline it was given."""
    env = spawn_env if spawn_env is not None else _pi_env()
    # SM.112 -- one cap for the stage child. Only on a REAL launch: a test
    # that injected the Popen seam owns its own child.
    if cap is not None and subprocess.Popen is _REAL_POPEN:
        cmd = mem_cap.wrap_argv(cmd, cap)
    if subprocess.Popen is _REAL_POPEN and subprocess.run is not _REAL_RUN:
        return subprocess.run(cmd, capture_output=True, text=True, env=env,
                              timeout=budget)
    grants = max(0, int(stage.get("max_extensions", 1) or 0))
    n = 0
    deadline = time.monotonic() + budget
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=env)
    while True:
        try:
            out, err = proc.communicate(
                timeout=max(0.0, deadline - time.monotonic()))
            return subprocess.CompletedProcess(cmd, proc.returncode, out, err)
        except subprocess.TimeoutExpired:
            if n >= grants or not _stage_is_producing(stage):
                proc.kill()
                out, err = proc.communicate()
                raise subprocess.TimeoutExpired(cmd, deadline, output=out,
                                                stderr=err)
            n += 1
            budget = stage.get("extension_s") or budget
            deadline = time.monotonic() + budget
            if view is not None:
                view.stage_extension(stage["label"], budget, n, pid=proc.pid)


def _run_stage_pi(cfg: dict, stage: dict, knobs: dict, run_args: dict,
                  out=sys.stdout, view: "RunView | None" = None,
                  prior: dict | None = None,
                  spawn_env: dict | None = None,
                  context_text: str | None = None,
                  timeout_s: float | None = None) -> tuple[int, "dict | None"]:
    """Execute ONE stage on the pi harness: spin the pi binary headlessly with
    the resolved provider/model/thinking and the rendered prompt, capture its
    stdout, parse the last JSON object, and validate it against the stage's
    schema. `prior` is the validated return of a prior stage over the same
    repeat key, merged into the prompt's render context (the chain mechanism).

    Returns (0, value) on success (schema-valid JSON produced); (rc>0, None)
    on failure. The value is the parsed return, so the caller can thread it
    into a later stage's prompt for the same repeat key. The kid writes any
    artifact (a draft body) itself under the scratch dir the prompt names; the
    runner does not fabricate it.

    `spawn_env` is the env the pi process runs under; when None the inherited
    `_pi_env()` is used, so a view-less/legacy caller is byte-unchanged. The
    live pi path passes the ONE per-run env from
    `_resolve_workflow_spawn_env()`.

    `timeout_s` is the stage's wall-clock budget, resolved by the CALLER from
    the manifest (`stage["timeout_s"]` > `manifest["timeout_s"]` >
    `_DEFAULT_STAGE_TIMEOUT_S`) — this function never re-reads a manifest
    (hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-
    miss-keeps-its-name conjunct (5)). None means the module default."""
    import subprocess
    budget = _DEFAULT_STAGE_TIMEOUT_S if timeout_s is None else timeout_s
    cap = mem_cap.resolve_memory_cap(cfg)
    k = knobs[stage["label"]]
    prompt = render_stage_prompt(stage, run_args, prior=prior) \
        + _return_shape_block(stage, run_args)
    if context_text:
        prompt = f"{context_text}\n\nSTAGE TASK:\n{prompt}"
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
    attempts: list[dict] = []
    # Bounded retry, ONLY for a transient (5xx/stream-signature) failure: at
    # most 3 attempts, sleeping 15 then 45 s through the injectable seam.
    while True:
        try:
            proc = _run_stage_proc(
                cmd, budget=budget, stage=stage, spawn_env=spawn_env,
                view=view, cap=cap)
        except subprocess.TimeoutExpired:
            # A timeout is reported as ELAPSED TIME FIRST, never as "could not
            # start": TimeoutExpired IS a SubprocessError and the string it
            # carries buries the whole argv -- prompt and all -- behind the
            # one true fact that the process DID start and ran long before
            # being cut. Caught before OSError/SubprocessError on purpose
            # (except clauses are ordered). rc 2, one attempt, no retry.
            # Landed independently by two rounds (SM.70 item 3 here; also
            # hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-
            # timeout-says-timed-out-... from mur-sm-60) -- this is the
            # merged shape, reconciled at a season2/main merge conflict.
            # A wall-cut stage whose result_file is complete resolves.
            digest = _result_file_value(stage, run_args, view)
            if digest is not None:
                return 0, digest
            if view is not None:
                view.stage_failed(stage["label"],
                                   f"timed out after {budget:g} s")
            print(f"workflow.py: stage {stage['label']} timed out after "
                  f"{budget:g} s", file=sys.stderr)
            return 2, None
        except (OSError, subprocess.SubprocessError) as exc:
            # An unrunnable binary is NOT transient: one attempt, rc 2,
            # byte-identical to before.
            if view is not None:
                view.stage_failed(stage["label"], f"could not start pi: {exc}")
            print(f"workflow.py: stage {stage['label']} could not start pi: "
                  f"{exc}", file=sys.stderr)
            return 2, None
        output = proc.stdout or ""
        if proc.returncode == 0:
            if attempts:
                # Name the successful attempt too (a success never sleeps).
                attempts.append({"attempt": len(attempts) + 1,
                                 "signature": None, "sleep_s": 0})
                if view is not None:
                    view.stage_attempts(stage["label"], attempts)
            break
        signature = _pi_failure_is_transient(output, proc.stderr or "", stage)
        if signature is None:
            # SM.112 -- the cap's kill is NAMED, never the generic rc: the
            # cap predicate is checked FIRST, the wall timeout raised above.
            if mem_cap.is_cap_death(proc.returncode, cap,
                                    output + (proc.stderr or "")):
                if view is not None:
                    view.stage_failed(stage["label"],
                                      f"memory-cap (rc={proc.returncode})")
                print(f"workflow.py: stage {stage['label']} killed by memory-cap "
                      f"rc={proc.returncode}", file=sys.stderr)
                return 3, None
            # rc != 0 WITHOUT the transient signature is a real failure, never
            # retried (falsifier: a stage retried on a failure without it).
            if view is not None:
                view.stage_failed(stage["label"],
                                  f"pi exited rc={proc.returncode}")
            print(f"workflow.py: stage {stage['label']} pi exited rc="
                  f"{proc.returncode}\n{output[-2000:]} {proc.stderr or ''}",
                  file=sys.stderr)
            return 3, None
        max_attempts = len(_PI_RETRY_BACKOFF_S) + 1
        n = len(attempts) + 1
        if n >= max_attempts:
            # Exhausted: `sleep_s: 0` — there is no sleep after the last try.
            attempts.append({"attempt": n, "signature": signature,
                             "sleep_s": 0})
            if view is not None:
                view.stage_attempts(stage["label"], attempts)
                view.stage_failed(
                    stage["label"],
                    f"pi exited rc={proc.returncode} after {n} transient "
                    f"attempt(s) (signature: {signature})")
            print(f"workflow.py: stage {stage['label']} gave up after {n} "
                  f"transient attempts (signature: {signature})\n"
                  f"{output[-2000:]}", file=sys.stderr)
            return 3, None
        sleep_s = _PI_RETRY_BACKOFF_S[n - 1]
        attempts.append({"attempt": n, "signature": signature,
                         "sleep_s": sleep_s})
        if view is not None:
            # The stage stays `running` across a retry: a run that succeeds on
            # attempt 2 must end `ok`, never `failed`.
            view.stage_attempts(stage["label"], attempts)
            view.stage_started(stage["label"],
                               f"attempt {n + 1}/{max_attempts} after "
                               f"{signature}")
        print(f"workflow.py: stage {stage['label']} transient attempt "
              f"{n}/{max_attempts} (signature: {signature}); retrying in "
              f"{sleep_s}s", file=sys.stderr)
        _RETRY_SLEEP(sleep_s)
    violations: list[str] = []
    try:
        value = _resolve_lenient_return(stage.get("schema"), output,
                                        violations)
    except (ValueError, json.JSONDecodeError) as exc:
        # `_resolve_lenient_return` swallows per-candidate parse errors; a
        # raise here is unexpected (a broken schema), so keep it fatal.
        if view is not None:
            view.stage_failed(stage["label"], f"return parse error: {exc}")
        print(f"workflow.py: stage {stage['label']} return parse error: "
              f"{exc}\n--- output tail ---\n{output[-2000:]}",
              file=sys.stderr)
        return 4, None
    if value is None:
        # No valid block in stdout: a declared result_file may still hold it.
        digest = _result_file_value(stage, run_args, view)
        if digest is not None:
            return 0, digest
        if stage.get("result_file"):
            if view is not None:
                view.stage_failed(stage["label"], "no schema-valid JSON and "
                                  "no complete result_file")
            print(f"workflow.py: stage {stage['label']} declared result_file "
                  f"but neither stdout nor the file carried a schema-valid "
                  f"return", file=sys.stderr)
            return 2, None
        # The pi process SUCCEEDED and returned prose with no schema-valid
        # JSON. That is `unstructured`, never a failure: the run continues,
        # the stage's whole text rides the value so the next stage's `prior`
        # can read it, and the run summary shows it in its own column.
        # Dedupe: a fenced candidate and its bare span are the same text, so
        # the same violation would otherwise be recorded twice.
        seen: set[str] = set()
        violations = [v for v in violations
                      if not (v in seen or seen.add(v))]
        if view is not None:
            view.stage_unstructured(stage["label"], output, violations)
        else:
            out.write(f"[unstructured] {stage['label']} "
                      f"({len(output)} chars)\n")
        if violations:
            # A JSON return that FAILED its schema is not the same thing as
            # prose: name the violation the run kept instead of losing it.
            print(f"workflow.py: stage {stage['label']} returned JSON that "
                  f"violates its schema ({len(violations)} violation(s)): "
                  f"{violations[0]}", file=sys.stderr)
        else:
            print(f"workflow.py: stage {stage['label']} returned no schema-valid "
                  f"JSON; recorded unstructured ({len(output)} chars)",
                  file=sys.stderr)
        ret = {"unstructured": output}
        if violations:
            ret["violations"] = violations
        return 0, ret
    if view is not None:
        view.stage_finished(stage["label"], value)
    else:
        out.write(f"[ok] {stage['label']} -> "
                  f"{json.dumps(value, ensure_ascii=False, sort_keys=True)[:200]}\n")
    return 0, value


# The undeclared default wall-clock budget for one stage, raised 600 -> 3600
# by the SM.105 owner verbatim (2026-09-18: "increase the timeout ... like 60
# mins to be safe with optional extension"). Named here so the resolver is
# the ONE place the default lives; `_run_stage_pi` still guards its own
# `timeout_s is None` for legacy callers, and that guard resolves to this
# same number.
_DEFAULT_STAGE_TIMEOUT_S = 3600

# A load-scaled wall is capped at this multiple of the declared budget.
_LOAD_CAP_MULT = 2.0


def _current_load() -> float:
    """The ONE load source a wall may scale on; tests patch THIS seam."""
    return os.getloadavg()[0]


def _whole_seconds(value: float) -> int:
    """A resolved budget, floored to whole seconds and never to ZERO.

    A 0<v<1 budget is a positive number, so it clears the refusal, but
    `int(0.5)` truncates it to 0 and `subprocess.run(timeout=0)` raises
    `TimeoutExpired` immediately — the same silent kill a declared 0 causes.
    Every truncation site (with and without load scaling, stage wall and
    context build) floors at ONE second instead
    (goal:g15.29.20 FR-C1; hypothesis:context-budget-never-floors-to-zero-
    and-is-pinned)."""
    return max(1, int(value))


def _resolve_stage_timeout(stage: dict, manifest: dict) -> int:
    """The stage's wall-clock budget in seconds, DECLARED — never truthy.

    Presence, not truthiness: a stage-level `timeout_s` wins whenever the key
    is present and not None, so a declared `0` is not silently replaced by the
    manifest value. The old `st.get("timeout_s") or manifest.get("timeout_s")`
    did exactly that (hypothesis:l4-workflow-residue-sub-floor-marker-dead-
    code-and-truncation conjunct (5)).

    🔴 THE MEANING OF `0`, defined here and only here, is definition (a) from
    the brief: a zero-second budget is an INVALID budget, and the run is
    REFUSED BY NAME before any stage is dispatched (`run_workflow` catches the
    ValueError and exits non-zero with one stderr line naming the key and the
    stage, before the per-run key is minted). A negative or non-numeric value
    is refused the same way. Refusing is observable; the alternatives are not
    — `subprocess.run(timeout=0)` raises `TimeoutExpired` immediately and
    kills EVERY stage of the run, which is the silent kill the falsifier
    names, and definition (b) (`0` means wait forever) is indistinguishable
    from a hung stage until it has already hung.

    An absent value anywhere falls through to the manifest value and then to
    `_DEFAULT_STAGE_TIMEOUT_S` (3600 since SM.105).
    """
    label = stage.get("label")
    if "timeout_s" in stage and stage["timeout_s"] is not None:
        raw = stage["timeout_s"]
        where = f"stage {label!r} timeout_s"
    else:
        raw = manifest.get("timeout_s")
        where = f"stage {label!r} inherits workflow timeout_s"
    if raw is None:
        return _DEFAULT_STAGE_TIMEOUT_S
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw <= 0:
        raise ValueError(
            f"{where}={raw!r} is not a positive number of seconds; a budget "
            f"of 0 (or less, or non-numeric) is not a request to wait "
            f"forever — the run is refused before any stage is dispatched")
    # Opt-in load scaling (absent key = byte-for-byte today's number).
    lf = (stage["load_factor"] if "load_factor" in stage
          else manifest.get("load_factor"))
    if lf is None:
        return _whole_seconds(raw)
    if isinstance(lf, bool) or not isinstance(lf, (int, float)) or lf <= 0:
        raise ValueError(
            f"stage {label!r} load_factor={lf!r} is not a positive number")
    return _whole_seconds(min(raw * (1.0 + lf * _current_load()),
                              raw * _LOAD_CAP_MULT))


def _resolve_context_timeout(stage: dict, manifest: dict) -> int:
    """The stage's CONTEXT-BUILD budget in seconds, DECLARED — never truthy.

    Same resolution shape as `_resolve_stage_timeout` (which owns the stage
    WALL): stage `context_timeout_s` > manifest `context_timeout_s` >
    `_DEFAULT_CONTEXT_TIMEOUT_S` (60, the literal this replaces). Presence,
    not truthiness: a declared stage key wins even when 0, and a declared 0,
    negative, bool or non-numeric value is REFUSED BY NAME before any stage
    runs — `run_workflow` resolves both budgets in the same try/except, so the
    refusal is one path with rc 5 and `--dry-run` agrees with the live run.

    Load scaling is opt-in and reads the same `load_factor` cells as the wall
    (a context build is itself slower under load, which is the incident this
    closes) and is capped at `_LOAD_CAP_MULT` x the declared budget; absent
    everywhere means the declared number, byte-for-byte.
    """
    label = stage.get("label")
    if "context_timeout_s" in stage and stage["context_timeout_s"] is not None:
        raw = stage["context_timeout_s"]
        where = f"stage {label!r} context_timeout_s"
    else:
        raw = manifest.get("context_timeout_s")
        where = f"stage {label!r} inherits workflow context_timeout_s"
    if raw is None:
        return _DEFAULT_CONTEXT_TIMEOUT_S
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw <= 0:
        raise ValueError(
            f"{where}={raw!r} is not a positive number of seconds; a budget "
            f"of 0 (or less, or non-numeric) is not a request to wait "
            f"forever — the run is refused before any stage is dispatched")
    lf = (stage["load_factor"] if "load_factor" in stage
          else manifest.get("load_factor"))
    if lf is None:
        return _whole_seconds(raw)
    if isinstance(lf, bool) or not isinstance(lf, (int, float)) or lf <= 0:
        raise ValueError(
            f"stage {label!r} load_factor={lf!r} is not a positive number")
    return _whole_seconds(min(raw * (1.0 + lf * _current_load()),
                              raw * _LOAD_CAP_MULT))


def _failed_dependency(stage: dict, failed_keys: dict) -> str | None:
    """The base label this stage depends on that has a failed slice, or None.
    A repeated slice depends on the SAME `_repeat_key` of its base; a simple
    stage depends on the whole base. A repeated stage never consults its own
    base label, so a failed slice never skips a sibling slice (SM.105)."""
    deps = stage.get("chained_from") or stage.get("depends_on")
    if not deps:
        return None
    deps = [deps] if isinstance(deps, str) else deps
    for d in deps:
        keys = failed_keys.get(d)
        if keys and ("_repeat_key" not in stage
                     or stage["_repeat_key"] in keys):
            return d
    return None


#: The three env markers a LIVE Claude Code session exports. Their presence
#: is what tells a native Workflow tool call (the caller IS Claude Code) apart
#: from a headless `workflow.py run --harness claude-code` invocation, which
#: must keep printing the SM.120 stderr notice and execute nothing
#: (hypothesis:l4-same-harness-handback-...).
CLAUDE_CODE_SEAM_VARS = (
    "CLAUDECODE", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_MESSAGING_SOCKET",
)


def _claude_code_seam_present(env: dict | None = None) -> bool:
    """True when the caller IS a live Claude Code session (all three seam
    vars exported), False for any other caller. `env` defaults to
    `os.environ`, and a test passes an explicit mapping so BOTH branches are
    assertable without forking a session — the three shipped tests that call
    `run_workflow(..., "claude-code", ...)` directly inherit the ambient
    seam and must clear it to keep testing the seam-ABSENT path."""
    e = os.environ if env is None else env
    return all(e.get(v) for v in CLAUDE_CODE_SEAM_VARS)


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
    # The RUNNER resolves the project root and hands it to every stage prompt
    # as `{project_root}` — no prompt hardcodes a checkout path, so a run
    # started in a git worktree mints into THAT worktree's graph. Added AFTER
    # the run key is minted: a path is environment, not identity, and must
    # never enter the descriptive key (`rr-tm57`, unchanged).
    args = dict(args or {})
    args.setdefault("project_root", str(repo))
    out.write(f"[run-key] {run_key}\n")
    cfg_row = (cfg.get("workflows") or {}).get(key) or {}
    manifest = _load_manifest(repo, key)
    # hypothesis:brainstorm-manifest-route-refuses-a-missing-goal: a
    # manifest-declared `required_args` list (config-max, never a literal
    # per-workflow check here) is refused BY NAME before any stage expands
    # or dispatches -- the pi/pi-free route used to have no such guard at
    # all, unlike the native JS route's own required-goal check.
    _missing_args = [a for a in (manifest.get("required_args") or [])
                     if not str(args.get(a) or "").strip()]
    if _missing_args:
        print(f"workflow.py: workflow={key} refused: missing required "
              f"non-empty arg(s) {_missing_args} (manifest.required_args)",
              file=sys.stderr)
        # rc 2, distinct from the rc 5 stage-timeout refusal and rc 3/4
        # elsewhere in this function: a caller must be able to tell a
        # bad-args refusal (nothing about the manifest's stages was even
        # reached) from every other refusal class.
        return 2
    stages = _expand_stages(manifest, args)

    # No literal `'pi'` default (hypothesis:l4-workflow-types-and-default-
    # harness-are-a-geometry-node): with no explicit --harness the harness
    # resolves through the geometry node (per-workflow > per-type > prime
    # default), or refuses naming the node. An explicit --harness flag still
    # wins, envelope — it is the per-run override the CLI exposes.
    if not harness:
        harness, _level = _resolve_default_harness(root, key, manifest, cfg_row)
    try:
        _harness_name, harness_cfg = adapters.resolve(cfg, harness)
    except adapters.AdapterError as exc:
        raise ValueError(
            f"workflow {key!r}: invalid harness override {harness!r}: {exc}"
        ) from exc
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
    else:
        for st in stages:
            knobs[st["label"]]["model"] = _resolve_harness_model(
                harness_cfg, st, args)

    # Resolve EVERY stage's wall-clock budget BEFORE the dry-run return, so
    # `--dry-run` and the live run agree on `timeout_s`: the credential
    # decision the dry run already reflects is joined by the budget decision
    # — ONE resolution, ONE refusal path, no second copy to drift
    # (hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-
    # refused-run-key conjunct (3)). A budget that is not a positive number of
    # seconds is refused by NAME here, so `--dry-run` can no longer print OK
    # for a manifest the live run would refuse, no stage is started under it,
    # and no key is spent on it (conjunct (5) of hypothesis:l4-workflow-
    # residue-sub-floor-marker-dead-code-and-truncation; see
    # `_resolve_stage_timeout` for the definition of `0`). This also means a
    # manifest-level `timeout_s: 0` can no longer reach
    # `subprocess.run(timeout=0)` and silently kill every stage.
    stage_timeouts: dict[str, int] = {}
    stage_context_timeouts: dict[str, int] = {}
    for st in stages:
        try:
            stage_timeouts[st["label"]] = _resolve_stage_timeout(st, manifest)
            stage_context_timeouts[st["label"]] = \
                _resolve_context_timeout(st, manifest)
        except ValueError as exc:
            print(f"workflow.py: workflow={key} refused: {exc}",
                  file=sys.stderr)
            # rc 5, NOT 4: 4 is the stage return-parse error below, and a
            # caller must be able to tell a refused-before-any-stage run from
            # a stage that returned garbage (conjunct (4)).
            return 5

    if dry_run:
        # The credential decision BEFORE the dispatch lines, from the SAME
        # helper the live path mints through — reads only, never a mint.
        _would_mint, _reason = _credential_decision(root, cfg, harness)
        out.write(_credential_line(_would_mint, _reason) + "\n")
        for st in stages:
            out.write(_dispatching_line(st, knobs[st["label"]]) + "\n")
        out.write(f"[summary] workflow={key} harness={harness} "
                  f"stages={len(stages)} via dispatch.py kids\n")
        return 0

    view = RunView(key, stages, harness, out=out)
    view.run_started()
    if harness == "claude-code":
        # claude-code harness: the Workflow script is the runner; we only
        # resolve and describe — but through the SAME event stream the pi
        # path feeds, so the two surfaces differ only where execution does.
        # TWO callers reach here: (a) a NATIVE Claude Code session, whose
        # tool call we hand back exactly — the ONE registered name and the
        # resolved args — so the caller copy-pastes a call that runs; and
        # (b) a headless `--harness claude-code` run, which must say out loud
        # that it executed nothing (hypothesis:l4-a-workflow-run-on-the-
        # claude-code-harness-says-it-executed-nothing-and-names-the-two-real-
        # routes). The seam distinguishes them; the pi path never reaches here.
        if _claude_code_seam_present():
            # The registered workflow NAME is the script stem (`script` minus
            # `.js`), NEVER the config key: `review` -> `agi-round-review.js`
            # and `drafting` -> `agi-brief-drafting.js`, so formatting the key
            # would print two names that do not exist as `.claude/workflows/`
            # links and the copy-pasted call would fail.
            script = str(manifest.get("script") or "")
            wf_name = script[:-3] if script.endswith(".js") else script
            out.write(f"Workflow({json.dumps({'name': wf_name, 'args': args})})\n")
        else:
            print(f"workflow.py: no stage executed by workflow.py; "
                  f"{manifest.get('script')} runs under the Claude Code "
                  f"Workflow tool; a headless run is `--harness pi`",
                  file=sys.stderr)
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
    spawn_env, minted_key_hash = _resolve_workflow_spawn_env(
        root, cfg, run_key, harness, stages)
    if spawn_env is None:
        # A failed mint with no usable inherited key: refuse BY NAME, rc 3,
        # before any stage dispatches — a stage must never start on a
        # credential nothing verified (hypothesis:l4-pi-review-stages-...
        # item 5). The mint error is already on stderr verbatim.
        return 3
    # The minted key is revoked when the RUN ends, however it ends — success,
    # a stage failure (rc > 0) or a raised/timeout path — so the `finally` is
    # the whole point: a key that outlives its run is the falsifier this
    # closes (hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-
    # a-schema-miss-keeps-its-name conjunct (2)).
    try:
        prior_by_key: dict[tuple, dict] = {}
        # SM.105 isolation: `failed_keys` maps a base label (or a simple
        # stage's own label) to its failed repeat keys. The loop NEVER returns
        # on the first failure -- it marks THAT slice failed and continues,
        # skipping only stages that depend on a failed slice.
        failed_keys: dict[str, set] = {}
        first_rc: int | None = None
        for st in stages:
            dep = _failed_dependency(st, failed_keys)
            if dep is not None:
                view.stage_skipped(st["label"], f"dependency {dep!r} failed")
                print(f"workflow.py: workflow={key} skipped stage "
                      f"{st['label']} (dependency {dep!r} failed)",
                      file=sys.stderr)
                continue
            prior = None
            if "_repeat_key" in st and st.get("chained_from"):
                # `chained_from` over the same repeat key: the prior stage's
                # validated return merged into this stage's prompt context.
                prior = prior_by_key.get((st["chained_from"], st["_repeat_key"]))
            try:
                context_text = _stage_context(
                    repo, root, st, stage_context_timeouts[st["label"]])
            except (subprocess.TimeoutExpired, RuntimeError) as exc:
                # Fail THIS stage by name; siblings proceed under SM.105.
                reason = (f"context-build-timeout after {exc.timeout:g} s"
                          if isinstance(exc, subprocess.TimeoutExpired)
                          else f"context-build-failed: {exc}")
                view.stage_failed(st["label"], reason)
                print(f"workflow.py: workflow={key} stage {st['label']} "
                      f"{reason}", file=sys.stderr)
                if first_rc is None:
                    first_rc = 3
                failed_keys.setdefault(
                    st.get("_base_label", st["label"]), set()).add(
                        st.get("_repeat_key"))
                continue
            # The budget was resolved (declared, never truthy) before any
            # dispatch -- see `_resolve_stage_timeout` for `0` and the refusal.
            stage_timeout = stage_timeouts[st["label"]]
            rc, value = _run_stage_pi(
                cfg, st, knobs, args, out=out, view=view, prior=prior,
                spawn_env=spawn_env, context_text=context_text,
                timeout_s=stage_timeout)
            if value is not None:
                _persist_stage_value(root, run_key, st["label"], value)
                # A declared handoff list that came back EMPTY is a run-level
                # fact, not a stage failure: name it so a consumer can tell
                # "the stage dropped everything" from "the chain broke"
                # (the schema has no minItems, so both look identical).
                hfield = st.get("handoff_list")
                if (hfield and isinstance(value, dict)
                        and value.get(hfield) == []):
                    view.stage_empty_handoff(st["label"], hfield)
            if rc != 0:
                # MARK AND CONTINUE: this slice failed; siblings and every
                # independent stage still run. The run ends non-zero below.
                if first_rc is None:
                    first_rc = rc
                failed_keys.setdefault(
                    st.get("_base_label", st["label"]), set()).add(
                        st.get("_repeat_key"))
                print(f"workflow.py: workflow={key} stage {st['label']} "
                      f"failed (rc={rc}); continuing", file=sys.stderr)
                continue
            if "_repeat_key" in st and value is not None:
                prior_by_key[(st["_base_label"], st["_repeat_key"])] = value
        view.summary()
        _track_run(root, key, harness, view, run_key)
        return first_rc or 0
    finally:
        _revoke_run_credential(minted_key_hash, root)


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
    ap.add_argument("--root", default=argparse.SUPPRESS, help="explicit project root (default: walk up from cwd)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("run", help="resolve and run a workflow (the only sanctioned dispatch route)")
    rp.add_argument("name", help="config key (e.g. review, drafting) or agi-*.js script name")
    rp.add_argument("--harness", default=None,
                    help="harness declared in .agi/config.json (validated before run)")
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
    lk = sub.add_parser("link",
                        help="create the .claude/workflows/<script> symlinks for every registered workflow (idempotent)")
    nt = sub.add_parser("note",
                        help="record the claude-code harness's wf_ id beside a tracked run key")
    nt.add_argument("run_key",
                    help="descriptive run key to note the harness id against (e.g. mur-39)")
    nt.add_argument("--harness-id", required=True,
                    help="the harness-minted id to record (e.g. wf_ba530baa-dab)")
    val = sub.add_parser("validate",
                         help="check the registry invariant: agi-*.js <-> sibling <name>.json, and only implemented stages")
    for _p in sub.choices.values():
        _p.add_argument("--root", default=argparse.SUPPRESS, help="explicit project root")
    args = ap.parse_args(argv)

    root_arg = getattr(args, "root", None)
    root = _loc.find_project_root(start=root_arg)
    if root is None:
        where = f"--root {root_arg}" if root_arg else "cwd"
        print(f"workflow.py: no .agi project root found from {where}", file=sys.stderr)
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
    if args.cmd == "note":
        return note_workflow(root, args.run_key, args.harness_id)
    # the harness-resolution node may be absent (pre-prime) or a workflow may
    # declare an undeclared type: refuse LOUDLY naming the node, exit 2 — never
    # a traceback, never a silent literal fallback (hypothesis:
    # l4-workflow-types-and-default-harness-are-a-geometry-node).
    try:
        if args.cmd == "list":
            return list_workflows(root)
        if args.cmd == "status":
            return status_workflow(root, args.key)
        if args.cmd == "link":
            return link_workflows(root)
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
    except (WorkflowsNodeError, ValueError, adapters.AdapterError) as exc:
        print(f"workflow.py: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
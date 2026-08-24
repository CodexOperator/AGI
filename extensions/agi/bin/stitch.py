#!/usr/bin/env python3
"""stitch.py — materialize level-3 nodes back into a runnable directory tree.

Reads `<PROJECT>/nodes/level3/*.md` (the graph repo) and either:

  --out DIR     resolve every level-3 node's `payload_ref` against the
                **engine repo** and copy that file into DIR, preserving the
                repo-relative path (`extensions/agi/bin/metrics.py` lands at
                `DIR/extensions/agi/bin/metrics.py`). This is the "graph is
                the source of truth" round trip stated in `goal:g6.1`.

  --verify      write nothing; report drift between the graph and the live
                engine tree in four categories (see below). This is the more
                valuable mode — it is the thing a plain `cp -r` cannot do at
                all, because `cp -r` has no independent record of what the
                tree is *supposed* to contain.

**Be honest about what this is.** Source code lives on disk exactly once —
never inlined into a node (`hyp:level3-node-anatomy`). A level-3 node is a
pointer (`payload_ref`) plus a mechanically-derived contract of that file's
imports/exports. So for an *existing* repo, `--out` materialization is
near-identity: resolve 73 pointers, copy 73 files. It is not a compiler and
it does not reconstruct anything `cp -r extensions/agi DIR` would not also
produce, byte for byte, given the same source tree.

**What the graph adds that `cp -r` cannot**: `cp -r` has no opinion about
whether the tree it copied is *complete* or *correct* — it just moves bytes.
The graph is an independent, separately-mintable claim about what the tree
should contain, so it can be checked against the tree instead of trusted
blindly. `--verify` turns that claim into four concrete checks a `cp -r`
literally cannot perform because it has nothing to compare against:

  1. missing_payload   — a node's `payload_ref` no longer exists on disk
                          (the node outlived the code).
  2. orphan_files       — a file in level3.py's scan scope
                          (`extensions/agi/src/**/*.py`, `extensions/agi/
                          bin/*.py`) with no level-3 node claiming it (the
                          code outran the graph).
  3. duplicate_payload_ref — two or more nodes claim the same `payload_ref`
                          with no provable version order between them
                          (ambiguous materialization; the anatomy node says
                          reject this at mint time — level3.py does not
                          currently enforce that, so this is also a level3.py
                          gap this script surfaces, not just a stitch-time
                          check). **Exemption (`goal:g6.3`):** a well-formed
                          version chain — distinct, contiguous `version`
                          integers where every node but the lowest-versioned
                          one names its immediate predecessor (the group
                          member exactly one version below it) in
                          `supersedes` — is not drift. It is reported
                          separately under `version_chains` instead. Anything
                          not provably a chain (a version collision, a
                          `supersedes` pointing at the wrong id or an id
                          absent from the group, a version gap) stays here;
                          ambiguity is a defect, only a provable order is
                          exempt.
  4. stale_contracts    — a node's contract block (the mechanically-derived
                          `how` half: imports, top-level defs, read/write
                          call sites) no longer matches what re-running the
                          *same* derivation against the *current* file would
                          produce. A node with no contract block at all is
                          reported under `unreadable_contracts` (drift) —
                          *except* a node stamped `origin: build-version`
                          with an *absent* block (no LEVEL3-CONTRACT markers
                          at all), which is not-yet-derived by design
                          (`level3.py` owns the contract shape and has not
                          been pointed at build-version nodes) and is
                          reported separately under `contracts_not_derived`
                          instead — informational, not drift. A block that
                          *is present but malformed* (bad YAML, truncated,
                          wrong shape) is never exempted by this, on any
                          node: that stays `unreadable_contracts` regardless
                          of origin, because a broken block is a real defect,
                          not an absent one.

On (4): the obvious design is a content hash of the source recorded in the
contract block at mint time, compared against a hash of the current file.
This script does **not** do that, and the reason is not laziness — it is
strictly worse than what it does instead, for this specific job:

  - No node in the corpus carries a mint-time hash (level3.py, which this
    script does not own, never wrote one) — there is nothing to compare
    against retroactively for the 73 real nodes. A hash-based check could
    only start protecting nodes minted *after* the generator is changed to
    add one; it is silent about every node that already exists.
  - A hash is binary (changed / not changed) and coarse — it fires on a
    changed docstring or a renamed local variable exactly as loudly as it
    fires on a changed import. It cannot say *what* drifted, so a human (or
    another agent) still has to re-derive the contract by hand to find out,
    which is the same `ast` walk this script already needs to do to compute
    the hash's comparison target in the first place. The hash adds a stored
    field and a mint-time write path; it does not remove the recompute step.
  - `how` is *specified* as mechanically reproducible (`hyp:level3-node-
    anatomy`, `exp:level3-scan-r1`) — deterministic given the same source
    text and the same `ast`-walk code. That means the freshness check does
    not need a stored fingerprint at all: this script re-runs the exact
    same derivation level3.py used (`level3.analyze_file`, imported by file
    path, never re-implemented — same reuse discipline level3.py itself
    uses for `write_frontmatter`) and diffs the result against what is
    stored, entry by entry. That is strictly more informative than a hash
    match/mismatch, and it costs nothing extra to store — the file is
    already being read for the missing/orphan checks in the same pass.

What a hash *would* still buy, and what this script cannot claim instead:
change detection that does not require re-running the deriving code, i.e. a
freshness check for a language `ast` cannot parse, or a `how` derivation
that stops being a pure function of the file (grows external inputs). The
recompute approach used here is coupled to `level3.py` staying importable
and staying a pure function of file content — a real cost, named plainly:
if `analyze_file`'s logic changes shape (new fields, new heuristics) without
this script's comparison logic changing to match, every existing node looks
"stale" even though nothing about the underlying code moved. That false
positive is not hypothetical — it is exactly what happens the day someone
edits level3.py's derivation and forgets this script exists. There is no
mint-time marker that would help there either; only keeping the two files
walked together (as this script already notes it must) prevents it.

**Scope limits, stated plainly:**

  - Materialization treats every node under `nodes/level3/*.md` as canonical
    (copies its `payload_ref`). The anatomy node describes a possible future
    "non-canonical / sub-file" node that would be read-only and skipped —
    no such node currently exists in the real corpus (verified: all 73 are
    one-node-per-file, per `exp:level3-scan-r1`) and there is no frontmatter
    field distinguishing the two shapes yet, so this script cannot honor
    that distinction; it is not implemented, not silently ignored.
  - `--verify`'s orphan-file scan reuses `level3.discover_files`'s scope
    definition exactly (imported, not reimplemented) so "orphan" always
    means "outside the graph but inside level3.py's own declared scope" —
    never a guess at what *should* have been scanned.
  - Non-`.py` engine files (`driver.sh`, the TypeScript bridge) have no
    level-3 nodes at all today and are correctly invisible to every check
    here — they are out of level3.py's scope, not silently dropped by this
    script.

Run:
    python3 bin/stitch.py --project PATH --verify [--engine-root PATH] [--strict]
    python3 bin/stitch.py --project PATH --out DIR [--engine-root PATH] [--force]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import yaml

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent  # .../extensions/agi
# Same convention as level3.py / decompose-engine.py: this script lives at
# <engine repo root>/extensions/agi/bin/stitch.py, so three levels up is the
# engine repo root. Overridable with --engine-root, chiefly for tests.
DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]


class StitchSafetyError(Exception):
    """Raised when an operation would write somewhere it must not."""


# --- reuse level3.py verbatim (imported by file path, never re-implemented) --
# `analyze_file` is the exact mechanical derivation that minted every stored
# contract; `discover_files` is the exact scope definition that decides what
# is in-graph vs. out-of-graph. Re-implementing either here would let this
# script's idea of "the file" or "the scope" quietly drift from level3.py's —
# precisely the failure mode this script exists to catch in the *nodes*, so
# it cannot be allowed to happen between these two files either.
_LEVEL3_PATH = BIN_DIR / "level3.py"
_spec = importlib.util.spec_from_file_location("level3_for_stitch", _LEVEL3_PATH)
level3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(level3)


# --- level-3 node loading (read-only; never touches nodes/level3/) -----------

_MARKER_SPAN_RE = re.compile(r"LEVEL3-CONTRACT:BEGIN(.*?)LEVEL3-CONTRACT:END", re.DOTALL)
_YAML_FENCE_OPEN = "```yaml"
_FENCE = "```"

# The exact `_extract_contract` reason string for "no markers at all" — the
# one contract_error that means *absent*, as opposed to *present but broken*
# (bad YAML, truncated, wrong shape). Only this exact reason, on a node
# stamped `origin: build-version`, is eligible for the `contracts_not_derived`
# exemption below; every other reason (and every other origin) stays drift.
_NO_CONTRACT_BLOCK = "no LEVEL3-CONTRACT block found in body"
_BUILD_VERSION_ORIGIN = "build-version"


class Level3Node:
    __slots__ = ("node_id", "path", "fm", "body", "payload_ref", "contract",
                 "contract_error", "version", "supersedes", "origin")

    def __init__(self, node_id, path, fm, body, payload_ref, contract, contract_error,
                 version=1, supersedes=None, origin=None):
        self.node_id = node_id
        self.path = path
        self.fm = fm
        self.body = body
        self.payload_ref = payload_ref
        self.contract = contract          # parsed dict, or None
        self.contract_error = contract_error  # str reason contract is None, or None
        self.version = version            # int; frontmatter `version`, default 1
        self.supersedes = supersedes      # str node_id, or None (frontmatter `supersedes`)
        self.origin = origin              # str frontmatter `origin`, or None


def _parse_frontmatter(text: str) -> tuple[dict, str] | None:
    """Split a node file into (frontmatter dict, body). None if malformed."""
    if not text.strip().startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, parts[2]


def _extract_contract(body: str) -> tuple[dict | None, str | None]:
    """Pull the fenced YAML contract block out of a node body.

    Returns (contract_dict, None) on success, (None, reason) on failure. A
    node with no contract markers, or an unparsable contract, is reported —
    never silently treated as fresh (that would hide exactly the kind of
    drift this tool exists to find).

    Bounding matters more than it looks: a `how` field can (and, on the real
    corpus, does — `level3:bin-heal`) contain a mechanically-unparsed call
    site whose literal text itself embeds a ``` fence, e.g. an f-string
    template being written to disk that contains a markdown code block. A
    naive "first ``` after ```yaml" search stops at that embedded fence, not
    the real closing one, and truncates the block mid-string — invalid YAML,
    not because the file is malformed but because the *parser* guessed
    wrong. `level3.py`'s own writer already had to solve this for the same
    reason (its `_cap` truncation exists downstream of the same problem);
    this reader solves it the same way: bound first by the harness markers
    (`LEVEL3-CONTRACT:BEGIN`/`:END`, which the model-authored prose can only
    ever appear *outside* of), then take the *last* ``` inside that bounded
    span as the closing fence, not the first.
    """
    span_m = _MARKER_SPAN_RE.search(body)
    if not span_m:
        return None, "no LEVEL3-CONTRACT block found in body"
    span = span_m.group(1)
    open_idx = span.find(_YAML_FENCE_OPEN)
    if open_idx == -1:
        return None, "no ```yaml fence found inside LEVEL3-CONTRACT block"
    after_open = span[open_idx + len(_YAML_FENCE_OPEN):]
    if after_open.startswith("\n"):
        after_open = after_open[1:]
    close_idx = after_open.rfind(_FENCE)
    if close_idx == -1:
        return None, "no closing ``` fence found inside LEVEL3-CONTRACT block"
    yaml_text = after_open[:close_idx]
    try:
        contract = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return None, f"contract block is not valid YAML: {exc}"
    if not isinstance(contract, dict):
        return None, "contract block did not parse to a mapping"
    return contract, None


def load_level3_nodes(project_root: Path) -> tuple[list[Level3Node], list[str]]:
    """All `type: level3` nodes under `<project_root>/nodes/level3/*.md`.

    Returns (nodes, warnings). A missing `nodes/level3/` directory degrades
    to an empty list with a warning, never an exception — the tree it would
    describe just has no level-3 layer yet, which is a fact to report, not
    a crash.
    """
    warnings: list[str] = []
    level3_dir = project_root / "nodes" / "level3"
    if not level3_dir.is_dir():
        warnings.append(f"no nodes/level3/ directory under {project_root} — 0 nodes")
        return [], warnings

    nodes: list[Level3Node] = []
    for md_path in sorted(level3_dir.glob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as exc:
            warnings.append(f"{md_path}: unreadable ({exc}) — skipped")
            continue
        parsed = _parse_frontmatter(text)
        if parsed is None:
            warnings.append(f"{md_path}: malformed frontmatter — skipped")
            continue
        fm, body = parsed
        if fm.get("type") != "level3":
            warnings.append(f"{md_path}: type={fm.get('type')!r}, not 'level3' — skipped")
            continue
        node_id = fm.get("id") or f"<unknown:{md_path.name}>"
        payload_ref = fm.get("payload_ref")
        payload_ref = payload_ref if isinstance(payload_ref, str) and payload_ref else None
        # `version` (G6.3, origin: build-version): defaults to 1 when absent —
        # that is the normal, unremarkable shape of every node minted before
        # this iteration. A *present but non-integer* value is different: it
        # means the frontmatter is malformed, and a malformed version must not
        # crash the load (same "degrade, report, never abort" discipline as
        # the rest of this loader) — coerce to 1 and warn instead.
        version_raw = fm.get("version", 1)
        try:
            version = int(version_raw)
        except (TypeError, ValueError):
            warnings.append(f"{md_path}: version={version_raw!r} is not an integer "
                             f"— treated as 1")
            version = 1
        supersedes = fm.get("supersedes")
        supersedes = supersedes if isinstance(supersedes, str) and supersedes else None
        origin = fm.get("origin")
        origin = origin if isinstance(origin, str) and origin else None
        contract, contract_error = _extract_contract(body)
        nodes.append(Level3Node(node_id, md_path, fm, body, payload_ref,
                                 contract, contract_error, version, supersedes, origin))
    return nodes, warnings


# --- verify: the four drift categories ---------------------------------------


def _entry_pairs(entries) -> Counter:
    if not isinstance(entries, list):
        return Counter()
    return Counter((e.get("name"), e.get("how")) for e in entries if isinstance(e, dict))


def diff_contract(stored: dict, fresh: dict) -> dict | None:
    """Structured diff between a stored contract and a freshly-derived one.

    Compares only the harness-mechanical slots: `parse_ok`/`parse_error` and
    the `(name, how)` pair of every `inputs`/`outputs`/`uncovered` entry.
    Never compares `why`/`perf`/`security` — those are free-text, model-owned,
    and not mechanically reproducible by design (`hyp:level3-node-anatomy`),
    so a mismatch there is not drift, it is the model doing its job.
    Returns None if nothing mechanical differs, else a dict of differences.
    """
    diffs: dict = {}
    if stored.get("parse_ok") != fresh.get("parse_ok"):
        diffs["parse_ok"] = {"stored": stored.get("parse_ok"), "fresh": fresh.get("parse_ok")}
    if stored.get("parse_error") != fresh.get("parse_error"):
        diffs["parse_error"] = {"stored": stored.get("parse_error"),
                                 "fresh": fresh.get("parse_error")}
    for bucket in ("inputs", "outputs", "uncovered"):
        stored_c = _entry_pairs(stored.get(bucket))
        fresh_c = _entry_pairs(fresh.get(bucket))
        if stored_c != fresh_c:
            diffs[bucket] = {
                "added": [{"name": n, "how": h} for n, h in (fresh_c - stored_c).elements()],
                "removed": [{"name": n, "how": h} for n, h in (stored_c - fresh_c).elements()],
            }
    return diffs or None


def _group_by_payload_ref(nodes: list[Level3Node]) -> dict[str, list[Level3Node]]:
    """Group nodes with a `payload_ref` by that ref, preserving `nodes`' own
    order within each group (i.e. `nodes/level3/*.md` filename-sorted order,
    per `load_level3_nodes`). Nodes with no `payload_ref` are excluded, same
    as every other check in this file."""
    groups: dict[str, list[Level3Node]] = {}
    for n in nodes:
        if n.payload_ref:
            groups.setdefault(n.payload_ref, []).append(n)
    return groups


def _is_well_formed_chain(group: list[Level3Node]) -> bool:
    """True iff `group` (all nodes sharing one `payload_ref`, size > 1) is a
    provably ordered version chain, per `goal:g6.3`'s convention:

      - every node has a distinct integer `version`;
      - sorted ascending, those versions form a contiguous run with no gaps
        (`max - min + 1 == len(group)` — a missing version would leave an
        orphan with no defined predecessor, so it is not a chain);
      - every node except the one with the lowest version has `supersedes`
        equal to the `node_id` of the group member exactly one version below
        it (its immediate predecessor).

    Any other shape — a version collision, `supersedes` naming the wrong
    predecessor or an id that is not in the group at all, a version gap —
    returns False. This function does not try to salvage a partial order out
    of that; ambiguity is a defect, and the caller reports the whole group as
    `duplicate_payload_ref`, exactly as it did before chains existed.
    """
    if len(group) < 2:
        return False
    versions = [n.version for n in group]
    if len(set(versions)) != len(versions):
        return False  # two (or more) nodes claim the same version
    by_version = {n.version: n for n in group}
    lo, hi = min(versions), max(versions)
    if hi - lo + 1 != len(group):
        return False  # a gap: some version in [lo, hi] has no node at all
    for v in range(lo + 1, hi + 1):
        if by_version[v].supersedes != by_version[v - 1].node_id:
            return False  # wrong predecessor, or supersedes points outside the group
    return True


def _chain_order(group: list[Level3Node]) -> list[str]:
    """Node ids of a well-formed chain, ascending by version (v1 -> v2 -> ...)."""
    return [n.node_id for n in sorted(group, key=lambda n: n.version)]


def verify_tree(project_root: Path, engine_root: Path) -> dict:
    """Report drift between the graph (`nodes/level3/`) and the live engine tree.

    Writes nothing. Degrades instead of raising: a missing/unreadable engine
    root is reported as its own condition and every check that needs the
    tree is skipped (not guessed), matching the rest of this repo's recent
    "diagnostics degrade instead of lying or aborting" discipline.
    """
    t0 = time.perf_counter()
    nodes, warnings = load_level3_nodes(project_root)

    engine_readable = engine_root.is_dir()
    if not engine_readable:
        warnings.append(f"engine root {engine_root} is missing or unreadable — "
                         f"payload/orphan/staleness checks skipped")

    scope_files: list[str] | None = level3.discover_files(engine_root) if engine_readable else None
    if engine_readable and scope_files is None:
        warnings.append(f"engine root {engine_root} is not a git repo — "
                         f"orphan-file check skipped")

    # --- category 3: duplicate payload_ref (+ informational version_chains) --
    ref_groups = _group_by_payload_ref(nodes)
    duplicate_payload_ref: dict[str, list[str]] = {}
    version_chains: dict[str, list[str]] = {}
    for ref, group in ref_groups.items():
        if len(group) < 2:
            continue
        if _is_well_formed_chain(group):
            version_chains[ref] = _chain_order(group)
        else:
            duplicate_payload_ref[ref] = [n.node_id for n in group]

    # --- category 1: missing payload ------------------------------------------
    missing_payload = []
    if engine_readable:
        for n in nodes:
            if not n.payload_ref:
                continue
            if not (engine_root / n.payload_ref).is_file():
                missing_payload.append({"node_id": n.node_id, "payload_ref": n.payload_ref})

    # --- category 2: orphan files ----------------------------------------------
    orphan_files: list[str] = []
    if scope_files is not None:
        claimed = {n.payload_ref for n in nodes if n.payload_ref}
        orphan_files = sorted(set(scope_files) - claimed)

    # --- category 4: stale / unreadable / not-yet-derived contracts -----------
    # A node with `contract is None` splits two different facts that used to
    # be conflated under one `unreadable_contracts` bucket:
    #   - *absent*: no LEVEL3-CONTRACT block at all, on a node stamped
    #     `origin: build-version`. Those nodes are hand-authored prose by
    #     design (`level3.py` owns the contract shape and has not derived one
    #     for them yet) — informational, not drift.
    #   - everything else (a block that is present but malformed, truncated,
    #     wrong shape; or an absent block on a node NOT stamped
    #     `origin: build-version`, e.g. a `level3-scan` node that lost its
    #     block — a genuine generator failure): stays `unreadable_contracts`,
    #     stays drift, exactly as before this split existed.
    stale_contracts = []
    unreadable_contracts = []
    contracts_not_derived = []
    for n in nodes:
        if not n.payload_ref or not engine_readable:
            continue
        abs_path = engine_root / n.payload_ref
        if not abs_path.is_file():
            continue  # already reported under missing_payload
        if n.contract is None:
            if n.origin == _BUILD_VERSION_ORIGIN and n.contract_error == _NO_CONTRACT_BLOCK:
                contracts_not_derived.append({"node_id": n.node_id,
                                               "reason": n.contract_error})
            else:
                unreadable_contracts.append({"node_id": n.node_id,
                                              "reason": n.contract_error})
            continue
        fresh = level3.analyze_file(abs_path)
        diff = diff_contract(n.contract, fresh)
        if diff is not None:
            stale_contracts.append({"node_id": n.node_id,
                                     "payload_ref": n.payload_ref,
                                     "diff": diff})

    runtime = time.perf_counter() - t0
    return {
        "project_root": str(project_root),
        "engine_root": str(engine_root),
        "engine_readable": engine_readable,
        "nodes_total": len(nodes),
        "scope_files_total": len(scope_files) if scope_files is not None else None,
        "missing_payload": missing_payload,
        "orphan_files": orphan_files,
        "duplicate_payload_ref": duplicate_payload_ref,
        "version_chains": version_chains,
        "stale_contracts": stale_contracts,
        "unreadable_contracts": unreadable_contracts,
        "contracts_not_derived": contracts_not_derived,
        "warnings": warnings,
        "runtime_seconds": runtime,
    }


def has_drift(report: dict) -> bool:
    return bool(report["missing_payload"] or report["orphan_files"]
                or report["duplicate_payload_ref"] or report["stale_contracts"]
                or report["unreadable_contracts"])


# --- materialize: write payload_ref files into an output tree ----------------


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _guard_out_dir(out_dir: Path, project_root: Path, engine_root: Path) -> None:
    """Refuse to write into the graph repo or the engine repo, ever."""
    out_r = out_dir.resolve()
    for forbidden, label in ((project_root, "graph repo"), (engine_root, "engine repo")):
        forbidden_r = forbidden.resolve()
        if _is_within(out_r, forbidden_r):
            raise StitchSafetyError(
                f"--out {out_dir} resolves inside the {label} ({forbidden_r}); refusing to write")


def materialize(project_root: Path, engine_root: Path, out_dir: Path,
                 force: bool = False, version: int | None = None) -> dict:
    """Copy every level-3 node's `payload_ref` from the engine tree into `out_dir`.

    Preserves the repo-relative path. Refuses to write into a non-empty
    `out_dir` unless `force=True`, and refuses unconditionally to write
    into `project_root` or `engine_root` (no force override for that — it
    is not a policy choice, it is data-loss prevention).

    Exactly one node is materialized per `payload_ref`:

      - A lone node for that ref: materialized as-is (unless `version` is
        given and does not match, see below).
      - A well-formed version chain (`_is_well_formed_chain`): materializes
        the **chain head** — the highest-versioned member — deterministically.
        This replaces the old "first writer wins" behavior for chains, which
        depended on filename sort order rather than on anything meaningful.
      - A genuine duplicate (anything not a provable chain): today's
        behavior, unchanged — first writer (by `nodes/level3/*.md` filename
        order) wins, the rest are reported under `skipped_duplicate`. This
        function does not start guessing at an order that the graph itself
        does not establish.

    `version`, when given, overrides "head wins" for chains: it materializes
    whichever chain member carries that exact version, and reports (never
    raises) any `payload_ref` whose chain has no such member under
    `skipped_no_version`. It does not attempt to resolve genuine duplicates —
    an ambiguous group stays ambiguous regardless of `version`.
    """
    t0 = time.perf_counter()
    _guard_out_dir(out_dir, project_root, engine_root)

    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise StitchSafetyError(
            f"{out_dir} is non-empty; refusing to write without --force")

    nodes, warnings = load_level3_nodes(project_root)
    if not engine_root.is_dir():
        warnings.append(f"engine root {engine_root} is missing or unreadable — nothing written")
        return {
            "nodes_total": len(nodes), "written": 0, "bytes_written": 0,
            "skipped_missing": [], "skipped_duplicate": [], "skipped_no_version": [],
            "chains_materialized": {}, "warnings": warnings,
            "runtime_seconds": time.perf_counter() - t0,
        }

    out_dir.mkdir(parents=True, exist_ok=True)

    ref_groups = _group_by_payload_ref(nodes)

    # --- decide exactly one target node (or none) per payload_ref ------------
    targets: list[Level3Node] = []
    skipped_duplicate: list[str] = []
    skipped_no_version: list[str] = []
    chains_materialized: dict[str, str] = {}

    for ref in sorted(ref_groups.keys()):
        group = ref_groups[ref]
        if len(group) == 1:
            node = group[0]
            if version is not None and node.version != version:
                skipped_no_version.append(ref)
                continue
            targets.append(node)
            continue

        if _is_well_formed_chain(group):
            if version is not None:
                node = next((n for n in group if n.version == version), None)
                if node is None:
                    skipped_no_version.append(ref)
                    continue
            else:
                node = max(group, key=lambda n: n.version)  # chain head
            targets.append(node)
            chains_materialized[ref] = node.node_id
        else:
            # genuine duplicate: unchanged from before chains existed —
            # first writer (original nodes list order) wins, rest reported.
            winner, *rest = group
            targets.append(winner)
            skipped_duplicate.extend(n.node_id for n in rest)

    written = 0
    bytes_written = 0
    skipped_missing: list[str] = []

    for n in targets:
        src = engine_root / n.payload_ref
        if not src.is_file():
            skipped_missing.append(n.node_id)
            continue
        dst = out_dir / n.payload_ref
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        written += 1
        bytes_written += src.stat().st_size

    return {
        "nodes_total": len(nodes),
        "written": written,
        "bytes_written": bytes_written,
        "skipped_missing": skipped_missing,
        "skipped_duplicate": skipped_duplicate,
        "skipped_no_version": skipped_no_version,
        "chains_materialized": chains_materialized,
        "warnings": warnings,
        "runtime_seconds": time.perf_counter() - t0,
    }


# --- reporting -----------------------------------------------------------


def print_verify_report(report: dict) -> None:
    print(f"stitch --verify: project={report['project_root']}")
    print(f"  engine root: {report['engine_root']} "
          f"({'ok' if report['engine_readable'] else 'UNREADABLE'})")
    print(f"  level-3 nodes: {report['nodes_total']}")
    if report["scope_files_total"] is not None:
        print(f"  in-scope engine files: {report['scope_files_total']}")
    for w in report["warnings"]:
        print(f"  WARN: {w}")

    print(f"\n  [1] missing_payload: {len(report['missing_payload'])}")
    for m in report["missing_payload"]:
        print(f"      {m['node_id']} -> {m['payload_ref']} (does not exist)")

    print(f"  [2] orphan_files: {len(report['orphan_files'])}")
    for f in report["orphan_files"]:
        print(f"      {f} (no level-3 node)")

    print(f"  [3] duplicate_payload_ref: {len(report['duplicate_payload_ref'])}")
    for ref, ids in report["duplicate_payload_ref"].items():
        print(f"      {ref} <- {', '.join(ids)}")
    print(f"      version_chains (informational, not drift): "
          f"{len(report['version_chains'])}")
    for ref, ids in report["version_chains"].items():
        print(f"      {ref}: {' -> '.join(ids)}")

    print(f"  [4] stale_contracts: {len(report['stale_contracts'])} "
          f"(+ {len(report['unreadable_contracts'])} unreadable)")
    for s in report["stale_contracts"]:
        buckets = ", ".join(sorted(s["diff"].keys()))
        print(f"      {s['node_id']} ({s['payload_ref']}): drift in {buckets}")
    for u in report["unreadable_contracts"]:
        print(f"      {u['node_id']}: {u['reason']}")
    print(f"      contracts_not_derived (informational, not drift): "
          f"{len(report['contracts_not_derived'])}")
    for c in report["contracts_not_derived"]:
        print(f"      {c['node_id']}: {c['reason']}")

    print(f"\n  runtime: {report['runtime_seconds']:.3f}s")


def print_materialize_report(stats: dict) -> None:
    print(f"stitch materialize: {stats['nodes_total']} level-3 node(s) considered")
    print(f"  written: {stats['written']} file(s), {stats['bytes_written']} byte(s)")
    if stats.get("chains_materialized"):
        print(f"  version chains resolved (head wins unless --version): "
              f"{len(stats['chains_materialized'])}")
        for ref, node_id in stats["chains_materialized"].items():
            print(f"    {ref} -> {node_id}")
    if stats["skipped_missing"]:
        print(f"  skipped (payload_ref missing on disk): {len(stats['skipped_missing'])}")
        for nid in stats["skipped_missing"]:
            print(f"    {nid}")
    if stats["skipped_duplicate"]:
        print(f"  skipped (duplicate payload_ref, first writer wins): "
              f"{len(stats['skipped_duplicate'])}")
        for nid in stats["skipped_duplicate"]:
            print(f"    {nid}")
    if stats.get("skipped_no_version"):
        print(f"  skipped (no chain member at the requested --version): "
              f"{len(stats['skipped_no_version'])}")
        for ref in stats["skipped_no_version"]:
            print(f"    {ref}")
    for w in stats["warnings"]:
        print(f"  WARN: {w}")
    print(f"  runtime: {stats['runtime_seconds']:.3f}s")


# --- main ------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Materialize level-3 nodes into a directory tree, or "
                     "verify the graph against the live engine tree without writing.")
    ap.add_argument("--project", required=True, help="graph repo root (has nodes/level3/)")
    ap.add_argument("--out", default=None,
                     help="destination directory for materialization "
                          "(required unless --verify)")
    ap.add_argument("--engine-root", default=None,
                     help="override the engine repo root (default: this script's own repo)")
    ap.add_argument("--force", action="store_true",
                     help="allow writing into a non-empty --out directory")
    ap.add_argument("--version", type=int, default=None,
                     help="with --out, materialize this version of every version "
                          "chain that has it, instead of the chain head "
                          "(default: highest version). A payload_ref with no "
                          "member at this version is skipped and reported, "
                          "never guessed.")
    ap.add_argument("--verify", action="store_true",
                     help="report drift only; write nothing")
    ap.add_argument("--strict", action="store_true",
                     help="with --verify, exit 1 if any drift is found")
    args = ap.parse_args(argv)

    project_root = Path(args.project).resolve()
    engine_root = Path(args.engine_root).resolve() if args.engine_root else DEFAULT_ENGINE_ROOT

    if args.verify:
        report = verify_tree(project_root, engine_root)
        print_verify_report(report)
        if args.strict and has_drift(report):
            return 1
        return 0

    if not args.out:
        print("ERROR: --out is required unless --verify", file=sys.stderr)
        return 2
    out_dir = Path(args.out).resolve()
    try:
        stats = materialize(project_root, engine_root, out_dir, force=args.force,
                             version=args.version)
    except StitchSafetyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print_materialize_report(stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

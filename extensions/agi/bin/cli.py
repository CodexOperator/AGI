#!/usr/bin/env python3
"""cli.py — agent-facing completion + verdict-emission CLI.

Agents call this to signal they're done. The driver picks up the rest.

Subcommands:
  done <iter_n> <agent_id> --verdict X --confidence Y [--node-id Z] [--parent P] [--notes ...]
  pending <iter_n> <agent_id> --reason "stuck on X"
  scaffold <iter_n> <agent_id> --type <node_type> --parent <parent_id> --slug <slug>
  status <iter_n>      — print all agent statuses for iter

`<iter_n>` is a legacy number (`1039` -> `sessions/iter-1039`) or a loop-scoped
id (`L1.08` -> `sessions/iter-L1.08`); `locations.iteration_id` parses both.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_gate  # noqa: E402
import frontmatter  # noqa: E402
import geometry_config  # noqa: E402
import locations  # noqa: E402
import node_writer  # noqa: E402
import spawn_budget  # noqa: E402
from evidence_gate import VERDICT_HELP, VERDICT_RE  # noqa: E402

# goal:s17 -- the type table and the scaffold routine both live in
# `bin/node_writer.py` now, and every writer imports them from there. They used
# to live here AND in `bin/dispatch.py`, whose copy was never gated and still
# minted the hyphenated spellings `[shape].md` calls non-canonical. Re-exported
# under the old names because `argparse` reads `NODE_TYPES` a few lines below
# and the `scaffold`/`done` help text is a documented surface.
#
# `idea` and `task` are in the table for a reason worth keeping written down:
# both are heavily used -- 71 and 91 nodes -- and neither could be created by
# the tool whose job is creating nodes, which is why the S17 falsifier "write a
# task with three parents" could not even be attempted through this path until
# S17. `idea` also matters as the only non-goal parentless-legal type, so it is
# the shape that proves `min_parents: 0` is honoured rather than merely declared.
CANONICAL_NODE_TYPES = node_writer.CANONICAL_NODE_TYPES
TYPE_ALIASES = node_writer.TYPE_ALIASES
NODE_TYPES = node_writer.NODE_TYPES


def _find_root() -> Path:
    """The graph root for cwd, via the one shared resolver (goal:g11.1).

    The walk this replaced knew only the legacy marker names, so under the
    goal:g11 layout it walked past `<repo>/.agi/` to `/` and exited 1 — every
    subcommand here was unusable in a migrated repo.
    """
    root = locations.find_project_root()
    if root is None:
        print("ERR: no agi project found from cwd up", file=sys.stderr)
        sys.exit(1)
    return root


def _session_root() -> Path:
    """The LOCAL session-dir root; iteration dirs resolve to the worktree.

    hypothesis:l4-seat-session-iter-dirs (half a) — iter-<id>/ and everything
    under them (the per-agent `agent.json`, the iteration `manifest.json`,
    `output.log`, `context.md`) belong to the WORKTREE that made them, so a
    seat harvests its own round from its own tree. This REVERSES the L3.38
    `l3-cli-done-worktree-manifest` rule that routed the record through
    `locations.shared_project_root` into the MAIN checkout (bookkeeping was
    "one body across worktrees", like the budget / comms / meter pins — but
    iteration dirs are not a tree-wide bound, so only the budget / comms /
    meter pins still resolve shared). Callers that READ fall back to the main
    checkout (via `_legacy_fallback`) when the local tree lacks the specific
    record, so an in-flight round whose manifest predates this change keeps
    resolving; the graph a kid edits is still the worktree's fork.
    """
    return _find_root()


def _legacy_fallback(local_root: Path, path: Path) -> Path:
    """Local-first, shared-fallback for one session file (hypothesis:
    l4-seat-session-iter-dirs, half a). Returns `path` unchanged when it
    exists under the local root; otherwise re-resolves it under the MAIN
    checkout, so records that predate the resolution change (or belong to a
    seat whose dirs live in main) still resolve. `done`/`pending`/`scaffold`
    write to whichever path this returns, keeping the record in the tree that
    already owns it.
    """
    if path.exists():
        return path
    shared = locations.shared_project_root(local_root) or local_root
    if shared == local_root:
        return path
    try:
        rel = path.relative_to(local_root)
    except ValueError:
        return path
    shared_path = shared / rel
    # Fall back to shared ONLY when the shared record actually exists.
    # Returning the shared path unconditionally routed a brand-new record
    # (present in NEITHER place) into main, reinstating the very routing
    # L4.37 reverses. A record that exists nowhere belongs to the LOCAL tree
    # that is creating it, not to main. (hypothesis:
    # l4-complete-and-fallback-invariants)
    if shared_path.exists():
        return shared_path
    return path


def _agent_path(root: Path, iter_n: int | str, agent_id: str) -> Path:
    # `iter_n` is a legacy int (`iter-007`) or a loop-scoped str (`iter-L1.08`);
    # `locations` is the one place either is spelled as a directory.
    return locations.iteration_dir(root, iter_n) / agent_id / "agent.json"


def _sibling_session_lookup(local_root: Path, path: Path) -> Path | None:
    """Union every linked git worktree's session dir, for one record.

    hypothesis:l4-a-branch-parent-cannot-signal-done (the THREE-TREE case). A
    `--branch` parent dispatched from a SEAT worktree has its `agent.json`
    written by the DISPATCHER into the SEAT's own session dir — dispatch.py
    resolves `sess_root = root` (the DISPATCHER's worktree), so the record is
    in NEITHER the parent's own worktree NOR the main checkout. The
    local->main `_legacy_fallback` therefore cannot reach it, and the parent's
    `done` refuses ("no agent record"). This resolves the record across every
    linked git worktree, exactly as `_evidence_corpus` unions every worktree's
    NODE corpus so a worktree-resident experiment resolves for `score`.

    Mirror of that deliberate tolerance: a half-created worktree (no `.agi`
    graph yet) must not take the lookup down, and an unreadable tree
    contributes nothing. Returns `None` when the record lives in none of
    local/main/sibling worktree — the caller's own refusal stays the source
    of truth for "absent", so absence stays distinguishable from a wrong
    lookup.
    """
    if not path.name == "agent.json":
        return None
    # The main checkout's graph root — siblings hang off `.agi/worktrees/`
    # (the harness places every linked worktree under the main graph tree,
    # exactly as the real repo does; a legacy layout with no worktrees just
    # has an absent `worktrees/` dir and this is a no-op).
    main = locations.git_common_root(local_root)
    main_graph = locations.find_project_root(main) if main else None
    if not main_graph:
        return None
    wt_root = main_graph / "worktrees"
    if not wt_root.is_dir():
        return None
    try:
        rel = path.relative_to(local_root)
    except ValueError:
        return None
    for tree in sorted(wt_root.glob("*")):
        if not tree.is_dir():
            continue
        sg = tree / ".agi"
        if not (sg / "config.json").is_file():
            continue
        cand = sg / rel
        if cand.is_file():
            return cand
    return None


def _resolve_session_record(sroot: Path, ap: Path) -> Path:
    """local -> main (`_legacy_fallback`) -> sibling worktrees.

    The one resolver `done`/`pending` use, so the SEAT-dispatched
    three-tree case (hypothesis:l4-a-branch-parent-cannot-signal-done)
    reaches the record wherever the dispatcher wrote it. Returns the FOUND
    path, or the unchanged local `ap` when the record lives in none of the
    three trees — the caller's `ap.exists()` refusal then still fires, so
    absence stays distinguishable from a wrong lookup and `done` never
    creates the record it then reads.
    """
    resolved = _legacy_fallback(sroot, ap)
    if resolved.exists():
        return resolved
    sib = _sibling_session_lookup(sroot, ap)
    return sib if sib is not None else resolved


def _evidence_corpus(root: Path) -> frozenset:
    """The evidence gate's corpus: the trees the cite-able nodes live in.

    hypothesis:l3w4-branch-tooling-blind (claim i). A `--branch` kid's node
    lives ONLY in its own git worktree (`<main>/.agi/worktrees/<slug>/`),
    so a parent reviewing that kid from the main checkout sees the gate
    built from `build_corpus(root / "nodes")` alone -> the kid's id does not
    resolve -> the parent's decisive `proved` is auto-demoted to a lean even
    though a real node was cited (L3.33/L3.34: every kid verdict under
    `--branch` silently under-scored). This unions in every linked worktree's
    corpus so a worktree-resident experiment resolves.

    Worktrees are a MAJOR-checkout layout under this repo (`.agi/worktrees/`
    resolved via `locations.git_common_root`); under the legacy layout there
    are none and `root / "worktrees"` is simply absent, so the corpus is the
    main graph alone -- unchanged behaviour.

    Deliberately tolerant: a half-created worktree (no `.agi/nodes` yet) must
    not take the gate down, and an unreadable tree contributes nothing. The
    gate's fail-closed rule still applies inside each tree -- `build_corpus`
    is what does the actual scan, so nothing here lets a bare word or a
    dangling id resolve.
    """
    corpus = set(evidence_gate.build_corpus(root / "nodes"))
    wt_root = root / "worktrees"
    if wt_root.is_dir():
        for tree in sorted(wt_root.glob("*")):
            if not tree.is_dir():
                continue
            nodes = tree / ".agi" / "nodes"
            if not nodes.is_dir():
                continue
            try:
                corpus |= set(evidence_gate.build_corpus(nodes))
            except evidence_gate.CorpusRootError:
                # A stray root with a nodes/ child, not a real worktree graph.
                continue
    return frozenset(corpus)


def _node_evidence_runs_raw(root: Path, node_id: str | None):
    """Read the *raw* `evidence_runs` value off an existing node file, if any
    (H4 inference). Returns it unnormalized (int / list / str / None) so the
    caller can both taxonomy-check and resolve it against the corpus (H4c) —
    normalizing here would throw away the shape a taxonomy check needs.
    """
    if not node_id:
        return None
    nf = _find_node_file(root, node_id)
    if not nf or not nf.exists():
        return None
    try:
        text = nf.read_text()
        fm = frontmatter.read_frontmatter(text)
        if fm is None:
            return None
    except Exception:
        return None
    return fm.get("evidence_runs")


#: One-line HTML comment the scaffold writes right after the closing `---` to
#: mark where the body starts (hypothesis:l3-done-broken-frontmatter). It is the
#: one reliable anchor `_ensure_frontmatter` repairs up to but never past: a
#: mangled frontmatter block with this line below it is provably all the kid's
#: body from here down, so the `---` block above it can be rebuilt safely.
_BODY_BEGIN = "<!-- BODY:BEGIN -->"
#: The fields a node's frontmatter must carry to be remotely usable: identity
#: (`id`), kind (`type`) and lineage (`parents`). Missing any of these is a
#: defect that makes a node the graph cannot place.
_FM_REQUIRED = ("id", "type", "parents")
#: write-log operation for a sanctioned frontmatter repair.
_FM_REPAIR_OP = "repair-frontmatter"


def _load_frontmatter(text: str) -> tuple[bool, dict | None, str]:
    """Parse a node file's leading frontmatter block.

    Returns ``(ok, fm, defect)``. ``ok=True`` means the ``---`` block is
    present, terminates, parses as a YAML mapping, and carries ``id``, ``type``
    and ``parents``. Anything short of that returns a defect the caller must
    either repair or refuse on -- NEVER a silent pass, because a node that
    cannot be read must not be mistaken for a node with no evidence
    (hypothesis:l3-done-broken-frontmatter, the L3.13 parse-failure incident).
    """
    import yaml

    parts = frontmatter.split_frontmatter(text)
    if parts is None:
        first = text.split("\n", 1)[0]
        if first.rstrip() != "---":
            return False, None, "missing opening `---` delimiter"
        return False, None, "unterminated `---` block (no closing delimiter)"
    try:
        fm = yaml.safe_load(parts[0])
    except Exception as exc:
        return False, None, f"frontmatter YAML parse failure: {exc}"
    if not isinstance(fm, dict):
        return False, None, "frontmatter is not a YAML mapping"
    missing = [k for k in _FM_REQUIRED if not fm.get(k)]
    if missing:
        return False, fm, "frontmatter missing required field(s): " + ", ".join(missing)
    return True, fm, None


def _coerce_fm_value(v: str):
    """Turn a salvaged frontmatter scalar string back into a Python value."""
    v = v.strip()
    if not v:
        return v
    low = v.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "~", "none"):
        return None
    if (v.startswith("{") and v.endswith("}")) or (
            v.startswith("[") and v.endswith("]")) or (
            (v.startswith('"') and v.endswith('"')) or
            (v.startswith("'") and v.endswith("'"))):
        try:
            import ast
            return ast.literal_eval(v)
        except Exception:
            pass
    try:
        return int(v)
    except Exception:
        return v


def _salvage_frontmatter(header: str) -> dict:
    """Recover ``key: value`` lines from a broken frontmatter block.

    A mangled ``---`` block can still carry valid scalar lines -- most
    importantly ``mint_id``, the durable identity the grid and write_guard key
    on. Keep what parses, drop the rest. Canonical identity
    (``id``/``type``/``parents``) always comes from the spawn manifest, never
    from salvage.
    """
    out: dict = {}
    for line in header.splitlines():
        m = re.match(r"^([A-Za-z][\w\-]*):\s*(.*?)\s*$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2)
        if raw.startswith("---"):
            continue
        out[key] = _coerce_fm_value(raw)
    return out


def _ensure_frontmatter(root: Path, node_file: Path, ap: Path,
                        node_id: str | None) -> tuple[bool, str]:
    """Validate a node's frontmatter before `done` records anything; repair it
    when safe (hypothesis:l3-done-broken-frontmatter).

    Returns ``(True, msg)`` when the frontmatter is valid, or was repaired from
    the spawn manifest (``ap``, the agent.json in the session dir -- which
    carries node id/type/parent). Returns ``(False, defect)`` when the node is
    damaged beyond safe repair; the caller must refuse, recording no demotion
    and no verdict change.

    Repair rebuilds the ``---`` block from the manifest **only when the body
    below is intact**, proven by the ``BODY_BEGIN`` marker the scaffold writes
    after the closing ``---``. Without that anchor there is no safe way to
    separate a mangled frontmatter from the start of the body: a repair might
    swallow the kid's work, which is worse than the defect.
    """
    text = node_file.read_text(errors="replace")
    ok, _fm, defect = _load_frontmatter(text)
    if ok:
        return True, "frontmatter ok"

    # Determine the body. A *cleanly closed* `---` block delimits it as
    # `parts[2]` even when the block itself is YAML-broken or missing required
    # fields -- the close means the body below is intact by construction, so it
    # can be repaired without the marker. Only when there is no closed block to
    # delimit the body (missing / unterminated `---`) is the BODY:BEGIN anchor
    # required: without it there is no safe way to tell a mangled frontmatter
    # from the start of the body, and a repair might swallow the kid's work.
    body = None
    header = None
    sp = frontmatter.split_frontmatter(text)
    if sp is not None:
        header, body = sp
    if body is None:
        if _BODY_BEGIN not in text:
            return False, (
                f"{node_file.name}: {defect}, and the body-start marker "
                f"({_BODY_BEGIN!r}) is absent -- cannot separate a mangled "
                "frontmatter from the body safely. Restore the `---` block "
                "(or edit below the closing `---` only) and re-run done."
            )
        header, _marker, body = text.partition(_BODY_BEGIN)
    manifest: dict = {}
    if ap and ap.exists():
        try:
            manifest = json.loads(ap.read_text())
        except Exception:
            manifest = {}
    # Preserve a block that parsed (it may just be missing fields); salvage
    # line-by-line only when it did not parse at all.
    new_fm = dict(_fm) if isinstance(_fm, dict) else _salvage_frontmatter(header or "")
    nid = manifest.get("node_id") or node_id or new_fm.get("id") or ""
    ntype = manifest.get("scaffolded_node_type") or (_fm or {}).get("type") or new_fm.get("type")
    if ":" in str(nid) and not ntype:
        ntype = str(nid).split(":", 1)[0]
    try:
        mparent = manifest.get("parent")
    except Exception:
        mparent = None
    if nid:
        new_fm["id"] = nid
    if ntype:
        new_fm["type"] = ntype
    if mparent:
        new_fm["parents"] = [mparent] if isinstance(mparent, str) else list(mparent)
    if isinstance(new_fm.get("parents"), str):
        new_fm["parents"] = [new_fm["parents"]]
    if not nid or not new_fm.get("type"):
        return False, (
            f"{node_file.name}: {defect} and the spawn manifest gives no node "
            "id/type to repair from -- cannot rebuild the frontmatter. Fix by "
            "hand, then re-run done."
        )
    # `body` is the raw remainder from either branch (the closed-block split or
    # the marker partition); it already carries the BODY:BEGIN marker when one
    # was present, so it is written through untouched.
    new_body = body
    repaired = "\n".join(
        ["---", *node_writer.render_frontmatter(new_fm), "---", ""]
    ) + new_body
    tmp = node_file.with_suffix(node_file.suffix + ".tmp")
    try:
        tmp.write_text(repaired, encoding="utf-8")
        os.replace(tmp, node_file)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    node_writer.log_write(root, _FM_REPAIR_OP, str(new_fm.get("id", "")),
                          node_file, repaired,
                          mint_id=str(new_fm.get("mint_id", "") or ""),
                          extra={"defect": defect})
    print(f"repaired broken frontmatter on {new_fm.get('id')} "
          f"from the spawn manifest ({defect})", file=sys.stderr)
    return True, "frontmatter repaired"


def _normalize_confidence(value: float) -> float:
    """`--confidence` is 0..1. A kid that passes 65 meant 0.65.

    The two numbers on this command are on different scales and the kid has to
    hold both at once: a lean verdict carries `:N` as an INTEGER PERCENT
    (`inconclusive_lean_proved:65`) while `--confidence` is a fraction. The
    2026-08-31 session found the first half of that confusion -- a kid wrote
    `:0.6`, was rejected, and fell back to `pending`, losing the lean -- and
    fixed it by making VERDICT_HELP say `N` is a percent. On 2026-09-01 a kid
    made the mirror error, passing the percent to `--confidence` as well and
    storing `confidence: 65.0` on a 0..1 field. Nothing checked the range.

    Normalized rather than rejected, and announced. The intent at 65 is not
    ambiguous, and this module already prefers recovering a kid's real work
    over discarding it for argument style -- see the `["3"]` evidence-runs
    collapse below, which reasons that "rejection is reserved for claims that
    are actively false". A percent written where a fraction belongs is a unit
    error, not a false claim. Outside 0..100 there is no recoverable intent,
    so that is an error.
    """
    if value is None or 0.0 <= value <= 1.0:
        return value
    if 1.0 < value <= 100.0:
        scaled = value / 100.0
        print(f"CONFIDENCE-NORMALIZED {value} -> {scaled} "
              "(--confidence is 0..1; a lean verdict's `:N` is an integer "
              "percent — they are different scales)", file=sys.stderr)
        return scaled
    raise ValueError(
        f"--confidence {value} is outside 0..1 (and outside 0..100, so it is "
        "not a percent either)")


def _alarm_dispatcher_on_done(root, iter_n, agent_id, node_id, verdict):
    """hypothesis:l4-a-round-alarms-its-dispatcher-by-default -- the round's
    ONE completion dm, sent with NO flag: the dispatcher was stamped into the
    manifest at spawn (`dispatched_by`), and a round that finishes alarms
    that seat exactly once. ids and numbers only -- iteration, agent, node id,
    verdict. Absent dispatcher -> one stderr line, no crash. An undeliverable
    dm is logged, never fatal to the round (this is called on the done: path,
    whose job is to record the verdict)."""
    dispatcher = None
    try:
        sroot = _session_root()
        iter_dir = locations.iteration_dir(sroot, iter_n)
        mpath = iter_dir / "manifest.json"
        if not mpath.is_file():
            return
        manifest = json.loads(mpath.read_text())
        row = next((a for a in manifest.get("agents", [])
                    if a.get("id") == agent_id), None)
        if row is None:
            return
        dispatcher = row.get("dispatched_by")
        if not dispatcher:
            print(f"warn: no dispatcher stamp for {agent_id}@{iter_n}; "
                  "no completion dm (l4-a-round-alarms-its-dispatcher-)",
                  file=sys.stderr)
            return
        import send as _send
        _send.send(
            root, dispatcher,
            f"iter={iter_n} agent={agent_id} node={node_id or '-'} "
            f"verdict={verdict}",
            agent_id)
    except Exception as exc:
        print(f"warn: completion dm to {dispatcher or 'dispatcher'} failed: "
              f"{exc}", file=sys.stderr)


def _mirror_terminal_into_manifest(ap: Path, rec: dict, agent_id: str) -> None:
    """hypothesis:l4-the-manifest-mirrors-terminal-agent-status -- the
    agent's OWN exit path (the source half; the reaper half lives in
    heal.py). A clean `cli.py done` writes the agent record's terminal
    status but leaves the iteration `manifest.json` beside it reading
    `running` until a later reaper pass. Mirror the same terminal fields
    ({status, finished_at, fail_reason}) onto the matching manifest entry, in
    the same write, so the round's own exit leaves both files agreeing.

    Best-effort and silent-on-failure: a missing, unreadable, or corrupt
    manifest, or an entry with no matching id, must NOT raise and must NOT
    change cmd_done's exit code -- this is how every agent ends; it cannot
    become fail-closed on the manifest. One stderr line at most.

    The manifest is a DOCUMENT with its own status ranking
    (hypothesis:l4-a-manifest-is-a-document-too): see `_AGENT_STATUS_RANK`
    and `_merge_manifests`. Mirror only when the record's status ranks AT
    OR ABOVE the entry's -- never downgrade a manifest entry that already
    carries a more authoritative terminal state.
    """
    try:
        mpath = ap.parent.parent / "manifest.json"
        if not mpath.is_file():
            return
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
        entries = manifest.get("agents")
        if not isinstance(entries, list):
            return
        rec_rank = _AGENT_STATUS_RANK.get(rec.get("status", ""), -1)
        target = None
        for entry in entries:
            if entry.get("id") != agent_id:
                continue
            if rec_rank >= _merge_status_rank(entry):
                target = entry
            break
        if target is None:
            return
        for key in ("status", "finished_at", "fail_reason"):
            if key in rec:
                target[key] = rec[key]
        mpath.write_text(json.dumps(manifest, indent=2))
    except Exception:
        print("warn: could not mirror terminal status into iteration "
              "manifest (best-effort)", file=sys.stderr)


def cmd_done(args: argparse.Namespace) -> int:
    if not VERDICT_RE.match(args.verdict):
        print(f"ERR: invalid verdict '{args.verdict}'. Allowed: {VERDICT_HELP}",
              file=sys.stderr)
        return 2
    try:
        args.confidence = _normalize_confidence(args.confidence)
    except ValueError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2
    root = _find_root()
    # Session dirs are LOCAL-first (hypothesis:l4-seat-session-iter-dirs,
    # half a): a seat resolves the record its own worktree made. Fall back to
    # the MAIN checkout only when the local tree lacks the record, so an
    # in-flight round whose manifest predates the change keeps resolving.
    sroot = _session_root()
    ap = _resolve_session_record(sroot, _agent_path(sroot, args.iter_n, args.agent_id))
    if not ap.exists():
        print(f"ERR: no agent record at {ap}", file=sys.stderr)
        return 1

    # hypothesis:l3-done-broken-frontmatter -- validate the node's frontmatter
    # BEFORE the evidence gate runs. The gate's job is to weigh evidence; it
    # must not run against a node it cannot even read. L3.13: a kid's write
    # tool mangled the `---` block, `done` first demoted `proved` then could
    # not parse the node at all, and the kid had to hand-restore the
    # frontmatter and re-run. A parse failure is not missing evidence. Repair
    # the `---` block from the spawn manifest when the body is intact;
    # otherwise refuse with a non-zero exit -- recording no demotion, no
    # `demoted_from`, and no verdict change.
    node_file = None
    if args.node_id:
        node_file = _find_node_file(root, args.node_id)
        if node_file and node_file.exists():
            _ok, _msg = _ensure_frontmatter(root, node_file, ap, args.node_id)
            if not _ok:
                print(f"ERR: {_msg}", file=sys.stderr)
                return 1
            # hypothesis:l3-node-without-mint-id -- a kid that wrote its own
            # node file with its own file tool leaves no `mint_id`, and
            # grid.py commit --all refuses to version it on every grid_sync
            # tick. Adopt it here, through node_writer (which refuses if a
            # `mint_id` already exists), so `done` turns an orphan the kid
            # left behind into a node the grid can version -- keyed from the
            # spawn manifest, exactly like the frontmatter repair above.
            adopted = node_writer.repair_mint(root, args.node_id, announce=True)
            if adopted.status == node_writer.REJECTED:
                print(f"ERR: {adopted.reason}", file=sys.stderr)
                return 1

    # H4 evidence gate. `--evidence-runs` wins; otherwise infer from the node
    # file the agent already wrote, so a real experiment isn't punished for a
    # missing flag.
    runs = args.evidence_runs
    # `--evidence-runs 3` still parses, and still means "a count I cannot
    # verify" -> a soft demotion, never a hard rejection. Without this collapse
    # the count arrives as the list `["3"]`, whose entries are not node-id
    # shaped, and the taxonomy check treats it like the `synthetic` sentinel:
    # exit 2, nothing written, the agent's work discarded over an argument
    # style that was the documented one until today. Rejection is reserved for
    # claims that are actively false; an honest unverifiable count is not that.
    if isinstance(runs, list) and runs and all(str(r).strip().isdigit() for r in runs):
        runs = max((int(str(r).strip()) for r in runs), default=0)
    if runs is None:
        runs = _node_evidence_runs_raw(root, args.node_id)
    # L3.33: a parent signals done with `--owns <kid-node-id>` and no
    # `--node-id` of its own — the kid's node IS the run being attested. The
    # gate above read only `args.node_id`, found nothing, and demoted every
    # decisive parent verdict to inconclusive_lean_*:50 even when the owned
    # node carried a resolvable `evidence_runs`. Read the owned node first.
    if runs is None and args.owns:
        for _owned in args.owns:
            runs = _node_evidence_runs_raw(root, _owned)
            if runs:
                break
    corpus = _evidence_corpus(root)
    gate = evidence_gate.apply_gate(
        args.verdict, runs, bypass=args.no_evidence_gate, corpus=corpus,
        # An `experiment` may name itself (it IS the run); anything else must
        # cite something other than itself. Type comes from the id prefix,
        # which is how every node id in this corpus is built.
        self_id=args.node_id,
        node_type=(args.node_id or "").split(":", 1)[0] or None,
    )
    evidence_gate.announce(gate)
    if gate.rejected:
        # H4c: same class of failure as an invalid verdict — nothing is
        # written. A sentinel like 'synthetic' is a taxonomy violation, not
        # an absence of evidence, so it doesn't get the softer demotion.
        print(
            f"ERR: evidence_runs taxonomy violation for '{args.verdict}': "
            f"{gate.taxonomy_violations!r} is not a resolvable node id "
            "(TODO.md H4c). Cite a real experiment id, or use "
            "--no-evidence-gate for historical backfills.",
            file=sys.stderr,
        )
        return 2
    verdict = gate.verdict

    rec = json.loads(ap.read_text())
    rec["status"] = "done"
    rec["finished_at"] = int(time.time())
    rec["verdict"] = verdict
    rec["confidence"] = args.confidence
    rec["node_id"] = args.node_id
    rec["parent"] = args.parent
    if args.owns:
        rec["owns"] = list(args.owns)   # goal:s27 — a parent's real artefact
    rec["notes"] = args.notes
    # Record the *references*, not the resolved count. Writing the count back
    # would be self-defeating under goal:g7.3: the node would come back out of
    # disk as a bare int, which no longer certifies anything, so a correctly
    # evidenced verdict would fail its own gate on the next read. The count is
    # derived; the ids are the evidence.
    rec["evidence_runs"] = list(runs) if isinstance(runs, (list, tuple)) else gate.evidence_runs
    if gate.demoted:
        rec["demoted_from"] = gate.original
        rec["demote_reason"] = gate.reason
    if gate.bypassed:
        rec["evidence_gate"] = "bypassed"
    ap.write_text(json.dumps(rec, indent=2))
    # hypothesis:l4-the-manifest-mirrors-terminal-agent-status -- the round's
    # own exit mirrors terminal status into the iteration manifest beside the
    # record, so readers of the manifest see a clean `done` immediately
    # instead of a stale `running` until a later reaper pass. Best-effort.
    _mirror_terminal_into_manifest(ap, rec, args.agent_id)

    # Write or update the node file with verdict info
    if args.node_id:
        node_file = _find_node_file(root, args.node_id)
        if node_file and node_file.exists():
            _append_verdict_to_node(node_file, verdict, args.confidence, args.notes,
                                    args.next_edge, gate, root=root,
                                    node_id=args.node_id,
                                    evidence_runs=args.evidence_runs,
                                    push_further=getattr(args, "push_further", None))
            # goal:s31 -- the completion half. A scaffold is born with what the
            # engine can derive from a slug; the rest is content only the kid
            # has, and the kid wrote it into the BODY because a kid writing
            # frontmatter is the trade s31 forbids. Lift it into the required
            # field now, through the gated writer. Never fatal: a node that
            # cannot be completed this way stays reported, not rejected -- the
            # kid's work is already on disk and is worth more than the field.
            try:
                filled = node_writer.derive_required_from_body(root, args.node_id)
                if filled.status == node_writer.UPDATED:
                    print(f"schema: filled required field(s) on {args.node_id} "
                          f"from its body (goal:s31)")
                # goal:s31 -- loud-but-never-fatal: if the lift left any
                # schema-required field still missing, say so on stderr. The
                # kid's work is already on disk; rc is unchanged either way.
                still_missing = _missing_after_lift(root, args.node_id)
                if still_missing:
                    print(
                        f"SCHEMA-WARNING: {args.node_id} still missing required "
                        f"field(s): {', '.join(still_missing)} (goal:s31). The "
                        f"kid's work is saved; backfill these or have a parent "
                        f"complete them.",
                        file=sys.stderr,
                    )
            except Exception as exc:
                # The derive above already warned loudly on a live failure via
                # its own except; this catch keeps `done` from ever dying on a
                # lift misstep. The lift is never fatal by design.
                print(f"warn: could not complete {args.node_id} from its body: "
                      f"{exc}", file=sys.stderr)
            print(f"updated verdict in: {node_file}")
        else:
            # Fallback: write verdict node. goal:s17 -- this is cli.py's second
            # node-creating path, and it goes through `node_writer.write_node`
            # like every other one, so it gets the spawn check for free rather
            # than by remembering to call it. A verdict is `min_parents: 1`
            # (`context/schemas/[verdict].md`), and this path has historically
            # emitted one with `parents` omitted whenever `--parent` was not
            # passed -- exactly the shape that put 21 parentless verdicts in
            # the corpus.
            extra = {
                "verdict": verdict,
                "confidence": args.confidence,
                "evidence_runs": gate.evidence_runs,
            }
            if args.next_edge:
                extra["next_edges"] = [args.next_edge]
            if gate.demoted:
                extra["demoted_from"] = gate.original
                extra["demote_reason"] = gate.reason
            if gate.bypassed:
                extra["evidence_gate"] = "bypassed"
            # goal:s14 -- `mint_id` comes from the writer, not a later backfill:
            # before it did, every verdict this path wrote was skipped by
            # `grid.py commit --all` and silently had no version history.
            res = node_writer.write_node(
                root, "verdict", args.node_id.replace(":", "_"),
                [args.parent] if args.parent else [],
                extra_fm=extra, body=args.notes or "",
                bypass=args.no_spawn_gate,
            )
            if res.rejected:
                print(
                    f"ERR: spawn rejected for {res.node_id}: {res.reason}. "
                    f"Fix: {res.gate.fix} "
                    "(--no-spawn-gate bypasses this, loudly.)",
                    file=sys.stderr,
                )
                return 2
            print(f"wrote verdict: {res.path}")

    # hypothesis:l3w4-branch-parent-commits -- the parent's ONE finishing
    # action, so it owns the worktree commit too. Commits the linked worktree
    # this parent runs in, if it holds uncommitted node writes; a no-op in
    # main (the loop owns main) and outside git. Never fatal.
    _auto_commit_worktree(root, args.agent_id, args.node_id, args.owns, verdict)

    # hypothesis:l4-a-round-alarms-its-dispatcher-by-default -- a round that
    # finishes alarms the seat that dispatched it: exactly ONE dm, sent with
    # no flag, right after the done: commit. Never fatal to the done path.
    _alarm_dispatcher_on_done(root, args.iter_n, args.agent_id,
                              args.node_id, verdict)

    print(f"agent {args.agent_id} status=done verdict={verdict}")
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    root = _find_root()
    sroot = _session_root()
    ap = _resolve_session_record(sroot, _agent_path(sroot, args.iter_n, args.agent_id))
    if not ap.exists():
        print(f"ERR: no agent record at {ap}", file=sys.stderr)
        return 1
    rec = json.loads(ap.read_text())
    rec["status"] = "pending"
    rec["finished_at"] = int(time.time())
    rec["pending_reason"] = args.reason
    ap.write_text(json.dumps(rec, indent=2))
    print(f"agent {args.agent_id} status=pending reason={args.reason}")
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    """Pre-create a node file skeleton so the agent just fills in the body."""
    root = _find_root()
    sroot = _session_root()
    # `--parent` repeats. Before goal:s17 it was a single REQUIRED flag, which
    # meant argparse -- not the schema -- decided how many parents a node may
    # have, and it decided "exactly one" for every type. That is the rule the
    # corpus contradicts (max 1 or 2 depending on type, and three shapes legally
    # parentless), and an argparse error names no rule and no schema file, so a
    # rejection taught nothing. The flag now collects; the gate is the authority.
    parents = [p for p in (args.parents or []) if p]

    # goal:s17 -- THIS is the spawn: a type and a parent, decided here and baked
    # into a file. `node_writer.write_node` canonicalises the type, runs the
    # spawn gate before touching the filesystem (so a rejection leaves no node
    # behind, the same convention `done` uses for an evidence_runs taxonomy
    # violation), mints the `mint_id` goal:s14 requires, and writes the file.
    # Approvals are announced too: an agent must be able to tell "checked and
    # fine" from "nothing looked".
    res = node_writer.write_node(
        root, args.node_type, args.slug, parents,
        bypass=args.no_spawn_gate,
    )
    if res.rejected:
        print(
            f"ERR: spawn rejected for {res.node_id}: {res.reason}. "
            f"Fix: {res.gate.fix} (--no-spawn-gate bypasses this, loudly.)",
            file=sys.stderr,
        )
        return 2
    if not res.written:
        print(f"SKIP: {res.path} already exists", file=sys.stderr)
        return 0
    print(f"scaffolded: {res.path}")

    # Record scaffold in agent.json so cli.py done knows what to update.
    # Local-first, shared fallback (hypothesis:l4-seat-session-iter-dirs,
    # half a) — same as `done` resolves it.
    ap = _legacy_fallback(sroot, _agent_path(sroot, args.iter_n, args.agent_id))
    if ap.exists():
        rec = json.loads(ap.read_text())
        rec["scaffolded_node"] = res.node_id
        rec["scaffolded_file"] = str(res.path)
        # hypothesis:l3-done-broken-frontmatter -- the spawn manifest is what a
        # later `done` repairs a mangled frontmatter from. Carry type + parent
        # here so the manifest alone can rebuild the `---` block.
        rec["scaffolded_node_type"] = res.node_type
        rec["scaffolded_parent"] = res.parents[0] if res.parents else ""
        ap.write_text(json.dumps(rec, indent=2))

    return 0


def _find_node_file(root: Path, node_id: str) -> Path | None:
    """Find a node file by its canonical id.

    goal:s17 -- the one lookup, in `node_writer`, beside the one write. This
    copy assumed the id prefix names the directory, so it could not resolve the
    147 corpus ids on an abbreviated prefix (`exp:`/`hyp:` for nodes under
    `nodes/experiment/` and `nodes/hypothesis/`). `post_wire.py`'s separate
    copy missed 417. Kept as a thin alias because it is called from six places
    here and the name is the more readable one at each of them.
    """
    return node_writer.find_node_file(root, node_id)


def _missing_after_lift(root, node_id) -> list[str]:
    """Which schema-required fields a node still lacks after the lift.

    goal:s31 -- the loud, never-fatal tail of the completion half: `done` lifts
    what the body advertises, then reports what common scaffolding still
    leaves missing rather than silently finishing with an invalid node. A
    parse failure returns [] -- the derive above already warned on stderr.
    """
    path = node_writer.find_node_file(root, node_id)
    if path is None:
        return []
    ok, fm, _ = _load_frontmatter(path.read_text())
    if not ok or not fm:
        return []
    ntype = node_writer.canonical_node_type(fm.get("type") or path.parent.name)
    return node_writer.missing_required(root, ntype, fm, node_id)


def _claim_node(root: Path, node_id: str, session_id: str, force: bool = False) -> tuple[bool, str]:
    """
    Atomically claim a node for a session. Returns (success, message).
    Uses fcntl.flock for inter-process mutual exclusion.
    """
    import fcntl
    node_file = _find_node_file(root, node_id)
    if not node_file or not node_file.exists():
        return False, f"node not found: {node_id}"

    import yaml
    lock_file = node_file.with_suffix(".lock")

    # Acquire exclusive lock
    with open(lock_file, "a") as lf:
        fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
        try:
            content = node_file.read_text()
            if not content.startswith("---"):
                return False, f"no frontmatter in {node_file}"

            parts = frontmatter.split_frontmatter(content)
            if parts is None:
                return False, f"malformed frontmatter in {node_file}"
            fm_text, body = parts

            try:
                fm = yaml.safe_load(fm_text) or {}
            except Exception as e:
                return False, f"YAML parse error: {e}"

            now = int(time.time())

            # Check if already claimed by someone else (skip if force=True for reclaim)
            if fm.get("claimed_by") and fm.get("claimed_by") != session_id and not force:
                claimed_at = fm.get("claimed_at", 0)
                age = now - claimed_at
                return False, (f"already claimed by {fm['claimed_by']} "
                               f"({age}s ago)")

            # Write claim
            fm["claimed_by"] = session_id
            fm["claimed_at"] = now
            fm["id"] = node_id

            # Serialize back to YAML
            new_fm_lines = []
            for k, v in fm.items():
                new_fm_lines.append(f"{k}: {repr(v) if isinstance(v, str) else v}")
            new_fm = "\n".join(new_fm_lines)
            new_content = f"---\n{new_fm}\n---\n{body}"

            # Atomic write: write to temp then rename
            tmp = node_file.with_suffix(".md.tmp")
            tmp.write_text(new_content)
            tmp.rename(node_file)
            # Log this sanctioned write so write_guard recognises it
            node_writer.log_write(root, "claim_node", node_id, node_file,
                                  new_content,
                                  extra={"session": session_id})
            return True, f"claimed {node_id} for {session_id} at {now}"
        finally:
            fcntl.flock(lf.fileno(), fcntl.LOCK_UN)


def _detect_stale(root: Path, threshold_seconds: int) -> list[dict]:
    """Scan all nodes, return list of stale claimed nodes."""
    import yaml
    nodes_dir = root / "nodes"
    stale = []
    now = int(time.time())
    for nf in sorted(nodes_dir.rglob("*.md")):
        try:
            content = nf.read_text()
            fm = frontmatter.read_frontmatter(content)
            if fm is None:
                continue
            if fm.get("claimed_by") and fm.get("claimed_at"):
                age = now - int(fm["claimed_at"])
                if age > threshold_seconds:
                    stale.append({
                        "node_id": fm.get("id", nf.stem),
                        "file": str(nf),
                        "claimed_by": fm["claimed_by"],
                        "claimed_at": fm["claimed_at"],
                        "age_seconds": age,
                    })
        except Exception:
            continue
    return stale


def cmd_claim(args: argparse.Namespace) -> int:
    root = _find_root()
    success, msg = _claim_node(root, args.node_id, args.session)
    print(msg)
    return 0 if success else 1


def cmd_detect_stale(args: argparse.Namespace) -> int:
    root = _find_root()
    stale = _detect_stale(root, args.threshold_seconds)
    if not stale:
        print(f"no stale claims (threshold={args.threshold_seconds}s)")
        return 0
    for s in stale:
        print(f"STALE node={s['node_id']} by={s['claimed_by']} age={s['age_seconds']}s")
    return 0


def cmd_reclaim(args: argparse.Namespace) -> int:
    root = _find_root()
    success, msg = _claim_node(root, args.node_id, args.session, force=True)
    print(msg)
    return 0 if success else 1


def _append_verdict_to_node(node_file: Path, verdict: str, confidence: float, notes: str,
                            next_edge: str | None = None, gate=None,
                            root: Path | None = None,
                            node_id: str | None = None,
                            evidence_runs: list | tuple | None = None,
                            push_further: str | None = None) -> None:
    """Add verdict frontmatter fields to an existing node file.

    `root`/`node_id` are how this reaches `node_writer.update_node`; both
    default from `node_file` so the older two-positional call still works, and
    the tests that predate `goal:g13` keep passing unchanged.
    """
    if node_id is None:
        node_id = f"{node_file.parent.name}:{node_file.stem}"
    if root is None:
        # <root>/nodes/<type>/<slug>.md, or the deprecated tree one deeper.
        root = node_file.parent.parent.parent
        if root.name == "deprecated":
            root = root.parent
    # goal:g13 — through the one gated in-place writer, not by hand.
    #
    # This function used to do line surgery on raw frontmatter: split on
    # `---`, filter out lines by string prefix, append new ones, rejoin. That
    # is a YAML writer built out of `str.startswith`, and it could not call
    # `evidence_gate.stamp()` because it never had a dict to stamp — which is
    # why the status-shadow demotion below had to be reimplemented against
    # text. Now there is a dict, so the shared routine does it.
    set_fm = {"verdict": verdict, "confidence": confidence}
    if gate is not None and evidence_runs:
        # hypothesis:l2-dispatch-restart-twin-node — Fix B: persist
        # evidence_runs into the node's own frontmatter at signal time so a
        # node citing itself as evidence survives a later grid-commit re-check.
        # Store the raw cited ids (the node IDs), not the resolved count.
        set_fm["evidence_runs"] = list(evidence_runs)
    if gate is not None:
        if gate.demoted:
            set_fm["demoted_from"] = gate.original
            set_fm["demote_reason"] = gate.reason
        if gate.bypassed:
            set_fm["evidence_gate"] = "bypassed"
    if next_edge:
        set_fm["next_edges"] = [next_edge]
    if push_further:
        set_fm["push_further"] = push_further

    # The status shadow, demoted in lockstep: after a demotion nothing in the
    # frontmatter may still read 'proved'/'disproved'. Only a decisive value is
    # touched, so a task's `status: pending` is never clobbered.
    if gate is not None and gate.demoted:
        try:
            from graph_core.persistence import frontmatter as _fmr
            current = _fmr.load_node_file(node_file).frontmatter.get("status")
        except Exception:
            current = None
        if current is not None and evidence_gate.is_decisive_shadow(
                str(current).strip().strip("\"'")):
            set_fm["status"] = verdict

    res = node_writer.update_node(root, node_id, set_fm=set_fm)
    if res.status == node_writer.REJECTED:
        print(f"warn: could not record the verdict on {node_id}: {res.reason}",
              file=sys.stderr)
    # Notes go under the SAME heading `post_wire` uses, and only when the body
    # does not already carry them.
    #
    # This used to write the notes bare -- `f.write("\n" + notes + "\n")` --
    # while `post_wire` separately appended `## Agent Notes\n{notes}`. Both run
    # on every kid, so every node got the text twice: once loose, once headed.
    # The kid contract blamed the kid for it ("Do not also write that sentence
    # into the body -- four kids in a row did, and it lands twice"), and the
    # accusation was false: no kid was writing it, two engine writers were.
    # Re-running `done` after an evidence-gate demotion made it three copies.
    #
    # L2.05: the raw append bypassed the logged writer, so write_guard.py
    # flagged every done-completed node as unsanctioned. Route through
    # update_node instead, which atomically rewrites and logs the final sha.
    if notes:
        try:
            from graph_core.persistence import frontmatter as _fmr2
            nf2 = _fmr2.load_node_file(node_file)
            if notes.strip() not in nf2.body:
                new_body = nf2.body
                if not new_body.endswith("\n"):
                    new_body += "\n"
                new_body += f"\n## Agent Notes\n{notes}\n"
                res2 = node_writer.update_node(
                    root, node_id, body=new_body)
                if res2.status == node_writer.REJECTED:
                    print(f"warn: could not add notes to {node_id}: {res2.reason}",
                          file=sys.stderr)
        except Exception as exc:
            print(f"warn: could not add notes to {node_id}: {exc}",
                  file=sys.stderr)


def _auto_commit_worktree(root: Path, agent_id: str, node_id: str | None,
                         owns: list | None, verdict: str) -> Path | None:
    """Give the commit to the parent at the moment it accepts its kid's node.

    hypothesis:l3w4-branch-parent-commits — a `--branch` parent runs inside a
    linked git worktree, and nothing commits there (a kid is contractually
    forbidden to commit, and the loop owns the main checkout), so a loop branch
    reaches merge-up holding one or more uncommitted node writes. `done` is the
    parent's ONE finishing action, so it owns that commit: when `root` resolves
    inside a linked worktree and that worktree is dirty, add + commit it so
    merge-up has a real commit to (merely-zero-ahead) refuse, a branch that
    previously reached the gate empty.

    ONLY in a linked worktree. In the main checkout — or outside any git repo —
    this is a silent no-op: the loop owns commits in main, and a parent running
    in main must not `git add -A` a tree it shares with sibling agents (that is
    the goal:g4.1 hazard, exactly). Worktree-ness is tested by the same probe
    the rest of the engine uses: the worktree's own git-dir resolving to a
    DIFFERENT repo than the project's common-dir, i.e.
    `locations.git_common_root(root)` != this checkout's own toplevel.

    Returns the committed checkout root on success, None otherwise. A commit
    failure prints a loud named ERR to stderr but NEVER discards the verdict
    already recorded — the same principle `cmd_done` applies a few lines above
    when the schema-fill step fails: the kid's work is on disk and is worth
    more than the commit.
    """
    try:
        checkout = locations.source_root(root)
        common = locations.git_common_root(root)
        toplevel = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True)
        if toplevel.returncode != 0 or not toplevel.stdout.strip():
            return None   # not inside a git repo -> nothing to commit
        checkout_root = Path(toplevel.stdout.strip())
        # Main checkout (or a config declared elsewhere): the loop owns commits
        # here, and this tree is shared, so never sweep it. Only a linked
        # worktree is this parent's private branch.
        if common.resolve() == checkout_root.resolve():
            return None
    except (OSError, subprocess.SubprocessError):
        return None

    status = subprocess.run(
        ["git", "-C", str(checkout), "status", "--porcelain"],
        capture_output=True, text=True)
    if status.returncode != 0 or not status.stdout.strip():
        return None   # clean worktree -> nothing to commit

    # `<agent_id> done: <node_id or owns[0]> verdict=<verdict>`
    ref = node_id or (owns[0] if owns else "node")
    subject = f"{agent_id} done: {ref} verdict={verdict}"

    add = subprocess.run(["git", "-C", str(checkout), "add", "-A"],
                         capture_output=True, text=True)
    if add.returncode != 0:
        print(f"ERR: worktree commit add failed in {checkout_root}: "
              f"{add.stderr.strip() or '(no stderr from git)'}",
              file=sys.stderr)
        return None

    commit = subprocess.run(
        ["git", "-C", str(checkout),
         "-c", "user.email=agi@local", "-c", "user.name=agi",
         "commit", "-qm", subject],
        capture_output=True, text=True)
    if commit.returncode != 0:
        print(f"ERR: worktree commit failed in {checkout_root}: "
              f"{commit.stderr.strip() or '(no stderr from git)'}",
              file=sys.stderr)
        return None

    print(f"committed worktree {checkout_root}: {subject}")
    return checkout_root


def cmd_status(args: argparse.Namespace) -> int:
    # Manifest + agent records resolve LOCAL-first, shared fallback
    # (hypothesis:l4-seat-session-iter-dirs, half a): a seat reads its own
    # round; it still sees a manifest/record that predates the change (or
    # belongs to a seat whose dirs live in main) via the main checkout.
    root = _find_root()
    sroot = _session_root()
    iter_dir = locations.iteration_dir(sroot, args.iter_n)
    manifest = _legacy_fallback(sroot, iter_dir / "manifest.json")
    if not manifest.exists():
        print(f"ERR: no manifest at {manifest}", file=sys.stderr)
        return 1
    m = json.loads(manifest.read_text())
    print(f"iter {args.iter_n}: {len(m['agents'])} agents")
    for a in m["agents"]:
        ap = _legacy_fallback(sroot, _agent_path(sroot, args.iter_n, a["id"]))
        rec = json.loads(ap.read_text()) if ap.exists() else a
        # A live agent past its deadline keeps `status: running` and gains
        # `overdue_since` (heal.py) -- print `running(overdue)` on this reader
        # too, the word the parent brief names (hypothesis:l4-the-parent-
        # brief-names-the-overdue-record-as-readers-print-it). The mark must
        # never claim `(overdue)` for a DEAD row: it is shown only when the
        # terminal word did not win (status is running or absent).
        status = rec.get("status")
        overdue = rec.get("overdue_since")
        mark = "(overdue)" if overdue and (not status or status == "running") else ""
        print(f"  {rec['id']}: status={status}{mark} verdict={rec.get('verdict', '-')} pid={rec.get('pid')}")
    return 0


# ---------------------------------------------------------------------------
# session-complete: bring a finished round's session dirs home
# (hypothesis:l4-session-dirs-come-home-when-the-round-is-done)
#
# `sessions/` is gitignored so a merge-up carries none of it. The iter dir
# that RAN a round lives in the WORKTREE that ran it, and nothing ever brings
# it into the main checkout -- the one place a cold reader or an audit looks.
# This command IS that step: a SESSION-COMPLETE migration, named and
# explicitly invoked, never a side effect and never on a timer.
# ONE sanctioned caller (hyp:l4-a-finished-rounds-session-dir-comes-home-\
# before-the-sweep-judges-it): the reaper's worktree sweep `_sweep_bring_home`
# (heal.py) may invoke this for a round that is leaseless + merged + clean +
# past-grace, so a finished round's session dir comes home before the sweep
# judges it -- and its OWN completeness guards still decide every migration.
#
# The three prime constraints, stated by number, hold together here:
#   (1) during a round the iter dir STAYS in the worktree that ran it -- this
#       command runs only when the round is over, so resolution does not
#       change mid-round;
#   (2) shared state (spawn budget, comms root, meter pins) stays in MAIN and
#       is untouched -- only `sessions/iter-<id>` dirs move, and the budget is
#       consulted read-only as a liveness signal;
#   (3) this migration step is the SESSION-COMPLETE move, COPY-THEN-VERIFY
#       (never move): copy the tree, byte-compare it, and only then remove the
#       source -- with `--dry-run` as the default testing posture.
#
# Central safety rule, duplicated nowhere else: this must NEVER be run against
# a live tree. Other seats dispatch while a round runs, and a live round's
# `manifest.json` is being written as a migration would read it. The guard is
# two independent completeness checks, both of which must pass: (a) no live
# spawn-budget lease names this iteration, and (b) every agent record in the
# source iter dir's manifest is terminal. A round that is still running is
# REFUSED, not partially moved.

#: Terminal statuses a round's agent records may rest in -- the same set the
#: reaper uses (dispatch.py TERMINAL). A record in any other state means the
#: round is still live and must not be migrated.
#: 🔴 `done-unreported` IS TERMINAL AND MUST BE IN THIS SET. It is what the
#: reaper writes when a round landed and only the report was lost — the most
#: common ending for a `--branch` parent, which authors no node and whose
#: `done` reaches its own worktree rather than the dispatcher's. All three of
#: this seat's rounds ended that way. Without it `session-complete` refused
#: every seat-dispatched round with "not every agent record is terminal;
#: round still running", measured live against `iter-L4.56` — a no-op wearing
#: a safety message, and precisely the case the command exists for.
#:
#: `dispatch.py:1738` carries the same four-name set and gets away with it by
#: accident: its reaper loop follows `if status in TERMINAL: continue` with
#: `if status != "running": continue`, so `done-unreported` is skipped by the
#: second guard and `all_terminal` is never cleared. Behaviourally terminal,
#: nowhere declared so. A reader that copies the SET without the guard — this
#: one did — inherits a refusal instead of a completion.
#: Since hyp:l4-one-definition-of-terminal the DEFINITION lives only in
#: `spawn_budget.TERMINAL`; this is an alias import so every reader shares it.
from spawn_budget import TERMINAL as TERMINAL_STATUSES  # noqa: E402 -- the ONE set


def _manifest_agent_statuses(iter_dir: Path):
    """The terminal-resolution shared by _iteration_agents_complete and
    _first_non_terminal -- the SINGLE body of the status-resolution loop, so a
    fix to one twin can never silently miss the other (hypothesis:l4-the-
    sweep-names-every-refusal-and-has-one-terminal-body). Reads the manifest's
    `agents` list, then re-reads each agent's own `agent.json` when present
    (the reaper writes the authoritative terminal status there first), so a
    record the manifest shows as `running` but whose `agent.json` is already
    terminal still counts.

    Returns (kind, states):
      kind 'missing' | 'unreadable' | 'ok'
      states a list of (agent_id, status) for every manifest entry (empty
      when the manifest has no agents).
    """
    mpath = iter_dir / "manifest.json"
    if not mpath.is_file():
        return ("missing", [])
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return ("unreadable", [])
    agents = manifest.get("agents") or []
    states = []
    for entry in agents:
        status = entry.get("status", "running")
        rec_path = iter_dir / str(entry.get("id", "")) / "agent.json"
        try:
            rec = json.loads(rec_path.read_text(encoding="utf-8"))
            status = rec.get("status", status)
        except (OSError, json.JSONDecodeError, ValueError):
            pass  # no agent.json: trust the manifest entry
        states.append((entry.get("id", "?"), status))
    return ("ok", states)


def _iteration_agents_complete(iter_dir: Path) -> bool:
    """Every agent record in `iter_dir`'s manifest is terminal.

    A missing or unreadable manifest, or an empty agents list, is NOT
    complete -- there is nothing to judge, so nothing may move.
    """
    kind, states = _manifest_agent_statuses(iter_dir)
    if kind != "ok" or not states:
        return False
    return all(status in TERMINAL_STATUSES for _aid, status in states)


def _first_non_terminal(iter_dir: Path):
    """The first `(agent_id, status)` in `iter_dir`'s manifest that is not
    terminal, or None when every manifest entry is terminal.

    The naming twin of `_iteration_agents_complete`; both now share ONE body
    in `_manifest_agent_statuses`, so the refusal names the SAME record a
    reader would see. Called only on a manifest-bearing (authority) source,
    so the missing/unreadable-manifest branches are defensive; the caller
    refuses such a source before reaching here.
    """
    kind, states = _manifest_agent_statuses(iter_dir)
    if kind == "missing":
        return ("?", "missing manifest")
    if kind == "unreadable":
        return ("?", "unreadable manifest")
    if not states:
        # An empty agents list is NOT complete -- nothing to judge, so nothing
        # may move; the same rule `_iteration_agents_complete` states. Kept
        # here at harvest (L4.255) so an authority with no records fails
        # CLOSED exactly as it did before the partial-source carry.
        return ("?", "no agents in manifest")
    for aid, status in states:
        if status not in TERMINAL_STATUSES:
            return (aid, status)
    return None


def _dir_snapshot(root: Path) -> dict:
    """A filesystem snapshot: relative path -> bytes, for every file under
    `root`. The symmetric ground truth for `_merge_verified`: a merged target
    is correct iff its snapshot EQUALS the union of every source's expected
    winner/loser locations."""
    out = {}
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        out[str(p.relative_to(root))] = p.read_bytes()
    return out


def _trees_match(src: Path, dst: Path) -> bool:
    """Byte-for-byte: every file under `src` exists under `dst` with equal
    bytes. The copy's verification, not its success -- a `copytree` that
    returns 0 can still have truncated a file, and the source may only be
    removed once this says the two trees agree.
    """
    try:
        src_files = [p for p in src.rglob("*")
                     if p.is_file() and _migratable(p.relative_to(src))]
        pending = set(src_files)
        for sp in src_files:
            rel = sp.relative_to(src)
            dp = dst / rel
            if not dp.is_file():
                return False
            if sp.read_bytes() != dp.read_bytes():
                return False
            pending.discard(sp)
        # The destination must not silently hold extra accepted files
        # (symlink targets, intermediates); require a symmetric file set.
        dst_files = {p.relative_to(dst) for p in dst.rglob("*")
                     if p.is_file() and _migratable(p.relative_to(dst))}
        return set(p.relative_to(src) for p in src_files) == dst_files
    except OSError:
        return False


# ---------------------------------------------------------------------------
# The merge. A `--branch` round writes its session dir to TWO trees at once
# (hypothesis:l4-a-round-lives-in-two-trees-so-coming-home-is-a-merge): the
# DISPATCHER's tree carries `manifest.json`, `output.log` and a parent
# `agent.json` whose record the reaper set to `done-unreported`; the CHILD's
# worktree carries `context.md` and the parent's OWN `agent.json`, whose
# record `cli.py done` wrote as `done`. Both are `sessions/iter-<id>/` and
# both must come home to the SAME target. A copy that runs one first and
# refuses on the non-empty target strands half the round in a worktree -- the
# exact outcome this command exists to prevent. So bringing a round home is a
# MERGE of complementary subtrees, not a copy of one,
# COPY-THEN-VERIFY-THEN-REMOVE-EACH-SOURCE-BY-ITS-OWN-CONTRIBUTION.
#
# The hard part is the CONFLICTING PATH: both trees may hold the same relative
# file (the parent `agent.json` for the same parent id) and they are two
# genuinely different documents, neither a copy of the other. The rule below
# resolves it by CONTENT SEMANTICS -- never by scan/iteration order -- and
# always keeps the loser recoverable rather than deleted.

#: `.manifest.lock` is NOT a document (hypothesis:l4-a-manifest-is-a-
#: document-too, `.manifest.lock` clause): it is a lock file whose only
#: statement is "some dispatch held a brief rename" (dispatch.py
#: `_manifest_lock`). Ranking, merging, or carrying it into the landing spot
#: is meaningless, so it is dropped from the migration entirely -- never
#: copied, never verified, never a conflict. `.tmp`/`.lock` intermediates are
#: transient by construction and cannot be the round's bookkeeping either.
_MANIFEST_LOCK = ".manifest.lock"

#: `win[rel]` sentinel for a path whose target bytes are SYNTHESIZED rather
#: than copied from a single source (the `manifest.json` union, below).
_SYNTHESIZE = "SYNTHESIZE-UNION"


def _migratable(rel: Path) -> bool:
    """Is `rel` a document this merge should carry? Everything except
    `.manifest.lock` -- see the constant's comment: a lock file, not data."""
    return rel.name != _MANIFEST_LOCK


#: Precedence for a conflicting `agent.json` terminal record. Higher rank is
#: the more authoritative statement of how the agent's round ended and wins
#: the conflict. `done` -- the agent's own record written through `cli.py
#: done` -- beats `done-unreported` -- the reaper's inference that the round
#: landed but the report was lost -- because one is the actor speaking for
#: itself and the other a caretaker guessing at the outcome. A path that is
#: not a readable agent record ranks -1 and falls through to the deterministic
#: slug tiebreak instead, so content semantics only ever decide agent endings.
_AGENT_STATUS_RANK = {
    "done": 5,
    "done-unreported": 4,
    "failed": 3,
    "hung-healed": 2,
    "pending": 1,
    "running": 0,
}


def _agent_status_rank(rel: Path, src: Path) -> int:
    """How authoritative is `src/rel` as an agent ending? Only `agent.json`
    records have a status to read; anything else is -1 (never wins on
    content, falls to the slug tiebreak). Unreadable JSON is -1 too, so a
    corrupt record is never silently treated as `done`."""
    if rel.name != "agent.json":
        return -1
    try:
        rec = json.loads((src / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError):
        return -1
    return _AGENT_STATUS_RANK.get(rec.get("status", ""), -1)


def _src_slug(src: Path) -> str:
    """The worktree slug a source iter dir lives under: `.../<slug>/.agi/
    sessions/iter-<id>` -> `<slug>`, the one stable name - not a filesystem
    scan order - a tiebreak can lean on."""
    return src.parent.parent.parent.name


def _merge_status_rank(entry: dict) -> int:
    """How authoritative is a `manifest.json` `agents` entry as how that
    agent's round ended? The SAME ranking as `agent.json` --
    `_AGENT_STATUS_RANK` (hypothesis:l4-a-manifest-is-a-document-too). A
    manifest entry and an agent record answer the same question, and two
    rankings for one question is the defect this chain has been removing all
    day. An entry with no id/status ranks -1 and never wins a per-id
    conflict, so junk is never silently treated as a terminal record."""
    return _AGENT_STATUS_RANK.get(entry.get("status", ""), -1)


def _merge_manifests(holders: list[Path]) -> dict:
    """The UNION of several complementary `manifest.json` docs.

    A `--branch` round's two trees each write the iteration `manifest.json`,
    and they are NOT versions of one file but two complementary halves of the
    round's bookkeeping (hypothesis:l4-a-manifest-is-a-document-too): the
    DISPATCHER's manifest is the launch record -- `commits_ahead`, the
    parent's restart bookkeeping, the agents it saw dispatch; the CHILD's
    covers the same round from the contestant's side. Picking one file
    wholesale by slug name (the alphabet) silently discards the other half
    from the file a later reader opens first -- the exact defect, one level
    up, that the `agent.json` content rule exists to fix. So: an agent id
    held by only one source is kept; an id held by TWO sources resolves its
    entry by `_merge_status_rank` -- the SAME ranking as `agent.json`, never
    a second ranking invented for one file; other top-level keys are taken
    from all sources in slug order, later wins. Order of the merged `agents`
    list is deterministic (first-seen by slug source then list order). A
    corrupt or unreadable source manifest contributes nothing and cannot
    abort the union."""
    holders = sorted(holders, key=_src_slug)
    by_id: dict[str, dict] = {}
    order: list[str] = []
    top: dict = {}
    for src in holders:
        try:
            m = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ValueError):
            m = {}
        for k, v in m.items():
            if k == "agents":
                continue
            top[k] = v
        for entry in m.get("agents") or []:
            aid = entry.get("id")
            if not aid or not isinstance(aid, str):
                continue
            if aid in by_id:
                if _merge_status_rank(entry) > _merge_status_rank(by_id[aid]):
                    by_id[aid] = entry
            else:
                by_id[aid] = entry
                order.append(aid)
    merged = dict(top)
    merged["agents"] = [by_id[aid] for aid in order]
    return merged


def _conflict_winner(rel: Path, holders: list[Path]) -> Path:
    """Deterministic winner for a relative path held by two or more sources.
    Decided by agent-terminal content semantics when the path is a readable
    `agent.json`; otherwise by the lexicographically smallest worktree slug.
    Never by scan order -- the whole point of the rule is that a merge must
    not resolve a conflict by whichever source happened to be listed first.
    """
    cur = holders[0]
    for nxt in holders[1:]:
        hc = _agent_status_rank(rel, cur)
        hn = _agent_status_rank(rel, nxt)
        if hn > hc:
            cur = nxt
        elif hn == hc and _src_slug(nxt) < _src_slug(cur):
            cur = nxt
    return cur


def _merge_plan(sources: list[Path]):
    """Compute the merge plan for a set of source iter dirs.

    Returns `(win, lose, conflicted)`:
      win  -- dict rel_path -> the source whose bytes land at `target/rel`.
      lose -- dict (src, rel) -> relative `.conflicts/...` path where that
             source's LOSING copy is preserved (recoverable, never deleted).
      conflicted -- dict rel_path -> (winner_slug, [loser_slug, ...]) for the
             dry-run plan display, so a reader sees which source wins each
             conflicting path before anything moves.
    """
    holders: dict[Path, list[Path]] = {}
    for src in sources:
        for p in src.rglob("*"):
            rel = p.relative_to(src)
            if p.is_file() and _migratable(rel):
                holders.setdefault(rel, []).append(src)
    win: dict[Path, Path | str] = {}
    lose: dict[tuple, str] = {}
    conflicted: dict[Path, tuple] = {}
    synth: dict[Path, bytes] = {}
    for rel, hs in holders.items():
        if len(hs) == 1:
            win[rel] = hs[0]
            continue
        if rel.name == "manifest.json":
            # Complementary halves, not versions: synthesize the UNION instead
            # of picking one file by slug. Every source's verbatim manifest is
            # still kept recoverable under `.conflicts/`. No single slug wins,
            # so the dry-run labels the winner `union`.
            win[rel] = _SYNTHESIZE
            synth[rel] = json.dumps(_merge_manifests(hs)).encode()
            los_slugs = []
            for loser in hs:
                slug = _src_slug(loser)
                los_slugs.append(slug)
                lose[(loser, rel)] = f".conflicts/{rel}.from-{slug}"
            conflicted[rel] = ("union", los_slugs)
            continue
        w = _conflict_winner(rel, hs)
        win[rel] = w
        los_slugs = []
        for loser in hs:
            if loser is w:
                continue
            slug = _src_slug(loser)
            los_slugs.append(slug)
            lose[(loser, rel)] = f".conflicts/{rel}.from-{slug}"
        conflicted[rel] = (_src_slug(w), los_slugs)
    return win, lose, conflicted, synth


def _merge_verified(sources: list[Path], target: Path, win: dict, lose: dict,
                    synth: dict) -> bool:
    """After the merge, every byte from every source is present in the target
    -- winner bytes at `target/rel`, synthesized union bytes at `target/rel`
    for a `_SYNTHESIZE` winner, loser bytes at their `.conflicts` path -- and
    nothing else. Symmetric: a copied target that is Missing or carries an
    unexpected file fails. The single operation that is this command's whole
    safety contract: never delete a source on the strength of "the target
    merely exists"."""
    expected: dict[str, bytes] = {}
    for src in sources:
        for p in src.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(src)
            if not _migratable(rel):
                continue
            if win.get(rel) is src:
                loc = target / rel
            else:
                loc = target / lose[(src, rel)]
            expected[str(loc.relative_to(target))] = p.read_bytes()
    for rel, data in synth.items():
        expected[str((target / rel).relative_to(target))] = data
    return expected == _dir_snapshot(target)


def _source_landed(src: Path, target: Path, win: dict, lose: dict) -> bool:
    """Did THIS source's own contribution land, byte-for-byte? The per-source
    half of remove-only-what-verifies: a source is removed only when its own
    winner bytes are at `target/rel` and its own losing bytes at its
    `.conflicts` path -- never because the target happens to exist or because
    a sibling verified."""
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        if not _migratable(rel):
            continue
        if win.get(rel) is src:
            loc = target / rel
        else:
            loc = target / lose[(src, rel)]
        try:
            if not loc.is_file() or loc.read_bytes() != p.read_bytes():
                return False
        except OSError:
            return False
    return True


#: A source iter dir is a sentence, not three states. Tolerantly tagged.
_MSG_DONE = "migrated"
_MSG_REFUSE = "REFUSE"


def _session_complete(
    main_graph: Path,
    iter_n,
    *,
    worktree: str | None = None,
    dry_run: bool = False,
    live_iters: set | None = None,
) -> int:
    """Merge every complete `iter_n` session dir under linked worktrees into
    the main checkout and return them to the round's home. Returns 0 only
    when at least one source migrated (a `--dry-run` returns 0 when it would).

    `main_graph` is the MAIN checkout's graph root. `worktree`, when given,
    restricts to one worktree slug. `live_iters`, when given as a set, is the
    reader's own liveness signal (test injection); otherwise it is computed
    read-only from the spawn budget. A `--branch` round may hold its session
    dir in TWO trees at once, so the bring-home is a MERGE: both sources land
    in the same target, a conflicting path is decided by content semantics
    (never scan order) with the loser kept recoverable under `.conflicts/`, and
    each source is removed only after ITS OWN contribution byte-verifies. A
    failed migrate leaves every involved side intact -- the partial target is
    removed, no source is touched until its own bytes agree.
    """
    dname = locations.iteration_dirname(iter_n)
    wt_root = main_graph / "worktrees"
    candidates: list[Path] = []
    if wt_root.is_dir():
        for tree in sorted(wt_root.glob("*")):
            if not tree.is_dir():
                continue
            if worktree and tree.name != worktree:
                continue
            sg = tree / ".agi"
            if not (sg / "config.json").is_file():
                continue
            it = sg / locations.SESSIONS_DIR_NAME / dname
            if it.is_dir():
                candidates.append(it)

    if not candidates:
        print(f"session-complete: no worktree holds an {dname} iter dir to "
              f"migrate (scanned {wt_root})")
        return 0 if dry_run else 1

    if live_iters is None:
        live_iters = spawn_budget.live_iteration_ids(main_graph)

    target = main_graph / locations.SESSIONS_DIR_NAME / dname
    # 🔴 THE TARGET-COLLISION GUARD. With two legal sources the natural merge
    # is to "merge into whatever is there", and that is exactly the sentence
    # a kid would write to loosen this. Do not. A pre-existing NON-EMPTY
    # target is content NOT produced by this invocation's own sources -- by
    # definition not one of this round's sources -- so it refuses, unchanged.
    # An empty placeholder (dispatch pre-creates one) is not data and may be
    # cleared, guarded by the `rmdir` that fails loudly on non-empty.
    if target.exists() and any(target.iterdir()):
        print(f"session-complete: {_MSG_REFUSE} {target} -- target already "
              f"exists and is not empty; refusing to overwrite")
        return 1

    # A round is ONE logical unit spread across trees. If ANY of its sources
    # is still live or its completeness cannot be judged, the whole round is
    # still running and NONE of it may come home -- migrating only the
    # finished half strands the other, precisely the half-a-round outcome this
    # command exists to prevent. With an old TWO-worktree round, however, only
    # the manifest-bearing half is judged for completeness; a manifest-LESS
    # partial copy is a CONTRIBUTOR, not a judge -- it rides into the merge
    # and never vetoes (hypothesis:l4-a-manifest-less-partial-source-never-
    # vetoes-a-rounds-bring-home).
    #
    # 1. LIVENESS is per-iteration and first: a live spawn-budget lease
    #    refuses the whole round whatever any record says.
    # 2. COMPLETENESS is judged only from manifest-bearing (authority)
    #    sources: no authority -> `no manifest.json in any source`; an
    #    authority with a non-terminal record refuses naming that agent and
    #    its status. A manifest-less candidate never refuses.
    ready: list[Path] = []
    refused_any = False
    if iter_n in live_iters:
        for src in candidates:
            print(f"session-complete: {_MSG_REFUSE} {src} -- a live lease is "
                  f"active for iteration {iter_n}; round still running")
        refused_any = True
    else:
        authorities = [s for s in candidates
                       if (s / "manifest.json").is_file()]
        if not authorities:
            print(f"session-complete: {_MSG_REFUSE} -- no manifest.json in any "
                  f"source for iteration {iter_n}; nothing to judge, nothing "
                  f"moves")
            refused_any = True
        else:
            for src in authorities:
                bad = _first_non_terminal(src)
                if bad is not None:
                    aid, st = bad
                    print(f"session-complete: {_MSG_REFUSE} {src} -- agent "
                          f"{aid} status={st} is not terminal; round still "
                          f"running")
                    refused_any = True
                    break
    if refused_any:
        return 0 if dry_run else 1
    ready = list(candidates)
    if not ready:
        return 0 if dry_run else 1

    win, lose, conflicted, synth = _merge_plan(ready)

    if dry_run:
        # 🔴 A dry run must show the MERGE PLAN, including which source wins
        # each conflicting path -- and it writes NOTHING (asserted on a
        # filesystem snapshot). At most it may print, never touch the tree.
        for src in sorted(ready, key=_src_slug):
            print(f"session-complete: WOULD migrate {src} -> {target}")
        for rel in sorted(conflicted, key=str):
            wslug, los = conflicted[rel]
            if wslug == "union":
                # a synthesized manifest union has no single slug winner
                print(f"session-complete: CONFLICT {rel} : union of "
                      f"{', '.join(los)}; original manifests kept at "
                      f".conflicts/{rel}.from-<slug>")
                continue
            for loser in los:
                print(f"session-complete: CONFLICT {rel} : {wslug} wins over "
                      f"{loser} (loser kept at .conflicts/{rel}.from-{loser})")
        return 0

    # COPY-THEN-VERIFY-THEN-REMOVE-EACH-SOURCE-BY-ITS-OWN-CONTRIBUTION.
    # Assemble the merged target from the plan first; only after the union
    # verifies is any source removed, and only its own contribution's.
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_dir():
            target.rmdir()  # clear a pre-created empty placeholder only
        for rel, wsrc in win.items():
            dp = target / rel
            dp.parent.mkdir(parents=True, exist_ok=True)
            if wsrc is _SYNTHESIZE:
                dp.write_bytes(synth[rel])
            else:
                shutil.copy2(wsrc / rel, dp)
        for (lsrc, rel), loc in lose.items():
            dp = target / loc
            dp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(lsrc / rel, dp)
    except (OSError, shutil.Error) as exc:
        print(f"session-complete: copy failed -> {target}: {exc}; "
              f"sources intact, no target left")
        shutil.rmtree(target, ignore_errors=True)
        return 1

    # The whole-round verification (the multi-source take on `_trees_match`).
    # A single conflict-free source still routes through `_trees_match` so the
    # byte-compare contract is one function, not two. If it fails, NO source
    # may be removed -- the target is discarded and every source left intact.
    if len(ready) == 1 and not lose:
        landed = _trees_match(ready[0], target)
    else:
        landed = _merge_verified(ready, target, win, lose, synth)
    if not landed:
        print(f"session-complete: VERIFY FAILED -> {target} -- source and "
              f"target differ; removing target, all sources intact")
        shutil.rmtree(target, ignore_errors=True)
        return 1

    # 🔴 PER-SOURCE removal. A source is removed only when ITS OWN
    # contribution verifies against the merged target -- not when the target
    # merely exists and not because a sibling verified. A source whose
    # contribution did not land stays in its worktree, recoverable.
    migrated = 0
    for src in sorted(ready, key=_src_slug):
        if _source_landed(src, target, win, lose):
            shutil.rmtree(src, ignore_errors=True)
            print(f"session-complete: {_MSG_DONE} {src} -> {target} "
                  f"(bytes match)")
            migrated += 1
        else:
            print(f"session-complete: {_MSG_REFUSE} {src} -- this source's own "
                  f"contribution did not verify; left intact at its worktree")

    return 0 if migrated else 1


def _main_graph_root(root: Path) -> Path:
    """The MAIN checkout's graph root, whether `root` is main or a worktree.

    A worktree's own graph root sits under `.agi/worktrees/<slug>/.agi`, and
    the linked worktrees hang off the MAIN graph tree -- so the migration
    must resolve to main before it can enumerate its own siblings. Mirrors
    `_sibling_session_lookup`: `git_common_root` finds the main checkout root,
    then `find_project_root` re-derives the graph directory there.
    """
    main = locations.git_common_root(root)
    if main is None or main == root:
        return root
    return locations.find_project_root(main) or root


def cmd_session_complete(args: argparse.Namespace) -> int:
    root = _find_root()
    main_graph = _main_graph_root(root)
    return _session_complete(
        main_graph,
        args.iter_n,
        worktree=args.worktree,
        dry_run=args.dry_run,
    )


def cmd_trimguard(args: argparse.Namespace) -> int:
    """hypothesis:l4-trimguard-subcommand — the HANDOFF.md §6 owner-quote-loss
    guard, folded in from .agi/sessions/trimguard.py (untracked) so a tracked
    tool owns the safety check the CLAUDE.md replacement policy depends on.

    Parse HANDOFF.md's '## §6 Owner decisions' section, extract every
    double-quoted span >= 25 chars (plus open-ended truncated quotes), grep
    .agi/nodes/ for each, and ABORT (exit 1) if any owner quote would be lost
    on a trim — else OK. Output and verdicts byte-identical to the original
    untracked script against the same HANDOFF.md fixture.
    """
    root = _find_root()          # the `.agi/` graph dir (locations convention)
    repo = root.parent           # checkout root — HANDOFF.md lives beside `.agi/`
    HAND = (repo / "HANDOFF.md").read_text().splitlines(True)
    start = next(i for i, l in enumerate(HAND) if l.startswith("## §6 Owner decisions"))
    sec = "".join(HAND[start:])
    spans = _collect_owner_spans(sec)
    print(
        f"§6 lines {start + 1}-{len(HAND)}  bytes={len(sec)}  real quoted spans: {len(spans)}"
    )
    missing = []
    for s in sorted(spans):
        probe = s[:55]
        r = subprocess.run(
            ["grep", "-rlF", probe, ".agi/nodes/"], cwd=repo, capture_output=True, text=True
        )
        if not r.stdout.split():
            missing.append(s)
            print(f"  MISSING  {probe!r}")
    if missing:
        print(f"\nABORT: {len(missing)} owner quote(s) resolve in NO node.")
        return 1
    print(f"\nOK: all {len(spans)} owner quotes resolve in .agi/nodes/ — safe to collapse.")
    return 0


def _collect_owner_spans(sec: str) -> set:
    """Extract every owner-quote span from a §6 body under QUOTE PARITY
    (hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span).

    A quote opens a span; the next quote closes it; an unterminated span
    counts only if it runs to end of ITS OWN line. An open-ended span is
    reported only when it STARTS at a real opening quote -- never at a quote
    the walk already consumed as the CLOSING quote of a closed span. The
    pre-fix code ran two independent regexes, and the open-ended one
    `["“]([^"“”\n]{25,})$` (re.M) matched the CLOSING quote of a closed
    span whenever that quote was the last on its line with 25+ non-quote
    chars after it, minting a phantom open span that wrongly ABORTed the
    trim on a fully-quoted line (HEADOFF §6 item 106).
    """
    MARK = re.compile(r"\s*\*?\(\d+ quotes? archived\)\*?\s*$")
    OPEN = '"“'   # what may OPEN a span
    CLOSE = '"”'  # what may CLOSE a span
    spans = set()
    for line in sec.splitlines():
        line = MARK.sub("", line)
        i, n = 0, len(line)
        while i < n:
            # A closing curly quote `”` outside a span is SKIPPED, never an
            # opener (hypothesis:l4-trimguard...). Only `"` and `“` open.
            if line[i] in OPEN:
                # a real opening quote: find the far edge of the span it bounds
                j = i + 1
                while j < n and line[j] not in CLOSE:
                    j += 1
                if j < n:
                    s = line[i + 1:j].strip().strip("*").strip()
                    if len(s) >= 25:
                        spans.add(s)
                    i = j + 1
                else:
                    # open-ended: quote runs to end of this line (truncated collapse)
                    s = line[i + 1:].strip().strip("*").strip()
                    s = " ".join(s.split(" ")[:-1])  # drop the truncated last word
                    if len(s) >= 25:
                        spans.add(s)
                    i = n
            else:
                i += 1
    return spans


def _post_rename_jobs(root: Path) -> list:
    """The worktree-owning seat rows to rename, read from the geometry config
    that is CURRENTLY on disk (post-first with the seats fallback, via
    geometry_config). Each job is {"name", "wt_rel"}: `name` is the seat name,
    `wt_rel` is the row's `worktree` cell (a repo-top-relative path whose
    basename spells `seat-<name>`). Rows whose worktree cell is empty, or that
    do not spell `seat-<name>`, are left alone (hypothesis:l4-a-seat-is-a-
    post-everywhere — rename only what the config itself declares).

    Parses the frontmatter directly (never node_writer, so a bare fixture node
    without parents/schema can be renamed) and never runs git.
    """
    path, key = geometry_config.resolve(root)
    jobs = []
    if path is None or not Path(path).exists():
        return jobs
    try:
        text = Path(path).read_text(encoding="utf-8")
        fm = frontmatter.read_frontmatter(text)
        if fm is None:
            return jobs
        rows = fm.get(key) or []
        if not isinstance(rows, list):
            return jobs
        for row in rows:
            if not isinstance(row, dict):
                continue
            wt = row.get("worktree") or ""
            base = Path(str(wt)).name
            if base.startswith("seat-") and len(base) > 5:
                jobs.append({"name": base[5:], "wt_rel": str(wt)})
    except Exception:  # noqa: BLE001  (a malformed config never takes the rename down)
        return jobs
    return jobs


def _post_rename_print(step: str, cmd: str, applied: bool,
                       rollback: str | None = None) -> None:
    tail = f"  -- rollback: {rollback}" if rollback else ""
    print(f"[{'APPLY' if applied else 'DRY '}] {step}: {cmd}{tail}")


def _post_rename_plan_path(root: Path) -> Path:
    """The resumability state file, under the graph root's sessions/ dir (a
    gitignored scratch area, so a clean checkout starts fresh)."""
    return Path(root) / "sessions" / "post-rename-plan.json"


def _post_rename_load_plan(root: Path) -> dict:
    """The {step_name: bool} done map, or {} when absent/corrupt."""
    try:
        data = _post_rename_plan_path(root).read_text(encoding="utf-8")
        loaded = json.loads(data)
        return loaded if isinstance(loaded, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _post_rename_save_plan(root: Path, text: str) -> None:
    """Atomically (write-then-rename) persist the plan file."""
    p = _post_rename_plan_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(p)


def _post_rename_has_origin(repo: Path) -> bool:
    r = subprocess.run(["git", "remote"], cwd=repo, capture_output=True, text=True)
    return "origin" in (r.stdout or "").split()


def _post_rename_current_branch(repo: Path) -> str:
    r = subprocess.run(["git", "branch", "--show-current"], cwd=repo,
                       capture_output=True, text=True)
    return (r.stdout or "").strip() or "HEAD"


def _post_rename_has_branch(repo: Path, branch: str) -> bool:
    r = subprocess.run(["git", "branch", "--list", branch], cwd=repo,
                       capture_output=True, text=True)
    return bool((r.stdout or "").strip())


def _post_rename_ls_remote(repo: Path, ref: str) -> bool:
    """True when `ref` (e.g. refs/heads/post/a@s2) exists on origin."""
    r = subprocess.run(["git", "ls-remote", "origin", ref], cwd=repo,
                       capture_output=True, text=True)
    return bool((r.stdout or "").strip())


def _post_rename_upstream(repo: Path, branch: str) -> str:
    """The upstream of `branch` (e.g. origin/post/a@s2) or '' when unset."""
    r = subprocess.run(["git", "rev-parse", "--abbrev-ref",
                        f"{branch}@{{upstream}}"], cwd=repo,
                       capture_output=True, text=True)
    return (r.stdout or "").strip()


def cmd_post_rename(args: argparse.Namespace) -> int:
    """hypothesis:l4-a-seat-is-a-post-everywhere — clause 3: the live rename
    (migration script + fixture proof; L4.306 FIX-ONLY). Renames the seat
    geometry to posts IN ORDER, printing every step AND its ROLLBACK:
      1. fetch
      2. git mv seats.md->posts.md, rewrite id:config:seats->config:posts and
         seats:->posts:, keeping mint_id BYTE-IDENTICAL
      3. COMMIT + PUSH posts.md as its own step (git add <dest> && commit; push
         the current branch when an `origin` exists) — leaves no dirty tree for
         the ack dirty-gate (L4.306 fix)
      4. git worktree move each .agi/worktrees/seat-<name> -> post-<name>
      5. git branch -m seat/<name>@s2 -> post/<name>@s2 (local)
      6. push the renamed branch (new) then delete the old, when origin exists
      7. git branch --set-upstream-to origin/post/<name>@s2 when origin exists
         (L4.306 fix: a bare `git push` in a renamed worktree fails without it)

    --dry-run changes NOTHING, prints the ordered steps, and does NOT write the
    plan file. --apply performs them against the --root graph (default: resolve
    normally — the LIVE tree, which is the Prime's job, never a kid's), recording
    each finished step in <root>/sessions/post-rename-plan.json so a re-run
    RESUME skips already-done steps (idempotent); each sub-operation also
    self-skips when its target state already holds, so a step that failed
    half-way through a job loop can resume. A failed step writes the plan
    recording exactly what completed before it. All git runs with cwd at the
    repo top derived from --root, so an --apply against a fixture tmp_path is
    hermetic and never touches the shared tree.
    """
    root = Path(args.root).resolve() if args.root else _find_root()
    apply = bool(args.apply)
    repo = root.parent if root.name == ".agi" else root  # checkout top for git
    cfg, _key = geometry_config.resolve(root)
    cfg = Path(cfg) if cfg else None

    if cfg is None:
        print("ERR: no geometry config to rename", file=sys.stderr)
        return 1
    # The SOURCE of the migration is always seats.md — never whatever resolve()
    # returned (post-first returns posts.md on a re-run). dest is always posts.md.
    seats_abs = cfg.parent / "seats.md"
    posts_abs = cfg.parent / "posts.md"
    seats_rel = seats_abs.relative_to(repo)
    dest = posts_abs.relative_to(repo)
    if not seats_abs.exists() and not posts_abs.exists():
        print("ERR: no geometry config (seats.md/posts.md) to rename", file=sys.stderr)
        return 1

    jobs = _post_rename_jobs(root)
    plan = _post_rename_load_plan(root) if apply else {}
    done = dict(plan.get("steps") or {})

    def step_done(key: str) -> bool:
        return bool(done.get(key))

    def mark(key: str) -> None:
        done[key] = True
        if apply:          # dry-run never writes the plan file
            _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))

    origin = _post_rename_has_origin(repo) if apply else False
    cur = _post_rename_current_branch(repo) if apply else "HEAD"

    # 1. fetch (dry-run: print only)
    _post_rename_print("fetch", "git fetch", apply)
    if apply and not step_done("fetch"):
        r = subprocess.run(["git", "fetch"], cwd=repo, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  note: git fetch rc={r.returncode} (no remote or offline); "
                  "continuing with the local rename", file=sys.stderr)
        mark("fetch")

    # 2. git mv seats.md -> posts.md + rewrite the frontmatter/worktree cells
    if posts_abs.exists() and not seats_abs.exists():
        _post_rename_print("git mv", f"skip {seats_rel} (already moved to {dest})",
                           apply, rollback=f"git mv {dest} {seats_rel}")
    else:
        _post_rename_print("git mv", f"git mv {seats_rel} {dest}", apply,
                           rollback=f"git mv {dest} {seats_rel}")
        _post_rename_print("rewrite frontmatter + worktree cells",
                           f"edit {dest} (id, seats:, worktree cells)", apply)
    if apply and not step_done("git_mv") and not (posts_abs.exists()
                                                   and not seats_abs.exists()):
        r = subprocess.run(["git", "mv", str(seats_rel), str(dest)], cwd=repo,
                           capture_output=True, text=True)
        if r.returncode != 0:
            _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
            print(f"ERR: git mv failed: {r.stderr.strip()}", file=sys.stderr)
            return 1
        posts_abs.write_text(
            _post_rename_rewrite(posts_abs.read_text(encoding="utf-8"),
                                 [j["name"] for j in jobs]),
            encoding="utf-8")
        mark("git_mv")
    elif apply and not step_done("git_mv"):
        mark("git_mv")   # already migrated (posts.md present, seats.md gone)

    # 3. COMMIT + PUSH posts.md as its OWN step (L4.306 fix: the ack dirty-gate
    #    refuses every ack while the tree is dirty — commit posts.md so a
    #    migrated tree is clean; push the current branch when origin exists)
    commit_cmds = [f"git add {dest}",
                   'git commit -m "post-rename: seats.md -> posts.md"']
    if origin:
        commit_cmds.append(f"git push origin {cur}")
    _post_rename_print("commit posts.md", " && ".join(commit_cmds), apply,
                       rollback="git reset --soft HEAD~1 && git mv posts.md seats.md")
    if apply and not step_done("commit_posts"):
        if not (posts_abs.exists() and not seats_abs.exists()):
            _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
            print("ERR: commit step reached before the git mv; aborting",
                  file=sys.stderr)
            return 1
        r_add = subprocess.run(["git", "add", str(dest)], cwd=repo,
                               capture_output=True, text=True)
        r_com = subprocess.run(["git", "commit", "-m",
                                "post-rename: seats.md -> posts.md"],
                               cwd=repo, capture_output=True, text=True)
        if r_com.returncode != 0 and "nothing to commit" not in r_com.stderr:
            _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
            print(f"ERR: git commit posts.md failed: {r_com.stderr.strip()}",
                  file=sys.stderr)
            return 1
        if origin:
            r_pu = subprocess.run(["git", "push", "origin", cur], cwd=repo,
                                  capture_output=True, text=True)
            if r_pu.returncode != 0:
                print(f"  note: git push origin {cur} rc={r_pu.returncode} "
                      f"(commit kept locally); {r_pu.stderr.strip()}",
                      file=sys.stderr)
        mark("commit_posts")

    # 4. git worktree move each seat-<name> -> post-<name>
    for j in jobs:
        old = j["wt_rel"]
        new = old.replace("seat-" + j["name"], "post-" + j["name"])
        skip = (repo / new).exists() and not (repo / old).exists()
        cmd = (f"git worktree move {old} {new}" if not skip
               else f"skip {old} (already {new})")
        _post_rename_print("git worktree move", cmd, apply,
                           rollback=f"git worktree move {new} {old}")
        if apply and not step_done("worktree_move") and not skip:
            r = subprocess.run(["git", "worktree", "move", old, new],
                               cwd=repo, capture_output=True, text=True)
            if r.returncode != 0:
                _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
                print(f"ERR: git worktree move {old} failed: {r.stderr.strip()}",
                      file=sys.stderr)
                return 1
    if apply:
        mark("worktree_move")

    # 5. rename branches local
    for j in jobs:
        old_b = f"seat/{j['name']}@s2"
        new_b = f"post/{j['name']}@s2"
        skip = _post_rename_has_branch(repo, new_b) and not _post_rename_has_branch(repo, old_b)
        cmd = (f"git branch -m {old_b} {new_b}" if not skip
               else f"skip {old_b} (already {new_b})")
        _post_rename_print("branch rename (local)", cmd, apply,
                           rollback=f"git branch -m {new_b} {old_b}")
        if apply and not step_done("branch_rename") and not skip:
            r = subprocess.run(["git", "branch", "-m", old_b, new_b],
                               cwd=repo, capture_output=True, text=True)
            if r.returncode != 0:
                _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
                print(f"ERR: git branch -m {old_b} failed: {r.stderr.strip()}",
                      file=sys.stderr)
                return 1
    if apply:
        mark("branch_rename")

    # 6. push the renamed branch (new, then delete old LAST) — when origin exists
    for j in jobs:
        old_b = f"seat/{j['name']}@s2"
        new_b = f"post/{j['name']}@s2"
        _post_rename_print("branch push (remote)",
                           f"git push origin {new_b} ; git push origin --delete {old_b}",
                           apply,
                           rollback=f"git push origin {old_b} ; git push origin --delete {new_b}")
    if apply and not step_done("branch_push"):
        if origin:
            for j in jobs:
                old_b = f"seat/{j['name']}@s2"
                new_b = f"post/{j['name']}@s2"
                if not _post_rename_ls_remote(repo, f"refs/heads/{new_b}"):
                    r = subprocess.run(["git", "push", "origin", new_b], cwd=repo,
                                       capture_output=True, text=True)
                    if r.returncode != 0:
                        _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
                        print(f"ERR: git push origin {new_b} failed: {r.stderr.strip()}",
                              file=sys.stderr)
                        return 1
                if _post_rename_ls_remote(repo, f"refs/heads/{old_b}"):
                    r = subprocess.run(["git", "push", "origin", "--delete", old_b],
                                       cwd=repo, capture_output=True, text=True)
                    if r.returncode != 0:
                        _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
                        print(f"ERR: git push origin --delete {old_b} failed: "
                              f"{r.stderr.strip()}", file=sys.stderr)
                        return 1
        mark("branch_push")

    # 7. set the upstream on each renamed branch (L4.306 fix) — after the push,
    #    so origin/post/<name>@s2 exists to bind to
    for j in jobs:
        new_b = f"post/{j['name']}@s2"
        _post_rename_print("branch upstream",
                           f"git branch --set-upstream-to origin/{new_b} {new_b}",
                           apply,
                           rollback=f"git branch --unset-upstream {new_b}")
    if apply and not step_done("branch_upstream"):
        if origin:
            for j in jobs:
                new_b = f"post/{j['name']}@s2"
                if _post_rename_upstream(repo, new_b):
                    continue
                r = subprocess.run(["git", "branch", "--set-upstream-to",
                                    f"origin/{new_b}", new_b], cwd=repo,
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    _post_rename_save_plan(root, json.dumps({"steps": done}, indent=2))
                    print(f"ERR: git branch --set-upstream-to origin/{new_b} failed: "
                          f"{r.stderr.strip()}", file=sys.stderr)
                    return 1
        mark("branch_upstream")

    print("dry-run: nothing changed" if not apply else "rename applied")
    return 0


def _post_rename_rewrite(text: str, names: list) -> str:
    """Return `text` with the seat->post renames applied line-preserving:
    `id: config:seats` -> `id: config:posts`, the bare list key `seats:` ->
    `posts:`, and every row `worktree` cell `seat-<name>` -> `post-<name>`.
    Every other line — most importantly `mint_id` — is passed through
    BYTE-IDENTICAL (hypothesis:l4-a-seat-is-a-post-everywhere: never edit
    mint_id, and never touch any row value but the worktree cell).
    """
    out = []
    for line in text.splitlines(keepends=True):
        s = line
        if s.startswith("id: config:seats"):
            s = s.replace("id: config:seats", "id: config:posts", 1)
        if s.strip() == "seats:":
            s = s.replace("seats:", "posts:", 1)
        for name in names:
            old = f'"worktree": ".agi/worktrees/seat-{name}"'
            new = f'"worktree": ".agi/worktrees/post-{name}"'
            if old in s:
                s = s.replace(old, new, 1)
        out.append(s)
    return "".join(out)


# --------------------------------------------------------------------------
# hypothesis:l4-branches-follow-the-season-grammar — `branch-reshuffle`.
# clause 3: ONE migration script renames local + remote branches from the
# legacy season spellings to the canonical season grammar, re-points every
# post worktree onto the new name, and PROPOSES (never writes) the ladder
# cells + the config:rotations F14 fact re-spellings — those two files are
# the Prime's cells. `--apply` is exercised ONLY against a --root fixture,
# never the live tree unless --root is omitted (the Prime's job).
# ---------------------------------------------------------------------------

_RS_SEASON_RE = re.compile(r"^season/s(\d+)$")
_RS_TOWN_RE = re.compile(r"^town/(.+?)/season/s(\d+)$")
_RS_LOOP_RE = re.compile(r"^loop/(.+?)@s(\d+)$")
_RS_SEAT_RE = re.compile(r"^seat/(.+?)@s(\d+)$")
_RS_LEGACY_RE = re.compile(r"\b(season/s\d+|town/[^\s\"',:]+/season/s\d+|loop/[^\s\"',:]+@s\d+|seat/[^\s\"',:]+@s\d+)\b")

# Cell files whose legacy branch spellings the migration PROPOSES to rewrite
# but must never edit directly (Prime-owned graph cells).
_RS_CELL_FILES = [
    "nodes/.geometry/ladder.md",
    "nodes/.geometry/rotations.md",
]


def _reshuffle_canonical(branch: str, season: int) -> str | None:
    """Canonical season-grammar name for a legacy `branch`, or None when it is
    already canonical / not legacy. Each mapping is the inverse of
    branches.py `_canonical_to_old`:
      season/s<N>          -> season<N>/main
      town/<t>/season/s<N> -> season<S>/<t>/season<N>/main   (S = root season)
      loop/<slug>@s<N>     -> season<N>/loops/<slug>
      seat/<name>@s<N>     -> season<N>/posts/<name>
    None leaves a feature branch or an already-canonical name alone."""
    m = _RS_SEASON_RE.match(branch)
    if m:
        return f"season{m.group(1)}/main"
    m = _RS_TOWN_RE.match(branch)
    if m:
        return f"season{season}/{m.group(1)}/season{m.group(2)}/main"
    m = _RS_LOOP_RE.match(branch)
    if m:
        return f"season{m.group(2)}/loops/{m.group(1)}"
    m = _RS_SEAT_RE.match(branch)
    if m:
        return f"season{m.group(2)}/posts/{m.group(1)}"
    return None


def _reshuffle_season(root: Path, arg_season: int | None) -> int:
    """The root season to build town main names from: the ladder's
    `current_season` frontmatter unless --season overrides it."""
    if arg_season is not None:
        return arg_season
    try:
        import yaml
        text = (root / "nodes/.geometry/ladder.md").read_text(encoding="utf-8")
        parted = frontmatter.split_frontmatter(text)
        if parted is not None:
            fm = yaml.safe_load(parted[0]) or {}
            return int(fm.get("current_season", 2))
    except Exception:  # noqa: BLE001 (missing/garbled ladder never blocks)
        pass
    return 2


def _reshuffle_branches(repo: Path) -> list[str]:
    """Every local + origin-tracking branch short name at `repo`."""
    out: list[str] = []
    r = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"],
        cwd=repo, capture_output=True, text=True)
    out += [b for b in r.stdout.split() if b]
    r = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes"],
        cwd=repo, capture_output=True, text=True)
    for b in r.stdout.split():
        if b.startswith("origin/") and len(b) > len("origin/"):
            out.append(b[len("origin/"):])
    # dedupe, keep order
    seen: set[str] = set()
    uniq = []
    for b in out:
        if b not in seen:
            seen.add(b)
            uniq.append(b)
    return uniq


def _reshuffle_jobs(repo: Path, season: int) -> list[dict]:
    """[{old,new}] branch renames, old name first, for every legacy branch at
    `repo`. Never runs a mutation, only for-each-ref reads."""
    jobs: dict[str, str] = {}
    for b in _reshuffle_branches(repo):
        new = _reshuffle_canonical(b, season)
        if new and new != b:
            jobs[b] = new
    return [{"old": k, "new": v} for k, v in sorted(jobs.items())]


def _reshuffle_worktrees(repo: Path) -> list[dict]:
    """[{path, branch}] worktrees on a legacy branch, from `git worktree list
    --porcelain`. Never mutates."""
    r = subprocess.run(["git", "worktree", "list", "--porcelain"],
                       cwd=repo, capture_output=True, text=True)
    wts: list[dict] = []
    for block in r.stdout.split("\n\n"):
        path = branch = None
        for line in block.splitlines():
            if line.startswith("worktree "):
                path = line[len("worktree "):]
            elif line.startswith("branch refs/heads/"):
                branch = line[len("branch refs/heads/"):]
        if path and branch and _reshuffle_canonical(branch, 1):
            wts.append({"path": path, "branch": branch})
    return wts


def _reshuffle_cell_edits(root: Path, season: int, jobs: list[dict]) -> list[str]:
    """Proposed (never applied) cell re-spellings for the Prime-owned cells.
    Each legacy spelling in the ladder/rotations cells is mapped through the
    same grammar as the branches, so a `core: season/s2` ladder cell reads as
    a `core: season2/main` proposal. Returns printable lines only; the caller
    prints them and writes nothing."""
    edits: list[str] = []
    for rel in _RS_CELL_FILES:
        p = root / rel
        if not p.exists():
            continue
        for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for tok in _RS_LEGACY_RE.findall(line):
                new = _reshuffle_canonical(tok, season)
                if new and new != tok:
                    edits.append(f"  {rel}:{ln}: {tok} -> {new}")
    return edits


def _reshuffle_refs_grid(repo: Path) -> str:
    """Byte source of truth for the refs/grid namespace: refname + object name
    per ref, one per line, refs sorted. Compare before/after for identity."""
    r = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid"],
        cwd=repo, capture_output=True, text=True)
    return "\n".join(sorted(r.stdout.splitlines())) + "\n"


_RESHUFFLE_KIND_ALIASES = {"main": "main", "mains": "main", "post": "post",
                           "posts": "post", "loop": "loop", "loops": "loop",
                           "town": "town_main", "towns": "town_main",
                           "town_main": "town_main"}


def _reshuffle_kinds(spec: str) -> set[str]:
    """`--kinds main,posts,towns` -> {"main", "post", "town_main"}; empty
    spec -> empty set (no filter). An unknown word is refused by name."""
    kinds: set[str] = set()
    for word in (w.strip().lower() for w in spec.split(",") if w.strip()):
        if word not in _RESHUFFLE_KIND_ALIASES:
            raise SystemExit(f"ERR: --kinds: unknown kind {word!r} "
                             f"(one of main, posts, loops, towns)")
        kinds.add(_RESHUFFLE_KIND_ALIASES[word])
    return kinds


def _reshuffle_kind(canonical: str) -> str:
    """The grammar kind of a canonical branch name ('' when unparseable)."""
    import branches  # noqa: PLC0415  (same dir; keeps cli.py's import list)
    try:
        return str(branches.parse(canonical).get("kind") or "")
    except Exception:  # noqa: BLE001
        return ""


def cmd_branch_reshuffle(args: argparse.Namespace) -> int:
    """hypothesis:l4-branches-follow-the-season-grammar clause 3 — the one
    migration script. --dry-run prints exactly what it WOULD do and touches
    nothing (the default when neither --apply nor --delete-old is given).
    --apply performs the local renames, pushes the new remote branch, and
    re-points every post worktree; it NEVER implies the remote delete. The
    remote delete is the separate --delete-old step, which refuses unless a
    green suite stamp exists. The ladder/rotations cell re-spellings are
    printed as proposals, never written. All git runs are cwd at `repo`
    derived from --root, so an --apply against a fixture is hermetic."""
    root = Path(args.root).resolve() if args.root else _find_root()
    repo = root.parent if root.name == ".agi" else root
    season = _reshuffle_season(root, args.season)
    apply = bool(args.apply)
    delete_old = bool(args.delete_old)
    if apply and delete_old:
        print("ERR: --apply and --delete-old are mutually exclusive; "
              "--delete-old is the separate final step", file=sys.stderr)
        return 1

    jobs = _reshuffle_jobs(repo, season)
    # Prime XIV ruling (mur-44 window, 04:18Z): `--kinds main,posts,towns`
    # runs FIRST and leaves the ~312 dead loop/* branches on their old
    # names -- harvest notes and experiment nodes cite them by name, and a
    # rename would make every citation stale for nothing. The kind of a job
    # is the kind of its NEW (canonical) name: main | post | loop | town_main.
    kinds = _reshuffle_kinds(getattr(args, "kinds", "") or "")
    if kinds:
        jobs = [j for j in jobs if _reshuffle_kind(j["new"]) in kinds]
    if not jobs:
        print("branch-reshuffle: no legacy branches to reshuffle")
        print("dry-run: nothing changed" if not (apply or delete_old) else "")
        return 0

    grid_before = _reshuffle_refs_grid(repo)

    # worktree re-points (post worktrees on a renamed branch)
    wts = _reshuffle_worktrees(repo)
    rename = {j["old"]: j["new"] for j in jobs}
    # ---- step 1: local rename + push new + worktree re-points
    print(f"branch-reshuffle (season={season}): {len(jobs)} legacy branch(es)")
    for j in jobs:
        _post_rename_print("branch rename (local)", f"git branch -m {j['old']} {j['new']}", apply)
        _post_rename_print("branch push (new)", f"git push origin {j['new']}", apply)
    for wt in wts:
        new = rename.get(wt["branch"])
        if new:
            _post_rename_print("worktree re-point",
                               f"git -C {wt['path']} checkout {new}", apply)

    # ---- ladder + rotations cell proposals (Prime-owned: print, never write)
    print("  cell re-spellings (PRINTED ONLY, Prime applies them):")
    for e in _reshuffle_cell_edits(root, season, jobs):
        print(e)
    if not _reshuffle_cell_edits(root, season, jobs):
        print("  (no legacy spellings found in ladder/rotations cells)")

    # ---- the remote delete is a SEPARATE step, never implied by --apply
    print("  NOTE: remote delete is NOT implied by --apply; run --delete-old "
          "separately, and only after the suite is green.")

    if delete_old:
        # root is the graph dir (.agi), so the stamp is under sessions/ there.
        stamp = root / "sessions/verified.stamp"
        if not stamp.exists():
            print(f"ERR: --delete-old refuses: no green suite stamp at {stamp}",
                  file=sys.stderr)
            return 3
        for j in jobs:
            _post_rename_print("branch delete (remote)",
                               f"git push origin --delete {j['old']}", True)
        print("delete-old: remote legacy branches removed")
        return 0

    if apply:
        # perform the local renames
        for j in jobs:
            r = subprocess.run(["git", "branch", "-m", j["old"], j["new"]],
                               cwd=repo, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"ERR: git branch -m {j['old']} failed: {r.stderr.strip()}",
                      file=sys.stderr)
                return 1
            # push the new branch to origin if origin exists
            rem = subprocess.run(["git", "remote"], cwd=repo,
                                 capture_output=True, text=True)
            if "origin" in rem.stdout.split():
                pr = subprocess.run(["git", "push", "origin", j["new"]],
                                    cwd=repo, capture_output=True, text=True)
                if pr.returncode != 0:
                    print(f"ERR: git push origin {j['new']} failed: "
                          f"{pr.stderr.strip()}", file=sys.stderr)
                    return 1
        # re-point worktrees
        for wt in wts:
            new = rename.get(wt["branch"])
            if not new:
                continue
            r = subprocess.run(["git", "-C", wt["path"], "checkout", new],
                               cwd=repo, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"ERR: git -C {wt['path']} checkout {new} failed: "
                      f"{r.stderr.strip()}", file=sys.stderr)
                return 1
        grid_after = _reshuffle_refs_grid(repo)
        same = "IDENTICAL" if grid_after == grid_before else "CHANGED"
        print(f"refs/grid: {same} before/after --apply (expected IDENTICAL)")
        print("apply: local renames + worktree re-points done; remote legacy "
              "branches NOT deleted (see --delete-old)")
        return 0

    print("dry-run: nothing changed")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_done = sub.add_parser("done")
    p_done.add_argument("iter_n", type=locations.iteration_id)
    p_done.add_argument("agent_id")
    p_done.add_argument("--verdict", required=True)
    p_done.add_argument("--confidence", type=float, default=0.5)
    p_done.add_argument("--node-id", default=None)
    p_done.add_argument("--parent", default=None)
    p_done.add_argument("--notes", default="")
    p_done.add_argument("--next-edge", default=None)
    p_done.add_argument(
        "--push-further",
        default=None,
        help="hypothesis:l3w4-push-further-loops — stamp `push_further: TEXT` "
             "on the node through the same gated writer --next-edge uses, so "
             "a later re-dispatch at this node id composes the continuation "
             "kid from this text.",
    )
    p_done.add_argument(
        "--owns", nargs="+", default=None, metavar="NODE_ID",
        help="goal:s27 — the kid node ids this agent is responsible for. A "
             "PARENT passes these instead of --node-id: it authors nothing of "
             "its own, so its completion is its kids' completion, propagated. "
             "Review prose belongs in those nodes' THOUGHT blocks until "
             "session linking lands (goal:g2.7, goal:g10.1).")
    p_done.add_argument(
        "--evidence-runs", nargs="+", default=None, metavar="NODE_ID",
        help="node ids of the backing experiment runs, e.g. --evidence-runs "
             "exp:foo-r1 exp:foo-r2. proved/disproved require at least one that "
             "resolves to a real node (TODO.md H4, goal:g3.1, goal:g7.3). "
             "Omitted = inferred from the node file's frontmatter. A bare "
             "count is accepted on the command line but no longer certifies "
             "anything: goal:g7.3 closed that hole, because a number nobody "
             "can resolve is exactly as cheap to type as the `synthetic` "
             "sentinel H4c already removed.")
    p_done.add_argument(
        "--no-evidence-gate", action="store_true",
        help="LOUDLY bypass the H4 evidence gate. For backfills/imports of "
             "historical nodes whose evidence lives outside the corpus. Stamps "
             "'evidence_gate: bypassed' on the node.")
    p_done.add_argument(
        "--no-spawn-gate", action="store_true",
        help="LOUDLY bypass the S17 spawn gate on the fallback verdict-node "
             "path. Stamps 'spawn_gate: bypassed'; treat as unreviewed.")
    p_done.set_defaults(func=cmd_done)

    p_pend = sub.add_parser("pending")
    p_pend.add_argument("iter_n", type=locations.iteration_id)
    p_pend.add_argument("agent_id")
    p_pend.add_argument("--reason", required=True)
    p_pend.set_defaults(func=cmd_pending)

    p_scaffold = sub.add_parser("scaffold")
    p_scaffold.add_argument("iter_n", type=locations.iteration_id)
    p_scaffold.add_argument("agent_id")
    p_scaffold.add_argument("--type", dest="node_type", required=True, choices=NODE_TYPES)
    p_scaffold.add_argument(
        "--parent", dest="parents", action="append", default=[],
        help="repeatable. How many are legal is decided by the type's spawn: "
             "block in context/schemas/[<type>].md (goal:s17), not by this "
             "flag -- omitting it is legal only for a parentless-legal type "
             "and is otherwise rejected by name.")
    p_scaffold.add_argument("--slug", required=True)
    p_scaffold.add_argument(
        "--no-spawn-gate", action="store_true",
        help="LOUDLY bypass the S17 spawn gate. Stamps 'spawn_gate: bypassed' "
             "on the node; treat any such node as unreviewed.")
    p_scaffold.set_defaults(func=cmd_scaffold)

    p_stat = sub.add_parser("status")
    p_stat.add_argument("iter_n", type=locations.iteration_id)
    p_stat.set_defaults(func=cmd_status)

    p_claim = sub.add_parser("claim")
    p_claim.add_argument("--node-id", required=True)
    p_claim.add_argument("--session", required=True)
    p_claim.set_defaults(func=cmd_claim)

    p_stale = sub.add_parser("detect-stale")
    p_stale.add_argument("--threshold-seconds", type=int, default=300)
    p_stale.set_defaults(func=cmd_detect_stale)

    p_reclaim = sub.add_parser("reclaim")
    p_reclaim.add_argument("--node-id", required=True)
    p_reclaim.add_argument("--session", required=True)
    p_reclaim.set_defaults(func=cmd_reclaim)

    p_sc = sub.add_parser(
        "session-complete",
        help="migrate a finished round's session dir from a worktree into "
             "main -- copy-then-verify, never move",
    )
    p_sc.add_argument("iter_n", type=locations.iteration_id)
    p_sc.add_argument(
        "--worktree", default=None,
        help="restrict migration to one worktree slug (default: all linked "
             "worktrees holding this iter dir)",
    )
    p_sc.add_argument(
        "--dry-run", action="store_true",
        help="print what would move and touch nothing -- the default "
             "testing posture",
    )
    p_sc.set_defaults(func=cmd_session_complete)

    p_tg = sub.add_parser(
        "trimguard",
        help="hypothesis:l4-trimguard-subcommand — §6 owner-quote-loss guard: "
             "ABORT if any double-quoted owner span in HANDOFF.md §6 resolves in "
             "no .agi/nodes/ file, else OK. Fold of the untracked trimguard.py.",
    )
    p_tg.set_defaults(func=cmd_trimguard)

    p_pr = sub.add_parser(
        "post-rename",
        help="hypothesis:l4-a-seat-is-a-post-everywhere — rename the seat "
             "geometry to posts IN ORDER (seats.md->posts.md, worktree cells, "
             "worktree dirs, branches). --dry-run prints the exact steps and "
             "changes nothing; --apply performs them against --root (never the "
             "live tree unless --root is omitted, which is the Prime's job).",
    )
    p_pr.add_argument(
        "--dry-run", action="store_true",
        help="print the ordered steps and change NOTHING — the default testing "
             "posture and the only mode a fixture may use without --root.")
    p_pr.add_argument(
        "--apply", action="store_true",
        help="perform the rename IN ORDER (git mv, rewrite, worktree move, "
             "branch rename). Dangerous against the live tree; always pass "
             "--root <fixture> in tests.")
    p_pr.add_argument(
        "--root", default=None,
        help="the graph root (.agi dir) to act on — required to run against a "
             "fixture repo; default resolves the live tree normally.")
    p_pr.set_defaults(func=cmd_post_rename)

    p_rs = sub.add_parser(
        "branch-reshuffle",
        help="hypothesis:l4-branches-follow-the-season-grammar — migration "
             "script: rename local + remote branches from legacy season "
             "spellings to the canonical grammar, re-point post worktrees, "
             "and PROPOSE (never write) the ladder/rotations cell "
             "re-spellings. --dry-run prints; --apply performs against "
             "--root; --delete-old is the separate final step that refuses "
             "without a green suite stamp.",
    )
    p_rs.add_argument(
        "--dry-run", action="store_true",
        help="print exactly what it WOULD do and change NOTHING — the "
             "default testing posture and the only allowed mode on this tree "
             "without --root.")
    p_rs.add_argument(
        "--apply", action="store_true",
        help="perform the local renames, push new remotes, and re-point "
             "worktrees. NEVER implies the remote delete. Against the live "
             "tree only when --root is omitted — the Prime's job.")
    p_rs.add_argument(
        "--delete-old", action="store_true",
        help="SEPARATE final step: git push origin --delete <old> for each "
             "reshuffled branch. REFUSES unless the green suite stamp exists.")
    p_rs.add_argument(
        "--root", default=None,
        help="the graph root (.agi dir) to act on — required to run --apply "
             "against a fixture repo; default resolves the live tree normally.")
    p_rs.add_argument(
        "--kinds", default="",
        help="comma list of kinds to reshuffle (main, posts, towns, loops); "
             "empty = every legacy branch. Prime ruling: --kinds "
             "main,posts,towns FIRST, dead loop/* keep their cited names")
    p_rs.add_argument(
        "--season", type=int, default=None,
        help="root season for town-main renames (default: ladder "
             "current_season).")
    p_rs.set_defaults(func=cmd_branch_reshuffle)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

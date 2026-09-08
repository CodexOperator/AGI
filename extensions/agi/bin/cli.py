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
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_gate  # noqa: E402
import locations  # noqa: E402
import node_writer  # noqa: E402
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
    """The project's ONE session-dir root across every git worktree.

    hypothesis:l3-cli-done-worktree-manifest — a `--branch` agent's session
    state lives in the MAIN checkout, and `cli.py done` must find it from the
    agent's own cwd. Agent session state (the per-agent `agent.json` and the
    iteration `manifest.json`) is the LOOP'S bookkeeping, and bookkeeping is
    one body across worktrees — the same rule as the spawn budget, the comms
    root, the meter pins and `.env`, which all resolve through
    `locations.shared_project_root`. The graph a kid edits is FORKED (that is
    the worktree); the record `done`/`scaffold` read and write is SHARED.
    """
    local = _find_root()
    return locations.shared_project_root(local) or local


def _agent_path(root: Path, iter_n: int | str, agent_id: str) -> Path:
    # `iter_n` is a legacy int (`iter-007`) or a loop-scoped str (`iter-L1.08`);
    # `locations` is the one place either is spelled as a directory.
    return locations.iteration_dir(root, iter_n) / agent_id / "agent.json"


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
        import yaml
        text = nf.read_text()
        if not text.startswith("---"):
            return None
        fm = yaml.safe_load(text.split("---", 2)[1]) or {}
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

    if not text.startswith("---"):
        return False, None, "missing opening `---` delimiter"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False, None, "unterminated `---` block (no closing delimiter)"
    try:
        fm = yaml.safe_load(parts[1])
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
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            body = parts[2]
            header = parts[1]
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
    # Session record is SHARED (main checkout) so a `--branch` parent running
    # in its worktree resolves the same agent.json its dispatch (from main)
    # wrote — not an empty worktree copy (hypothesis:l3-cli-done-worktree-manifest).
    sroot = _session_root()
    ap = _agent_path(sroot, args.iter_n, args.agent_id)
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

    # Write or update the node file with verdict info
    if args.node_id:
        node_file = _find_node_file(root, args.node_id)
        if node_file and node_file.exists():
            _append_verdict_to_node(node_file, verdict, args.confidence, args.notes,
                                    args.next_edge, gate, root=root,
                                    node_id=args.node_id,
                                    evidence_runs=args.evidence_runs)
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
            except Exception as exc:
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

    print(f"agent {args.agent_id} status=done verdict={verdict}")
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    root = _find_root()
    ap = _agent_path(_session_root(), args.iter_n, args.agent_id)
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
    # The record is SHARED (main checkout), same as `done` reads it.
    ap = _agent_path(sroot, args.iter_n, args.agent_id)
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

            parts = content.split("---", 2)
            if len(parts) < 3:
                return False, f"malformed frontmatter in {node_file}"
            fm_text, body = parts[1], parts[2]

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
            if not content.startswith("---"):
                continue
            parts = content.split("---", 2)
            if len(parts) < 2:
                continue
            fm = yaml.safe_load(parts[1]) or {}
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
                            evidence_runs: list | tuple | None = None) -> None:
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
    # Manifest + agent records are SHARED across worktrees
    # (hypothesis:l3-cli-done-worktree-manifest); resolve the session-side
    # root to the main checkout, never the worktree a caller stands in.
    root = _find_root()
    sroot = _session_root()
    iter_dir = locations.iteration_dir(sroot, args.iter_n)
    manifest = iter_dir / "manifest.json"
    if not manifest.exists():
        print(f"ERR: no manifest at {manifest}", file=sys.stderr)
        return 1
    m = json.loads(manifest.read_text())
    print(f"iter {args.iter_n}: {len(m['agents'])} agents")
    for a in m["agents"]:
        ap = _agent_path(sroot, args.iter_n, a["id"])
        rec = json.loads(ap.read_text()) if ap.exists() else a
        print(f"  {rec['id']}: status={rec.get('status')} verdict={rec.get('verdict', '-')} pid={rec.get('pid')}")
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

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

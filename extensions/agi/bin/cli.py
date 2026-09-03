#!/usr/bin/env python3
"""cli.py — agent-facing completion + verdict-emission CLI.

Agents call this to signal they're done. The driver picks up the rest.

Subcommands:
  done <iter_n> <agent_id> --verdict X --confidence Y [--node-id Z] [--parent P] [--notes ...]
  pending <iter_n> <agent_id> --reason "stuck on X"
  scaffold <iter_n> <agent_id> --type <node_type> --parent <parent_id> --slug <slug>
  status <iter_n>      — print all agent statuses for iter
"""
from __future__ import annotations

import argparse
import json
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


def _agent_path(root: Path, iter_n: int, agent_id: str) -> Path:
    return root / "sessions" / f"iter-{iter_n:03d}" / agent_id / "agent.json"


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
    ap = _agent_path(root, args.iter_n, args.agent_id)
    if not ap.exists():
        print(f"ERR: no agent record at {ap}", file=sys.stderr)
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
    corpus = evidence_gate.build_corpus(root / "nodes")
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
                                    node_id=args.node_id)
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

    print(f"agent {args.agent_id} status=done verdict={verdict}")
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    root = _find_root()
    ap = _agent_path(root, args.iter_n, args.agent_id)
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

    # Record scaffold in agent.json so cli.py done knows what to update
    ap = _agent_path(root, args.iter_n, args.agent_id)
    if ap.exists():
        rec = json.loads(ap.read_text())
        rec["scaffolded_node"] = res.node_id
        rec["scaffolded_file"] = str(res.path)
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
                            node_id: str | None = None) -> None:
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
    body = node_file.read_text() if notes else ""
    if notes and notes.strip() not in body:
        with open(node_file, "a") as f:
            f.write(f"\n\n## Agent Notes\n{notes}\n")


def cmd_status(args: argparse.Namespace) -> int:
    root = _find_root()
    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
    manifest = iter_dir / "manifest.json"
    if not manifest.exists():
        print(f"ERR: no manifest at {manifest}", file=sys.stderr)
        return 1
    m = json.loads(manifest.read_text())
    print(f"iter {args.iter_n}: {len(m['agents'])} agents")
    for a in m["agents"]:
        ap = _agent_path(root, args.iter_n, a["id"])
        rec = json.loads(ap.read_text()) if ap.exists() else a
        print(f"  {rec['id']}: status={rec.get('status')} verdict={rec.get('verdict', '-')} pid={rec.get('pid')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_done = sub.add_parser("done")
    p_done.add_argument("iter_n", type=int)
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
    p_pend.add_argument("iter_n", type=int)
    p_pend.add_argument("agent_id")
    p_pend.add_argument("--reason", required=True)
    p_pend.set_defaults(func=cmd_pending)

    p_scaffold = sub.add_parser("scaffold")
    p_scaffold.add_argument("iter_n", type=int)
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
    p_stat.add_argument("iter_n", type=int)
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

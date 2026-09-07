#!/usr/bin/env python3
"""metrics.py — compute and emit the loop's METRIC lines (TODO.md H3).

Was an inline heredoc inside `driver.sh:emit_metrics`, which made the
metric untestable and left `longest_chain_length` as the de-facto primary.
Agents proved that metric gameable — 9 chains x 2000 hops via shortcut
cycles (`hops=2*cycle+8`) carrying no signal, and the pathological
structure then broke the render path (H0c).

The primary metric now comes from `agi-tree.config.json`
(`metric_primary`), defaulting to :data:`DEFAULT_METRIC_PRIMARY` —
never chain length. `longest_chain_length` stays as a descriptive
secondary statistic.

`evidence_fraction` is the bridge to the H4 evidence gate: the fraction
of asserting verdicts that carry `evidence_runs >= 1`. It cannot be
inflated by adding hops — only by doing experiments.

Usage:
    metrics.py <project_root>
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
from evidence_gate import (  # noqa: E402
    DECISIVE_VERDICTS,
    build_corpus,
    normalize_evidence_runs,
    shadow_verdict_fields,
)

#: Fallback when a project's config omits `metric_primary`. Deliberately not
#: `longest_chain_length` (H3).
DEFAULT_METRIC_PRIMARY = "outcome_coverage"

#: Metrics that are descriptive only and must never be primary.
GAMEABLE_METRICS = ("longest_chain_length",)

#: Where `publish-engine.sh` used to record the outcome of every run it made
#: (goal:g7.10, pre-goal:g11). Kept only because `publish-engine.sh` itself and
#: its own test suite (`test_publish_alarm.py`) still read/write this path —
#: **metrics.py no longer turns it into a METRIC line** (goal:g11 residual,
#: see below). Generated state, gitignored, sitting beside
#: `context/INJECTION.md` because that is where this repo already keeps
#: generated state. Deliberately **not** under `nodes/`: gate 0 of
#: publish-engine.sh refuses on any uncommitted change under `nodes/`, so a
#: publish marker written there would arm, on every single run, the exact gate
#: it exists to report on.
PUBLISH_STATE_PATH = ("context", "publish-state.json")

#: `unpushed_commits` when the gap could not be measured at all.
#:
#: Not `0`. `0` is this metric's one *reassuring* value — "everything local is
#: on the remote" — so letting an unmeasurable repo collapse to it builds an
#: alarm that reports perfect health exactly when it is blind. `-1` is outside
#: the range of every true measurement (a commit gap is a count; it cannot be
#: negative), so it can be neither mistaken for one nor quietly averaged into
#: one. Unmeasurable is also not treated as the worst state — a freshly forked
#: project with no remote configured is unconfigured, not stranded — so this is
#: a small, out-of-range sentinel rather than a shouting one. The number says
#: "unknown" and the paired reason says which unknown; neither says "fine".
UNKNOWN_GAP = -1

#: Unpushed commits at or above which `emit` shouts.
#:
#: Measured, not picked, back when this repo and its engine were two repos
#: pushed by two separate hourly crons (`:07` graph, `:47` engine): over the 14
#: days to 2026-08-28 the busiest single hour in that pair produced **8**
#: commits in the graph and **9** in the engine. 20 cannot be one missed cycle
#: even at the worst rate ever observed here, and the outage this metric exists
#: for reached **25**. goal:g11 unified the two repos into one, pushed by one
#: `branch_push` cron, but the threshold's job — distinguishing one missed
#: cycle from a stall — has not changed, so the number is kept rather than
#: re-derived from a single cron's narrower history.
#:
#: The threshold governs only the shout. The count is emitted every run
#: whatever it is, so a reader watching the number sees a stall long before a
#: warning does; nothing about the measurement depends on this value being
#: right.
UNPUSHED_WARN_AT = 20

#: Seconds any single `git` call here may take. These are all local ref reads
#: and finish in milliseconds, but `metrics.py` runs on every `driver.sh
#: --smoke` and a smoke pass that can hang is not a cheap dry pass.
GIT_TIMEOUT_SECONDS = 10

#: Fallback traversable lineage fields when `[shape].md` is missing or has no
#: `edge_fields` declaration (goal:g12.3).
FALLBACK_TRAVERSABLE_FIELDS = frozenset({"parents"})

#: Frontmatter `status:` that retires a node file without deleting it.
DEPRECATED_STATUS = "deprecated"


def _load_traversable_fields(root: Path) -> frozenset[str]:
    """Read traversable edge fields from `[shape].md` context/schemas.

    Returns the set of frontmatter field names declared as
    ``traversable: true`` in the shape schema's ``edge_fields``.
    Falls back to :data:`FALLBACK_TRAVERSABLE_FIELDS` when the schema
    file is missing or has no valid ``edge_fields`` declaration
    (goal:g12.3, hypothesis:l2w2-metrics-season-edge).
    """
    import yaml
    shape_path = root / "context" / "schemas" / "[shape].md"
    if not shape_path.is_file():
        return FALLBACK_TRAVERSABLE_FIELDS
    try:
        text = shape_path.read_text(encoding="utf-8")
    except Exception:
        return FALLBACK_TRAVERSABLE_FIELDS
    if not text.startswith("---"):
        return FALLBACK_TRAVERSABLE_FIELDS
    parts = text.split("---", 2)
    if len(parts) < 3:
        return FALLBACK_TRAVERSABLE_FIELDS
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return FALLBACK_TRAVERSABLE_FIELDS
    ef = fm.get("edge_fields")
    if not isinstance(ef, dict):
        return FALLBACK_TRAVERSABLE_FIELDS
    traversable = set()
    for field_name, entry in ef.items():
        if isinstance(entry, dict) and entry.get("traversable") is True:
            traversable.add(str(field_name).strip())
    if not traversable:
        return FALLBACK_TRAVERSABLE_FIELDS
    return frozenset(traversable)


def _load_graph(root: Path):
    proj_src = root / "src"
    if (proj_src / "graph_core").is_dir():
        sys.path.insert(0, str(proj_src))
    sys.path.insert(0, str(PLUGIN_ROOT / "src"))
    from graph_core.loader import load_directory
    from graph_core.edge import Edge

    g, loaded = load_directory(root / "nodes")
    traversable = _load_traversable_fields(root)

    # Build node-id -> values for non-parents traversable fields from frontmatter.
    # These are fields like `next_edges` that are ``role: lineage`` and
    # ``traversable: true`` but are not the primary ``parents`` field.
    import yaml
    extra_forward: dict[str, list[str]] = {}
    other_fields = traversable - FALLBACK_TRAVERSABLE_FIELDS
    if other_fields:
        for nf in sorted((root / "nodes").rglob("*.md")):
            try:
                text = nf.read_text(encoding="utf-8")
            except Exception:
                continue
            if not text.startswith("---"):
                continue
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except Exception:
                continue
            if not isinstance(fm, dict):
                continue
            nid = fm.get("id")
            if not isinstance(nid, str) or not nid.strip():
                continue
            nid = nid.strip()
            vals = []
            for field in other_fields:
                raw = fm.get(field)
                if isinstance(raw, list):
                    for v in raw:
                        if isinstance(v, str) and v.strip():
                            vals.append(v.strip())
                elif isinstance(raw, str) and raw.strip():
                    vals.append(raw.strip())
            if vals:
                extra_forward[nid] = vals

    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id,
                                    relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

        # Forward edges from additional traversable fields (e.g. `next_edges`).
        # Creates edge: this_node -> target, and adds target to this_node's children.
        for tid in extra_forward.get(ln.node.id, []):
            if g.has_node(tid):
                try:
                    g.add_edge(Edge(source_id=ln.node.id, target_id=tid,
                                    relation="traversable"))
                except Exception:
                    pass
                ln.node.children.add(tid)
    return g


def longest_chain_length(g) -> int:
    """Longest descendant chain. Descriptive only — gameable (H3).

    Deliberately iterative. The recursive version raised RecursionError at ~990
    deep on the agi-tree corpus, whose chains were gamed to 2000 hops — the same
    defect H3b removed from render-context.py, and it aborted the whole metrics
    stage over a metric that is only descriptive. Back-edges resolve to 0 rather
    than looping, matching chain_engine's cycle convention.
    """
    cache: dict[str, int] = {}
    on_stack: set[str] = set()

    for root in g.node_ids:
        if root in cache:
            continue
        stack: list[tuple[str, bool]] = [(root, False)]
        while stack:
            nid, expanded = stack.pop()
            if expanded:
                n = g.get_node(nid)
                cache[nid] = max(
                    (cache.get(c, 0) + 1 for c in n.children if c != nid),
                    default=0,
                )
                on_stack.discard(nid)
                continue
            if nid in cache:
                continue
            n = g.get_node(nid)
            if n is None or not n.children:
                cache[nid] = 0
                continue
            on_stack.add(nid)
            stack.append((nid, True))
            for c in n.children:
                if c != nid and c not in cache and c not in on_stack:
                    stack.append((c, False))

    return max(cache.values(), default=0)


def _iter_frontmatter(nodes_dir: Path):
    import yaml
    if not nodes_dir.is_dir():
        return
    for nf in sorted(nodes_dir.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        if isinstance(fm, dict):
            yield nf, fm


_THOUGHT_RE = re.compile(
    r"<!--\s*THOUGHT:BEGIN(.*?)<!--\s*THOUGHT:END\s*-->", re.DOTALL)


def thought_stats(nodes_dir: Path) -> dict:
    """How much of the graph records why it changed (goal:g2.11).

    **Descriptive only, and it must stay out of `metric_primary`.** It is
    trivially gamed -- an agent told to raise it writes 786 empty
    justifications, and the project has already been burned once by scoring a
    quantity that motion alone could move (9 chains x 2000 hops carrying no
    signal). This counts a slot being filled; it cannot judge whether what
    fills it is true. Read it as coverage, never as quality.

    A block whose content is only whitespace counts as empty, so the marker
    alone cannot lift the number.
    """
    total = filled = 0
    if not nodes_dir.is_dir():
        return {"thought_coverage": 0.0, "nodes_with_thought": 0}
    for nf in sorted(nodes_dir.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        total += 1
        m = _THOUGHT_RE.search(text)
        if m and m.group(1).replace("-->", "").strip():
            filled += 1
    return {
        "thought_coverage": round(filled / total, 3) if total else 0.0,
        "nodes_with_thought": filled,
    }


def deprecated_node_ids(nodes_dir: Path) -> frozenset:
    """Ids of nodes declaring `status: deprecated`. `goal:s23`.

    Lives here, beside `node_lifecycle_stats`, so "what counts as retired" has
    exactly ONE definition. `render-context.py` imports it to keep retired
    nodes out of the injected map. A second predicate over there would be
    `goal:s17` again -- two definitions of one fact, and one of them is always
    the one a given reader consults.
    """
    ids = set()
    for _nf, fm in _iter_frontmatter(nodes_dir):
        st = fm.get("status")
        nid = fm.get("id")
        if (isinstance(st, str) and st.strip().lower() == DEPRECATED_STATUS
                and isinstance(nid, str) and nid.strip()):
            ids.add(nid.strip())
    return frozenset(ids)


def node_lifecycle_stats(nodes_dir: Path, node_count: int) -> dict:
    """Retirement counted at the node, not at the goal it answers to.

    `goal_attribution` already publishes `retired_goal_nodes`, and it answers a
    different question: how many nodes descend *only* from goals that have been
    retired. A node is caught by that without anyone ever touching it, and it
    flips back the moment a live goal adopts it. This counts the node's own
    declared lifecycle — `status: deprecated` in its frontmatter, the
    convention for retiring a node file that is **kept, never deleted**.
    Attribution versus declaration; conflating them would make both unreadable,
    so they are computed apart and stay apart.

    `node_count` keeps meaning every node file on disk. G7's invariant is that
    nothing the loop produces is silently lost, and a total that shrinks when
    work is retired is precisely the shape of loss it forbids — you could not
    tell a deprecation from a deletion. `active_node_count` is the number that
    is allowed to move.
    """
    deprecated = 0
    for _nf, fm in _iter_frontmatter(nodes_dir):
        st = fm.get("status")
        if isinstance(st, str) and st.strip().lower() == DEPRECATED_STATUS:
            deprecated += 1
    return {
        "deprecated_node_count": deprecated,
        "active_node_count": max(node_count - deprecated, 0),
    }


def _git_out(repo: Path, *args: str) -> str | None:
    """Stripped stdout of a local `git` command, or None if it did not succeed.

    Never raises and never inherits a stream: a metrics stage that can die on a
    missing binary, a permission error or a prompt is worse than one that
    cannot answer, because the whole run goes with it.
    """
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS,
        )
    except Exception:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def unpushed_commits(repo: Path) -> tuple[int, str]:
    """`(count, reason)` — commits on HEAD that the remote-tracking ref lacks.

    `reason` is `""` if and only if `count` is a real measurement. Every other
    value is a token naming *which* kind of blind, paired with
    :data:`UNKNOWN_GAP`; a caller can therefore never read a number without
    also being told whether it means anything.

    **Local only, on purpose, and this is the honest cost.** The count comes
    from `git rev-list --count @{upstream}..HEAD`, which reads
    `refs/remotes/origin/<branch>` off this disk. That ref only advances when
    this machine pushes or fetches, so the number means *commits this machine
    has not pushed*, not *commits the remote is missing* — if someone else
    pushed, it over-reports. Deliberate: `metrics.py` runs on every `driver.sh
    --smoke`, `--smoke` is meant to be a cheap dry pass, and a `git fetch` here
    would put network I/O in it. Over-reporting stranded work is also the
    correct direction for an alarm to be wrong.

    Generic over what `repo` points at — a project's own root, or (pre-g11,
    and still true for a project that clones the engine in per the layout
    documented in `CLAUDE.md`) a nested engine clone. The refusals, in the
    order they are checked:

    `missing`
        No such directory. A directory that does not exist yet is not
        failing at anything.
    `not-a-repo`
        Not a git repo, or not the *root* of one. The second half is the load
        bearing one: if `repo` were an ordinary directory inside some other
        repo rather than its own clone, `git -C` would happily answer for the
        **enclosing** repo — a wrong number that reads as a measurement,
        which is the one outcome worse than no number.
    `detached-head`
        `@{upstream}` is a property of a branch. A detached HEAD has none, so
        the question has no answer rather than the answer `0`.
    `no-upstream`
        A branch with no configured upstream. Ordinary in a fresh fork.
    `git-failed`
        `rev-list` ran and did not produce a number.
    """
    if not repo.is_dir():
        return UNKNOWN_GAP, "missing"

    top = _git_out(repo, "rev-parse", "--show-toplevel")
    if top is None:
        return UNKNOWN_GAP, "not-a-repo"
    try:
        # samefile, not string equality: `<project>/agi` is a symlink in at
        # least one real project and `--show-toplevel` reports the resolved
        # path, which would never compare equal to the path we were handed.
        if not os.path.samefile(top, repo):
            return UNKNOWN_GAP, "not-a-repo"
    except OSError:
        return UNKNOWN_GAP, "not-a-repo"

    if _git_out(repo, "symbolic-ref", "--quiet", "HEAD") is None:
        return UNKNOWN_GAP, "detached-head"
    if _git_out(repo, "rev-parse", "--verify", "--quiet", "@{upstream}") is None:
        return UNKNOWN_GAP, "no-upstream"

    out = _git_out(repo, "rev-list", "--count", "@{upstream}..HEAD")
    try:
        return max(0, int((out or "").strip())), ""
    except ValueError:
        return UNKNOWN_GAP, "git-failed"


def push_gap_stats(root: Path) -> dict:
    """The stranded-push alarm (goal:s20).

    Originally the other half of goal:g7.10's publish alarm: that alarm
    measured the **local commit**, `publish-engine.sh` committed a *separate*
    engine repo and deliberately did not push it (pushing was the hourly push
    cron's job, and for the engine repo that cron did not exist), and the gap
    was invisible from both sides — publish reported success, the local tree
    was healthy, and the remote sat **3 days and 25 commits** behind. It was
    noticed by looking at GitHub, which is the failure mode goal:g7.10 existed
    to remove.

    goal:g11 removed the boundary that made that a two-repo question:
    `payloads/`, the staged engine checkout and `publish-engine.sh`'s write
    into it are retired, and one push cron (`branch_push`) now covers what
    used to be two. What survives, and is still genuinely useful, is the
    single question that boundary never changed: **is anything committed on
    this machine still only on this machine?** A push that succeeds with
    nothing to push reads identical to a healthy repo; only a gap **count**,
    not a timestamp, tells the two apart. `unpushed_reason` is `""` if and
    only if `unpushed_commits` is a real measurement (see `unpushed_commits`
    for what every other value means).

    `root` is the *graph* root (`<repo>/.agi` under the unified layout, or the
    repo root itself under the legacy one) — the same argument every other
    stat in this module takes. `unpushed_commits` demands `repo` be the git
    toplevel, and under the unified layout `.agi` is not: it is a directory
    *inside* the repo, so measuring `root` directly would answer
    `not-a-repo` on every unified project, forever — the exact permanent
    sentinel this bug fix exists to remove. `locations.repo_root` resolves
    the actual toplevel for either layout (identity under the legacy one,
    parent-of-`.agi` under the unified one), so this is the one caller of
    `unpushed_commits` that does *not* pass its own `root` straight through.
    """
    n, reason = unpushed_commits(locations.repo_root(root))
    return {
        "unpushed_commits": n,
        "unpushed_reason": reason,
    }


def evidence_stats(nodes_dir: Path) -> dict:
    """Evidence accounting over verdict-bearing nodes.

    Denominator is *asserting* verdicts — everything except `pending`.
    `pending` is excluded on purpose: H4 permits it without evidence, so
    counting it would penalise honest uncertainty.

    `evidence_runs` is resolved against the corpus (goal:g3.1 / H4c) using
    the exact same `build_corpus` + `normalize_evidence_runs` functions
    `evidence_gate.py` uses to gate a write. One definition, shared by
    import, not reimplemented here — so this metric and the gate cannot
    read the same field and disagree (that drift was the H4c root cause).

    `unevidenced_decisive_verdicts` reads `verdict:` and nothing else, on
    purpose — its definition has to stay stable to be comparable across
    runs. The blind spot that leaves is counted separately as
    `shadow_decisive_verdicts`: a node can assert `proved` in the legacy
    `status:` shadow (`evidence_gate.SHADOW_VERDICT_FIELDS`) either
    *contradicting* an honest demoted `verdict:`, or with no `verdict:`
    field at all — in which case the whole verdict was invisible to every
    number here. Both were true of this corpus before the gate demoted
    shadows in lockstep; the counter is the regression alarm that they do
    not come back.
    """
    corpus = build_corpus(nodes_dir)
    asserting = 0
    backed = 0
    decisive = 0
    decisive_backed = 0
    pending = 0
    shadow = 0
    shadow_orphaned = 0
    for _nf, fm in _iter_frontmatter(nodes_dir):
        v = fm.get("verdict")
        has_verdict = isinstance(v, str) and bool(v.strip())
        v = v.strip() if has_verdict else None
        # Shadow defect: a `status: proved` that `verdict:` does not back up.
        # A shadow that *agrees* with a decisive `verdict:` is not a defect —
        # it is redundant, and the gate will demote both together.
        if shadow_verdict_fields(fm) and v not in DECISIVE_VERDICTS:
            shadow += 1
            if not has_verdict:
                shadow_orphaned += 1
        if not has_verdict:
            continue
        runs = normalize_evidence_runs(fm.get("evidence_runs"), corpus=corpus)
        if v == "pending":
            pending += 1
            continue
        asserting += 1
        if runs >= 1:
            backed += 1
        if v in DECISIVE_VERDICTS:
            decisive += 1
            if runs >= 1:
                decisive_backed += 1
    return {
        "verdicts_asserting": asserting,
        "verdicts_pending": pending,
        "verdicts_evidence_backed": backed,
        "evidence_fraction": (backed / asserting) if asserting else 0.0,
        "decisive_verdicts": decisive,
        "decisive_evidence_fraction": (decisive_backed / decisive) if decisive else 0.0,
        # Gate-violation counter: should be 0 once H4 holds in both writer
        # paths. Nonzero = a bypass or a hand-edited node.
        "unevidenced_decisive_verdicts": decisive - decisive_backed,
        # Shadow-channel counter: should be 0. Nonzero = a node advertises
        # 'proved'/'disproved' in `status:` that its `verdict:` does not
        # support — the contradiction the lockstep demotion exists to stop.
        "shadow_decisive_verdicts": shadow,
        # Subset of the above with no `verdict:` field at all: a decisive
        # claim that every other number in this dict is blind to.
        "shadow_decisive_no_verdict": shadow_orphaned,
        # goal:g13 — nodes whose `link_ref`/`payload_ref` names a file that is
        # not there. Should be 0. This is the *counted* half of the two chosen
        # failure behaviours: a single-node read raises `MissingLink` where a
        # caller can act, and a bulk scan lands here instead of dying on one
        # node out of nine hundred. Same shape as
        # `unevidenced_decisive_verdicts` — a number whose only healthy value
        # is zero, naming a specific repairable defect.
        "broken_links": _broken_links(nodes_dir),
    }


def _broken_links(nodes_dir) -> int:
    """`links.count_broken_links`, defensively.

    Imported here rather than at module scope so a project whose checkout
    predates `links.py` still computes every other metric. A metrics run that
    dies because one counter is unavailable would take the whole `--smoke`
    gate with it, and that gate is what verifies the node count did not drop.

    Degrading is not the same as degrading silently — the counter says so on
    stderr rather than reporting a healthy 0 it did not compute. A metric that
    reads 0 because it failed is exactly the quiet failure `goal:g13` exists
    to remove, and it would be a poor joke to build one into the counter.
    """
    try:
        import links
        return links.count_broken_links(Path(nodes_dir).parent)
    except Exception as exc:
        print(f"METRIC_WARNING broken_links_unavailable={type(exc).__name__}: "
              f"{exc}", file=sys.stderr)
        return 0


#: goal:g11.1 — re-exported from `locations` rather than redefined. The
#: accepted marker names are a property of the layout, not of this module.
#: `render-context.py` imports `read_config` from here, so both halves of the
#: config lookup have to agree with the shared resolver, not just one.
config_path = locations.config_path


def read_config(root: Path) -> dict:
    cfg_path = config_path(root)
    if cfg_path is None:
        return {}
    try:
        return json.loads(cfg_path.read_text()) or {}
    except Exception:
        return {}


def primary_metric_name(cfg: dict) -> str:
    """Config's `metric_primary`, else the non-gameable default (H3)."""
    name = cfg.get("metric_primary")
    if not isinstance(name, str) or not name.strip():
        return DEFAULT_METRIC_PRIMARY
    return name.strip()


#: Goal states whose chains still accrue score.
#:
#: **`complete` is here, and its absence was a live defect** (goal:g5,
#: revised 2026-09-01). The original rule collapsed `complete` and retired
#: into one non-scoring bucket, and the collapse was measured on 2026-09-01:
#: a sweep marked nine goals `complete`/retired on falsifiers and
#: `outcome_coverage` fell 0.27 -> 0.232 with no work undone and no node
#: removed. **The metric penalised finishing**, which is a disincentive
#: against the goal sweep this project needs.
#:
#: The two states mean different things:
#:   - `complete` — achieved. Its chains are real, still extendable, and its
#:     evidence is permanent corpus. Completing must never look like
#:     regression.
#:   - retired — the goal stopped making sense. Its results are not useful to
#:     the corpus as a whole, so they leave the score (but stay in the graph
#:     and stay attributable).
SCORING_GOAL_STATUSES = frozenset({"active", "horizon", "complete"})

#: Goal states that stop accruing score. `retired` is canonical;
#: `phasing-out` is the legacy spelling and is accepted forever — projects
#: predating the rename carry it, and a reader that stops recognising it
#: would silently start scoring their retired chains.
RETIRED_GOAL_STATUSES = frozenset({"retired", "phasing-out"})

#: `hypothesis:an-mvp-that-points-backward-is-score-neutral` (goal:g3, L1.08).
#:
#: `[mvp].md` defines an mvp as pointing **forward** — "the code that
#: satisfies it is a `build` node ... and an mvp points forward at what that
#: build owes rather than containing it." A backward mvp is a closure minted
#: for work already done: the file it names already exists, and the body says
#: so in the past tense rather than proposing it. Left uncaught, minting one
#: raises `outcome_coverage`'s numerator for zero forward-pointing content —
#: exactly the motion goal:g3 says scoring cannot move.
#:
#: **The rule, stated precisely, is a conjunction:**
#: 1. **No forward evidence** — the mvp carries no `source_files`, no
#:    `payload_ref`, and no `build`-typed node names it as a parent (the
#:    mechanical trail `level3.py` would leave if a build had actually been
#:    minted *for* this mvp).
#: 2. **The body reads as a verification of existing code**, not a design
#:    proposal — it cites an already-passing test count (`"1382/1382 pass"`,
#:    `"all 1382 existing pass"`) or an explicit already-checked claim
#:    (`"verified in-tree"`, `"the mechanism is real"`).
#:
#: Both conditions must hold: (1) alone would misfire on a genuine mvp whose
#: build hasn't landed *yet*, and (2) alone would misfire on a genuinely
#: forward mvp that merely cites a sibling's test count in passing. Measured
#: against the full corpus at time of writing (48 mvp nodes, `goal:g3`/L1.08
#: audit): exactly 2 match — both true closures for already-shipped changes,
#: 0 false positives on the other 46.
_BACKWARD_MVP_RE = re.compile(
    r"verified in-tree"
    r"|the mechanism is real"
    r"|\d+/\d+\s+(?:tests?\s+)?pass"
    r"|all\s+\d+\s+(?:new\s+|existing\s+)?(?:tests?\s+)?pass",
    re.IGNORECASE,
)


def _mvp_forward_violations(nodes_dir: Path, types: dict, parents: dict) -> frozenset:
    """mvp ids that fail `[mvp].md`'s forward-pointing rule. See `_BACKWARD_MVP_RE`.

    Takes `types`/`parents` already built by `goal_attribution`'s own pass
    (no second full-graph walk needed for those) and does one further,
    mvp-scoped read for body text, since `_iter_frontmatter` deliberately
    reads frontmatter only and body text is needed here to see the
    past-tense verification language a backward mvp gives itself away with.
    """
    build_parents: set[str] = set()
    for nid, ntype in types.items():
        if ntype == "build":
            build_parents.update(parents.get(nid, ()))

    backward: set[str] = set()
    if not nodes_dir.is_dir():
        return frozenset()
    for nf in sorted(nodes_dir.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        import yaml
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        if not isinstance(fm, dict) or fm.get("type") != "mvp":
            continue
        nid = fm.get("id")
        if not isinstance(nid, str) or not nid.strip():
            continue
        nid = nid.strip()
        has_forward_evidence = (
            bool(fm.get("source_files"))
            or bool(fm.get("payload_ref"))
            or nid in build_parents
        )
        if has_forward_evidence:
            continue
        if _BACKWARD_MVP_RE.search(parts[2]):
            backward.add(nid)
    return frozenset(backward)


def goal_attribution(nodes_dir: Path) -> dict:
    """Map every node to the goals it descends from, and score accordingly.

    goal:g5 — `status` is a field the engine acts on, not a human
    convention. Three things follow from that and all three are here:

    1. A node under a **retired** goal is **excluded from the primary
       metric** but **kept attributable** — still in the graph, still
       reachable, still counted in the descriptive totals. Retiring must not
       look like deleting. A node under a `complete` goal keeps scoring; see
       `SCORING_GOAL_STATUSES` for why that distinction was worth a revision.
    2. A node under no goal at all keeps scoring. That is deliberate and
       conservative: most of this corpus predates goal nodes, and silently
       zeroing it would be a metric change disguised as a lifecycle rule.
       Attribution is a reason to *exclude*, never the only reason to
       include.
    3. **Removal can only ever take a closed chain out of the ratio, never
       bare denominator weight.** A hypothesis that never reached an mvp
       stays in the denominator no matter how it leaves. This is the
       anti-gaming clause and it is the whole reason the rule is not one
       constant: if removal could drop unconverted hypotheses, then removing
       in bulk — which is exactly what a sweep does — would raise
       `outcome_coverage` for free, and nothing in the metric could tell that
       apart from honest cleanup. This project has already paid once for a
       gameable primary metric (goal:g3); it does not need a second one
       wearing a lifecycle field as a disguise.

    **A node leaves scoring for two reasons, and clause 3 covers both
    (goal:g3, L1.08).** goal:g5 wrote clause 3 for goal *retirement*, the
    only removal that existed then. `status: deprecated` is the second, and
    it was unguarded: deprecation is removal at the node instead of at the
    goal, and *removal must obey the same law as addition* — it cannot move
    the primary on its own. The hole was not theoretical. This corpus carries
    61 `origin: build-site` hypotheses and **zero** build-site mvps; 52 of the
    61 never reached a verdict. Deprecating that generated set — the whole
    point of the cleanup L1.09 does — would have dropped up to 61 nodes out
    of the denominator and nothing at all out of the numerator:
    `outcome_coverage` 0.271 -> 0.470, earned by deleting nothing and proving
    nothing. Under the guard it moves by 0.000, and
    `deprecation_score_delta` reports the 0.199 that was refused.

    **"Closed" is measured against the mvps that are themselves leaving, not
    against every mvp**, and that pairing is what makes the clause hold under
    deprecation. Goal retirement never needed it: retirement applies to a
    whole subtree, so a chain's mvp and its hypothesis always left together.
    Deprecation is per node and couples nothing — deprecating a hypothesis
    whose mvp stays live would drop the denominator while the numerator kept
    the credit, which is the same free lift by a shorter route. Nine of this
    corpus's build-site hypotheses are exactly that shape. So a hypothesis
    may leave only when the mvp that closed it is leaving too; while its mvp
    is still being counted for it, the hypothesis is still open as far as
    scoring is concerned.

    The residual, stated rather than hidden: a *set* of removed nodes can
    still raise the ratio if many hypotheses share one leaving mvp
    (removing 5 hypotheses and 1 mvp beats the corpus ratio). That case is
    shared with goal:g5's own clause 3 and is not introduced here; the
    per-chain rule bounds it, it does not eliminate it.

    Returns counts, not opinions — `compute` decides what to do with them.
    """
    statuses: dict[str, str] = {}
    parents: dict[str, list] = {}
    types: dict[str, str] = {}
    deprecated: set[str] = set()

    # Which edge fields to follow for lineage walks (goal:g12.3).
    # Read from the shape schema so `season_parents` and other
    # non-traversable fields are excluded mechanically rather than
    # hardcoded (hypothesis:l2w2-metrics-season-edge).
    traversable = _load_traversable_fields(nodes_dir.parent)
    # Inverted index for forward-pointing traversable fields (e.g. `next_edges`).
    # If node A has `next_edges: [B]`, then B's ancestor A should be reachable
    # when walking UP from B.
    extra_ascendants: dict[str, list[str]] = {}

    for _nf, fm in _iter_frontmatter(nodes_dir):
        nid = fm.get("id")
        if not isinstance(nid, str) or not nid.strip():
            continue
        nid = nid.strip()
        types[nid] = str(fm.get("type") or "")
        raw = fm.get("parents")
        parents[nid] = [p.strip() for p in raw if isinstance(p, str) and p.strip()] \
            if isinstance(raw, (list, tuple)) else []
        # Additional traversable fields: build inverse relationships for
        # forward-pointing edges so the upward walk can reach the source node.
        for field in traversable:
            if field == "parents":
                continue
            raw_other = fm.get(field)
            if isinstance(raw_other, list):
                for v in raw_other:
                    if isinstance(v, str) and v.strip():
                        tid = v.strip()
                        extra_ascendants.setdefault(tid, []).append(nid)
        st = fm.get("status")
        # Same predicate as `deprecated_node_ids`, over an iteration this
        # function is already making. One definition of "retired node", two
        # readers of it — not two definitions (goal:s17).
        if isinstance(st, str) and st.strip().lower() == DEPRECATED_STATUS:
            deprecated.add(nid)
        if types[nid] == "goal":
            statuses[nid] = st.strip() if isinstance(st, str) and st.strip() else "active"

    # Merge inverse relationships from forward-pointing traversable fields
    # into the parent mapping so the upward walk can also reach nodes that
    # point TO this node via fields like `next_edges`.
    for child_id, ascendants in extra_ascendants.items():
        parents.setdefault(child_id, []).extend(ascendants)

    # goal:g3 / L1.08 — mvps that fail `[mvp].md`'s forward-pointing rule.
    # Computed from the `types`/`parents` this pass already built, plus one
    # further mvp-scoped body read (see `_mvp_forward_violations`).
    backward_mvp_ids = _mvp_forward_violations(nodes_dir, types, parents)

    def goals_of(nid: str) -> set:
        """Goal ids reachable upward from `nid`. Cycle-safe by construction."""
        seen, stack, found = {nid}, list(parents.get(nid, ())), set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur in statuses:
                found.add(cur)
                continue  # a goal's own parents are goals; stop at the first
            stack.extend(parents.get(cur, ()))
        return found

    # Pass 1 — who would leave scoring, before the open-hypothesis clause is
    # applied. Two independent reasons: every goal it answers to is retired
    # (goal:g5), or it declares its own retirement (`status: deprecated`).
    # For an **mvp** this answer is already final, because the sparing clause
    # only ever applies to a hypothesis — which is what lets pass 2 ask "is
    # the mvp that closed this chain leaving too?" without a fixpoint.
    goals_cache: dict[str, set] = {}
    leaving: dict[str, bool] = {}
    for nid, ntype in types.items():
        if ntype == "goal":
            continue
        gs = goals_of(nid)
        goals_cache[nid] = gs
        # Retired only when every goal it answers to is retired. A node
        # shared with a live goal still earns its keep.
        goal_ok = (not gs) or any(statuses.get(g) in SCORING_GOAL_STATUSES for g in gs)
        leaving[nid] = (not goal_ok) or (nid in deprecated)

    # Nodes on a chain that reached an mvp **which is itself leaving**.
    # Computed by walking UP from those mvps rather than down from every
    # hypothesis: `parents` is the edge direction stored on disk, so this
    # needs no inverted index and no second traversal order to keep in sync.
    # Stops at goals — a goal is not "on" its own chain, and walking through
    # one would join every chain under it.
    closed_chain: set = set()
    for nid, ntype in types.items():
        if ntype != "mvp" or not leaving.get(nid, False):
            continue
        stack = [nid]
        while stack:
            cur = stack.pop()
            if cur in closed_chain or cur in statuses:
                continue
            closed_chain.add(cur)
            stack.extend(parents.get(cur, ()))

    scoring_mvp = scoring_hyp = 0
    retired_nodes = retired_open_hyp = unattributed = 0
    deprecated_excluded = deprecated_open_hyp = 0
    backward_mvp = 0
    for nid, ntype in types.items():
        if ntype == "goal":
            continue
        gs = goals_cache[nid]
        if not gs:
            unattributed += 1
        if leaving[nid]:
            # Clause 3. A leaving mvp is on its own closed chain by
            # definition, so this only ever spares a hypothesis whose mvp is
            # not leaving with it — the one thing removal must not be able to
            # launder out of the ratio.
            spared = ntype == "hypothesis" and nid not in closed_chain
            # Which reason is reported when both apply: goal retirement, the
            # older and coarser one. The buckets partition the leaving set so
            # they can be summed; `deprecation_score_delta` needs the
            # deprecation-only count, because a node the goal rule already
            # holds is not a node this guard is holding.
            goal_retired = not ((not gs) or
                                any(statuses.get(g) in SCORING_GOAL_STATUSES
                                    for g in gs))
            if spared:
                scoring_hyp += 1
                if goal_retired:
                    retired_open_hyp += 1
                else:
                    deprecated_open_hyp += 1
            elif goal_retired:
                retired_nodes += 1
            else:
                deprecated_excluded += 1
            continue
        if ntype == "mvp":
            # A backward mvp is not "leaving" (it is not deprecated and its
            # goal is not retired) — it stays in the graph and stays
            # attributable. It just does not get to raise the numerator: the
            # closure it describes was never a forward-pointing design, so
            # counting it would be exactly the motion goal:g3 forbids. Its
            # parent hypothesis is untouched by this branch and keeps scoring
            # normally in the denominator — a backward mvp cannot spare its
            # own hypothesis the way a deprecated one can (clause 3 above is
            # deliberately not extended here).
            if nid in backward_mvp_ids:
                backward_mvp += 1
            else:
                scoring_mvp += 1
        elif ntype == "hypothesis":
            scoring_hyp += 1

    by_status: dict[str, int] = defaultdict(int)
    for st in statuses.values():
        by_status[st] += 1

    return {
        "scoring_mvp_count": scoring_mvp,
        "scoring_hypothesis_count": scoring_hyp,
        # goal:g3 / L1.08 — mvps excluded from `scoring_mvp_count` for failing
        # `[mvp].md`'s forward-pointing rule (`_BACKWARD_MVP_RE`), reported so
        # the exclusion is auditable rather than a silent drop. Not "leaving":
        # these nodes stay in the graph, stay attributable, and are neither
        # deprecated nor under a retired goal — they just do not raise the
        # numerator for a closure that was never a forward design.
        "backward_mvp_count": backward_mvp,
        "retired_goal_nodes": retired_nodes,
        "retired_open_hypotheses": retired_open_hyp,
        # goal:g3 / L1.08 — the deprecation half of clause 3, reported so the
        # guard is auditable rather than implicit. `deprecated_open_hypotheses`
        # is what the guard is holding in the denominator right now;
        # `deprecated_excluded_nodes` is what deprecation did legitimately
        # remove from scoring. Mirrors `retired_open_hypotheses` /
        # `retired_goal_nodes`, and the four buckets partition the leaving set.
        "deprecated_open_hypotheses": deprecated_open_hyp,
        "deprecated_excluded_nodes": deprecated_excluded,
        "unattributed_nodes": unattributed,
        # 2026-09-06 owner decision (L3 brainstorm, HANDOFF §6 item 10): the
        # active-goal COUNT and its cap are gone — long-term goals are
        # `goal_kind: perpetual` and there is no max_goals_active cap for the
        # count to trip. `goals_active` was emitted only for that warning;
        # with the cap removed nothing read it, so per the re-brief it was
        # dropped too. `goals_horizon` survives as a descriptive status count.
        "goals_horizon": by_status.get("horizon", 0),
        # goal:g5 — `goals_retired` counted `complete` too, which is the same
        # collapse `SCORING_GOAL_STATUSES` used to make. Reporting a finished
        # goal as retired is how the number stopped meaning anything.
        "goals_retired": sum(by_status.get(s, 0) for s in RETIRED_GOAL_STATUSES),
        "goals_complete": by_status.get("complete", 0),
        "goal_count": len(statuses),
    }


def outcome_coverage(mvp_count: int, hypothesis_count: int) -> float:
    """The default primary metric: mvps per hypothesis.

    Goal-attributable — it moves only when a hypothesis actually reaches an
    mvp, so padding hops cannot shift it (H3). Shared with
    `bin/render-context.py`, which reports it in the injected map, so the map
    and the METRIC lines can never disagree about what the loop is scored on.
    """
    return mvp_count / max(hypothesis_count, 1)


def deprecation_score_delta(attr: dict) -> float:
    """What the guard is refusing to hand deprecation. **Never positive.**

    `outcome_coverage` as computed, minus `outcome_coverage` with the
    deprecation guard removed — that is, with every deprecated hypothesis the
    guard is holding simply dropped from the denominator. It is `0.0` when
    nothing is being held and negative by exactly the free lift a cleanup
    would otherwise have collected.

    **Read the sign as the law, not as a loss.** goal:g3 says added motion
    cannot move the score; the same sentence has to be true of removal, or
    the cheapest way to raise the primary is to delete the evidence against
    it. A number that can only be `<= 0` is that law made checkable every
    run: the guard cannot pay out, only refuse.

    Not clamped, because it cannot need clamping. The two ratios share a
    numerator, and the unguarded denominator is the guarded one minus a
    non-negative count, so the unguarded ratio is >= the guarded one for
    every possible corpus — `max(..., 1)` included. The `<= 0` is arithmetic,
    not a check that happens to pass.

    Reported against `outcome_coverage` specifically, and named for it in
    spirit if not in letter: `metric_primary` is configurable, but this is
    the metric the guard is written to protect, and a delta that silently
    re-pointed at whatever the config named would answer a different question
    each time it moved.
    """
    mvps = attr["scoring_mvp_count"]
    held = attr["deprecated_open_hypotheses"]
    guarded = outcome_coverage(mvps, attr["scoring_hypothesis_count"])
    unguarded = outcome_coverage(mvps, attr["scoring_hypothesis_count"] - held)
    return round(guarded - unguarded, 3)


def compute(root: Path) -> dict:
    g = _load_graph(root)

    by_type: dict[str, int] = defaultdict(int)
    for n in g.nodes:
        by_type[n.type] += 1

    mvp_count = by_type.get("mvp", 0)
    hyp_count = by_type.get("hypothesis", 0)
    non_leaf = [n for n in g.nodes if n.children]
    branching = sum(len(n.children) for n in non_leaf) / max(len(non_leaf), 1)
    avg_depth = sum(len(n.parents) for n in g.nodes) / max(len(g), 1)

    # goal:g5 — score over live goals only. `mvp_count` stays whole-graph so
    # the descriptive total and the scored total are both visible; a gap
    # between them is exactly how much work is parked behind retired goals.
    attr = goal_attribution(root / "nodes")

    m: dict[str, float | int | str] = {
        "longest_chain_length": longest_chain_length(g),
        "avg_chain_depth": round(avg_depth, 2),
        "mvp_count": mvp_count,
        "outcome_coverage": round(
            outcome_coverage(attr["scoring_mvp_count"],
                             attr["scoring_hypothesis_count"]), 3),
        "chain_branching_factor": round(branching, 2),
        "node_count": len(g),
        "edge_count": g.edge_count,
    }
    m.update(attr)
    m["deprecation_score_delta"] = deprecation_score_delta(attr)
    # goal:g7.10 — node-level retirement, kept apart from `retired_goal_nodes`
    # above (that one is goal attribution; this one is the node's own status).
    m.update(node_lifecycle_stats(root / "nodes", m["node_count"]))
    # goal:s20, post-goal:g11 — the stranded-push gap. `hours_since_successful_
    # publish` and `publish_blocked_reason` (goal:g7.10) measured a two-repo
    # publish boundary that goal:g11 removed; they were dropped rather than
    # kept reporting a sentinel for a publish that structurally cannot happen
    # any more (mvp:g11-crons-metrics-residual). This one honest number
    # survives the merge: whether this repo's own HEAD is ahead of its remote.
    m.update(push_gap_stats(root))
    ev = evidence_stats(root / "nodes")
    m.update(ev)
    # goal:g2.11 — descriptive coverage of the authored THOUGHT region.
    # Secondary by construction: see thought_stats' docstring for why it must
    # never be `metric_primary`.
    m.update(thought_stats(root / "nodes"))
    m["evidence_fraction"] = round(ev["evidence_fraction"], 3)
    m["decisive_evidence_fraction"] = round(ev["decisive_evidence_fraction"], 3)
    # Composite suggested by H3: depth is only worth what the evidence
    # behind it is worth. Bounded by evidence_fraction <= 1.
    m["evidence_weighted_depth"] = round(avg_depth * ev["evidence_fraction"], 3)
    return m


def emit(root: Path, out=None) -> dict:
    out = out if out is not None else sys.stdout
    cfg = read_config(root)
    m = compute(root)
    primary = primary_metric_name(cfg)

    if primary in GAMEABLE_METRICS:
        print(
            f"!! METRIC-WARNING metric_primary='{primary}' is gameable (TODO.md H3): "
            "agents reached 9 chains x 2000 hops via shortcut cycles carrying no "
            f"signal. Move it to secondary_metrics and set metric_primary to "
            f"'{DEFAULT_METRIC_PRIMARY}' or 'evidence_fraction'.",
            file=sys.stderr,
        )
        print(f"METRIC_WARNING gameable_primary={primary}", file=out)

    # goal:g5 -> 2026-09-06 owner decision (L3 brainstorm, HANDOFF §6 item
    # 10): the active-goal cap and its warning are DELETED, not re-designed.
    # A long-term goal is *always* active, so "active" never meant in-flight;
    # it only selected what chain-building aims at, and budgeting that with a
    # number just pressured runs to mislabel real goals `horizon` to silence
    # it. Long-term goals become `goal_kind: perpetual` instead, and there is
    # no active-goal cap at all (re-brief of hypothesis:l2-goals-active-exempt
    # — the fix is to delete, not to exempt).

    # goal:g7.10's publish-stall alarm used to live here: a non-empty
    # `publish_blocked_reason` meant the last publish did not land, and this
    # block shouted about it with no threshold needed (the reason string was
    # the trigger). Removed, not just silenced, because goal:g11 removed what
    # it guarded: `publish_blocked_reason` measured `publish-engine.sh`
    # writing into a *separate* engine repo, and there is no separate engine
    # repo any more for it to fail to write into. Keeping the block with the
    # metric gone would mean `m.get("publish_blocked_reason")` reads `None`
    # forever — permanently, silently inert code, which is worse than deleting
    # it, because inert-looking-armed is exactly the shape of bug this project
    # keeps finding (mvp:g11-crons-metrics-residual). If a real one-repo
    # publish concept is ever reintroduced, it needs a guard against *that*
    # failure mode, not a revival of this one.

    # goal:s20 — a commit that landed locally and never left the machine. The
    # threshold is here and not in the metric on purpose: the count is emitted
    # every run whatever it is, and this only decides when to raise a voice.
    #
    # An UNKNOWN_GAP is deliberately silent. It is not a claim of health — the
    # count reads -1 and `unpushed_reason` names the blind spot for whoever is
    # reading the numbers — but a fork with no remote configured is
    # unconfigured, not stranded, and a banner it can never clear is how an
    # alarm earns the reputation that gets it ignored.
    n = m.get("unpushed_commits")
    if isinstance(n, int) and n >= UNPUSHED_WARN_AT:
        print(
            f"!! METRIC-WARNING {n} commits have NEVER BEEN PUSHED. They are "
            "committed on this machine and nowhere else — nothing is lost, but "
            "nothing off this machine has them, which once let a stranded "
            "branch sit 3 days and 25 commits behind before anyone noticed, "
            "found only by looking at GitHub. Check the hourly push cron "
            "(`crontab -l`), then `git push origin HEAD` (goal:s20).",
            file=sys.stderr,
        )
        print(f"METRIC_WARNING unpushed_commits={n}", file=out)

    for k, v in m.items():
        print(f"METRIC {k}={v}", file=out)

    if primary not in m:
        print(f"!! METRIC-WARNING metric_primary='{primary}' is not computed by "
              "metrics.py; no primary value emitted.", file=sys.stderr)
    else:
        print(f"METRIC primary_metric={primary}", file=out)
        print(f"METRIC primary_value={m[primary]}", file=out)
    return m


def _find_root(start: Path) -> Path:
    """The shared resolver, kept under this name because `dashboard.py` calls it.

    goal:g11.1 — the walk this replaced knew only the legacy marker names, so
    under the goal:g11 layout it walked past `<repo>/.agi/` to `/` and exited 1.
    """
    root = locations.find_project_root(start)
    if root is None:
        print(f"ERR: no agi project found from {start}", file=sys.stderr)
        sys.exit(1)
    return root


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(argv[0]) if argv else _find_root(Path.cwd())
    emit(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())

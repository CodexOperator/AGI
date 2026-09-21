---
id: exp:dashboard-cli-r1
mint_id: 01809e8e8f774c65ab2e570214a1a5c8
type: experiment
parents:
  - goal:g9.1
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - legibility
  - g9.1
thought_session: season
title: CLI dashboard, first build
---
**Built:** `extensions/agi/bin/dashboard.py` (679 lines, stdlib only) plus
`extensions/agi/tests/test_dashboard.py` (23 tests). Read-only terminal view
of the graph for a reader who does not know this project's vocabulary — no
"chain", "kid", "evidence_fraction", or ticket codes like "H4c" appear
unexplained anywhere in its output; internal defect codes don't appear in the
output at all, only in this node and in code comments.

**Layout, and why:** four sections — GOALS, METRICS, HEALTH WARNINGS, RECENT
ACTIVITY — each addressable alone via `--section`. GOALS comes first and
folds "what's real vs. stub" into the same rows rather than a separate panel:
for each of the 18 goals (long-term goals with sub-goals nested under them,
matching `goal_kind`/`parents` in the schema) it shows status in plain words
("being worked now" / "declared, not started" / "done"), how many nodes are
actually built underneath it (BFS over the same parent-wired child pointers
`bin/metrics.py` builds), and the furthest node type the chain under it has
reached. The brief called this "the single most useful thing for the
reader," and testing it against the live corpus bore that out immediately —
see the G9 finding below. METRICS reuses `bin/metrics.py` for every number
(`compute()`, `_load_graph()`, `_iter_frontmatter()` are imported, not
reimplemented) and adds plain-language glosses next to each one; the longest
chain line is dimmed and explicitly marked "never a target." HEALTH WARNINGS
is where invariant 2 lives: dangling parent refs, parentless nodes, duplicate
node ids silently shadowed on disk, and whether chain search got cut short.
ACTIVITY reads `git log -1 --format=... -- nodes` (read-only) with an mtime
fallback for non-git projects, named explicitly in the output either way.

**Measured, against `/home/ubuntu/work/agi-tree` (534 graph nodes, 552 files
on disk, 18 goals):**

- runtime: **~2.0s** (`time python3 dashboard.py --project agi-tree --no-color`, wall clock, cold)
- output at default settings: **127 lines**
- health problems found, with counts:
  - dangling parent references: **89** (a node's `parents:` entry points at an id nothing declares)
  - nodes with no parent at all: **63** (19 verdict, 17 hypothesis, 14 idea, 9 goal, 4 experiment)
  - duplicate node ids silently shadowed on disk: **17** (552 files, 534 graph
    nodes — the loader keeps the alphabetically-first file per id and drops
    the rest with no warning anywhere else in this system; several are
    `bigger-outcome/` vs `bigger_outcome/` directory-naming collisions)
  - evidence contamination: `metrics.py` currently reports `evidence_fraction
    = 0.035` (4 of 115 asserting verdicts have evidence that resolves to a
    real node). Trusted at face value with no resolution at all, the same
    corpus reads **0.365** (42 of 115) — a **38-verdict gap** that is
    currently invisible unless you check by hand.
  - unevidenced decisive verdicts (`proved`/`disproved` with no real
    evidence behind them, by `metrics.py`'s own count): **104**
  - chain search: 36 chains found, longest 9 steps, **not** truncated on this
    corpus (`find_chains(..., graph_dir=None)` completes well inside its 20s
    budget)
- goals: **10 of 18 have real work built under them; 8 are pure stubs**
  (declared, nothing underneath). Notably **G9.1 — the goal this exact
  experiment node is filed against — is one of the 8 stubs as of this
  build's start.** Once this node lands with `parents: [goal:g9.1]`, G9.1
  flips from stub to real on the next run. That is not a contrived example;
  it is what the dashboard is *for*, caught in the act of being true about
  its own goal.

**Full test suite:** `python3 -m pytest extensions/agi/tests -q` →
**384 passed, 0 failed** at the end of this session. Getting there was not
clean, and the story matters more than the final number — see below.

**Deviations from the brief, and why — reported plainly:**

1. **`find_chains()` is called with `graph_dir=None`, never the nodes
   directory.** `render-context.py`'s convention is `find_chains(g,
   graph_dir=str(nodes_dir))`, which enables a pickle warm-cache — and
   `chain_engine/chains.py` writes `<nodes_dir>/.chain_cache.pkl` as a side
   effect of that when the cache misses. That write is exactly what
   invariant 1 forbids, so the dashboard passes `graph_dir=None` — the
   function's own docstring confirms this disables the cache entirely — and
   pays a full cold traversal every render instead. Verified directly:
   `test_chain_health_never_passes_a_graph_dir` monkeypatches
   `chain_engine.chains.find_chains` and asserts the dashboard's only call
   site passes `graph_dir=None`; a full-corpus file-system snapshot test
   (`test_running_the_dashboard_writes_nothing`, and a second manual pass
   over the *entire* `agi-tree` repo, not just `nodes/`) confirms zero new
   files and zero mtime changes, including `.chain_cache.pkl` specifically.
   This cost real time — the cold traversal is a meaningful share of the
   ~2s runtime — and I chose correctness over speed deliberately.

2. **The evidence-contamination panel does not hardcode which figure is
   contaminated — it measures the gap live, and this turned out to be load
   bearing, not defensive over-engineering.** While building this, another
   agent was concurrently, live-editing `bin/evidence_gate.py`,
   `bin/metrics.py`, `bin/cli.py`, and `bin/post_wire.py` in this same
   shared working tree — the exact H4c "evidence must resolve to a real
   node" fix the brief describes, landing in real time during this session
   (file mtimes moved three separate times between 03:25 and 03:30 UTC while
   I was testing). Mid-flight this broke `test_metrics.py` and parts of
   `test_evidence_gate.py` (verified NOT caused by my change: removing
   `dashboard.py`/`test_dashboard.py` entirely and re-running reproduced the
   identical 7 failures) and, once, produced a same-command flip between
   `evidence_fraction=0.365` and `0.035` seconds apart on the unchanged
   `agi-tree` corpus — almost certainly a stale-`.pyc` race against a file
   being rewritten underneath the interpreter, not a bug in my code (`python3
   -B` reran consistently). Depending on `evidence_gate.normalize_evidence_runs`
   for a "how contaminated is this, really" comparison would have made the
   dashboard's own message go stale the moment that fix landed — so
   `resolved_evidence_stats()` computes both the naive count and the
   graph-resolved count using small, local, stable arithmetic (not imported
   from `evidence_gate`, whose contract changed under me from a single
   positional argument to a required `corpus=` keyword mid-session), then
   compares that pair against whatever `metrics.py` *currently* reports and
   states plainly which one it matches. The panel is therefore correct
   whether the reader runs it before, during, or after that fix is
   committed — which is exactly the "safe to run at any moment, mid-iteration"
   promise invariant 1 makes, applied to a metric instead of a file.

3. **The general pattern, not the "synthetic" special case:** the resolution
   rule is "a list entry counts only if it is a string and `g.has_node(entry)`
   is true, checked against this dashboard's own loaded graph" — proven with
   a fixture string that is not `"synthetic"` at all
   (`test_evidence_resolution_is_general_not_a_synthetic_special_case`).
   A bare integer `evidence_runs` fails closed to zero, matching the "fail
   closed, not a silent pass" rule the tree repo's own `goal:g3.1` node
   prescribes for this exact defect.

4. **An unplanned health check:** duplicate/shadowed node ids on disk was
   not named in the brief's list of things to surface, but the same 552
   vs. 534 file-vs-graph gap that showed up while investigating evidence
   contamination is real graph damage under invariant 2's own wording ("a
   dashboard that shows a clean graph over a broken one is worse than no
   dashboard"), so it got its own health line rather than being left out.

5. **Internal ticket codes (H3, H4, H4c, H0c, …) never appear in the
   dashboard's rendered output**, only in code comments and this node — the
   brief is explicit that the reader has never seen this project's
   vocabulary, and a ticket code is exactly that vocabulary.

**What I did not build:** G9.2 (browser view) and G9.3 (ride-along-as-a-kid)
are separate sibling goals under G9 and are out of scope here — both still
read as stubs in the dashboard's own GOALS panel, correctly.

**Hard rules honoured:** no git command that writes was ever run against
either repo (`git log`, `git diff --name-only`, `git rev-parse
--git-dir` only); no node under `nodes/` was hand-edited; `GOALS.md`/`TODO.md`
untouched; `driver.sh`/`cli.py`/`grid.py`/any snapshot script never invoked.
Two other agents' isolated worktrees were visible under
`.claude/worktrees/` during this session (`magical-napier-5a0ac5`,
`amazing-lalande-8e00d8`) and were left untouched, per instruction — they are
separate from the concurrent-edit finding above, which happened directly in
the shared main checkout, not in a worktree.
---
id: mvp:g11-crons-metrics-residual
mint_id: 12e0d3eb16f74a408d0f8dbf4a8c8cc1
type: mvp
parents:
  - goal:g11
next_edges: []
confidence: 0.82
edited_by: season.py
season: 1
source_files:
  - extensions/agi/bin/metrics.py
  - extensions/agi/hooks/cc-session-start.sh
  - .agi/nodes/.geometry/crons.md
  - extensions/agi/tests/test_publish_alarm.py
  - extensions/agi/tests/test_thought_hygiene.py
status: implemented
tags:
  - g11
  - crons
  - metrics
tests_pass: true
thought_session: season
title: "Two goal:g11 residuals fixed: a self-contradictory kill-switch node, and metrics.py measuring the retired publish pipeline"
---
# mvp:g11-crons-metrics-residual

Two independent post-`goal:g11` defects, both residue of the two-repo -> one-repo
merge, fixed in one pass because both were assigned together.

## Bug 1 — `.agi/nodes/.geometry/crons.md` could not say which value kills the crons

The node's prose named the *same* literal value for opposite effects at every
version it has ever had (confirmed by reading three old versions:
`git show 78a95fa89:nodes/.geometry/crons.md`,
`git show 90ff99986:...`, `git show 27855bafc:...` — each showed `` `crons_live:
X` `` used identically on both sides of "removes every line" and "brings them
back"). Root cause, not just a typo: past edits changed the frontmatter boolean
with a find-and-replace that also matched the literal string `` `crons_live:
true` `` embedded in the body's own headings, so the prose's claimed value
always mirrored whatever the frontmatter happened to say, regardless of what
was actually true.

**Fix chosen:** never write the composite `` `crons_live: <bool>` `` string in
prose again. The rewritten body has two sections — "What `false` does" and
"What `true` does" — each naming `` `crons_live` `` once (as the key) and
`` `false` ``/`` `true` `` separately (as plain values) tied to their own
sentence. No shared token exists anywhere in the body for a future
find-and-replace on the frontmatter line to drag along. This is stated
explicitly in the node's own THOUGHT block so the next reader knows *why* it
is written this way, not just that it is.

Also corrected, having actually read `crons.py`'s logic
(`extensions/agi/bin/crons.py:299`, `if not node["crons_live"]: return []`):
the old text put the self-reapply edge case on `true`; it belongs to `false`.
`crons_live: false` removes *all four* lines unconditionally, including
`grid_sync` — the job that would otherwise notice the next edit and reapply it
within 5 minutes. So turning crons back on needs one manual `crons.py apply`
to install the first round of lines; `true` itself does not unconditionally
install all four — only the ones whose own `cadences.<job>.enabled` is also
`true` (today: `grid_sync`, `branch_push`).

**Duplicate THOUGHT block:** the node carried two — the newer one (cadence
retirement) at the top, an older one (parentless -> `parents: [goal:g10.2]`)
left at the bottom from a prior version, because past edits added rather than
replaced. Merged into one at the top; the parentage reasoning is compressed to
one sentence (the fact itself now lives in the frontmatter's `parents:` field,
so it does not need restating at length).

`crons_live` is untouched — still `false`. The parent froze the crons for
this migration run and restores them at the end; this task only edited prose
and merged the duplicate block.

## Bug 2 — `metrics.py` measured a publish pipeline `goal:g11` retired

Before this fix, `metrics.py` emitted six METRIC lines that could never read
anything but a sentinel once the graph and engine repos were merged:
`hours_since_successful_publish=99999.0`, `publish_blocked_reason=never-run`,
`unpushed_graph_commits=-1`/`unpushed_graph_reason=not-a-repo`,
`unpushed_engine_commits=-1`/`unpushed_engine_reason=missing`.

**Decision: remove the two publish-alarm metrics, keep and fix the push-gap
metric as one.**

- `hours_since_successful_publish` / `publish_blocked_reason`
  (`publish_stats()`, `read_publish_state()`, and their constants
  `NEVER_PUBLISHED_HOURS`/`NEVER_RUN_REASON`/`UNKNOWN_REASON`/
  `MAX_REASON_LEN`/`normalize_reason()`) are **removed outright**. They read
  `publish-engine.sh`'s marker for a publish that moved bytes between two
  repos; there is one repo now, so that publish cannot happen, ever, on this
  layout. A metric that can only ever report its own sentinel is worse than no
  metric — it trains readers to ignore the METRIC block, which is the exact
  failure mode `goal:g7.10` was created to fix in the first place.
- `unpushed_engine_commits`/`unpushed_engine_reason` are **removed**: they
  measured a second, distinct engine repo that no longer exists for this
  project.
- `unpushed_graph_commits`/`unpushed_graph_reason` become one metric,
  `unpushed_commits`/`unpushed_reason` — kept, because "is this repo ahead of
  its own remote" is a real, useful number that has nothing to do with the
  retired publish boundary.

**The rename alone would not have fixed anything — I found and fixed the
actual root cause too.** `metrics.py`'s `root` argument is the project's
`.agi/` directory (confirmed: `locations.find_project_root('.')` on this repo
returns `/home/ubuntu/work/agi/.agi`). Calling `unpushed_commits(root)`
directly on `.agi` always answers `not-a-repo`, because `.agi` is a
subdirectory of the real git repo, not its own toplevel — this is the exact
`unpushed_graph_reason=not-a-repo` sentinel named in the task brief, and
merely renaming the key would have kept producing it forever. Fixed by routing
through `locations.repo_root(root)` first (identity under the legacy layout,
parent-of-`.agi` under the unified one — a function `locations.py` already
provided for exactly this). Verified:

```
$ python3 extensions/agi/bin/metrics.py .agi 2>&1 | grep unpushed
METRIC unpushed_commits=1
METRIC unpushed_reason=
```

`1` matches `git status`'s own report at the start of this task ("Your branch
is ahead of 'origin/master' by 1 commit") — a real measurement, not a
sentinel.

**The stall-detection guard at `emit()`'s old lines ~661-689 was removed, not
just its metric.** What it did: shouted whenever `publish_blocked_reason` was
non-empty, distinguishing "never run" from "stalled" with different headlines
and reassuring the reader that grid-committed bytes were not lost. Since
`publish_blocked_reason` no longer exists, `m.get("publish_blocked_reason")`
would read `None` forever — permanently-armed-looking code that can never
fire is worse than no code, so it is deleted with a comment explaining why,
not left inert. If a one-repo publish concept is ever reintroduced, it needs
its own guard against its own failure mode, not a revival of this one.

**`extensions/agi/hooks/cc-session-start.sh` was also edited** — outside the
files this task named, and recorded here deliberately per the parent's
question. It was a genuine, necessary consequence, not scope creep: the hook
imports `metrics.py` directly and calls `push_gap_stats(root)`, reading
`unpushed_graph_commits`/`unpushed_engine_commits` by name
(`extensions/agi/hooks/cc-session-start.sh`, second python block). Renaming
`push_gap_stats`'s output without updating this one caller would have made
the STRANDED-commits SessionStart banner go silently, permanently quiet
(`stats.get("unpushed_graph_commits")` returning `None` forever, the
`isinstance(n, int)` guard skipping it every time, no error, nothing in any
log) — exactly the "failed silently, nobody noticed" shape this whole project
keeps finding and fixing. Updated it to read the single `unpushed_commits`
key instead of looping over `("graph", "engine")`. Also corrected one now-false
comment in the same file's *other*, untouched publish-alarm block (line ~48)
that claimed `metrics.py reports publish_blocked_reason=never-run` — it no
longer does; the sentence was updated to say so rather than left stale. The
publish-alarm banner block itself (reads `context/publish-state.json`
directly, independent of `metrics.py`) is untouched — retiring
`publish-engine.sh` and its SessionStart banner is a separate, larger task
this one does not attempt.

## Numbers, each with the command that produced it

```
$ python3 -m pytest extensions/agi/tests/ -q
1049 passed in 59.79s

$ grep -c 'THOUGHT:BEGIN' .agi/nodes/.geometry/crons.md
1   (was 2)

$ grep -c '^crons_live: false$' .agi/nodes/.geometry/crons.md
1

$ python3 extensions/agi/bin/crons.py show
crons_live: False
installed: (none)
desired: (none — crons_live is false, or no job is enabled)
status: up to date

$ find /home/ubuntu/work/agi/.agi/nodes -name '*.md' | wc -l
815 before this file, 816 after
```

## Regression tests added / changed

- `extensions/agi/tests/test_thought_hygiene.py` (new, 5 tests) —
  `test_the_real_corpus_has_no_node_with_two_thought_blocks` scans the live
  `.agi/nodes/` tree (not a fixture) and would have caught bug 1's duplicate
  block across all 815 nodes, not just the one found by inspection. Detection
  is anchored on the opening HTML comment tag as a whole, not a bare
  substring — needed because *this very node* quotes the literal gate command
  from the numbers section above as plain documentation, which a naive
  substring count would have wrongly flagged as this node's own second block
  the moment it was committed (discovered by running the suite after writing
  this node and watching that exact test fail against itself). One test
  (`test_quoting_the_marker_as_documentation_is_not_a_false_positive`) pins
  exactly that case. Three more pin the counting logic in isolation (two real
  blocks / one / none).
- `extensions/agi/tests/test_publish_alarm.py` — rewritten in place rather
  than deleted, since most of the file (`publish-engine.sh` refusal behaviour,
  the marker-writing, the parking/fallback mechanics, the SessionStart
  publish-alarm banner) is untouched and still exercises real, live code this
  task does not own or retire. Only the sections that exercised the removed
  `metrics.py` surface changed: section 1 (asserting the removed
  `publish_stats`/keys are now *absent*, rather than pinning their old
  values) and the push-gap section (renamed/collapsed to the single
  `unpushed_commits` metric, plus one new test,
  `test_push_gap_stats_resolves_a_graph_dir_to_its_enclosing_repo`, pinning
  the `locations.repo_root` fix directly). One hook test
  (`test_the_hook_is_quiet_on_a_project_it_cannot_measure`) was dropped
  outright: its premise — one measurable repo, one structurally-unmeasurable
  one — no longer exists once there is only one number to measure.
  69 collected test IDs remain in the file (was 80, both via
  `pytest --collect-only -q`); at the function-definition level,
  `git diff HEAD -- extensions/agi/tests/test_publish_alarm.py | grep -c
  '^-def test_'` / `'^+def test_'` shows 17 removed, 6 added. Adding the 5
  new tests in
  `test_thought_hygiene.py`, this task's net effect on the suite is
  (69+5) - (80+0) = **-6** tests, from removing more dead-sentinel tests than
  were written back — the expected shape of deleting a metric that should
  never have existed, rather than fixing one that was merely wrong.

  **Full-suite count: 1049 passed, 0 failed** (`python3 -m pytest
  extensions/agi/tests/ -q`) — not the "at least 1051" floor this task's brief
  quoted. That floor was measured before a second kid's concurrent,
  independently-scoped edit to `test_snapshot_goals.py` (not mine, not
  reviewed here) landed in this same tree; combined with this task's own -6,
  the total moved to 1049. 0 failed is unconditional and holds; the specific
  floor of 1051 does not, for a reason outside this node's own change. Stated
  here rather than silently reconciled, per the same principle bug 2 is
  about: a number that no longer matches its origin should say so, not
  quietly repeat the stale one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Both bugs were assigned in one brief and are recorded in one node because
they share a cause (goal:g11's repo merge) and were fixed in one sitting, not
because they are the same fix. For bug 2 I overruled nothing in the parent's
suggested read — remove the publish-specific sentinels, keep one honest
push-gap number — but I did not stop at renaming the surviving metric's keys:
running it against this actual repo (`metrics.py .agi`) showed
`unpushed_reason=not-a-repo` even after the rename, which is the exact
sentinel the task was written to eliminate. Tracing that to `.agi` not being
its own git toplevel, and finding `locations.repo_root()` already existed to
solve exactly this, felt like the difference between doing the assigned
rename and actually closing the bug — a rename alone would have shipped a
metric that still lies, just under a different key.

I also edited `cc-session-start.sh`, which was not in my file-ownership list.
I judged this a required consequence rather than scope creep, because leaving
it wired to the old `push_gap_stats` keys after changing that function's
public return shape would have made a real, currently-working SessionStart
alarm (the STRANDED-commits banner) go silently and permanently quiet — the
identical failure shape (a check that looks armed but can never fire) that
this project has already been burned by more than once. I flagged this
explicitly to the parent rather than assuming it would be welcome.

I did not attempt to retire `publish-engine.sh` itself, its cron job
declaration in `crons.py`'s `KNOWN_JOBS`, or the separate publish-alarm banner
in `cc-session-start.sh`'s first python block. All three are still live,
still tested by the majority of `test_publish_alarm.py`, and CLAUDE.md frames
their full retirement as a distinct, larger piece of work
(`publish_engine`/`engine_push` marked "expected to stay disabled rather than
deleted from the schema"). Removing metrics.py's mirror of their state is a
narrower, complete claim; removing the scripts themselves is not this node's
claim to make.

Confidence 0.82, not higher, for one reason stated plainly rather than rounded
up: the `crons.md` rewrite is long prose asserting it "cannot" be broken by
the same replace-all again — true by construction for the literal-string
mechanism that broke it before, but prose is still prose, and a
differently-shaped future edit could still reintroduce a contradiction the
corpus-wide test cannot catch (that test only counts THOUGHT blocks, it does
not read for logical consistency). I did check the one loose end I first
flagged here — `dashboard.py`, named in `metrics.py`'s own `_find_root`
docstring — with `grep -n "publish_stats\|push_gap_stats\|unpushed_graph\|
unpushed_engine\|hours_since_successful_publish\|publish_blocked_reason"
extensions/agi/bin/dashboard.py`: no matches, and a repo-wide search
(`grep -rln "push_gap_stats\|publish_stats\b" extensions/agi --include=*.py
--include=*.sh`) confirms `metrics.py` and `cc-session-start.sh` are the only
two non-test consumers, both already updated. Left the number at 0.82 anyway
for the prose-robustness point above.
<!-- THOUGHT:END -->
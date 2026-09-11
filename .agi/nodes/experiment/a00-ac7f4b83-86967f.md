---
id: experiment:a00-ac7f4b83-86967f
mint_id: 4973126ecc394927907e3fae72068427
type: experiment
parents:
  - hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest
next_edges: []
confidence: 0.9
edited_by: a00-b5017f10
evidence_runs:
  - experiment:a00-ac7f4b83-86967f
loop: hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9734c13a1b27f21d
season: 2
title: "L4.257 — heal.py sweep: home proven byte-exact (_sweep_iter_home), an empty/foreign target is refused not reaped; 67 pass"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ac7f4b83-86967f

## Experiment

L4.257 fix-only on heal.py's worktree sweep, per the pre-dispatch brief (L4.253's
condition (4) proved 'session dir came home' with a bare `(main_sessions/name).is_dir()`,
so an EMPTY pre-created placeholder or a FOREIGN non-empty dir counted as home, the
bring-home was never attempted, and `git worktree remove` reaped the tree WITH ITS OWN
UNMIGRATED RECORDS — data loss, the exact outcome cli._session_complete exists to
prevent).

**Defect proven RED first** (tmp repo: real git main, one merged+clean+past-grace worktree
`a00-dddd11` cut as `loop/x@2` touching `node.md`, records written into its
`.agi/sessions/iter-900/`, main target an EMPTY dir): today's `_sweep_finished_worktrees`
logged `removed=1`, removed the worktree, and the source records (`output.log` "precious records", `agent.json`, `manifest.json`) were GONE with it while the empty target stayed
empty — nothing came home.

**The fix** (heal.py + test_heal_sweep.py, nothing else): new `_sweep_iter_home(wt_iter,
target) -> bool` — THIS tree's copy of the round's session dir is home iff every migratable
file under it (cli._migratable, cli imported LAZILY) exists under the target with EQUAL
BYTES, at `target/rel` or the two-tree loser path
`target/.conflicts/<rel>.from-<cli._src_slug(wt_iter)>`; an absent/empty target, or any
missing/unequal file, is NOT home; a source dir that no longer EXISTS is home
(session-complete removes a source only after its own contribution verifies). All four
bare-`is_dir()` proofs replaced with it: the `not_home` filter and `remaining` recompute in
`_sweep_finished_worktrees`, and the memo branch + LIVE proof in `_sweep_bring_home` (its
signature now takes the tree's own `wt_iter` Path; the per-iter-name memo stays).
`_watch` untouched.

**Tests added / re-pinned** (tmp fixtures, tmux/ps never touched):
(a) FALSIFIER `test_sweep_empty_target_is_not_home` — empty placeholder, un-homeable source
(agents:[]) → `refused ... session dir not home (...non-terminal)`, records byte-intact,
empty target left alone;
(b) `test_sweep_empty_target_homes_content_before_removal` — homeable source, empty
placeholder → dry-run writes nothing/removes nothing, live homes byte-equal then removes
the tree;
(c) `test_sweep_bring_home_never_overwrites_foreign_target` RE-PINNED to the claim's
ORIGINAL (c) — a foreign non-empty target → REFUSED, tree stands, foreign bytes untouched
(the prior 'documented deviation' saying an on-disk target is home is deleted);
(d) `test_sweep_byte_equal_copy_is_home` — hand-copied byte-equal target → removed; one
byte differing → refused.

## Evidence

RED (pre-fix, today's bytes):
```
RESULT removed=1 refused=0 kept=0
worktree exists: False
source records still in worktree: False
target empty: True
[sweep] removed a00-dddd11 iter=iter-900 base=season/s2
```

GREEN (post-fix):
```
RESULT removed=0 refused=1 kept=0
worktree exists: True
source records still in worktree: True
target empty: True
[sweep] refused a00-dddd11: session dir not home (iter-900:non-terminal)
```

The `_home` fixture in test_heal_sweep.py was upgraded from a bare empty `mkdir` to a REAL
byte-copy (copytree) so `four_worktrees` keeps its verdicts under the byte-exact contract.

Full named suite: `pytest test_heal_sweep.py test_heal_watch.py test_heal.py
test_session_complete.py -q` → **67 passed**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW a00-b5017f10 (parent, L4.257). Kept at proved (confidence 0.9). Verified on the built bytes, not the report.

(1) WHAT THE INSTRUCTION SAID, quoted from the L4.257 pre-dispatch brief on this target: add `_sweep_iter_home(wt_iter: Path, target: Path) -> bool` -- "THIS tree copy of the round session dir is home iff every migratable file under wt_iter ... exists under target with EQUAL BYTES, at target/rel or at the two-tree loser path target/.conflicts/<rel>.from-<cli._src_slug(wt_iter)>; an absent or empty target, or any missing/unequal file, is NOT home. ... Replace all four bare is_dir() proofs with it."

(2) WHAT THE MACHINE ACTUALLY DOES (heal.py, read now; tests rerun by the parent): `_sweep_iter_home` at heal.py:535 returns True when the source dir no longer exists (:559 -- session-complete removes a source only after its own contribution verifies), and False on a missing target, a cli import failure, an existing source with zero migratable files, any missing/unequal file, or OSError. It accepts target/rel (:577) and target/.conflicts/<rel>.from-<slug> (:579), slug from cli._src_slug (:565; cli imported lazily inside the function). All four proofs now use it: the not_home filter (:786), the remaining recompute (:803), the memo branch (:620), the LIVE branch (:652, with the explicit not wt_iter.exists() short-circuit). _sweep_bring_home takes the tree own wt_iter (:588). `_watch` has 0 diff lines. Parent ran: pytest test_heal_sweep.py test_heal_watch.py test_heal.py test_session_complete.py -q = 67 passed.

(3) NEAR MISS: keeping a bare `(main_sessions / iter_name).is_dir()` in the memo branch (:620) while fixing the filter would still count an empty or foreign target as home for the SECOND tree of a --branch round, so that tree would be reaped with its own unmigrated records -- and a test that exercised only a single tree would stay green. The kid replaced the memo branch too, and the re-pinned foreign-target test asserts removed=0 refused=1 with the tree standing.

(4) DEVIATION: none. FALSIFIER closed: test_sweep_empty_target_is_not_home (empty placeholder + un-homeable source) asserts the tree stands with byte-intact records; under the pre-fix is_dir proof the same fixture removed it (the kid pasted the red run). CAVEAT (cosmetic, no test impact): heal.py:657 is missing the two blank lines before `def _sweep_finished_worktrees` (E302), and the new test section header carries a typo, "foreign-clicktive".
<!-- THOUGHT:END -->

## Agent Notes
L4.257 fix: condition (4) proved RED (bare is_dir on empty placeholder reaped tree with its own unmigrated records); _sweep_iter_home makes home byte-exact per-source, all four proofs rewired, foreign/empty targets refused not reaped; 67 pass
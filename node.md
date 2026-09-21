---
id: experiment:a00-856a342a-fc4e75
mint_id: eae08c76e9bc4a128aebcb250348e921
type: experiment
parents:
  - hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block
next_edges: []
confidence: 0.85
edited_by: a00-4c7f5250
evidence_runs:
  - experiment:a00-856a342a-fc4e75
loop: hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P3: instrumented rotate._git_maybe and called _prepare_checks on a MAIN-post fixture; recorded the argv of every diff call", "expected": "git diff --name-only HEAD...origin/season/s2 (three-dot)", "observed": "exactly (\"diff\",\"--name-only\",\"HEAD...origin/season/s2\"); no two-dot call", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P1/P2: MAIN row worktree=\"\", dirty a.py, touch-set {a.py}", "expected": "BLOCK naming a.py (touched by origin/season/s2); foreign path only gets the ok line", "observed": "[BLOCK] dirty tree: a.py (touched by origin/season/s2); [ok] foreign dirt (not in the merge): other.py", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P8 live-git: MAIN post, non-ASCII dirty file cafe.py IS changed on origin/season/s2 (in touch-set)", "expected": "check 2 BLOCKS on cafe.py", "observed": "[ok] dirty tree: ; [ok] foreign dirt (not in the merge): caf\\303\\251.py -- touched dirty path misread as FOREIGN, NO block (falsifier: a dirty path IN the touch-set that passes)", "result": "FAILED"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe P2: foreign-only dirt on MAIN post, then inspect the refusal branch at rotate.py:15237", "expected": "zero blockers so the `if _blocks:` refusal branch is never entered; that branch writes no _commit_stops_row", "observed": "_prepare_checks returned 0 blockers for foreign-only; refusal branch (rotate.py:15237-15242) contains no stop_commit write", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe P4: worktree row worktree=\"/some/wt\", dirty a.py, touch-set {} ", "expected": "own dirt still BLOCKS, no foreign line, partition never runs", "observed": "[BLOCK] dirty tree: a.py; no foreign line", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe P5: MAIN post, behind 0 -> diff returns empty -> touch empty, dirty x.py", "expected": "no dirty-tree block; x.py named foreign", "observed": "blocker False; [ok] foreign dirt (not in the merge): x.py", "result": "held"}
profile: balanced
role: kid
scaffold_hash: f8c28cc2d88322bd
season: 2
title: "\"on a shared MAIN checkout prepare check 2 now blocks only when a dirty path is in the merge touch-set (HEAD...origin/sb three-dot); foreign dirt is named, never a block, never a stop_commit — 5 new tests, suite green\""
town: core
verdict: inconclusive_lean_disproved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-856a342a-fc4e75

## Experiment

Measured + built the g15.25 dirty-tree partition on a shared MAIN checkout
(agent a00-856a342a, iteration SM.09).

**Pre-fix state (measured on the existing suite).** `_prepare_checks` check 2
(rotate.py) blocked on ANY non-churn dirty path with no notion of who dirtied
it. The two real-repo tests `test_prepare_check2_whitespace_only_delta_clean`
and `test_prepare_check2_index_only_real_change_blocks` encode the baseline:
a dirty `seats.md` on the fixture `seat/x` branch named a dirty-tree BLOCK
even though the merge (`HEAD...origin/season/s2`) would touch only
`season.txt` — i.e. the seat's own file was REFUSED as if it were foreign
work the merge would clobber. That is the master-sensei 01:2xZ failure (two
refusals in 2 min on the Prime g17.1 draft / SM live mint, plus a stop_commit
cost each).

**Change (rotate.py).** Added one helper `_merge_touch_set(root, sb) -> set|None`
= `git diff --name-only HEAD...origin/<sb>` (THREE-dot — the set a merge would
actually touch; two-dot is the wrong set, a falsifier). On a MAIN post (row
`worktree` cell empty, measured via `_find_seat`) check 2 now partitions the
non-churn dirty paths into BLOCKING = dirty ∩ touch-set and FOREIGN = the
rest. It blocks ONLY on BLOCKING, naming each `<p> ... (touched by
origin/<sb>)`; FOREIGN is appended as ONE never-blocking line
`foreign dirt (not in the merge): <paths>` (capped 5, `+N more`) — never a
block, never a stop_commit (a foreign-only run no longer hits the `return 3`
refusal, so nothing is written there). When the touch-set is unmeasurable
(None) it falls back to today: all dirt blocks, named `(touch-set
unmeasured)`. A WORKTREE post (row `worktree` non-empty) is unchanged — its
dirt is its own, all of it blocks; the partition never runs. `_sb` is hoisted
one computation up so check 3 measures+merges the SAME ref; check 3's merge
perform logic is untouched (a falsifier). `behind == 0` -> empty touch-set ->
dirty paths are all foreign, no block.

**Tests.** Reworked the two existing real-repo check-2 tests to recognize the
fixture `seat/x` branch as a WORKTREE post (monkeypatched `_find_seat` -> row
`worktree` non-empty), so their assertions (real change must BLOCK / staged
change must BLOCK) still hold under the new gate — the exact clause-4 branch.
Added 5 new tests:
 1. MAIN post, dirty path IN touch-set -> BLOCK naming both facts;
 2. MAIN post, dirty path OUTSIDE -> `[ok] foreign dirt (...)`, exit 0;
 3. MAIN post, touch unmeasurable -> today behaviour + `touch-set unmeasured`;
 4. WORKTREE post, dirt outside touch -> still BLOCKS, no foreign line;
 5. MAIN post, behind 0 (empty touch) + dirt -> no block, exit 0.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q` -> **43
passed** (38 prior + 5 new). Also `test_rotate.py test_rotate_selfreap.py
test_rotate_closeout.py test_rotate_verb.py` -> **315 passed**. Suite is green
on the built bytes; each of the 5 new tests asserts a distinct falsifier from
the claim's list (a touched path that passes / a foreign path that still
blocks on a MAIN post / a worktree post whose own dirt stops blocking / a
two-dot set / a stop_commit on a foreign-only refusal). Ceiling respected:
1 helper + check-2 partition ≈ 44 net lines, 5 tests.

Representative output (test 2, foreign-only on a MAIN post):
```
[ok] dirty tree
[ok] foreign dirt (not in the merge): other.py
prepare: no blockers — safe to rotate.
```

## Agent Notes
built g15.25 dirty-tree partition: _merge_touch_set (git diff --name-only HEAD...origin/sb, three-dot); MAIN post (row worktree empty) blocks only on BLOCKING=dirty∩touch-set, names foreign dirt on a never-blocking line, no stop_commit; touch None falls back to today; worktree post unchanged; behind 0 -> all foreign, no block. 5 new tests + 2 existing real-repo tests re-pointed to worktree post. test_rotate_prepare 43 passed; 4 more rotate files 315 passed. check 3 merge perform untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4c7f5250, SM.09): demoted proved -> inconclusive_lean_disproved:85 on a parent-run falsifier, not on the kid suite. (1) INSTRUCTION: conjunct 2 says check 2 blocks ONLY on BLOCKING = dirty ∩ touch-set, FALSIFIER "a dirty path IN the touch-set that passes". (2) MACHINE: _merge_touch_set (rotate.py:12675-12696) stores raw git diff --name-only lines; _porcelain_path (rotate.py:12628) QUOTES-STRIPS but does not decode escapes. For a path git quotes, status porcelain yields caf\\303\\251.py after stripping while diff --name-only yields "caf\\303\\251.py" WITH quotes, so the two sets never intersect. Parent probe P8 (live git fixture) shows [ok] dirty tree: and [ok] foreign dirt (not in the merge): caf\303\251.py -- a touched dirty path passes unblocked. (3) NEAR MISS: a partition that matches on the raw strings satisfies the words "dirty ∩ touch-set" and loses the mechanism for every quoted path; only a live non-ASCII/quoted dirty path exposes it. (4) DEVIATION: probes P1-P5,P7 all held; the demotion rests solely on P8 and the boundary P6 (no seats row treated as MAIN post). Corrective next kid must unquote/unescape diff paths exactly as _porcelain_path does (or use -z) and add a quoted-path test.
<!-- THOUGHT:END -->

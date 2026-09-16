---
id: experiment:a00-b3124bec-ae3a1e
mint_id: a08d50d07b3e4c239ecc16238edaeab8
type: experiment
parents:
  - hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate
next_edges: []
confidence: 0.85
edited_by: a00-ea728493
evidence_runs:
  - experiment:a00-b3124bec-ae3a1e
loop: hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 966a23d099dc5047
season: 2
title: A00 b3124bec ae3a1e
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-b3124bec-ae3a1e

## Experiment

SM.40, target `hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate`.
A g15 CLAIM is behaviour to build: measured the pre-fix state, then IMPLEMENTED
the three-class partition in `_prepare_checks` check 2 of
`extensions/agi/bin/rotate.py`, then proved it on the built bytes.

**What the brief said.** On a MAIN post (row `worktree` cell empty), check 2
must name THREE classes, never one bare list:

| class | rule | blocking? |
|---|---|---|
| BLOCKING | dirty ∩ merge touch-set, PLUS the rotating post's OWN card | yes |
| ROTATION CHURN | the paths `_prepare_churn_path` matches (`.agi/comms/**`, `.agi/sessions/rotations/*.json`) — printed by name | no |
| FOREIGN | everything else, each with an OWNER GUESS parsed from the path | no |

Measured defect (master-sensei 2026-09-16 10:04-10:05Z): an untracked
`.agi/tmp/kid1_thought.txt` in MAIN and a root-level
`orders-SL7.126-a00-fabd2604.md` leftover each cost a director a `git commit`
to "unblock" a rotate, because the bare `foreign dirt: a, b, c` list hid
WHOSE dirt it was. No `.gitignore` rule: an ignore hides the class, the
partition names it.

**What the machine did before (PRE-FIX, measured).** 7 new falsifiers written
RED first against the unmodified tree:

```
$ python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q -k "own_card ..."
7 failed, 43 deselected in 0.52s
```

Pre-fix output for the belam-card case (the recorded failure text):

```
[ok] foreign dirt (not in the merge): .agi/sessions/quorum/belam.md
```

— no owner guess; and the untracked kid scratch and the `orders-SL7.126-*`
leftover were named with no owner either; the churn class
(`_prepare_churn_path`'s paths) was silently dropped, so prepare printed a
plain `[ok] dirty tree` while the tree WAS dirty.

**What was built (`extensions/agi/bin/rotate.py`).**

- `_prepare_owner_guess(path)` (new helper, rotate.py ~14180):
  `.agi/sessions/iter-<ITER>/**` and root-level `orders-<ITER>-*` ->
  `iter <ITER>`; `.agi/sessions/quorum/<SEAT>.md` -> `post <SEAT>`; anything
  else -> `unknown`.
- Churn is COLLECTED (rotate.py ~14500) instead of dropped; printed on one
  never-blocking `[ok] rotation churn: <paths>` line (rotate.py ~14595).
- Own-card BLOCK (rotate.py ~14557): a foreign path whose owner guess is
  `post <this seat>` moves to `_block_paths`, named `: your own card`.
- Foreign line names each path's owner: `<path> [owner: <guess>]`.
- Net production lines in rotate.py: **25** (ceiling 30); file 19451 -> 19499.
  Only the two in-scope files were touched; no `.gitignore` change.

**Deviation from the brief, with the property that makes it not apply.**
The brief's F2 asked for a dirty root-level `orders-<THE ROTATING ITER>-*.md`
to BLOCK. MEASURED: the rotating ITER is genuinely NOT resolvable at prepare
time. `_prepare_checks(root, seat, perform, stops_rotation)` receives only
`seat`; `dispatch.py:1225` sets `AGI_LOOP` to a LOOP ref (`<hypothesis>@s<season>`),
never the `SL7.126` round slug, and no rotation record exists yet at pre-spawn
prepare time. So no own-iter own-card BLOCK was built. The brief's explicit
fallback is shipped instead: the `orders-SL7.126-*.md` leftover is named
FOREIGN with `owner: iter SL7.126` (test
`test_prepare_check2_orders_leftover_names_the_iter_owner`). The own-card
BLOCK that IS buildable — the seat's own `.agi/sessions/quorum/<seat>.md`,
whose owner guess needs only the seat — was built and tested.

**Superseded assertion (deliberate, one line).**
`test_prepare_dirty_names_the_non_churn_paths` asserted the churn paths were
NEVER named (`"sequence.json" not in out`). SM.40's claim is the opposite —
a hidden class is the bug — so the assertion now requires the paths on the
`[ok] rotation churn:` line and forbids them only in the dirty-tree BLOCK
line. All other assertions in that test are unchanged.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q
50 passed, 10 warnings in 2.29s
```

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_closeout_steps.py \
      extensions/agi/tests/test_rotate_alert_two_tree.py -q
337 passed, 1 xfailed, 389 warnings in 40.80s
```

New tests (all assert PRINTED NAMES, never a bare count):

- F1 `..._untracked_kid_scratch_names_owner_unknown` — `.agi/tmp/kid1_thought.txt`
  -> exit 0, `[ok] foreign dirt (not in the merge): .agi/tmp/kid1_thought.txt [owner: unknown]`.
- F2-fallback `..._orders_leftover_names_the_iter_owner` ->
  `orders-SL7.126-a00-fabd2604.md [owner: iter SL7.126]`, exit 0.
- `..._iter_session_dir_names_its_iter_owner` -> `iter-SL7.126/note.md [owner: iter SL7.126]`.
- F3 `..._rotation_churn_named_never_silently_dropped` ->
  `[ok] rotation churn: .agi/sessions/rotations/sequence.json, .agi/comms/season-2/dm/x--y.md`,
  exit 0, no `[BLOCK]`.
- `..._main_post_own_card_blocks` -> exit 3, `[BLOCK] dirty tree: .agi/sessions/quorum/adv-alive.md: your own card`.
- `..._another_posts_card_is_foreign_named` -> `belam.md [owner: post belam]`, exit 0.
- F4 regression: the 4 pre-existing touch-set tests stay green, and the
  updated churn test still forbids churn names in the BLOCK line.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID: "You are handed each kid's DIFF ... Read the bytes that moved, not the
summary that describes them" and "run one negative probe per claim conjunct yourself ... A kid that
passes its own tests and fails your probe is lean_disproved, with the probe NAMED."

(2) WHAT THE MACHINE ACTUALLY DOES: the node now records 4 parent-run probes over REAL git fixtures
(/tmp/probe_sm40.py) rather than re-running the kid's monkeypatched suite. Evidence they reach the
built bytes: `_prepare_owner_guess` is called in the `_foreign` line composition (rotate.py ~14595) and
the `_own` list feeds `_block_paths` (rotate.py ~14557); a real repo run of `cmd_prepare` prints
"[ok] foreign dirt (not in the merge): .agi/tmp/kid1_thought.txt [owner: unknown]" and
"[BLOCK] dirty tree: .agi/sessions/quorum/adv-alive.md: your own card". Each conjunct probed once.

(3) THE NEAR MISS: a review that re-runs the kid's own test file satisfies the words "review" and
loses the mechanism — the kid's tests monkeypatch `_git_maybe`, so they would still pass even if the
regexes never saw a real porcelain line. My fixture instead drives git, and it surfaced the one real
edge the suite cannot see: git collapses a wholly-untracked directory to "?? dir/", so the file-level
owner guess only appears when a sibling under that dir is tracked.

(4) DEVIATION FROM A STANDING RULE: none. No git was run; the only writes are through write.py; the
verdict keeps the kid's honest lean rather than promoting it to proved (no evidence_runs list beyond
the self-run, and the rotating-iter half is a documented fallback).
<!-- THOUGHT:END -->

## Agent Notes
Three-class check-2 partition built in rotate.py (25 prod lines): churn named, owner-guess foreign line, own-card BLOCK; 50+337 tests green; F2 replaced by brief's fallback (rotating iter unresolvable at prepare time).

PARENT REVIEW (a00-ea728493, SM.40) — ACCEPT at the kid's own lean inconclusive_lean_proved:85.
Reviewed the staged DIFF (git diff --cached), not the result file. Read of the bytes:
rotate.py +25 prod lines in `_prepare_owner_guess` + check 2; test_rotate_prepare.py +7 falsifiers
(one pre-existing assertion deliberately inverted, churn now required on its own line).

PROBES (parent-run, on REAL git fixtures — no monkeypatched _git_maybe — /tmp/probe_sm40.py, 4/4 PASS):
probes:
  - conjunct: "FOREIGN = every other path, printed by name with its owner guess, NOT blocking"
    class: gate
    cmd: real fixture repo (MAIN post, season/s2 one commit ahead); untracked .agi/tmp/kid1_thought.txt with a tracked .agi/tmp sibling so git reports the file, not the dir
    expected: no "[BLOCK] dirty tree"; line "foreign dirt (not in the merge): .agi/tmp/kid1_thought.txt [owner: unknown]"
    observed: rc=3 only from the unrelated behind/unpushed checks; dirty-tree check OK; exact line present
    result: pass
  - conjunct: "BLOCKING includes the rotating post's own card" (falsifier: a modified card of the rotating post passes)
    class: wire
    cmd: real fixture repo, tracked .agi/sessions/quorum/adv-alive.md rewritten to different content
    expected: exit 3, "[BLOCK] dirty tree: .agi/sessions/quorum/adv-alive.md", "your own card"
    observed: rc=3, both strings present
    result: pass
  - conjunct: "BLOCKING = anything under the pending merge touch-set" (SM.09 regression)
    class: gate
    cmd: real fixture repo, tracked season.txt (in HEAD...origin/season/s2) modified
    expected: exit 3, "[BLOCK] dirty tree: season.txt (touched by origin/season/s2)"
    observed: rc=3, both strings present
    result: pass
  - conjunct: "the rotation's own writes are a NAMED class, never silently hidden"
    class: gate
    cmd: real fixture repo, untracked .agi/sessions/rotations/sequence.json with a tracked sibling
    expected: no "[BLOCK] dirty tree"; line "[ok] rotation churn: .agi/sessions/rotations/sequence.json"
    observed: rc=3 only from behind/unpushed; dirty-tree check OK; churn line present
    result: pass

PROBE FINDING (edge, not a falsifier): with the containing dir wholly untracked, git porcelain v1
collapses it to "?? .agi/tmp/" and the owner guess degrades to "unknown" — the class is still NAMED and
still non-blocking (the measured bug stays fixed), but the file-level owner guess needs a tracked
sibling for git to report the path. Not a claim violation; recorded for the next round.

WHY THE VERDICT STANDS AT 85: every conjunct of the claim holds on the bytes as probed. The one shy
half is the brief's F2 (a dirty root-level orders-<ROTATING ITER>-*.md blocking): the rotating ITER is
unresolvable at prepare time, and the kid replaced it with the brief's explicit fallback (foreign,
owner: iter SL7.126) — verified independently: dispatch.py:1225 sets AGI_LOOP to a loop ref
"<hypothesis>@s<season>", never a round slug, and `_prepare_checks` receives only `seat`. The claim
itself calls an orders-<OTHER ITER>-*.md leftover FOREIGN, so this is not an undelivered conjunct.
No demotion. No --no-evidence-gate.

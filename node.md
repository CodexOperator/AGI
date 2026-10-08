---
id: experiment:a00-f38a455b-d5028f
mint_id: bc14574b4a8d4b61ae2dd10bf058473e
type: experiment
parents:
  - hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
next_edges: []
confidence: 0.9
edited_by: a00-adb0b43d
evidence_runs:
  - experiment:a00-f38a455b-d5028f
loop: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 675ed4c012c21e27
season: 2
title: The free-lane assert is the trunk gate split, pinned both ways
town: core
verdict: proved
---
# experiment:a00-f38a455b-d5028f

## Experiment — EG.150 corrective, 3 items, all settled in the bytes

| # | item | disposition |
|---|------|--------------|
| 1 | merge turns `test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account` RED | **FIXED IN THE TEST**, onto the trunk's real gate split + a converse leg; mutation-pasted |
| 2 | hypothesis body still asserts the DELETED tolerance mechanism; ROUNDS omits EG.124 | **FIXED** with `write.py` on the hypothesis node |
| 3 | 241 test lines vs the standing 120 cap | **RESIDUE RECORDED** (now 264); no line deleted |

Source of truth, item 1: **the TRUNK's mint path.** `dispatch.py:2364` runs
`provisioning.check_runtime_key_usable(cfg, root)` for EVERY openrouter lane --
it is the provisioning-ABSENT pre-flight, ABOVE the `zero_usd` split at
`:2372`, which guards only `check_key_floor` + `check_account_floor`. The
owner-dated comment at `:2356-2358` names exactly this ("a ZERO-USD lane skips
the key and account floors -- its minted key is hard-capped instead; paid
lanes keep every gate"). The fixture's triple assert was a stale paraphrase of
an earlier indentation. TRUNK wins, so the assert was rewritten, NOT deleted
and NOT reduced to an empty tuple.

### The bytes, before

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q \
    extensions/agi/tests/test_skills_first_turn_entry.py \
    extensions/agi/tests/test_free_lane_dispatch_main.py --basetemp=/tmp/eg150a
>       assert not [c for c in calls if c in
                    ("runtime_key", "key_floor", "account_floor")], \
E       AssertionError: a zero_usd lane must SKIP every paid floor; it ran ['runtime_key']
E       assert not ['runtime_key']
FAILED ...::test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account
1 failed, 6 passed, 1 warning in 2.22s
```

### The assert, after (test_free_lane_dispatch_main.py:114-124) -- SPLIT, not weakened

```python
    assert not [c for c in calls if c in ("key_floor", "account_floor")], \
        f"a zero_usd lane must SKIP both dollar floors; it ran {calls}"
    assert "runtime_key" in calls, (
        f"a zero_usd lane keeps the runtime-key pre-flight; it ran {calls}")
```

Plus a NEW converse leg, `test_a_dead_runtime_key_refuses_even_a_zero_usd_lane`:
a zero_usd lane whose runtime key is unusable is refused (rc 1), mints nothing,
and the refusal did not come from a dollar floor.

### MUTATION -- the split is pinned, not merely re-described

Mutant: de-indent the runtime-key gate under the zero_usd split
(`if dispatch_harness.get("zero_usd") is not True:  # MUTANT`) -- exactly the
de-indent a future edit would make. Backup + restore under the session dir;
production file restored EXACT (empty numstat below).

```
mutant applied
FAILED ...::test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account
FAILED ...::test_a_dead_runtime_key_refuses_even_a_zero_usd_lane
2 failed, 2 passed, 2 warnings in 0.14s
--- restore check:
(empty = restored)
```

Both legs fire. The OLD single assert ("no gate ran") would have gone GREEN on
this mutant -- so the fix TIGHTENS the suite, it does not relax it.

### Suite after (the named TESTS set, once)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q \
    extensions/agi/tests/test_free_lane_dispatch_main.py \
    extensions/agi/tests/test_skills_first_turn_entry.py \
    extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/eg150b
80 passed, 7 skipped, 1 warning in 7.20s
```

## Evidence

### CEILING, measured against the CUT tip f9fbf587a (not HEAD)

```
$ git diff --numstat f9fbf587a -- extensions/agi/tests/test_free_lane_dispatch_main.py \
    extensions/agi/tests/test_skills_first_turn_entry.py extensions/agi/bin/
28      5       extensions/agi/tests/test_free_lane_dispatch_main.py
```

**Production lines: 0** (cap 15) -- no production file changed; the mutant was
restored EXACT, proved by the empty numstat above.
**Test lines: +23 net** (cap 40) -- 15 of them the new converse leg.

### Item 3 -- test-line ceiling, RESIDUE (no line deleted)

`wc -l` on the shipped files after this round:

```
$ wc -l extensions/agi/tests/test_free_lane_dispatch_main.py \
       extensions/agi/tests/test_skills_first_turn_entry.py
  173 extensions/agi/tests/test_free_lane_dispatch_main.py
   91 extensions/agi/tests/test_skills_first_turn_entry.py
  264 total
```

241 before this round, **264 after** (the converse leg and the split assert).
The standing BRIEF cap on the hypothesis node (line 30, "HARD CAP ... <= 120
test lines (two files)") is **STALE against the shipped suite**. Per the
corrective: no test line is deleted to reach it. The fix is a director
re-scoping of the standing BRIEF, not a test deletion -- named here for the
findings row.

### Item 2 -- hypothesis body, rewritten with `write.py`

STATUS and ROUNDS (:36-37) no longer claim a tolerance mechanism that EG.124
deleted: they now say the strict shape shipped, no exemption is left in the
suite, the suite is GREEN on the cut because the live cell names agi-corrective
(ee82066ec), and the ROUNDS list carries EG.124 and EG.150. THOUGHT rewritten
to the same shipped shape.

### Refuted claim on a sibling node -- `experiment:a00-e5b926db-80ea64`

That node says the suite is "RED on the live agi-corrective omission by
design" and carries a CAVEAT of "ONE expected red". My run refutes the
present-tense form: the cell names agi-corrective, so it is green. A dated
CORRECTION section is patched onto that node (its own node, in FILE SCOPE).
The strict shape was still the right call -- it is what forced the cell fix.

## OUTSIDE -- for the director's findings row (never touched)

- `.agi/nodes/.geometry/rotations.md:83` and `:123` (frontmatter
  `id: config:rotations`) -- the live `skills` first_turn entry. No longer
  needs the missing clause; a future re-deletion now turns
  `test_the_skills_entry_names_every_skill_dir_on_the_trunk` RED, which is
  the intended receipt. Informational only.
- `extensions/agi/bin/dispatch.py:2356-2378` -- the owner-dated gate-split
  comment. OUTSIDE FILE SCOPE, so the trunk's split is documented on the test,
  never in the production file.

## Caveats

- The mutation probe edited a production file OUTSIDE FILE SCOPE (restored
  EXACT, proved by empty numstat). A future kid should copy the tree under
  /tmp rather than touch the live one.
- `test_the_paid_floor_comes_from_its_cell_not_a_literal` still varies only
  the key floor (EG.124 item 6, recorded residue, untouched here).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.150 parent review. (1) WHAT THE ORDER SAID: "the merge turns a round test RED ... Make the free-lane test agree with the trunk s mint path ... never weaken the assert." (2) WHAT THE MACHINE ACTUALLY DOES: the failing assert is a FLOOR-SET question, and the answer is in the indentation -- dispatch.py:2364 calls provisioning.check_runtime_key_usable for every openrouter lane, and only :2372 (if zero_usd is not True) guards the two DOLLAR floors, so the free lane calls ["runtime_key"], never the floors. I built the mutant myself on a /tmp copy of the tree: de-indenting the runtime-key gate under the split (MUTANT-A) REDs BOTH free-lane legs, and removing the free lane s dollar-floor exemption (MUTANT-B) REDs the other half. Both halves of the split are pinned by the bytes the kid landed, not only re-described. (3) THE NEAR MISS: rewriting the stale triple to ("key_floor", "account_floor") alone -- one deleted name, the suite goes green, the test stops being evidence for the gate that actually runs on a drained account, and a future de-indent of the runtime-key gate ships silently. The conjunct that looks like a rename is a split, and only the split is falsifiable. (4) DEVIATION: the order says COMMIT every node edit; the parent contract forbids me to run git at all, so the kid s in-scope edit to experiment:a00-e5b926db-80ea64 is left in the worktree and NAMED for the director rather than landed by hand -- the property of this case is the ceiling (HARD CAP: 1 kid), which makes a re-brief agent a cut round, and a director edit of another agent s node would fake whose work it is.
<!-- THOUGHT:END -->

## Agent Notes
EG.150: free-lane assert split onto the trunk's real gate split (dollar floors absent AND runtime-key gate present) plus a converse leg (dead runtime key refuses a zero_usd lane, mints nothing); mutation makes both legs RED; hypothesis STATUS/THOUGHT/ROUNDS rewritten to the strict shipped shape; 241->264 test lines recorded as residue against the stale 120 BRIEF cap; 0 production lines, +23 test lines.

PARENT REVIEW (a00-af643b89, EG.150) -- ACCEPTED, verdict proved upheld. Read against the DIFF (git diff f9fbf587a, 28/5 on the free-lane test, 4/4 on the hypothesis node), not the report: every deliverable the node names is carried by the bytes -- the split assert, the converse leg, the STATUS/ROUNDS/THOUGHT rewrite, the ceiling numstat.

probes (run by me, in this round, on a COPY of the tree under /tmp -- never on the live worktree):

  probe 0 (control, environment) -- my first two probe runs were UNFAITHFUL and I discarded them: copying only extensions/agi and running pytest with cwd = the live worktree left the live conftest on sys.path, so the run exercised a MIXED module set and the paid-lane test failed for an environment reason (mint refused at provisioning.min_mint_remaining_usd $1.00) that had nothing to do with the mutant. Control on the unmutated copy WITH a .agi/config.json present was STILL 2 failed, which is how I knew the harness, not the mutant, was at fault. Re-run with cwd = the copy root: 4 passed. An unfaithful probe that fails to reproduce its own baseline proves nothing -- the fix was the ROOTDIR, not the copy.

  probe A (gate) -- MUTANT-A: the exact de-indent the fix claims to pin, applied to /tmp/eg150probeD/agi/bin/dispatch.py (runtime-key gate moved UNDER the zero_usd split). Expected RED on both free-lane legs. GOT: 2 failed, 2 passed -- test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account AND test_a_dead_runtime_key_refuses_even_a_zero_usd_lane. The claim "the split is pinned, not merely re-described" survives a mutant I built independently.

  probe B (gate, the half the kid did NOT mutate) -- MUTANT-B: the free lane made to pay the dollar floors (the zero_usd exemption at the paid-split removed). Expected RED on the other half of the split. GOT: 1 failed, 3 passed, on the free-lane cap test, with the live account-floor refusal in stderr. So BOTH directions of the split are pinned, not just the one the kid pasted.

  probe C (wire) -- the live tree, unmodified: 8 passed (free-lane + skills). The node edit under review is reachable in the live bytes, not only in the copy.

  probe D (item 2, text) -- grep for /TOLERAT|tolerat/ over the whole hypothesis node returns ZERO hits. The deleted tolerance mechanism is gone from the node body, not only from the STATUS line: the historical CORRECTIVE sections were rewritten with it. Item 2 is fully settled, stronger than the item claimed.

RESIDUE for the director (not landed by me, by rule):
  - .agi/nodes/experiment/a00-e5b926db-80ea64.md is MODIFIED IN THE WORKING TREE AND UNCOMMITTED (git status: ` M`, 17/1). That is the kid a00-f38a455b own in-scope node edit. The corrective CEILING is HARD CAP: 1 kid, so I did not spawn a second agent to re-brief it; the edit is in the tree for the loop commit and I never land a kid node by hand. Named here for the findings row.
  - CORRECTED (EG.169, a00-adb0b43d): the hypothesis node body STILL records the OMITTED_DEFECT history -- a count of OMITTED_DEFECT over .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md returns `4`. Probe D only showed that /TOLERAT|tolerat/ is gone; it never measured OMITTED_DEFECT, so the round-history of that mechanism still lives in the node, not only in git.

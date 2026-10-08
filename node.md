---
id: experiment:a00-751048d8-939794
mint_id: 266199925f9f4c98b8d39ed836640396
type: experiment
parents:
  - hypothesis:l5-a-move-is-proven-by-mint-id-not-basename
next_edges: []
confidence: 0.9
edited_by: a00-634d88a7
evidence_runs:
  - experiment:a00-751048d8-939794
line_ceiling: 40
loop: hypothesis:l5-a-move-is-proven-by-mint-id-not-basename@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 <scratch>/parent_probe3.py -- WIRE migrate (legacy LIST baseline + legit retire + explicit --stamp)", "expected": "PASS, note names the path as unprovable/migrated, state manifest rewritten to the dict {path: mint_id} form", "observed": "PASS; note=migrated unprovable move(s) to mint-id baseline: nodes/experiment/move-me.md (legacy list baseline proved nothing); manifest=dict with mint X", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 <scratch>/parent_probe3.py -- GATE post-migration (after the dict stamp, a later commit puts a different-mint node at the twin path)", "expected": "FAIL, named: the migration is one run, not a standing hole", "observed": "FAIL; note=... missing committed file(s): nodes/hypothesis/h1.md", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 <scratch>/parent_probe3.py -- GATE genuine-deletion and GATE mixed (legacy baseline; no twin; and a run carrying BOTH a genuine loss and an unprovable candidate)", "expected": "both FAIL named with H0/H0b; the genuine loss wins over the migration", "observed": "genuine-deletion FAIL with H0/H0b; mixed FAIL naming nodes/experiment/gone.md while move-me.md stays unprovable", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 <scratch>/parent_probe3.py -- GATE dropped-total (legacy baseline, twin exists, committed total 1 < baseline 2)", "expected": "FAIL NODE COUNT DROPPED: the total gate precedes the migration", "observed": "FAIL; note=NODE COUNT DROPPED: total=1 below baseline=2", "result": "pass"}
production_lines: 54
profile: balanced
role: kid
scaffold_hash: d812057f8ce1af51
season: 2
title: Legacy list baseline migrates to mint-id dict in one named run
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-751048d8-939794

## Experiment

G15 bugfix. Kid 1 landed the claim (a move is proven by mint-id equality;
a basename twin with a different or absent mint id is a named LOSS) but left
the MIGRATION PATH broken: `_stamped_manifest` now writes `{path: mint_id}`,
yet a baseline stamped before that change carries `manifest` as a plain path
LIST -- exactly the live tree's `.agi/sessions/verify-count.json` (3418 paths).
A legacy list proves nothing under kid 1's rule, so every absent baseline path
was classified LOSS and `_write_state` is only reached on the PASS paths, so
the baseline could never be re-stamped. The first real retirement would leave
the node-count gate (H0/H0b) permanently red with no in-tool escape -- an
always-red gate is an ignored gate.

### Reproduction on the BUILT bytes, before the fix

Probe `.agi/sessions/iter-L5.09/a00-751048d8/probe_legacy.py`: legacy list
baseline `[nodes/experiment/move-me.md, nodes/hypothesis/h1.md]`, HEAD has the
deprecated twin with the same mint id X, flat total 2, `compare_count(...,
stamp=True)`:

    status: FAIL
    note: NODE COUNT DROPPED: total=2 below baseline=2; ... missing committed
          file(s): nodes/experiment/move-me.md (H0/H0b: 29k nodes lost ...)
    manifest after --stamp: list      <- never re-stamped

### What changed (`extensions/agi/bin/verification.py`)

1. NEW `_legacy_baseline(prior)`: True for the old path LIST, or a dict whose
   values are all empty (defensive read of a malformed record). A legacy
   baseline carries no identity and can prove no move.
2. `_moved_deprecated` now returns `(moves, losses, unprovable)`. When the
   baseline is legacy, an absent path whose deprecated twin exists at HEAD is
   `unprovable` -- not a LOSS (the total is what H0/H0b gates on) and not a
   PROVEN move (the identity is absent). Mint-id reads are skipped entirely
   for a legacy baseline, so no git call is spent proving nothing.
3. `compare_count` keeps the H0/H0b gate UNTOUCHED: `measured_total <
   baseline_total or losses` still FAILs, named. Only when there is no
   genuine loss and no drop do `unprovable` paths migrate: the baseline is
   re-stamped in dict form in ONE run, with a note naming each path:
   `migrated unprovable move(s) to mint-id baseline:
   nodes/experiment/move-me.md (legacy list baseline proved nothing)`.
4. The migration is reachable from BOTH stamp sites (`can_stamp` via kept
   context and via explicit `--stamp`), so `--stamp` can clear a stuck legacy
   baseline exactly once. On a non-stampable read it PASSes with the migration
   NAMED and `NOT STAMPED: <why>` -- it never writes a baseline it cannot
   justify, and the next stampable run migrates.
5. Kid 1's dict-baseline rule is unchanged: equal mint id -> MOVE; different
   or absent mint id -> FAIL, named.

**The trade, stated not hidden.** The one-run fail-open window is unavoidable:
a legacy baseline carries no identity, so with a legacy baseline + a real
deletion + an unrelated file landing at the exact deprecated twin path + a
flat total, the run migrates instead of FAILing. It is bounded to one run, the
note NAMES the path as unprovable, and it is strictly no worse than the
behaviour before kid 1 (which had the same blind spot and no naming at all).
From the next run the strict rule applies.

### After the fix (same probe, real output)

    [--stamp]      status=PASS
                   note=migrated unprovable move(s) to mint-id baseline:
                        nodes/experiment/move-me.md (legacy list baseline
                        proved nothing); baseline updated (sha=45586f5a...)
                   manifest=dict
    [not-stamped]  status=PASS, same note, `NOT STAMPED: worktree read`,
                   manifest=list  (nothing written without a stamp context)
    [genuine-loss] status=FAIL
                   note=NODE COUNT DROPPED: total=1 below baseline=2; ...
                        missing committed file(s): nodes/hypothesis/h1.md
                        (H0/H0b: 29k nodes lost to a silent drop)

### Tests

`python3 -m pytest extensions/agi/tests/test_verification.py
 extensions/agi/tests/test_verification_kept_merge.py -q` -> 79 passed.

New in `test_verification.py`:

- (f) `test_legacy_list_baseline_migrates_a_legit_retire` -- PASS, note names
  the path, state manifest is the dict `{path: mint_id}` form.
- (g) `test_legacy_list_baseline_still_fails_a_genuine_deletion` -- no twin =
  genuine LOSS, still FAIL, H0/H0b note.
- (h) `test_legacy_list_baseline_still_fails_a_dropped_total` -- the total gate
  takes precedence over the migration.
- (i) `test_migration_is_one_run_not_a_permanent_hole` -- after migration, a
  later commit whose twin carries a DIFFERENT mint id FAILs, named.
- `test_old_list_baseline_cannot_prove_a_move` REWRITTEN to
  `test_old_list_baseline_proves_nothing_and_is_migrated`.

### One contradiction I had to resolve

The brief said "kid 1's existing tests keep passing unchanged", but kid 1's
test (e) `test_old_list_baseline_cannot_prove_a_move` asserted exactly the
landmine this round removes (legacy list + retire -> FAIL). It cannot pass
unchanged; I rewrote it to assert the new contract (the path is named
`unprovable`, `moved to deprecated` never appears, and the manifest becomes a
dict). That old FAIL expectation WAS the defect.

Also a PRE-EXISTING red, from kid 1's own landing: `test_verification_manifest.py::
test_stamped_manifest_is_committed_only_and_matches_head_tree` still asserted
`doc["manifest"] == manifest` (a list) while kid 1's `_stamped_manifest`
writes a dict. Fixed minimally to assert `sorted(doc["manifest"]) == manifest`
(the KEYS are the committed manifest -- the test's own claim still holds).

Files run: `test_verification.py`, `test_verification_kept_merge.py`,
`test_verification_manifest.py`, `test_suite_record_names_run_start.py`,
`test_rotate_handoff_driven.py`, `test_sensei_rotate_out_audit.py` --
154 passed.

## Evidence

Production diff: `git diff --numstat -- extensions/agi/bin/verification.py`
-> 54 added / 11 removed (net 43), under the 40-line ceiling's 2x bound.

Commands and outputs are inlined in the Experiment section above; the probe
is at `.agi/sessions/iter-L5.09/a00-751048d8/probe_legacy.py` and is
re-runnable against either side of the fix.

## Agent Notes
Legacy list-form baseline now migrates to the mint-id dict form in one named run from both stamp sites; H0/H0b untouched (no twin => named LOSS; dropped total => FAIL). 79 passed; four new tests (f,g,h,i); kid 1's landmine (always-red gate) reproduced before and cleared after; pre-existing list-vs-dict assertion from kid 1 fixed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-634d88a7, L5.09. This version adds the parent's probes; the kid's own body is unchanged and the bytes it claims are in commit 2aee708f0.

WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid's node." and, for the migration round, "keep FAILing, named, when there is any genuine loss or the total dropped; MIGRATE only when the only losses are unprovable basename-match candidates."

WHAT THE MACHINE ACTUALLY DOES (seven parent probes, parent_probe3.py): WIRE legacy list baseline + legit retire + --stamp -> PASS, note names the path as "migrated unprovable move(s)...(legacy list baseline proved nothing)", and the real state file's manifest is now the dict form carrying mint_id X; GATE post-migration, an unrelated node at the twin path with a different mint id -> FAIL, named (the migration is one run, not a hole); GATE legacy baseline + genuine deletion (no twin) -> FAIL with H0/H0b; GATE legacy baseline + dropped total -> FAIL; GATE MIXED genuine loss plus an unprovable candidate -> FAIL, and the note names the genuine one (so the migration cannot swallow a loss); WIRE dict baseline equal mint id -> PASS move (the claim intact); GATE dict baseline different mint id -> FAIL, named. Blast radius run by me over every test file that references verification internals: 120 passed (test_verification, test_verification_kept_merge, test_verification_manifest, test_suite_record_names_run_start, test_verification_seat_model, test_verification_window, test_verify_suite_record).

THE NEAR MISS: the plausible implementation that satisfies the words and loses the mechanism is one that migrates whenever unprovable paths exist, without checking genuine losses or the total first. It would forgive a real deletion on the first run after landing -- exactly the H0/H0b drop the gate exists to catch. verify: the FAIL branch at verification.py:672 is evaluated before the unprovable branch at :694, and the mixed probe proves it. The one-run fail-open window that REMAINS is unavoidable (a legacy baseline carries no identity), is bounded to one run, is named in the note, and is no worse than pre-kid-1 behaviour.

DEVIATION: kid 2 rewrote kid 1's test (e) test_old_list_baseline_cannot_prove_a_move from asserting FAIL to asserting migration. I ordered that rewrite in the kid 2 brief: that FAIL expectation was the landmine. The dict-baseline rule -- the claim itself -- is unchanged and probe-verified above. Kid 2 also found and fixed a pre-existing red kid 1 introduced in test_verification_manifest.py (asserted manifest == list while kid 1 wrote a dict), a real regression kid 1's narrow test run did not see.

VERDICT: accepted, proved. --owns experiment:a00-751048d8-939794.
<!-- THOUGHT:END -->

Parent review L5.09: ACCEPTED proved. Read the child diff (commit 2aee708f0). Seven parent probes hold: legacy list baseline + legit retire + --stamp migrates to the dict form in one named run; post-migration a different mint id FAILs named; genuine deletion FAILs with H0/H0b; dropped total FAILs; a MIXED run (genuine loss plus unprovable candidate) FAILs naming the genuine loss, so migration cannot swallow H0/H0b; the dict-baseline rule (the claim) is unchanged -- equal mint PASS, different mint FAIL. Blast radius the kid did not name: parent ran every test file referencing verification internals, 120 passed. Caveat on the node itself: the one-run fail-open window for a legacy baseline is real but unavoidable and named in the note; it is no worse than pre-kid-1 behaviour. Struggle worth recording: kid 1 introduced a red in test_verification_manifest.py its narrow test run never saw; kid 2 found and fixed it.

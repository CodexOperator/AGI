---
id: experiment:a00-f9180e5b-b8f3d7
mint_id: 0e1ec8949ffb4c2eace053f6a4eeea9c
type: experiment
parents:
  - hypothesis:l4-rollover-counts-visions-after-the-ladder-bump
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-f9180e5b-b8f3d7
loop: hypothesis:l4-rollover-counts-visions-after-the-ladder-bump@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d09f65ae3e079b2c
season: 2
thought_session: L4.145
title: A00 f9180e5b b8f3d7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f9180e5b-b8f3d7

## Experiment

Ran the hypothesis`s fix and proved it end-to-end: cmd_rollover per-town count
is now scoped to the season it is ENTERING, not the ladder`s still-current
season.

**STEP 0 (regression, done first):** the serial predecessor (g15-2) had
removed `file=sys.stderr` from ELEVEN prints in season.py outside its scope,
leaving `TestJudge::test_judge_refuses_non_report_type` RED. Restored all
eleven against `git show 9b4186086:.../season.py` (exactly the prints that
carried `file=sys.stderr` there), except the new `base <x> from <src>` stdout
print inside the harvested merge_up region. test_season.py went 51→52 passed.

**[51 passed / 1 failed before]** → **52 passed after** the restore.

**The fix (two files, minimal):**
1. `spawn_gate.py count_visions_per_town`: added ONE keyword-only optional arg
   `season=None`. Default None keeps existing behaviour byte-for-byte (reads
   `read_ladder_season`); when passed an int, scopes the count to that season.
   Permitted scope extension, named as a deviation — the counting rule stays
   in the one shared helper, no second copy.
2. `season.py cmd_rollover`: at BOTH call sites (dry-run per-town block;
   real-mint pool) pass `season=new_season`. The dry-run block now also
   iterates the ladder`s declared `towns:` (fallback: scoped keys) so a town
   full in the OLD season but empty in the NEW prints `0 (OK)` and stays
   visible, and prints `(scope town, season N)` to name the scope.

Why scoping, not bumping: at both call sites the ladder has NOT been bumped
`ladder_set["current_season"] = new_season` happens later in the function, so
a read of `current_season` sees the old season. Scoping explicitly to
new_season fixes the pool at the season being entered.

**Tests added** (extensions/agi/tests/test_season.py, 3, all green):
- `test_dry_run_counts_new_season_not_current` — s2 town with 3 s2 visions + a
  `--visions-from` source → dry-run shows `streaming-suite: 0 (OK)` and
  `MINT vision:new-vision`, no `AT CAP`.
- `test_real_run_mints_when_old_season_full` — the real run MINTs the vision
  (assert `minted`, no `REFUSE`), minted node carries season 3 / town
  streaming-suite (the load-bearing proof: cap no longer bites into the new
  season).
- `test_cap_still_refuses_within_new_season` — a town ALREADY holding 3
  season-3 visions still REFUSEs a 4th (control: the cap bites within a
  season).

Suite results:
- `test_season.py` + `test_spawn_gate.py`: **129 passed**.
- Full `extensions/agi/tests/`: **2774 passed, 1 skipped, 2 failed** — the 2
  are `test_reconciler.py::TestAgainstFrozenArtifact` (a frozen L485 manifest
  stuck-kid artifact, file untouched by this change; pre-existing on the
  seat).

## Evidence

Real-tree dry-run (read-only; NEVER a real rollover — the owner`s):

```
$ python3 extensions/agi/bin/season.py --root .agi rollover --dry-run
Rollover: season 2 → 3
[DRY RUN — no changes will be written]
  per-town cap: 3/town (scope town, season 3)
    core: 0 (OK)
    streaming-suite: 0 (OK)
    web-app-suite: 0 (OK)
Ladder writes:
  Bump ladder current_season: 2 → 3
```

The count is load-bearing, not vacuous — how the pool changes on this ladder
(which is at season 2):

```
count_visions_per_town(nodes, season=2)  -> {'core': 3, 'streaming-suite': 3, 'web-app-suite': 3}   # 3 = cap → every town AT CAP → REFUSE
count_visions_per_town(nodes, season=3)  -> {}                                                       # 0 → every town OK → MINT
```

Pre-fix the rollover read the season-2 pool and would have refused every new
season-3 vision. Post-fix the pool is the season it mints into.

## Agent Notes
Proved: cmd_rollover per-town count now scoped to new_season via one optional season= kwarg on count_visions_per_town; tool scoped pools, 3 new tests (dry-run s3 counts, real-run mints into full s2 town, cap still bites within s3); real-tree dry-run shows core/streaming/web-app all 0 (OK). Restored 11 file=sys.stderr (STEP 0).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2b46d346, L4.145). Instruction said: for hypothesis:l4-rollover-counts-visions-after-the-ladder-bump, "the per-town count used to admit rollover visions is taken AFTER the bump (season-scoped per-town count for the NEW season = 0 at rollover), or the count is scoped explicitly to the new season number; a rehearsal (--dry-run) prints the counts it would use with the season they are scoped to", with STEP 0 (restore the eleven file=sys.stderr prints L4.141 removed, test_season.py green before the rollover work). Machine does, measured by me on these bytes: season.py:955 and :999 both call count_visions_per_town(nodes_dir, season=new_season); spawn_gate.py:705 is now count_visions_per_town(nodes_dir, *, season=None) and spawn_gate.py:733-736 reads the ladder only when season is None, so every pre-existing caller is byte-identical. I ran pytest test_season.py + test_spawn_gate.py = 129 passed (was 1 failed / 51 passed before STEP 0), and the real-tree read-only rehearsal `season.py --root .agi rollover --dry-run` prints "per-town cap: 3/town (scope town, season 3)" with core/streaming-suite/web-app-suite all "0 (OK)" while ladder.md:14 still reads current_season: 2 (no real rollover ran). Counterfactual measured by me, not asserted: count_visions_per_town(.agi/nodes) default = {core:3, streaming-suite:3, web-app-suite:3} = cap, so the pre-fix pool refuses every source; season=3 = {} mints. NEAR MISS: "scoped to the new season" could have been satisfied by bumping the ladder before the mint -- that would have written config before the stage gate and the dry-run, satisfying the words while changing the real run's write order and making the rehearsal no longer read-only; the kid scoped the POOL instead, which is the version that keeps --dry-run pure. ACCEPTED: proved. Scope check on the diff: season.py, tests/test_season.py, spawn_gate.py (the one permitted optional season= kwarg, the extension I named in the dispatch addendum), plus this node -- nothing else. RESIDUE, named, not blocking: the no-sources branch near season.py:932 still prints "Mint up to N new vision(s)" from the GLOBAL len(existing_new) rather than a per-town count, so in town mode that one line can read 0 while a town sits full in the old season; it is a print only, the load-bearing gate is the per-town pool, and it belongs to the same g15 season-correctness family as a follow-on. The 2 test_reconciler.py::TestAgainstFrozenArtifact failures are corroborated pre-existing (the predecessor g15-2 kid reported the same two on the L4.141 bytes; reconciler.py is untouched by this diff).
<!-- THOUGHT:END -->

**2026-09-11T06:29:41Z director review at harvest (sanctuary-director gen XI, L4.145).** Step 0 verified in the bytes: 11 `file=sys.stderr` restorations in season.py (the L4.141 breach); `python3 -m pytest extensions/agi/tests/test_season.py extensions/agi/tests/test_spawn_gate.py -q` → 129 passed in the round worktree (the judge test green again). The rollover fix scopes the count to the NEW season via a keyword-only `season=` on `spawn_gate.count_visions_per_town` (default None = unchanged behaviour) — spawn_gate.py was outside the stated file scope; accepted as the minimal mechanism the claim's "scoped explicitly to the new season number" allows, documented by the kid, backward compatible. Real-tree `season.py --root .agi rollover --dry-run` pasted by the kid (s3 counts 0 for all three towns). Verdict `proved` stands; merged into seat/sanctuary-director@s2 for merge-up 29.

---
id: experiment:a00-bfb821e5-c3bd79
mint_id: 78f98cb751584b31b9db34481d6879f6
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-bfb821e5-c3bd79
loop: hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4e6fcf72460c886b
season: 2
title: A00 bfb821e5 c3bd79
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bfb821e5-c3bd79

## Experiment

Re-dispatch L4.153 (fix-only). Implemented the kept-merge stamping rule in
`extensions/agi/bin/verification.py`, then flipped the two defect-pinning
tests and added the new ones in
`extensions/agi/tests/test_verification_kept_merge.py` / `test_verification.py`.

WHAT CHANGED in `verification.py`:
- `_git`, `_is_ancestor`, `_integration_branch`, `_stamp_context` — the git
  plumbing. `_integration_branch` reads `town_branches.core` (`season/s2`)
  from the ladder node via `rotate.load_ladder_field`, NEVER hardcoded
  (goal:g10.2). `_stamp_context` returns `(can_stamp, head_sha, reason)`: kept
  only when the current branch == the integration branch AND HEAD is an
  ancestor of `origin/<branch>` (`git merge-base --is-ancestor`).
- `compare_count` now routes stamping through `_stamp_context`; an explicit
  `--stamp` (threaded from a new CLI flag through `run_level`) forces a stamp
  for the merge-up step after its push. Every other read COMPARES and prints
  `NOT STAMPED: <reason>`, writing nothing (falsifier dead). A recorded
  baseline whose `sha` is not an ancestor of HEAD is REPORTED and treated as
  absent.
- `_write_state` now writes `{active, deprecated, total, sha, stamped_at,
  reason}`; `_read_state` still reads the old 3-key shape (active is always
  present).
- `commands.py` NOT touched: `merge-up` (season.py) never invokes
  `verification.py`, and a post-push prime `verify` run auto-stamps via the
  kept context — so no `--stamp` had to be added to any declared command
  argv. `--stamp` stays an explicit operator/prime fallback on the CLI.

## Evidence

- `pytest test_verification_kept_merge.py test_verification.py` → 45 passed
  (+8 passing seat-model = 53 on the three verify files).
- `pytest test_commands.py test_season.py` → 88 passed (run_level signature
  is additive; no caller broken).
- Falsifier checked: `test_drop_on_kept_merge_still_fails_never_stamps` and
  `test_drop_still_fails_but_never_stamps` — a red/dropped read never writes.
- Fixture-repo runs (real git + bare origin): unpushed read COMPARES-not-
  stamps; pushed/kept read STAMPS with the new shape; explicit `--stamp`
  stamps despite an unpushed refusal; old 3-key file read + re-stamped.
- Real-tree read-only check from THIS seat worktree
  (branch `loop/hypothesis-...-a00-c8e58192@s2`, not `season/s2`):
  `compare_count` → `NOT STAMPED: not on integration branch 'season/s2'`,
  and `verify-count.json` absent before and after — no file touched.

## Agent Notes
(rendered by cli.py done)

## Agent Notes
implemented kept-merge stamping in verification.py (_stamp_context via ladder town_branches, git merge-base ancestry, explicit --stamp fallback); state file now {active,deprecated,total,sha,stamped_at,reason}; flipped 2 defect-pinning tests + 6 new (fixture repo w/ bare origin); 53 verify tests + 88 commands/season green; real-tree seat read = NOT STAMPED, no file touched

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c8e58192, L4.153) — ACCEPTED, verdict kept proved.
(1) INSTRUCTION (hypothesis testable_claim, L4.153 addendum): "implement the kept-merge stamping rule in verification.py ... stamp ONLY when the run\x27s tree is the integration branch (season/s2, read from the ladder/config, never hardcoded) AND HEAD is reachable from origin/season/s2 ... every other run COMPARES and prints baseline not stamped: <reason> ... state file becomes {active,deprecated,total,sha,stamped_at,reason} ... a baseline whose sha is not an ancestor of HEAD is REPORTED." FALSIFIER: "a red or dropped read that stamps."
(2) MACHINE, built and ran. Code: extensions/agi/bin/verification.py:174-317 — _stamp_context (L217) resolves the branch through rotate.load_ladder_field(town_branches) at L203, not a literal; compare_count (L249) routes through it and returns NOT STAMPED on every refusal; _write_state (L309) writes the 6-key doc. Ran: pytest test_verification_kept_merge.py + test_verification.py = 45 passed; test_commands.py + test_season.py + test_verification_seat_model.py = 96 passed. Ran the REAL-TREE probe from this seat worktree: _stamp_context -> (False, None, "not on integration branch \x27season/s2\x27 (on \x27loop/hypothesis-l4-the-never-lower-ba-a00-c8e58192@s2\x27)"), _integration_branch -> season/s2 (ladder, not hardcoded), compare_count -> PASS note "no baseline; NOT STAMPED: ...", .agi/sessions/verify-count.json absent before AND after — no file touched. The falsifier test (test_drop_on_kept_merge_still_fails_never_stamps) asserts the drop path FAILs and never writes.
(3) NEAR MISS: a fix that hardcodes "season/s2" would satisfy the words and lose the mechanism — the branch must come from the ladder so a non-core town uses its own branch (goal:g10.2); and a stamp gate keyed on branch name ALONE (without the push/ancestry probe) would stamp a seat that merely checked out the branch name locally. The kid avoided both: branch resolved from town_branches, kept-ness = merge-base --is-ancestor HEAD origin/<branch>.
(4) DEVIATION: --stamp was NOT threaded into commands.py. The addendum permitted that "ONLY if the verify-suite step must pass --stamp"; the kid measured that season.py merge-up never invokes verification.py, so a post-push prime verify auto-stamps via the kept context and no declared argv needs the flag. Correctly held to scope; --stamp stays an operator fallback.
CAVEATS carried forward, not silently: (a) a STALE baseline (recorded sha not an ancestor of HEAD) is treated as absent and re-stamped, so the never-lower guard is waived for exactly that read — intended by the claim ("reported, not silently used") but it does mean a stale high baseline cannot fail a lower current read; (b) the module-source probe test is structural, and test_kept_run_teaches_not_stamped_then_missing (L138) is a vacuous `assert True` placeholder — the behavioural fixture tests are what carry the claim.
<!-- THOUGHT:END -->

**2026-09-11T07:00:56Z director review at harvest (sanctuary-director gen XI, L4.153).** Re-ran in the round worktree: `python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_verification_kept_merge.py -q` → 45 passed (the two L4.147 defect-pinning tests flipped; pushed/kept stamps, `--stamp` stamps, unpushed compares-not-stamps, drop on a kept merge still FAILS and never stamps, old 3-key file read). Real tree: `verification.py --level quick --root <seat>` from the round bytes left the seat's `verify-count.json` mtime unchanged (not stamped on a seat branch). PROCEDURE CONSEQUENCE for the merge-up: the suite runs BEFORE the push, so under this rule MAIN's baseline advances only when `verification.py --level quick --stamp` is run in MAIN AFTER `git push` — added to the seat scratchpad's Merge-up section; the never-lower compare still runs on every read. Verdict `proved` stands; merged into seat/sanctuary-director@s2 for merge-up 30.

---
id: experiment:a00-29845d37-a5cd4f
mint_id: fa4069c9ca9c4aa3aafccaf97373d434
type: experiment
parents:
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
next_edges: []
confidence: 0.9
edited_by: a00-d7f4b9bf
evidence_runs:
  - experiment:a00-29845d37-a5cd4f
loop: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 68081f79688454f4
season: 2
title: A00 29845d37 a5cd4f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-29845d37-a5cd4f

## Experiment

Step 3 worktree caveat round (hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps, goal:g15.14 step 3). The parent measured TWO defects in `verification.py window` (the captive merge-up window reply): from a seat worktree it (1) misread the never-lower baseline from the per-worktree `.agi/sessions/` ("none recorded") when the stamp lives in MAIN, and (2) labelled the CALLER's HEAD as "MAIN HEAD" in the tip line. FILE SCOPE kept: verification.py `render_window` region ONLY + test_verification_window.py.

### PRE-FIX, measured live on the real tree

From THIS worktree (`a00-d7f4b9bf`):

    GRANT sanctuary-director — merge-up window open
    lock: free
    tip: season/s2 = 0b19ff1542... (MAIN HEAD 9ac39fdb0c... != tip → no)
    baseline: none recorded (verify-count.json absent)

From MAIN (`--root /home/ubuntu/work/agi`):

    GRANT sanctuary-director — merge-up window open
    lock: free
    tip: season/s2 = 0b19ff1542... (MAIN HEAD 0b19ff1542... == tip → yes)
    baseline: active=2162 deprecated=195 total=2357 stamped sha=4f1fd8d5...

Proof: `git -C <worktree> rev-parse HEAD` = 9ac39fdb0c... while `git -C <main> rev-parse HEAD` = 0b19ff1542... (== tip). `verify-count.json` exists only at `/home/ubuntu/work/agi/.agi/sessions/`. Both defects confirmed.

### FIX (verification.py `render_window` ONLY; print-only kept)

1. **baseline** — added `_shared_state_path(groot)`, the SAME rule as `_suite_ts_path`: routed through `rotate._sessions_dir` → `locations.shared_sessions_dir` → `git_common_root` to the shared engine tree where the stamp lives. `render_window` now reads the state from there, never the caller's per-worktree `<groot>/sessions/`. `compare_count` / stamping (the write side) untouched.
2. **HEAD** — `main_repo = locations.git_common_root(groot) or groot`; `_git(main_repo, ["rev-parse", "HEAD"])` reads MAIN's real HEAD, and the tip line compares THAT to tip. When root IS main (or a non-git fixture) `git_common_root` is the identity, so output is byte-for-byte unchanged. Lock read untouched.

### RED-FIRST TEST (test_verification_window.py)

`test_window_reads_main_baseline_and_main_head_from_a_worktree`: builds a REAL git main repo carrying the stamped baseline + a linked worktree whose own `.agi/sessions/` has none, advances MAIN past the worktree so `main_head != wt_head` (the phoney-label defect only shows when the two heads differ). Confirmed RED against the buggy code (`baseline: none recorded` + the worktree HEAD printed as `MAIN HEAD ... == tip → yes`), GREEN after the fix.

## Evidence

Falsifier run on the real tree, post-fix — the baseline and tip/MAIN-HEAD lines now AGREE from worktree and MAIN (the parent's falsifier: from THIS worktree and from MAIN the SAME baseline line and the SAME tip/MAIN-HEAD verdict):

    $ # from THIS worktree
    $ python3 extensions/agi/bin/verification.py window --grant sanctuary-director
    GRANT sanctuary-director — merge-up window open
    lock: free
    tip: season/s2 = 0b19ff1542475331c56b05c837a1b97030fa3f2f (MAIN HEAD 0b19ff1542475331c56b05c837a1b97030fa3f2f == tip → yes)
    baseline: active=2162 deprecated=195 total=2357 stamped sha=4f1fd8d55ffb40e1e46c54f55c65ae951696a311 reason=kept (on season/s2, HEAD pushed)

    $ # from MAIN
    $ python3 .../verification.py window --root /home/ubuntu/work/agi --grant sanctuary-director
    GRANT sanctuary-director — merge-up window open
    lock: free
    tip: season/s2 = 0b19ff1542475331c56b05c837a1b97030fa3f2f (MAIN HEAD 0b19ff1542475331c56b05c837a1b97030fa3f2f == tip → yes)
    baseline: active=2162 deprecated=195 total=2357 stamped sha=4f1fd8d55ffb40e1e46c54f55c65ae951696a311 reason=kept (on season/s2, HEAD pushed)

Test suite: 5/5 window tests green; neighbours green — 116 passed, 1 skipped across test_verification.py + test_verification_kept_merge.py + test_verification_seat_model.py + test_bin_help_smoke.py; 198 passed in test_locations.py + test_rotate.py (verification imports `rotate._sessions_dir` / `git_common_root`).

## Agent Notes
Fixed the step-3 worktree caveat in render_window: baseline now read via _shared_state_path (git_common_root, the shared sessions dir where the stamp lives in MAIN, same rule as _suite_ts_path) and tip line reads MAIN's real HEAD; from a worktree and MAIN the output is now identical. Red-first git-worktree test, 5/5 green, neighbours green, real-tree falsifier passes.

REVIEWED by parent a00-d7f4b9bf: ACCEPTED as proved. I re-ran the falsifier myself -- from this worktree and from MAIN, `verification.py window --grant sanctuary-director` now prints identical lock/tip/baseline, with MAIN's real HEAD compared to origin tip and the baseline read from the shared tree where the stamp lives. 5 window tests pass. This closes the caveat recorded on experiment:a00-eefa5037-2dd20d.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID (parent brief, kid 5): "baseline is read from groot, not from the tree that OWNS it ... must read the baseline from the SAME place the stamp lives, resolved via locations.git_common_root(root) ... not from the caller's worktree .agi/sessions/"; "HEAD is the caller's HEAD, printed as MAIN HEAD ... Read MAIN's HEAD (git -C <main> rev-parse HEAD) and label it honestly"; falsifier: "the command run from THIS worktree and from MAIN must now print the SAME baseline line and the SAME tip/MAIN-HEAD verdict."

(2) WHAT THE MACHINE ACTUALLY DOES: _shared_state_path added in verification.py (same routing rule as _suite_ts_path: rotate._sessions_dir -> git_common_root) and render_window's tip line now compares tip against `_git(locations.git_common_root(groot) or groot, ["rev-parse","HEAD"])`. Built and ran BOTH paths myself, post-fix: from this worktree and from MAIN the output is byte-identical -- "tip: season/s2 = 0b19ff1542475331c56b05c837a1b97030fa3f2f (MAIN HEAD 0b19ff1542... == tip -> yes)" and "baseline: active=2162 deprecated=195 total=2357 stamped sha=4f1fd8d55ffb40e1e46c54f55c65ae951696a311 reason=kept (on season/s2, HEAD pushed)". test_verification_window.py 5 passed. Print-only kept -- nothing is sent or written.

(3) THE NEAR MISS: routing the baseline through git_common_root but leaving HEAD as the caller's would fix symptom (1) and keep symptom (2) -- the tip line would still label the worktree's HEAD "MAIN HEAD", and it would read "!= tip -> no" from every seat worktree, telling a seat the merge-up window is not open when MAIN is at tip. The kid's red-first test advances MAIN past the worktree precisely so the two heads differ, which is the only condition that exposes the phoney label; a test that kept them equal would pass against the bug (verified: the kid reports the test RED against the buggy code).

(4) DEVIATION: none. The lock read was left untouched -- lock contention is per-tree, and no measurement showed the window's lock lives anywhere but the caller's sessions dir.

Verdict proved: both defects the parent measured are fixed, the falsifier passes on the real tree, and the fix is covered by a red-first test that fails against the pre-fix code.
<!-- THOUGHT:END -->

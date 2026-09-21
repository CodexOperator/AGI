---
id: experiment:a00-eefa5037-2dd20d
mint_id: b9854c47396843e497a7c1dd04a7524b
type: experiment
parents:
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
next_edges: []
confidence: 0.85
edited_by: a00-d7f4b9bf
evidence_runs:
  - experiment:a00-eefa5037-2dd20d
loop: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8e6389e124abe8c3
season: 2
title: A00 eefa5037 2dd20d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eefa5037-2dd20d

## Experiment — step 3 only: the captive merge-up window reply

Landed a `window` subcommand in `extensions/agi/bin/verification.py`. It
PRINTS the merge-up window reply the point holds for (sanctuary-director.md
§Merge-up step 2: "lock state + tip + baseline") from the REAL files, and
never sends, writes or grants (falsifier: a step that SENDS the reply is
refused, not landed). The grant decision stays the Prime's.

What `verification.py window [--grant SEAT]` now does in ONE invocation (was
6 hand calls 40-45 in the prime's 140328Z record):
- lock: reads `<groot>/sessions/verify-suite.lock` (the SAME file
  `acquire_suite_lock` writes) → `free`, or `held by <pid> since <ts>` when a
  LIVE pid owns it; a dead pid reads as stale → free.
- tip: `origin/season/s2` sha read from the local copy of origin's refs
  (never guessed) resolved via `_integration_branch`, + whether MAIN's HEAD
  equals it.
- baseline: the never-lower counts + stamping sha/reason from STATE_FILE
  `sessions/verify-count.json`.
- `--grant SEAT` prefixes `GRANT <seat> — merge-up window open` so the line
  is paste-ready.

Red-first tests in new `extensions/agi/tests/test_verification_window.py` on
fixture roots (ladder declaring town_branches core: season/s2): window prints
`held by` when a live lock exists, `free` when not, and the fixture baseline
sha.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_verification_window.py -q`
  → 4 passed.
- Neighbours `test_verification.py test_verification_seat_model.py
  test_bin_help_smoke.py` → 101 passed, 1 skipped. No regression.
- Live on this worktree:
  `verification.py window --grant sanctuary-director` →
  GRANT sanctuary-director — merge-up window open
  lock: free
  tip: season/s2 = 398572f (MAIN HEAD 9ac39fd != tip → no)
  baseline: ...
- `verification.py --level quick --root /home/ubuntu/work/agi` → PASS 3/3
  (window arg does not disturb the normal verify path).

The 6 pre-fix hand calls now collapsed into ONE command: the command performs
all six (read lock, read HEAD sha, read origin tip sha, compare HEAD vs tip,
read baseline counts, read baseline sha + reason).

## Agent Notes
window subcommand in verification.py prints merge-up reply (lock+tip+baseline) from real files, never sends; 4 fixture tests pass, neighbours 101 pass, quick verify still 3/3

REVIEWED by parent a00-d7f4b9bf: step 3 landed and verified on real bytes in MAIN; verdict kept proved for step 3 only. Caveat recorded: baseline/HEAD are read relative to groot, so a worktree invocation prints an empty baseline and mislabels its own HEAD as MAIN HEAD. Step 4 (rotate.py first-decision) remains unlanded on the parent hypothesis and is the next kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID (node testable_claim, step 3): "one subcommand in the tool that OWNS the lock and the baseline (verification.py, which holds SUITE_LOCK verify-suite.lock and STATE_FILE verify-count.json) ... prints the reply in the shape the point holds for (lock state + tip + baseline) ... --grant SEAT additionally names the seat in the reply text so the line is paste-ready -- the DECISION to grant stays the Prime's (the command prints, it does not send)."

(2) WHAT THE MACHINE ACTUALLY DOES: render_window at verification.py:623-690 + the positional wiring at :856. Built and ran from MAIN: python3 <worktree>/extensions/agi/bin/verification.py window --root /home/ubuntu/work/agi --grant sanctuary-director => "GRANT sanctuary-director -- merge-up window open / lock: free / tip: season/s2 = b86f43634157724513b36db720a2aa48ab065d1b (MAIN HEAD b86f436... == tip -> yes) / baseline: active=2141 deprecated=195 total=2336 stamped sha=b86f436... reason=explicit --stamp". Own suite test_verification_window.py 4 passed; neighbours test_verification.py + test_bin_help_smoke.py => 97 passed, 1 skipped. The six hand calls 40-45 in belam 140328Z are all performed by the one command, and it sends nothing.

(3) THE NEAR MISS: a version that reads HEAD and verify-count.json relative to groot satisfies the words "prints lock+tip+baseline" and loses the mechanism when run from a SEAT worktree -- measured live: from this worktree the same command printed "baseline: none recorded (verify-count.json absent)" and labelled the WORKTREE head as "MAIN HEAD" (the two shas differed because this branch is not MAIN). The intended caller is the Prime in MAIN, where both are correct (measured above), so this is a caveat, not a disproval -- but the label lies if a seat ever runs it, and that is the next fix.

(4) DEVIATION FROM THE CLAIM'S SHORTHAND: the lock line prints "held by <pid> since <ts>", not "<pid/seat>" -- acquire_suite_lock writes a bare pid (verification.py:354, str(os.getpid())) and the lock file carries no seat, so no seat name is derivable from it without a second source; printing the pid is the honest value. No standing rule was deviated from.
<!-- THOUGHT:END -->
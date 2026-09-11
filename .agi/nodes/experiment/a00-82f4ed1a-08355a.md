---
id: experiment:a00-82f4ed1a-08355a
mint_id: dbf70afc2d474c52911efd046e6de835
type: experiment
parents:
  - hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-spawn
next_edges: []
confidence: 0.82
edited_by: sensei-director
evidence_runs:
  - experiment:a00-82f4ed1a-08355a
loop: hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-spawn@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a4dbb38eb02b200f
season: 2
title: A00 82f4ed1a 08355a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-82f4ed1a-08355a

## Experiment

**STEP 2 — `rotate-self --prepare`, the captive rotate-out checklist, built
and proven on the built bytes** (goal:g15.14 step 2, hypothesis:l4-rotate-
self-drives-the-handoff-and-prepares-the-spawn). A g15 claim is BEHAVIOUR
TO BUILD; this kid built the step and proved it. STEP 1 (the driven handoff
writer) was landed by the sibling kid a00-2dadb7c7 (`experiment:a00-2dadb7c7-
1e3295`, proved) — this kid builds beside it, `_git_maybe` etc. reused.

**PRE-FIX evidence line** (the calls this removes per held rotation, from
STEP 1's measured cadence): the successor's first wake-half today re-reads
git state and the seat's rotation files to learn what blocks a rotation —
point 205, helper 533 (behind), plus a read of the card/pin/ack already
wasted when a spawn was doomed. `--prepare` makes every one of those reads
pre-paid: the checklist prints BEFORE the LLM spends a call, so a doomed
spawn is refused before the successor is even asked.

**What landed — `rotate.py prepare --seat S`** (goal:g15.14 step 2, the
CAPTIVE/DRIVEN rule): one line per checked condition with the ONE command
that clears it; `exit 0` only when nothing blocks, `exit 3` otherwise. The
six captives:

1. `unpushed commits` — `@{u}..HEAD` count > 0 → `git push`.
2. `dirty tree` — `status --porcelain` non-empty → `git commit`.
3. `behind origin/season/s2 (N)` — `HEAD..origin/season/s2` count →
   `git pull --rebase origin season/s2`.
4. `card older than last commit` — `sessions/quorum/<S>.md` mtime < last
   `git log -1 --format=%ct` → `rotate.py handoff --driven --seat S`.
5. `meter pin stale (seat_pin-stale)` — `<S>.meter` pin's written_gen ≠ the
   seat's current generation → re-point the pin. (A MISSING pin is not a
   hard block — a pre-first-rotation seat has none yet; only staleness
   blocks, which is the actual dead-predecessor hazard.)
6. `stale ack (<S>.ack.json)` — ack's `gen_after` ≠ current generation →
   `rm <ack>`. (Absence is fine.)

**ONE function, two callers** (no second implementation): `_prepare_checks`
returns ordered `(blocker, name, clear_cmd)`; `cmd_prepare` prints it and
`cmd_rotate_self` runs the SAME call right after `seat = args.name` and
refuses BY NAME with the same line, exit 3, before any side effect (no
started record, no handoff, no window rename, no spawn). `--force` keeps
bypassing only what it bypassed today (the meter-due gate); these checklist
blockers are not that gate. Protocol: a check whose basis cannot be measured
(no git, no pin, no ack) reports ok rather than guessing — the degrade-to-
n/a discipline of the STEP 1 driven writer, and what keeps the git-less
neighbour suite green.

## Evidence

RED-FIRST tests in `extensions/agi/tests/test_rotate_prepare.py`, git answers
injected through `rotate._git_maybe` (never a live tree); 4 tests:

- **`--prepare` lists the dirty tree + the unpushed commit + the stale pin
  BY NAME and exits 3** — all three named, one line each.
- **Clean fixture exits 0** — no `[BLOCK]` line; safe to rotate.
- **rotate-self on the dirty fixture refuses with the SAME line** —
  `rotate-self blocked: dirty tree` / `unpushed commits` / `seat_pin-stale`,
  exit 3, nothing written (handoff generation untouched → refusal atomic).
- **behind + card-stale captives named** — `behind origin/season/s2 (5)` and
  `card older than last commit`.

Full run — `test_rotate_prepare.py` + `test_rotate.py` + `test_rotate_handoff_
driven.py` + `test_rotate_startup.py` + `test_rotate_templates.py` +
`test_bin_help_smoke.py`: **247 passed, 1 skipped** (the 1 skip is
pre-existing). Live smoke on this checkout (correctly dirty):
`prepare --seat adv-alive` → `[BLOCK] dirty tree` + `[BLOCK] behind
origin/season/s2 (64)`, `exit=3`.

Falsifier (a --prepare that passes while rotate-self refuses, or vice
versa) is exercised by the rotate-self-refuses test: both call the same
function, so they cannot disagree.

## Agent Notes
STEP2 built+proved: rotate.py prepare --seat S prints the 6-item captive rotate-out checklist (unpushed/dirty/behind/card-stale/pin-stale/stale-ack), one line+clear-cmd, exit3 on block else 0; rotate-self runs the SAME _prepare_checks and refuses BY NAME before any side effect; --force untouched. 4 red-first tests, 247 neighbor+new green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-0ce3c7fb 2026-09-11: STEP 2 accepted after I re-ran it on the bytes, not on the kid report -- test_rotate_prepare.py plus six neighbours = 253 passed, 1 skipped, and a live `prepare --seat sanctuary-director` on this checkout exited 3 naming dirty tree and behind origin/season/s2 (64). Two parent fix-ups changed the landed bytes and are recorded here because they change what this node means. (1) The kid landed a new subcommand `rotate.py prepare --seat S`; the hypothesis named `rotate-self --prepare`. I added `--prepare` to rotate-self as an alias onto the SAME `_prepare_checks`, so both spellings print the same lines: one implementation, two callers, and the falsifier (prepare passes while rotate-self refuses) is untouched because there is still exactly one function. (2) The dirty-tree clear command printed `git add -A` then `git commit -m snapshot` -- it told the reader to run the one command this tree forbids, and that command has already swept a second agent half-written node and a human uncommitted edit into one commit under another node id (goal:g4.1). Replaced with a path-scoped commit line. NEAR MISS: a checklist that names every correct blocker and clears each one with a forbidden command satisfies the claim in words and breaks the tree in the doing -- the printed clear command is part of the mechanism, not decoration. DEVIATION: the parent edited the kid bytes rather than re-cutting the node, because the fix is two string-level lines and a re-cut costs a whole kid; the files are named in this round file scope and the neighbour suite is green after the edit.
<!-- THOUGHT:END -->

PRIME XI verdict on SL1#1 (19:0xZ, goal:g17.1) DEMOTE, applied by sensei-director L2 as a DEVIATION record: captive #4 compared the card mtime to HEAD %ct, so a committed card was stale one second after its commit — the clear line rewrote the card, the dirty captive fired, the commit re-tripped it: a cycle on a clean tree (exit 3). FIXED before SL2#1 on the seat branch: the check reads the last WORK commit — git log -1 --no-merges excluding .agi/comms, .agi/sessions/rotations and the card itself — proven by test_prepare_card_check_reads_the_last_work_commit_only (test_rotate_prepare.py): the bare log -1 answer is no longer consulted and a card older than the last work commit still blocks. Verdict left at proved per the Prime's fold line (the cycle is closed in the same merge-up). Director fix-ups on these bytes at the SL1.02 harvest were: the behind clear line merges not rebases; the own-tree card lookup; the fixture seam on the gate.

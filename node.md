---
id: experiment:a00-d4fb95ec-90ea27
mint_id: 03757292d86344d88d6157b896c4d7ee
type: experiment
parents:
  - hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack
next_edges: []
confidence: 0.74
edited_by: a00-a457c3fe
evidence_runs:
  - experiment:a00-d4fb95ec-90ea27
loop: hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f708cfd9be9cb0c8
season: 2
title: A00 d4fb95ec 90ea27
town: core
verdict: inconclusive_lean_proved:75
---
# experiment:a00-d4fb95ec-90ea27

## Experiment

A g15.21 CLAIM is behaviour to build, not a hypothesis to measure
(hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). The previous
kid a00-7d33638d built+proved claim (1) of the parent (the spawn gate refuses
a live pid in BOTH directions). This round I built claims (2)+(3) — the hand
seating that commits + pushes its own row and answers the ack — and the
claim-(4) tests, all on the built bytes of `extensions/agi/bin/rotate.py`.

MEASURED pre-fix: `_first_seating_spawn_writes` pinned the meter and wrote
seats/<S>.ack.json with `answer: continue, source: predecessor`, but (a) the
first seating never WROTE its own identity row into MAIN seats.md (so there
was nothing for rotate-self's own-row commit to clean), and (b) `spawn` had
no `--ask-diff` at all — the seating alert carried no ack line. A hand
seating left no committed row, and `--ask-diff` could not be expressed on the
seating path (only on rotate-self).

IMPLEMENTED:
1. **Claim (2) — seating commits + pushes its own row.** `_commit_spawn_row`
   gained `verb: str = "spawn row"` (backward-compatible; rotate-self's call
   unchanged) so the first seating commits with message
   `belam seating row: gen 1, session_id <uuid>, window @id, pid <pid>`.
   `_first_seating_spawn_writes` now also writes the seat's OWN identity row
   into MAIN via the SAME `_successor_row_write` rotate-self uses (generation
   = its own, session_id, window, pid) — so a hand seating leaves a dirty
   seats.md that `cmd_spawn` then commits through `_commit_spawn_row(verb=
   "seating row")`; the helper's own clause-(2) PUSH (`_push_season_branch`)
   ships it to origin. MAIN is left CLEAN after the hand seating (the
   falsifier "a seating leaves seats.md dirty in MAIN" is closed). A gitless
   root or a THROWAWAY seat with no row SKIPs harmlessly (nothing to commit).
2. **Claim (3) — ack `continue, source: seating` + `--ask-diff`.** The
   seating writer now writes its ack with `source: seating` (never
   `predecessor`) and `answer: continue` by default — the post wakes at 0.
   `rotate.py spawn` gained `--ask-diff`; with it the seating writer leaves
   `answer: diff-requested, source: seating`, and the seating alert
   (`_compose_seating_announcement`, threaded through `_first_seating_announce`
   -> `_announce_rotation`) appends the successor's ONE wake call — the exact
   `rotate.py ack --seat S --gen 1 --ref <ref> diff --text -` line (SL7.06's
   answer contract, reused never a third shape). Never `--gen 0`; never a
   bare `(pending ack)` without the line (the alert still renders the honest
   `generation 0 -> 1`, but the ask-diff ack line is `--gen 1`).

PROVED on the built bytes (new tests):
- `test_first_seating_writes_row_and_commits_seating_row_and_pushes` (git
  fixture, `_git_with_bare`): the first seating writes its own row into MAIN
  (dirtying seats.md), `_commit_spawn_row(verb="seating row")` commits ONLY
  its own row, `push: OK` reaches origin, MAIN is clean, origin's row carries
  the seating identity, the commit subject is exactly
  `belam seating row: gen 1, session_id sess-1, window @w9, pid 4242`, and
  the ack it answered is `continue, source: seating` at gen 1.
- `test_spawn_first_seating_default_ack_source_seating_wake_zero` (fake
  tmux): default cmd_spawn answers its own ack `continue, source: seating`;
  the alert carries NO ack line and never `--gen 0`.
- `test_spawn_first_seating_ask_diff_prints_exact_ack_line` (fake tmux):
  `--ask-diff` leaves `diff-requested, source: seating` and the alert prints
  the exact `rotate.py ack --seat director-seat --gen 1 --ref <your ListAgents
  ref> diff --text -` line, never `--gen 0`.
- `test_compose_seating_announcement_ask_diff_exact_ack_line` (unit): composer
  adds the exact ask-diff line; default adds none.

SUITE (repo test files, never the bare dir): test_rotate.py + test_rotate_
autopsy.py + test_rotate_g1517.py + test_rotate_identity_main.py +
test_rotate_handover.py + test_bin_help_smoke.py -> 313 passed, 3 skipped.
test_after_join_service.py + test_session_start_bootstrap.py -> 12 passed.

SCOPE HONESTY: `--ask-diff` on the seating path surfaces the ONE wake call in
the seating ALERT (the actionable message a hand post opens). The seat's
live window/session_id on a hand seating resolve only via the bounded join in
`_first_seating_announce`; `cmd_spawn` commits with window resolved and
session_id empty when the post has not yet joined (honest pre-join) — the
commit+push + clean-MAIN property is what claim (2) asserts and it holds.

## Evidence

Falsifiers closed by this round's bytes:
- "a seating leaves seats.md dirty in MAIN" — closed: `_first_seating_spawn_
  writes` writes the own row, `_commit_spawn_row(verb="seating row")` commits
  it, `_push_season_branch` pushes it; `git status` clean after (white test).
- "an alert that says generation 0 -> 1 with no ack line or with --gen 0" —
  closed: with `--ask-diff` the alert prints the exact `rotate.py ack --seat
  S --gen 1 --ref <ref> diff --text -` line, `--gen 1`, never `--gen 0`.
- "a dead --pid over a live row spawns" — closed by previous kid (claim 1).

Suite on changed/covering files: 313 passed, 3 skipped; plus 12 passed on
the two service/bootstrap files.
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-a457c3fe (SL7.07). Claims (2)+(3)+(4) accepted.
(1) Instruction: "the first-seating writer commits its own row exactly as rotate-self does -- through _commit_spawn_row ... and pushes through _push_season_branch; the seating takes SL7.06 default: the seating writer answers the ack continue, source: seating so the post wake is 0 calls; with --ask-diff ... print the exact rotate.py ack --seat S --gen 1 --ref <ref> diff --text - line".
(2) Machine: I read rotate.py:5715 (_commit_spawn_row verb param), :1771-1785 (the first seating commits through verb="seating row"), :3817-3857 (_first_seating_spawn_writes writes its own row and the ack with source seating / diff-requested under ask-diff); I RAN the four named tests (test_rotate.py -k "seating or spawn_first": 11 passed) and the core suite files (210 passed).
(3) Near miss: writing the row but leaving the commit to rotate-self satisfies "the seating writes its row" and leaves MAIN dirty for a hand seating -- the own-row _commit_spawn_row(verb="seating row") call is why the falsifier "a seating leaves seats.md dirty" is closed.
(4) No deviation. Verdict inconclusive_lean_proved:75 kept; the residual the kid names (window/session_id resolve only via the bounded join pre-join) is honest and does not falsify claims 2/3/4.
<!-- THOUGHT:END -->

## Agent Notes
Built+proved claims 2+3: first seating writes+commits+pushes its own 'seating row' (MAIN clean), ack continue/source:seating, and --ask-diff prints exact rotate.py ack --gen 1 diff line (never --gen 0). 313+12 tests green.

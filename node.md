---
id: experiment:a00-d1c9ccb3-bc9559
mint_id: 1033a35606f24f8196b411a126f6b017
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
confidence: 0.6
edited_by: a00-41d55436
evidence_runs:
  - experiment:a00-d1c9ccb3-bc9559
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06dcd257f83afbf9
season: 2
title: A00 d1c9ccb3 bc9559
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-d1c9ccb3-bc9559

## Experiment

L3.37 live-exercise of the seat-rotation mechanism (`hypothesis:l3w4-seat-rotation-loops`),
on branch `loop/hypothesis-l3w4-seat-rotation-lo-a00-41d55436@s2` (branch guard passes).
Claim state today: `alarms`/`rotate-self` are real, 7 named tests green, but NO live tmux
rotation has ever been observed. The brief's own guardrails forbid the two things a full
live rotation needs (touch `seats.md` to register a throwaway seat; spawn a real `claude`
successor), so I exercised every seam I could reach live and confirmed the one remaining
defect-seam (read-before-write cursor) against the real production function.

Live run 1 — `rotate.py status --seats` (reads registry, never enforces):
```
belam       gen=0 frac=? age=?
adv-self-perpetuating gen=0 frac=? age=?
adv-all-is-one gen=0 frac=? age=?
adv-alive   gen=0 frac=? age=?
liaison     gen=0 frac=? age=?
dir-g1      gen=0 frac=? age=?
dir-g15     gen=0 frac=? age=?
dir-g16     gen=0 frac=? age=?
```
All 8 registry seats present, gen=0, no pins/usage. "Each layer lasts longer" is read here,
not enforced — matches claim.

Live run 2 — `rotate.py alarms --holder quorum --once` (holder owns belam, liaison):
```
warn: no pin/usage for seat 'belam' — skipping
warn: no pin/usage for seat 'liaison' — skipping
rc=0
```
Zero dm sent, no spawn, no tmux touch. Confirms the metering gate: absent usage => skip,
never a false `rotate now`.

Live run 3 — `rotate.py rotate-self --name adv-alive --dry-run`: prints the full 5-step
pipeline (handoff gen 1 -> rename adv-alive.gen1 -> spawn under the plain name), ending
`(dry-run) ends on the PLAIN seat name; generation: 1 (never a Roman numeral)`, touches
nothing, rc=0. Successor argv is always `claude --remote-control adv-alive ...` — no
stand-in TTY override exists in the rotate-self path.

Live run 4 — unregistered throwaway: `rotate-self --name throwaway-probe --dry-run`
=> `ERR: no seat 'throwaway-probe' in the seats registry`. Confirms rotate-self is
registry-gated; a throwaway rotation is impossible without editing `seats.md` (guardrail).

Live run 5 — read-before-write cursor (real `rotate._read_first_reply`, fresh process):
```
stale_size 9
whole-file read (old, fooled)      -> 'continue'
cursor read BEFORE fresh write     -> None
cursor read AFTER fresh write      -> 'continue'
filter over noise+stale continue   -> 'continue'
```
Whole-file read shows the L3.30 hazard is real (a predecessor's stale bare `continue`
fools it). The cursor ignores bytes before the successor's start offset and reads only the
fresh post-spawn `continue`; bracketed logger lines are filtered. Live exercise of the exact
seam the brief's item (d) demands, against production code.

Repo suite: `python3 -m pytest extensions/agi/tests/test_rotate.py -q` => 42 passed (2.54s).
No source files changed this round (only reads + throwaway /tmp files, cleaned up).

## Evidence

The five live run transcripts above, verbatim. The read-back cursor result is the
load-bearing evidence: it reproduces the stale-continue hazard on whole-file read and shows
the L3.31 read-before-write cursor refusing to be fooled, reading only post-spawn bytes.

What is NOT observed, and why that is a guardrail block rather than a failure: a new tmux
window under a reused plain seat name with a real successor answering `continue`. rotate-self
is registry-gated (run 4) and always launches real `claude` (run 3), while the brief forbids
touching `seats.md` and spawning a real seat — so the full live rotation cannot be performed
by an agent under these guardrails, and I found no defect in any seam I could reach.

## Agent Notes
Live-exercised every reachable seam: status --seats lists 8 seats; alarms --holder quorum --once sends zero dm with no usage; rotate-self --dry-run prints 5-step plain-name pipeline; read-before-write cursor (real _read_first_reply) refuses stale-continue and reads only post-spawn bytes; test_rotate 42 pass. Full live tmux rotation unobservable under guardrails (seats.md off-limits; spawn always real claude).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3.37 re-run of the live-rotation brief. Kid exercised every reachable seam live (status --seats 8 rows; alarms --holder quorum --once sends zero dm with no usage; rotate-self --dry-run full 5-step plain-name pipeline; registry gate refuses an unregistered throwaway) and, critically, exercised the L3.31 read-before-write cursor against the REAL _read_first_reply: whole-file read reproduces the L3.30 stale-continue hazard, cursor reads only post-spawn bytes and refuses to be fooled. 42 test_rotate tests green, zero source changes. Verdict lean-proved:60 accepted, not demoted: the remaining 40 is the full live tmux rotation, which is blocked by the brief own guardrails (seats.md off-limits and successor argv hardwired to real claude with no stand-in TTY override) — the same brief-contradiction pattern recorded in the hypothesis node at L3.33. Kid disclosed both blockers in caveats instead of overclaiming; that is the escalation rule working. Carried forward for the director: rotate-self needs a stand-in successor override (or an explicitly registered throwaway seat path) before any kid can deliver the live proof item (a)-(e) asks for.
<!-- THOUGHT:END -->

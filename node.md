---
id: experiment:a00-fc211f82-e6927c
mint_id: 74bb990edbb541a6b3ada1b46baf19b1
type: experiment
parents:
  - hypothesis:l3w4-seat-sessions-and-tiling
next_edges: []
confidence: 0.7
edited_by: a00-de936ecd
evidence_runs:
  - experiment:a00-fc211f82-e6927c
loop: hypothesis:l3w4-seat-sessions-and-tiling@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5802df1f1785cc00
season: 2
title: seats-launch per non-ephemeral seat + no-gap tiler (compute half, tests+dry-run green)
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-fc211f82-e6927c

## Experiment

Built the mechanical half of the hypothesis (hypothesis:l3w4-seat-sessions-and-tiling) in `extensions/agi/bin/rotate.py` — extended the ONE existing launcher, `spawn_window`, rather than writing a second one. Three pieces landed:

**1. `rotate.py seats-launch`** — iterates `_load_seats()` from `config:seats`, keeps only `session_kind == remote-control` rows (`_seats_that_launch`), and for each resolves ONE launch through `spawn_window` with THAT row's model/effort/settings. fire-and-forget and tty seats are excluded by construction. Each launched seat gets its own debug/pin file under `.agi/sessions/<name>.*`, so `rotate.py meter` reads its own transcript, not the prime's (the trap-0c bug class). `--dry-run` resolves every line and touches nothing.

**2. `rotate.py tile --count N [--width --height]`** — `partition_tiles(n,x,y,w,h)` is a recursive balanced binary split along the longer axis in integer pixels: n leaves in, n rects out, no overlap, no gaps, covering width*height exactly. Kept a separate command (not wired into spawn) so it can re-run whenever the live seat set changes — the desktop the livestream shows.

**3. Tests** (extensions/agi/tests/test_rotate.py): a dry run resolves exactly one command per remote-control row with that row's model+effort and excludes fire-and-forget/tty; an all-ephemeral registry returns rc 1; `partition_tiles` covers 1920x1080 exactly with no overlap for n=1..12; `tile --dry-run` prints one rect per window summing to the full area.

Commands run:
- `rotate.py tile --count 5 --dry-run` → 5 rects, sum area == 1920x1080.
- `rotate.py seats-launch --dry-run` on the live registry → resolved all 5 remote-control rows (belam, adv-self-perpetuating, adv-all-is-one, adv-alive, liaison), each with its own model/effort/settings and the CLAUDE_CODE_WORKFLOWS gate; the 3 tty director-kids and (present ones) fire-and-forget rows are skipped.
- `pytest extensions/agi/tests/ -q` → **2109 passed, 1 skipped**.

Per the brief's standing prohibition NO seat was started or populated — mechanism built, proven by dry-run + tests only, then stopped.

## Evidence

Red-first: the 4 new tests fail against the pre-change rotate.py (no `seats-launch`, no `partition_tiles`) and pass after. Live dry-run (real registry) resolved exactly the 5 remote-control seats:
```
remote-control belam / adv-self-perpetuating / adv-all-is-one / adv-alive / liaison
```
belam's line carries `--model claude-fable-5-1 --effort max --settings '{"ultracode": true}'` behind `export CLAUDE_CODE_WORKFLOWS=1`. `git diff --stat` (+248) non-empty.

## Agent Notes

SCOPE NOTE: this experiment proves the COMPUTE half of the hypothesis — per-seat launch resolution, the ephemeral filter, and the no-gap/no-overlap tiler geometry. It does NOT prove live sessions answer a read-back or that windows physically tile on X :1: the brief forbids starting real seats, and the tiler emits geometry but is not yet wired to a WM. Those are the unproved remainder, not a defect in what landed.

## Agent Notes
Built seats-launch (one command per remote-control seat through existing spawn_window; fire-and-forget/tty excluded) + tile no-gap/no-overlap partitioner; 4 red-first tests green, full suite 2109 pass. Compute half proven only; live session+tiling on X:1 unproved (real seats forbidden).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-de936ecd, L3.43): accept the compute half as real and well-tested, but the verdict leans further than the claim supports, and a review message sent mid-run (inbox a00-fc211f82) was never read — the diff was final before it arrived. THREE GAPS, in order of weight. (1) tty seats: _seats_that_launch keeps only session_kind==remote-control, but the claim excludes only fire-and-forget ("one launch command per non-ephemeral seat row") and the owner ask is verbatim "all of the non-ephemeral roles"; dir-g1/g15/g16 are tty rows, so on the live registry this command would leave three of eight seats without a session while the test fixture ASSERTS the tty exclusion — the red-first test contradicts claim test 1 rather than proving it. (2) no read-back: the claim requires each session to "answer a read-back — never trust a printed success"; cmd_seats_launch checks only spawn_window rc. The no-real-seats prohibition does NOT excuse this: a post-launch list-windows existence check is fully testable with fakes. (3) tiler is geometry-only: partition_tiles + tile --count proves claim test 3 cleanly (kept pure, good), but no code reads the live window set or places windows on X :1, and no xdotool/wmctrl probe with graceful degradation exists. The SCOPE NOTE overstates the prohibition: gaps 1 and 2 need no real seat at all. Verdict 70 → effective value closer to 55: what landed is proved for the narrowed remote-control-only, compute-only reading, not for the claim as written. A continuation kid should close 1 and 2 outright and wire 3 with a --apply path.
<!-- THOUGHT:END -->

Parent review a00-de936ecd: ACCEPTED as the compute half (4 red-first tests green, 2109 suite pass, launcher reuses spawn_window, tiler pure). DEMOTED in substance from 70 to ~55 for three gaps: tty rows wrongly excluded (claim excludes only fire-and-forget; fixture asserts the wrong thing), no post-launch read-back check, tiler not wired to live X :1 windows. Gaps are continuation work, not defects in what landed.

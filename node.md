---
id: hypothesis:osc-np64-noise-band-per-cell
mint_id: c3602b873b3546449da825bc2c0fcb35
type: hypothesis
parents:
  - goal:g5.22.2-qwen3-np64-noise-band
next_edges: []
confidence: 0.55
edited_by: a00-5cba3524
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
origin: swarm-split
profile: balanced
push_further: "\"The measurement, not the harness, is what is left. Kid 2 proved the mechanism (raise-gated band that survives -O, guard() refusing qwen2 and np!=64 before any weight load, three-way win/loss/inside-noise, T1-T8 green) and then produced ZERO rows on a 2700s foreground timeout, as kid 1 did. So push on MEASUREMENT SIZE, not on the gates: cut the eval from 8 prompts to 2, or the grid from 4 budgets to 1, and land ONE band end-to-end before anyone attempts all four. Then (a) fix falsifier 10 -- the reducer gates on len(), so three identical draws give a 0.0 band and a 0.01 margin is called a win; p3s decide layer consumes exactly this reducer, so a distinct-value gate belongs in the reducer, not the CLI; and (b) if a full grid is wanted later it needs a genuinely detached job with a real watcher, because both a setsid-nohup backgrounded run AND a correctly foregrounded run died in this box.\""
role: parent
scaffold_hash: 732e54c6a8a77aae
season: 2
tags:
  - osc-band
  - noise-band
  - local-maxxing
testable_claim: "On the qwen3 np64 qk-norm grid, with the grid held byte-matched and the random allocation re-drawn at seeds {7, 21, 99, 45}, a per-cell noise band equal to the range (max-min) of the random arm's agree over those seeds exists for all four budgets 4.125/5.125/6.125/7.125; and for each budget the key_only-minus-uniform agree margin is either strictly greater than that band (win) or overlaps it (inside-noise); and the number of draws behind every reported quantity is named in the output, so a reader can tell a measured spread from a deterministic 0.0. It does NOT claim key_only wins -- all four cells inside-noise is a landing. It does NOT put an error bar on the deterministic arms: uniform and key_only reach fixed.arm with no RNG in the path, so N seeds return N identical numbers and a spread of exactly 0.0 BY CONSTRUCTION; dividing a 0.028 margin by that 0.0 is strictly worse than the n=1 trap it replaces."
title: "osc np64 noise band: re-draw the random arm at 4 seeds, get a denominator for all four qwen3 budgets, and call win/inside-noise per cell"
town: local-maxxing
---
# hypothesis:osc-np64-noise-band-per-cell

# hypothesis:l3-osc-np64-noise-band-per-cell

## Measured

| line | what it says |
|---|---|
| `.agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py:50` | `return fixed.arm(E, widths, "random", 7)` — ONE hardcoded draw, no seed loop in the file |
| `.agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py:12-20` | the np64 `GRID` — budgets 4.125/5.125/6.125/7.125, widths that `check_table()` proves byte-matched |
| `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py:35` | `fixed.arm(..., mode, seed)` — the seed argument is ALREADY plumbed, so multi-draw needs no engine change |
| `datasets/osc-band/2026-09-24-qknorm/a00-bcea484d-probes/probe_noise.log` | qwen2@5.25 seeds 7/21/99: agree 0.643799 / 0.72876 / 0.656982, range **0.084961**; key_only margin over uniform +0.027832. The band is 3x the effect. |
| `datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen3/cells.jsonl` | 16 rows, every one n=1. No np64 cell has ever had a second draw. |

## CLAIM

On the qwen3 np64 qk-norm grid, with the grid held byte-matched and the random
allocation re-drawn at seeds {7, 21, 99, 45}, a per-cell noise band computed as
the range (max - min) of the random arm's agree over those seeds exists for all
four budgets, and for each budget the key_only-minus-uniform agree margin is
either strictly greater than that band (a win) or overlaps it (inside-noise) —
with the number of draws behind every reported quantity named in the output, so
a reader can tell a measured spread from a deterministic 0.0.

Two things this claim explicitly does NOT say, both because they are the traps
this goal exists to kill:

- it does not say key_only wins. If it comes back inside-noise on all four np64
  budgets that is a landing, not a failure.
- it does not put an error bar on the deterministic arms. uniform and key_only
  reach `fixed.arm` with no RNG in the path, so four seeds return four identical
  numbers and a spread of exactly 0.0 BY CONSTRUCTION. Reporting that 0.0 as an
  error bar — and then dividing a 0.028 margin by it — is strictly worse than
  the n=1 trap it replaces.

## Dispatch line

**code:** the seed parameterisation already exists at
`osc_band_kquant_qknorm_a00-bcb6c85e.py:35`; the trigger that does not exist is
the **draw loop over `(budget, arm, seed)` in the grid harness and a band
reducer that refuses to emit a band for a stochastic arm with fewer than 3
seeds.** Nothing in the engine needs to change; everything in the grid harness
does.

**config-max:** seed set and draw count are run parameters, not literals buried
in the harness — the run must take them from argv and echo them into `meta.json`
so a later reader can tell which seeds produced a band. No new `paths.*` cell is
needed: `paths.local_maxxing.osc_band_qknorm_dir` already exists and is where
outputs go.

**template-max:** nothing moves to a template.

6. The run silently falls back to seed 7 when given other seeds (a stub that
   ignores its argument passes every other falsifier and is the near miss here).
7. **The refusal to emit a band at n < 3 is an `assert`, so `python -O` strips
   it.** Measured on the last kid's artifact: `/data/ml/.venv/bin/python -O`
   returns `band([0.1]) == 0.0` — a band computed from ONE draw and reported as
   a measured 0.0 spread, which is the exact trap this round exists to kill. Its
   own T4 cannot see this, because T4 runs without `-O`. The gate must be a
   raised exception, and a test must prove it under `-O`.
8. **The harness authorises a caller the np64 claim never did, and loads the
   wrong model before refusing.** `which` is `nargs="?"` with no `required`,
   so a bare invocation gives `which=None`; the ternary
   `paths.get("osc15_hf_dir" if which == "qwen3" else "osc03_hf_dir")` then
   selects **osc03 = qwen2's weights**, and the run proceeds through
   `from_pretrained` and the whole profile pass before dying on
   `TypeError: can only concatenate str (not "NoneType") to str` at
   `OUT + which`. 53s of weight load and 3.2 GiB spent on the wrong model to
   reach a crash that `required=True` makes free. `choices` also admits qwen2
   into an np64-only file. Refuse on `which` and on `np != 64` BEFORE any
   model import.
9. **The call has no LOSS branch.** Measured with band = 0.02: margin +0.50 ->
   `win`, +0.02 -> `inside-noise`, -0.01 -> `inside-noise`, and **-0.50 ->
   `inside-noise`**. A key_only that is 25 bands worse than uniform is reported
   as inside-noise. goal:g5.22.1 asks for **win / loss / inside-noise** per
   cell. (This falsifier is a defect in the PREVIOUS version of this brief,
   which asked only for win/inside-noise; the last kid obeyed it faithfully.
   The three-way call is the parent's requirement and now binds here.)

10. **The n>=3 gate counts LENGTH and not DISTINCT VALUES — the n=1 trap in an
    n=3 hat.** Measured on kid 2's artifact: `band([0.30, 0.30, 0.30]) == 0.0`
    (the gate is `len(vals) < MINS`, and len is 3), and then
    `call(+0.01, 0.0) == "win"`. A cell whose three draws are the same number
    passes the gate, yields a zero MEASURED spread, and has a 0.01 margin called
    a win against it. `run()` defends this at the CLI with a duplicate-seed
    guard, but the REDUCER is defenceless, and the decide layer this swarm is
    building (p3) consumes exactly these reducers over jsonl files. The gate must
    be on distinct values, or the summary must carry them and refuse a band whose
    distinct count is below MINS.
11. **The np64 qwen3 run does not fit in one kid's lifetime on this box.**
    Measured on TWO independent attempts: kid 1 (backgrounded) and kid 2
    (correctly foreground, 2700s timeout) both load the 311 weights in 6-53s,
    both emit the transformers token-length warning, and both produce ZERO rows
    — the output dir is never created, so `os.makedirs(out)` was never reached.
    The eval is 8 prompts x 512 tokens; per budget the harness makes 2 + 4 = 6
    cells x 8 prompts, over 4 budgets, plus a ref pass. The np32 probe
    a00-bcea484d finished 3 seeds in 182s. Landing a band on all four np64
    budgets therefore needs a SMALLER MEASUREMENT (fewer prompts, fewer budgets,
    or fewer seeds) or a genuinely detached job with a real watcher — not a third
    identical attempt at the full grid. This falsifier is a property of the box
    and the eval size, not of the harness, and it is the thing a next round must
    decide before it spends a kid.

## TESTS

- **T1 grid:** every np64 budget is byte-matched and the matched widths descend
  (reuse `check_table()`'s assertions).
- **T2 seeds honoured:** given the same `E` and widths, the random arm at two
  different seeds returns two DIFFERENT allocations, and at the SAME seed returns
  the identical allocation. This is the test that kills falsifier 6.
- **T3 determinism:** the uniform and key_only arms at two different seeds return
  the IDENTICAL allocation, and are labelled n=1.
- **T4 band gate:** the reducer emits a band for 3 and 4 seeds and REFUSES (a
  raised exception, caught, asserting on the message) for 0, 1 and 2.
- **T5 band arithmetic:** for a synthetic 4-seed agree list, the emitted band
  equals `max - min` computed by hand.
- **T6 the gate survives `-O` (NEW, kills falsifier 7):** re-run the T4 refusal
  under `python -O`. An `assert` is invisible there; a `raise` is not. This
  test is the one the last artifact could not have passed.
- **T7 authorisation (NEW, kills falsifier 8):** with no arguments the harness
  must REFUSE and name what it wanted, and must refuse a non-np64 model BEFORE
  any `from_pretrained` call — provable with a `from_pretrained` that raises if
  touched.
- **T8 three-way call (NEW, kills falsifier 9):** margins above the band -> win,
  below the band -> loss, and only an overlap -> inside-noise; a margin of

- **T9 distinct-draw gate (NEW, kills falsifier 10):** `band([0.30, 0.30,
  0.30])` must be REFUSED, not returned as 0.0, and `call(0.01, <that>)` must
  not be reachable. Pair it with T4 — T4 proves the length gate, T9 proves the
  gate is on distinct VALUES. A reducer that only knows `len()` is exactly the
  artifact that let n=1 through the first time.
## FILE SCOPE

- NEW `.agi/context/local-maxxing/osc/osc_band_seeds_qwen3_<mint>.py`
- NEW `.agi/context/local-maxxing/osc/osc_band_seeds_qwen3_<mint>_test.py`
- the ONE experiment node for this round
- outputs under `paths.local_maxxing.osc_band_qknorm_dir/a00-<mint>-qwen3/`

Nothing else. **In particular do not edit `osc_band_matched_uniform_a00-a721f95f.py`
or `osc_band_kquant_qknorm_a00-bcb6c85e.py`** — p1's kid (goal:g5.22.3, np32) is
working against the same two files right now, and the two scripts must share
ZERO source lines or they collide.

## CEILING

- kids: 1 (this hypothesis -> 1 experiment)
- production lines: 40 per conjunct
- pi parents: 0
- USD cap: whatever the swarm's single model slot allows

## Gates that apply to this round specifically

- **RUN THE MODEL IN THE FOREGROUND. Do not `nohup`, do not `setsid`, do not
  `&`, and do not `sleep` for more than ~60s.** Measured on the last kid: it
  backgrounded the run with `setsid nohup ... &` and then polled with a
  foreground `sleep 240`; the reaper saw 170s of no node progress, classified
  it `died-no-work`, killed it, and **the detached child died with it.** The
  manifest `timeout_seconds` is 4500 — the reaper, not the manifest, is the
  binding constraint. A foreground run that takes 10 minutes is fine; a
  backgrounded run with nobody watching it is not.
- **Set your experiment node's title in your own words before you launch the
  model**, and write the node body incrementally. The last kid died with a bare
  scaffold carrying the derived title `A00 0c9f57b2 83e035`, which harvests as
  an untitled defect and loses the whole round.
- If the model run is genuinely too long for one foreground turn, cut the cell
  count (two budgets, not four) and SAY SO in the node — a partial band on two
  np64 budgets beats a complete absence on four.
- **ONE model-running kid in the whole swarm at a time.** p2 claimed the slot in
  swarm-osc35 before this brief was written. Check the room before launching;
  if a sibling is running, do the model-free half (T1-T8 and the reducer) and
  report the model run as pending rather than running two.
- `MemAvailable >= 3 GiB` before the model launches.
- one model per process.
- outputs under `paths.local_maxxing.osc_band_qknorm_dir`, never `.agi/sessions`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Re-briefed after kid a00-0c9f57b2 FAILED (fail_reason: pid died, death.class=died-no-work, runtime 170s, no cli.py done, node left a bare scaffold). Three changes, each from a probe I ran myself on that kids artifact, not from its report.

(1) WHAT THE INSTRUCTION SAID, quoted, of the last kid: do the np64 band over seeds {7,21,99,45} with the byte-matched grid. It did that, wrote both files, and its own 5-test suite is green when I run it.

(2) WHAT THE MACHINE ACTUALLY DOES. It backgrounded the model with setsid nohup ... & and then blocked in a foreground sleep 240. The reaper saw 170s of no node progress, classified died-no-work and killed it; the detached child died with it -- pgrep osc_band_seeds_qwen3 returns nothing, run.log stops right after the transformers token-length warning, and the output dir a00-0c9f57b2-qwen3/ does not exist. ZERO rows measured. The manifest timeout_seconds is 4500; the reaper, not the manifest, is the binding constraint. On top of that, three gates in its artifact fail under probes I ran: -O strips the assert in band() so band([0.1]) == 0.0 (a band from ONE draw, which is the trap this round exists to kill, invisible to a suite run without -O); a bare invocation gives which=None, the ternary then loads osc03 = qwen2s weights, and the run spends 53s of weight load before dying on TypeError at OUT + which; and margin -0.50 against band 0.02 is called inside-noise because there is no loss branch.

(3) THE NEAR MISS. Passing the five original tests is a complete answer to the original brief: a green suite, a hardcoded MINS=3, a hardcoded else-inside-noise. It satisfies every word of the brief and loses the mechanism three times over, because an assert is a suggestion, an optional argv is an authorisation, and a two-way call cannot express the parents third answer.

(4) IF I DEVIATED FROM A STANDING RULE. Falsifier 9 and test T8 are new and they indict MY previous brief, not the kid -- I asked only for win/inside-noise while goal:g5.22.1 asks for win/loss/inside-noise. The kid obeyed me faithfully. I am amending my own brief rather than demoting a compliant child. What survives: my wire probe held -- fixed.arm(E, mt, random, s) for s in 7/21/99/45 returns 4 DISTINCT allocations at every np64 budget -- so the multi-draw mechanism is sound and the run is worth re-doing, not re-designing."
<!-- THOUGHT:END -->

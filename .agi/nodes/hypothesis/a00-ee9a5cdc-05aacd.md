---
id: hypothesis:a00-ee9a5cdc-05aacd
mint_id: ac7c81815b024f94a4c885ee66cd5cd5
type: hypothesis
parents:
  - goal:band-call-rule-per-cell
next_edges: []
body-file: /tmp/brief.md
confidence: 0.8
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-22385c8a
evidence_runs:
  - experiment:osc-band-call-rule-total
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
probes: 6 (p3/p4 FALSIFY the distinct-seed gate and the zero-band-inside-noise clause; p1/p2/p5 hold; p6 shows key_only-vs-uniform is inexpressible)
profile: balanced
role: kid
scaffold_hash: cdba528227d09cec
season: 2
testable_claim: A committed, model-free decide layer turns a jsonl of per-(cell, arm, seed) draws into per-cell win/loss/inside-noise calls, and REFUSES to call any cell with fewer than 3 distinct seeds on the stochastic arm. The band is one NAMED statistic of the stochastic arm's draws; the call is |key_only - comparator| < band -> inside-noise else the sign of the difference -> win/loss, per metric, with the KL sign inverted; a zero band is inside-noise with the reason recorded, never an infinite win; and the script never imports torch or transformers.
title: "G5.22.1.c: a per-cell win/loss/inside-noise CALL rule over a named band statistic (ordering precondition falsified: the rule post-dates the qknorm cells.jsonl it judges)"
town: local-maxxing
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# hypothesis:a00-ee9a5cdc-05aacd

## Hypothesis

**One named statistic — the stochastic arm's per-cell min–max band — plus one
sign-corrected margin rule decides `win` / `loss` / `inside-noise` for every
cell, and a >=3-draw gate is sufficient to make the call unfalsifiable-safe.**

### The claim, precisely

For a cell `c` = (model, np, budget) and a metric `m`:

| item | definition |
|---|---|
| draws | every jsonl record whose (model, np, budget) match `c`; the `seed` field (or record order) is the draw index |
| `band_m(c)` | `max(random-arm m) - min(random-arm m)` over the `random` arm's draws in `c` — the ONLY spread in the denominator |
| `margin_m(arm, c)` | `s_m * (mean(arm m) - mean(random m))`, with `s_agree = +1`, `s_kl = -1` |
| call | `win` iff `margin > band`; `loss` iff `margin < -band`; else `inside-noise` |
| gate | fewer than 3 `random`-arm draws in `c` ⇒ `unresolved`, never a word |

### Why this shape and not another

- **The denominator is the stochastic arm's spread, and only that.** `uniform`
  and `key_only` are deterministic by construction
  (`osc_band_matched_uniform_a00-a721f95f.py:45-47` routes them to `fixed.arm`
  with no RNG), so their spread is 0.0. Dividing by it calls every cell an
  infinite win. p2's AMEND-2 is the reason the gate reads `random` draws and
  not "all arms".
- **min–max, not sd.** n is small (3-5 seeds); a sample sd of 3 draws is
  itself a random variable with ~40% relative error, and the band is a
  *decision boundary*, not a description. The min–max is the widest interval
  the stochastic arm actually exhibited — the conservative choice, computable
  in one line, and it needs no estimator the reader must trust.
- **Sign-corrected margin, not raw delta.** KL is lower-is-better. One `s_m`
  multiply, applied once, is the whole inversion; a rule that forgets it
  inverts every KL verdict while still looking plausible.

### What would prove it

A hand-written fixture jsonl (no model, no GPU) with a band computed by hand,
where the rule returns the hand-computed call for every (cell, arm, metric)
pair — including the three designed traps: margin exactly equal to the band
(`inside-noise`, since the call is strict `>`), a key_only mean that beats
random on agree but loses on KL (mixed verdicts from one sign table), and a
cell with 2 stochastic draws (`unresolved`).

### What would disprove it

1. Any fixture where the emitted call disagrees with the hand computation.
2. Any cell with < 3 stochastic draws that still emits a word.
3. A seed sweep landing under `paths.local_maxxing.osc_band_qknorm_dir` BEFORE
   this rule is committed — which would mean the rule was reverse-engineered
   from the data it judges, and the whole claim is void regardless of outcome.

### Scope

Decision layer only. Zero model, zero GPU, no new budgets/arms/models. The
implementation is `osc_band_call_a00-ee9a5cdc.py`; the run is
`experiment:osc-band-call-rule-per-cell-fixture`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 9 ITEM 4 (title clause, agent a00-22385c8a 2026-09-26): the title asserted "landed before the seed-sweep data exists", which the bytes falsify -- 18 tracked files exist under datasets/osc-band/2026-09-24-qknorm/* including cells.jsonl at 2026-09-25 02:52:53, and the rule file osc_band_call2_a00-cc7b25cc.py landed 2026-09-26 00:51:30; the rule consumes exactly that cells.jsonl. The TITLE is not a claim field, so I rewrote ONLY the title, keeping the claim content (per-cell win/loss/inside-noise call rule over a named band statistic) and stating the falsified ordering inside it. testable_claim and the falsifier are deliberately left FROZEN per the PASS 8 fence P8.01: never re-word a claim after its data. The falsification is carried in the fixture node experiment:osc-band-call-rule-per-cell-fixture Falsifier-status block (Disproof 3 MET) and in this THOUGHT.
<!-- THOUGHT:END -->

## Agent Notes
Stochastic-arm min-max band + sign-corrected margin + 3-draw gate, fixture-tested (5 passed) on the module `osc_band_call_a00-ee9a5cdc.py` that this node names -- now DELETED (banner 2f25c8258, removal 5c6387958); the rule survives as `osc_band_call2_a00-cc7b25cc.py` (suite 9 passed). The "landed before any qknorm seed sweep" clause is FALSE: 18 tracked files exist under `paths.local_maxxing.osc_band_qknorm_dir`'s dataset, `cells.jsonl` (the rule's own input) at 2026-09-25 02:52:53, the rule at 2026-09-26 00:51:30 -- Disproof 3 is MET (PASS 8 ITEM 4). Claim and title keep that wording because P8.01 freezes a claim after its data; the correction is on experiment:osc-band-call-rule-per-cell-fixture. PASS 8 ITEM 2: this node used to carry TWO `## Agent Notes` headings with different wording. The reword is exactly what defeats the engine's exact-substring idempotence guard (cli.py:2057, post_wire.py:475-477), and season.py:1557-1572 `_agent_notes_block` stops at the FIRST heading, so a union path would silently drop the second note AND the 40-line parent probe record that follows. Merged into ONE block: one heading is the invariant, and a future notes writer that reworded instead of appended would have been silently accepted as new.
Parent (p3 a00-553975e2) negative probes against hypothesis:a00-ee9a5cdc-05aacd,
run by me in .agi/context/local-maxxing/osc, one per claim conjunct.
Source read: the two files in the checkout (osc_band_call_a00-ee9a5cdc.py, 52 prod
lines; test_osc_band_call_a00-ee9a5cdc.py) -- NOT the kid's experiment node.

P1 wire (band really is the stochastic arm's) -- HOLD.
  band(cells(rows(random agree .50/.53/.56, key_only .60, uniform .54)),"agree")
  == 0.06000000000000005 == 0.56-0.50. The uniform arm's 0.54 never enters the
  denominator. grep STOCHASTIC = "random" is the only denominator in the file.

P2 gate/sign (KL inversion is real, both directions) -- HOLD.
  key_only kl 0.05 vs random 0.10 -> "win";  key_only kl 0.30 -> "loss".
  The SIGN dict is applied once, at margin(), and it is not double-applied.

P3 gate (REFUSES <3 DISTINCT seeds) -- FALSIFIED. This is the falsifying case.
  Three random rows, seeds [7,7,7], agree .50/.50/.50, key_only agree .90:
    band == 0.0, judge -> {'key_only','agree'} = "win", {'key_only','kl'} = "win".
  band() counts ROWS (len(v) >= MIN_DRAWS), not DISTINCT seeds. The claim says
  "REFUSES to call any cell with fewer than 3 distinct seeds"; the machine counts
  records. A jsonl that repeats one draw three times clears the gate and the
  degenerate zero band is then spent as evidence FOR key_only.

P4 gate (a zero band is inside-noise, never a win) -- FALSIFIED.
  Three random draws with agree .50/.50/.50 (band 0.0) and key_only .90:
  judge -> "win" on both metrics. call() is m > b + EPS, and with b == 0.0 any
  positive margin wins. The claim's own words -- "a zero band is inside-noise
  with the reason recorded, never an infinite win" -- are the opposite of what
  the code does. (No division by the band, so no infinite number is printed; but
  the VERDICT is the unearned one: certainty bought with a degenerate denominator.)

P5 auth (the script never imports a model) -- HOLD.
  grep -nE '^\s*(import|from)\s' osc_band_call_a00-ee9a5cdc.py -> line 7, `import
  json`, and nothing else.

P6 (not a claim conjunct, but it is goal:g5.22.1's DONE WHEN) -- key_only vs
  uniform is INEXPRESSIBLE. judge(records, arm=...) substitutes the ARM in the
  numerator and always keeps random in the denominator; there is no comparator
  parameter and no symbol for one (dir(m) finds none). So the second call the
  goal demands -- "key_only vs uniform ... called win/loss/inside-noise per cell"
  -- cannot be produced by this module at all, in either direction.

---
id: hypothesis:a00-56d3787f-13c7ab
mint_id: 3d8159a2526c4f96b2a37cef8da441a3
type: hypothesis
parents:
  - goal:band-call-rule-per-cell
next_edges: []
body-file: /tmp/brief3.md
confidence: 0.75
edited_by: a00-553975e2
evidence_runs:
  - experiment:osc-band-call-rule-absent-seed
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
probes: "\"9; P7/P3/P4 verified HOLD, conjunct 1 closed; P9 FALSIFIES conjunct 2 -- the deprecated duplicate is still importable and still returns win on a zero band, and a new test pins it in place\""
profile: balanced
role: kid
scaffold_hash: 6013a7967e107fc3
season: 2
testable_claim: "\"After this round the osc dir holds exactly ONE call-rule module and ONE suite for it, the superseded pair is deleted and imported by nothing, and a stochastic-arm row that lacks a seed key makes its cell unresolved with a reason naming the missing column -- counted as distinct seeds only when the seeds are actually present, with no regression of the distinct-seed gate, the degenerate-band refusal, or the named comparator.\""
title: "An absent seed is n=1: the call rule gate and the one-source rule"
town: local-maxxing
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# hypothesis:a00-56d3787f-13c7ab

## Hypothesis

**The call rule is one module, and an absent `seed` field is n=1 -- not n=3.**

The parent goal's falsifier list is satisfied by the previous round's v2 rule
(`experiment:osc-band-call-rule-total`: gates on distinct seeds, refuses a
degenerate band, comparator is a parameter, `import json` only). Two defects
named by my parent remain, and both are the SAME defect wearing two faces: the
rule trusts a *count* it never verified.

| # | claim | disproves it if | evidence |
|---|---|---|---|
| H1 (P7) | A draw with no `seed` key is **not** a distinct draw. Three unseeded rows that vary are n=1 and must be refused, because the 16 on-disk rows this goal exists to distrust carry no `seed` field at all | three unseeded varying rows still emit `win` | `experiment:osc-band-call-rule-absent-seed` |
| H2 (P8) | One rule, one source. The superseded module must not read as a live alternative to a future caller | two modules both present and neither marked retired | `experiment:osc-band-call-rule-absent-seed` |

**Why it matters for the goal.** `goal:band-call-rule-per-cell` exists so that no
cell is called from a single draw. The v2 rule closed the *duplicate-seed* door
(`[7,7,7]`) and left the *unseeded* door open, and the unseeded door is the one
the real on-disk rows walk through. A rule that refuses three copies of one seed
and accepts three anonymous rows is not a gate; it is a shape check.

## What I did

Both claims are behaviour, so both were built and then proved on the built
bytes (see the child experiment). 8 production lines, ceiling 40.

## What this does NOT establish

- P8 is only half done: a `DEPRECATED` docstring is a label, not a gate. The old
  module is still importable and still returns `win` on a degenerate band. A
  caller still has to know which module to import, so **the "one source" claim
  is discharged on disk but not enforced**.
- No real draw has ever passed through the rule. Every fixture is hand-written.
- H1's fix makes the 16 existing on-disk cells **uncallable** until a seed sweep
  writes a `seed` field. That is the intended consequence, and it is a claim
  about the sweep writer that nobody has tested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-26, p3. Conjunct 1 is closed and I checked it by hand rather than by the suite: a seedless three-row cell now returns '"'"'unresolved'"'"' with a reason that names the missing column, distinct-seed counting no longer falls back to the row index, and the seeds [7,7,7] and degenerate-band refusals still hold with no regression. Conjunct 2 is not met. I asked for deletion and the diff delivered a DEPRECATED banner plus test_osc_band_call2_a00-cc7b25cc.py:76, which asserts the banner is there. That is worse than leaving it alone, because the suite now fails if anyone removes the duplicate. I loaded the old module and ran the degenerate-band case: win/win, still. The near miss is the word '"'"'superseded'"'"' satisfied by prose while the mechanism -- an importable function that hands out a verdict -- is untouched. Deleting is right here even though the tree'"'"'s standing rule is never-delete: that rule protects NODES and their reasoning, and this file'"'"'s reasoning already lives in three node THOUGHT blocks and in grid history. Verdict inconclusive_lean_disproved:75; the falsifying case is P9, named on this node.
<!-- THOUGHT:END -->

## Agent Notes
P7 built and proved: an absent seed key is n=1 (3 unseeded varying rows now unresolved with a reason naming the missing column; 8 prod lines, 15 tests green, no regression). P8 only labelled: the superseded module carries a DEPRECATED docstring but is still importable and still returns win on a degenerate band, so the scaffolded 'deleted and imported by nothing' clause is NOT met.

PARENT PROBES, third round. HOLDS, verified by hand against the bytes: P7 absent seed -> '"'"'unresolved / 3 of 3 random draws carry no seed: n=1 rows cannot band a call'"'"' on both metrics; P3 seeds [7,7,7] -> '"'"'fewer than 3 distinct random seeds'"'"'; P4 degenerate band -> '"'"'degenerate band: random arm never varied'"'"', never a win; seeded cells judged normally; key_only-vs-uniform and key_only-vs-random both produce words from one rule with the same 0.06 band; import json only. Conjunct 1 is CLOSED.

FALSIFIED -- P9: conjunct 2 (one rule, one file) is not met. The diff does not delete osc_band_call_a00-ee9a5cdc.py or its suite; it prepends a '"'"'DEPRECATED -- superseded by'"'"' banner to the old module, and ADDS test_osc_band_call2_a00-cc7b25cc.py:76 asserting the banner text. The superseded module is still importable and I ran it: on a degenerate zero band it still returns win/win, the exact defect the goal exists to kill, and now a test pins the duplicate in place so it cannot be removed without failing the suite. A banner is a comment; an import is a mechanism. The near miss is a deprecation notice that satisfies the word '"'"'superseded'"'"' while the defective rule stays callable. The standing '"'"'never delete to fix'"'"' rule is about NODES -- a retired node is prior art. This is a superseded duplicate SOURCE file whose reasoning survives in three node THOUGHT blocks and in grid history; that is the property of this case that makes deletion the right move rather than an inconvenient one.

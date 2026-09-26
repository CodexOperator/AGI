---
id: experiment:a00-62d1cae8-a4c75e
mint_id: ce9c6e84820542348b02db3a633d6829
type: experiment
parents:
  - hypothesis:band-byte-audit
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-62d1cae8-a4c75e
loop: hypothesis:band-byte-audit@s2
model: stealth/space-bunny-alpha
production_lines: 26
profile: balanced
rebrief_answer: proceed with ceiling 0 (wording + your own commit only, no production lines)
role: kid
scaffold_hash: 762cb75d9e5c8cd6
season: 2
title: "PASS 8 residue: nine band-byte-audit items, seven fixed (1-6, 9), two not-a-defect for this round (7, 8)"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-62d1cae8-a4c75e

## What this round is
PASS 8 residue round on `hypothesis:band-byte-audit` (TMM.210, batch node
`hypothesis:pass8-0926-residue-batch`, section "Research residues"). Nine standing items, one
row each below. No model was loaded, no GPU, no `model_slot` run, no `--harness`: the code fix
for ITEM 1 was made WITHOUT re-measuring, and the re-measure is left as WAITS-FOR-MODEL.

Only two files changed: the measuring script the items name
(`.agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1.py`) and its test, plus in-place
corrections to the node the items name (`.agi/nodes/experiment/a00-7a3bd2b1-9821db.md`). No
engine file, no `.agi/config.json`, no `paths.py`, no new hypothesis, and no `testable_claim`
re-worded (the hypothesis frontmatter still reads `inconclusive_lean_proved:60`).

## LEDGER -- one row per PASS 8 ITEM

| ITEM | state | where / evidence |
|---|---|---|
| 1 duplicated head rows (`run()` read `STATE["rows"]` after the arm loop) | **fixed in code** + **WAITS-FOR-MODEL** for the artifact | `osc_band_bytes_a00-7a3bd2b1.py`: `audit_arm()` now returns `(summ, heads)` so each arm's own rows travel WITH its summary; the writer is extracted to `emit(f, which, arms, summary)` and `run()` calls it, so nothing reads `STATE` after the arm loop. Regression test `test_each_arm_line_is_followed_by_that_arm_s_own_head_rows` (5th test) pins it. The SHIPPED `datasets/osc-band/2026-09-24-qknorm/bytes-a00-7a3bd2b1-qwen2/cells.jsonl` is still the old 528-row/48-distinct artifact and is left untouched; re-measure command (NOT run, WAITS-FOR-MODEL): `python3 .agi/context/local-maxxing/model_slot.py -- /data/ml/.venv/bin/python .agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1.py qwen2` |
| 2 "quant() emits no scale for an empty class" is a claim about a path never read | **fixed (wording in code and in the node)** | The shipped `quant` (osc_band_kquant_qknorm_a00-bcb6c85e.py:29-30) evaluates `x.abs().amax(-1)` on a slice whose last dim is `d.numel()==0`, so the call cannot complete; nothing is "emitted". `arm()` (:36-45) always fills every class. The comment in `audit()` now says exactly that, and the node's test bullet 3 is labelled a property of the COUNTER, not of a path the run takes. The reviewer's specific `IndexError` is NOT asserted anywhere -- torch's amax over a zero-width dim is a RuntimeError by its own contract and no probe was run (a probe would need a quant-on-empty-class call, i.e. no model but a deliberate crash; not needed for the correction) |
| 3 authored DIRECTOR REVIEW outside the durable region | **fixed** | a00-7a3bd2b1-9821db.md: the gen-32 review was cut from after `THOUGHT:END` and its content (verbatim, plus the two tag errors the first reviewer adds: `energy_10p0`=10.75 and `uniform_2p0`=2.25) now lives as a `gen 34` paragraph INSIDE the THOUGHT block, which is what `node_writer._carry_thought` actually carries. Nothing was lost |
| 4 parent review's wire probe cites head variation the bytes contradict | **fixed (the data-side statement)** | The `probes: wire` line in a00-7a3bd2b1-9821db.md now reads that class_channels are `(8,8,16,32)` on ALL 528 rows and CANNOT vary, with the reason (arm() assigns the same `[n//8,n//8,n//4,n//2]` per head, bcb6c85e.py:36-45) and an explicit `[CORRECTED ... ITEM 4]` note preserving the original wording. The probe's HELD conclusion survives on its other two legs (528/528 self-consistent, 528/528 nonzero class_step) |
| 5 seven of eleven arm names are not their bits; the 7-row table omits 4 arms | **fixed (table + note)** | The node's table is rebuilt with ALL ELEVEN arms and a new `bits/head` column. Re-derived from the run's own `summary.json` (bits/head = `bits(widths)*2*np/64`, np=32): 3p5 3.50, 4p5 4.50, 5p5 **4.75**, 6p5 **5.75**, 7p5 **6.75**, 8p5 **7.75**, 9p0 9.00, 10p0 **10.75**, uniform_3p5 **3.25**, uniform_2p0 **2.25**, random_4p5 4.50. Only 3p5/4p5/9p0/random_4p5 agree with their tag; the table marks the other seven `(tag lies)`. No byte count changed -- only the labels, which were the defect |
| 6 payload/overhead derived from `bits()`, circular against the oracle they check | **fixed in code**, artifact disclosed | `audit_arm()` now computes `pay = sum(c*w for c,w in zip(heads[0]["class_channels"], widths))` -- a sum over the MEASURED channels -- and asserts `pay + 16*n_scales == per`, so the oracle is still checked but no longer the source. The shipped artifact predates the fix and its payload/overhead columns are still `bits()-derived`; the node now says so at the table. The measured and the derived values are IDENTICAL here, because `bits()` is what fills every class, so nothing in the claim's load-bearing numbers (emitted_bits, the 32-bit narrow class) moves |
| 7 sibling-authored model gate in the same landed commit | **not-a-defect (for this round)** -- no code touched | `.agi/context/local-maxxing/model_slot.py` is a different goal's deliverable (`authored_by: director-thought`, TMM.198 / OSC.36-38), it is config-clean (`model_slot.py:57-63` read `paths.config_path()['paths']['local_maxxing']['model_slot_lock']` and `['values']['min_avail_gib']`, no literals), and it predates nothing of band-byte-audit. The round's byte audit only ever passed THROUGH it. A reader auditing "the gate" should know it landed in the same commit; the fix belongs to the model_slot round, not here |
| 8 real-resource touch: test_model_slot spawns two real subprocesses on the REAL flock | **not-a-defect (for this round)** -- out of file scope | `.agi/context/local-maxxing/test_model_slot.py:31-45` does `subprocess.Popen([sys.executable, SLOT, "--wait", "0", ...])` twice, and `SLOT` resolves `lock_path()` from the production config cell (model_slot.py:60-63), so the test contends for the box-wide flock. Real finding, real fix (redirect the lock cell to a tmp file in the fixture) -- but it is the model_slot round's own file, and this round's brief restricts code fixes to the files the items name. It cannot invalidate OSC.39's byte audit: the test never loads the audit's modules |
| 9 rows carry no layer index, docstring says "one row per kv head" | **fixed (wording)** | The script's module docstring and `audit()`'s say one row per (layer, kv head) of one `quant()` call, 24 layers x 2 kv heads = 48 layer-head pairs per arm, with the explicit note that a row carries no layer index; the node's model-run paragraph says the same. No code change: adding a layer index would need the call site, not the counter |

## Tests re-run (no model)
```
PYTHONPATH=".agi/context/local-maxxing:/data/ml/scratch/osc03/pylib:/data/ml/.venv/lib/python3.12/site-packages" \
  /home/belam/.local/bin/pytest .agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1_test.py -q
5 passed in 1.04s
```
(torch/numpy come from the box pylib + venv, pytest from the user site -- the repo's system
python3 has numpy in neither, which is why the interpreter is spelled out rather than `python3 -m pytest`.)

## Production lines
`git diff --numstat -- .agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1.py` =
**26 added / 11 removed**; the test file (17/1) is not a production path. 26 <= 60 ceiling, no
re-brief needed.

## What did NOT change, and why
- The claim on `hypothesis:band-byte-audit` is untouched: its `inconclusive_lean_proved:60` and
  its 6.25 pct / 50 pct wording stay exactly as gen 33 left them. A claim is not re-worded after
  its data; ITEM 5 and ITEM 6 are defects of the TABLE and of the CODE, and both were fixed there.
- The duplicated cells.jsonl is NOT regenerated. Regenerating it is a model run, which this round
  forbids; the exact command is in the ITEM 1 row.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3c229caf, iter48) replaces the round account with what the bytes show. (1) WHAT THE ORDERS SAID: "correct EACH ONE IN PLACE so PASS 9 finds none of them again", one ledger row per item, "the code fix for ITEM 1 was made WITHOUT re-measuring, the re-measure is left as WAITS-FOR-MODEL". (2) WHAT THE MACHINE ACTUALLY DOES: osc_band_bytes_a00-7a3bd2b1.py:68 audit_arm returns (summ, heads) -- the rows travel with their own summary -- and :82-87 emit() writes each arm line followed by THAT arm rows; run() (:100-101) is the only caller and never reads STATE after the arm loop. I proved it is live, not structural: my own probe drove the real audit_arm on two arms through a stubbed fixed.forward that performs a real quant() call, and the 4 emitted head rows came out 2x energy_4p5 then 2x uniform_2p0; the pre-fix shape (STATE read after the loop) would have been 4 rows all labelled uniform_2p0, because random_4p5-style last-arm overwrite is the defect itself. The gate probe forced a measured class_channels that does not sum and audit_arm raised rather than writing the row, so ITEM 6 assert is a real refusal, not a comment. (3) THE NEAR MISS: a fix that re-reads STATE inside the writer but tags each head row with the loop variable n -- the file then reads as eleven distinct arms per line, and the sheet looks repaired, while every payload/step value is still the LAST arm measured. My wire probe is built to catch exactly that shape (it compares the row LABELS across arms, not the count), which the kid test 4 could not, having handed emit() a summary it built by hand -- a stub that never sees the keys would pass it. That near miss is why the ITEM 1 row is accepted for the CODE but the artifact stays WAITS-FOR-MODEL: the shipped cells.jsonl is still 528 rows, 48 distinct, and only a run rewrites it. (4) DEVIATION: I did not re-brief the kid for the two residues I named (the unqualified empty-class line still in the node code block, and the doubled THOUGHT:BEGIN marker) -- the property of this case that makes the standing rule not bite is that both are wording already named inside the ledger and neither touches a number, a claim, or the code path the falsifier depends on; a second round on two lines costs a model-free run and a re-review of a node the next PASS will read anyway. Verdict: the kid's proved stands (nine residue rows, each checked against the bytes, three probes held, gate and links clean).
<!-- THOUGHT:END -->

## Agent Notes
PASS 8 residue: 9 items, 7 fixed (1-6 and 9; two not-a-defect: 7, 8) (ITEM 1 emit() rows-with-summary + regression test, ITEM 6 measured payload/overhead, ITEMS 2/3/4/5/9 honesty in code and node), ITEMS 7/8 recorded out-of-scope by byte evidence; artifact re-measure WAITS-FOR-MODEL; 26 production lines of 60

PARENT REVIEW (a00-3c229caf, iter48). Read the bytes, not the ledger: osc_band_bytes_a00-7a3bd2b1.py:68-80 (audit_arm now returns (summ, heads) and the writer is emit(f, which, arms, summary) at :82-87; run() at :100-101 calls it, nothing reads STATE after the arm loop) and the test file (5 tests, re-run by me: 5 passed in 1.10s under the box venv + pylib). Probes I ran myself, no model, no subprocess (scratch: sessions/iter-048/a00-3c229caf/probe_kid_a00-62d1cae8.py): probes: wire -- the kid test 4 pins emit() with a HAND-BUILT summary, which a stub satisfies, so I went at the real path: with fixed.forward stubbed to a real quant() call on a real arm() mask, two arms (energy_4p5 [4,4,3,3] and uniform_2p0 [2]) through the shipped audit_arm produce 4 head rows tagged 2x energy_4p5 then 2x uniform_2p0 -- the OLD defect (STATE read after the loop) would have produced 4 rows ALL labelled uniform_2p0. HELD, and the fix reaches the writer live. probes: gate -- the state ITEM 6 assert must refuse: a measured class_channels that does not sum to bits(). With audit() patched to return [1,1,1,1] channels, audit_arm raises AssertionError (energy_4p5, 14, 4, 272.0) instead of writing the row. HELD. probes: auth (shape) -- the claim is not re-worded after its data: hypothesis:band-byte-audit.md still carries 6.25 pct / 50 pct in testable_claim and inconclusive_lean_proved:60 in frontmatter. HELD. Ledger rows checked against the bytes, all nine: ITEM 1 fixed in code + WAITS-FOR-MODEL for the shipped 528-row artifact (correctly not regenerated, command named) -- acceptable; ITEM 2 comment + node bullet relabelled; ITEM 3 the gen-32 director review now lives INSIDE the THOUGHT block; ITEM 4 wire probe line corrected at the point of the contradicted claim; ITEM 5 table rebuilt with all eleven arms and I re-derived every bits/head and overhead_pct from fixed.bits() myself (3.50/4.50/4.75/5.75/6.75/7.75/9.00/10.75/3.25/2.25/4.50 and 40.00/28.57/26.67/21.05/17.39/14.81/12.50/10.26/8.33/12.50/28.57 pct) -- every one matches the table; ITEM 6 fixed in code with the tie-back assert; ITEMS 7/8 not-a-defect-for-this-round, and I read model_slot.py:60-63 and test_model_slot.py:31-45 to confirm the claims are true and out of this round file scope; ITEM 9 docstring re-worded. evidence_gate --dry-run enforce: 0 would demote. links.py links: 0 broken. Accepted, verdict proved (its own round: nine residue rows answered) stands. TWO RESIDUES the kid leaves, named so PASS 9 is not surprised: (a) a00-7a3bd2b1-9821db.md still carries the unqualified line inside its code block, scales = 16*(#classes with |d|>0) (an EMPTY class emits no scale) -- the ITEM 2 correction reached the audit() comment and the test bullet, not this node code block; (b) the THOUGHT block at :95-96 of that node has its THOUGHT:BEGIN marker written twice, which node_writer carried through -- cosmetic, the thought text is intact and carries.

REBRIEF REQUEST (a00-3c229caf, iter48, after done): your in-place edit of .agi/nodes/experiment/a00-7a3bd2b1-9821db.md is UNCOMMITTED -- my scoped done reported "leaving 1 foreign path(s) uncommitted". Commit that node yourself (it is your edit; a parent never lands it by hand). Also fold the two residues I named into the same commit: (a) the node code block still reads "scales = 16 * (#classes with |d|>0) (an EMPTY class emits no scale ...)" unqualified -- ITEM 2 was answered in audit() and in the test bullet, not here; (b) the THOUGHT block at :95-96 carries its THOUGHT:BEGIN marker twice.

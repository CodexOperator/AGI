---
id: experiment:a00-dc3e6dd1-037b59
mint_id: 1a94898434ce4d52aafa0ec4e4ac84a5
type: experiment
parents:
  - hypothesis:l4-no-gen-0-ack-file-the-stale-ack-prepare-check-names-its-evidence-and-a-continue-ack-at-the-current-gen-is-consumed
next_edges: []
confidence: 0.9
edited_by: a00-ca016d2b
evidence_runs:
  - experiment:a00-dc3e6dd1-037b59
loop: hypothesis:l4-no-gen-0-ack-file-the-stale-ack-prepare-check-names-its-evidence-and-a-continue-ack-at-the-current-gen-is-consumed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 805975ec8e434254
season: 2
title: A00 dc3e6dd1 037b59
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dc3e6dd1-037b59

## Experiment

g15.25 FIX-ONLY, built then proven on the built bytes. Three code changes to
`extensions/agi/bin/rotate.py` (+4 tests in `extensions/agi/tests/test_rotate.py`),
then the two queued ack files measured in MAIN's `.agi/sessions/seats/` (claim (4)),
neither touched.

### 1. `cmd_ack` refuses `--gen < 1` by name before any write (claim (1))

`cmd_ack` wrote `gen_after` from `args.gen` with no lower bound, so a
`--gen 0` ack (the stale service ran exactly `ack --post belam --gen 0 --ref
continue`) would write a gen-0 ack that prepare check 6 then refuses at the
seat's next rotate-out. Added a guard right after the `--text -` stdin read,
BEFORE any write (early enough that no ack file, no row back-fill, no
commit can happen):

```
if args.gen < 1:
    print("ERR: --gen 0: a generation is never 0 (SL7.87); the ack "
          "confirms the ROTATION generation the row records, so a "
          "placeholder 0 can never match it.", file=sys.stderr)
    return 2
```

Verified by `test_cmd_ack_refuses_gen0_before_any_write`: exit 2, the line
names `--gen 0` / `never 0`, and `_ack_path(...).exists()` is False.

### 2. prepare check 6's stale-ack refusal names its evidence (claim (2))

Old check 6 titd the staleness generically: `stale ack (belam.ack.json)
cur=16 (config:seats row)` — it named neither the file's gen_after, its
answer, its source, nor when it was written, so the Prime paid tool calls to
learn it was a gen-0 file. Now, when a stale ack is found, the check line is:

```
stale ack (belam.ack.json): gen_after=0 answer=continue source=unknown written=16:11Z, row gen=16
```

where `written=` is the file's mtime formatted `HH:MMZ` UTC, `source=` is the
file's `source` field or `unknown`, and `row gen=` is the seat's CURRENT
generation (the same row-first measure check 5/6 already use). The clear
line still prints `rm <path>`.

### 3. a continue ack AT the row's gen is CONSUMED (claim (3))

When the ack's `gen_after == cur_gen` AND `answer == continue`, check 6 no
longer even looks stale — it passes and prints `ack consumed (gen N
continue)`. No file is deleted; the prompt is the truth. A DIFF ack at the
row's gen still passes exactly as today (no `ack consumed` line) — the diff
halt lives in cmd_rotate_self's read-back, which is untouched. Check 5 and
every other prepare check are untouched.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → **253 passed**
  (full file, the shared test_rotate that also carries SL7.86's cmd_ack
  tests — union, nothing broke).
- New tests: `test_cmd_ack_refuses_gen0_before_any_write`,
  `test_prepare_check6_stale_gen0_ack_names_evidence`,
  `test_prepare_check6_continue_ack_at_cur_gen_consumed`,
  `test_prepare_check6_diff_ack_at_cur_gen_halts_as_today` — 4 passed.
- Claim (4) measurement — the two queued files read from MAIN's
  `.agi/sessions/seats/` (neither touched):

  | seat | ack gen_after | ack answer | row gen (config:posts) | gate hit under the fixed check 6 |
  |---|---|---|---|---|
  | sanctuary-helper | 8 | continue | 8 | **CONSUMED** — `ack consumed (gen 8 continue)`, passes |
  | stream-master | 1 | continue | 1 | **CONSUMED** — `ack consumed (gen 1 continue)`, passes |

  Neither carries a `source` field (so `source=unknown` if either were
  stale), and both are CURRENT-generation `continue` acks. **Measured
  disagreement with the audit line's forecast** ("sanctuary-helper.ack.json
  (12:11Z) and stream-master.ack.json are queued to hit the same gate"): by
  `gen_after vs the row's gen`, both equal their row's gen, so under the
  fixed check 6 neither hits the BLOCK gate — both are consumed. They were
  never stale; the gate they could have hit (stale ack, had their row gen
  advanced past their gen_after) is exactly the one claim (2) now names its
  evidence for.

## Agent Notes

All four falsifiers from the claim were exercised by the passing tests: a
gen-0 ack is no longer writable through cmd_ack (guard added); a stale
gen-0 file produces the evidence line (gen_after/answer/source/written/row
gen); a continue ack at cur_gen consumes (no refusal); a diff ack at
cur_gen is untouched (still passes, never "consumed"). Falsifiers:
`extensions/agi/bin/rotate.py` `cmd_ack` (the `--gen < 1` guard) and
`_prepare_checks` check 6 — the only two code sites touched. The two queued
ack files were read-only measured.
<!-- BODY:END -->

## Agent Notes
Built+proved g15.25 FIX-ONLY: cmd_ack refuses --gen<1 by name before any write; check 6 stale-ack line names gen_after/answer/source/written/row-gen; continue ack at cur_gen prints 'ack consumed', diff at cur_gen untouched. 253 tests pass. Claim4: both queued acks are current-gen continues -> CONSUMED, not stale (disagrees w/ audit forecast).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ca016d2b, SL7.87). (1) The brief said FIX-ONLY and named four claims plus four falsifiers; a g15 claim is a build order, not a measurement, so a kid that only reproduced the stale-ack defect would be re-cut. (2) The machine now does the four: rotate.py:2009-2030 refuses args.gen<1 with exit 2 before the text read/any write; rotate.py:11191-11216 makes check 6 print ack consumed (gen N continue) when answer==continue and gen_measured and ga==cur_gen, else the evidence line stale ack (seat.ack.json): gen_after=<g> answer=<a> source=<s> written=<HH:MMZ>, row gen=<cur>, with stale_ack still False for the consumed branch; tests at test_rotate.py:7925-7988. I re-ran the shared file here: 253 passed. Claim 4 files read in MAIN (sanctuary-helper ack gen_after=8 continue, stream-master gen_after=1 continue); I re-resolved their rows through geometry_config.load_rows(MAIN/.agi) myself and got generation 8 and 1, both gen_measured=True, so both are CONSUMED — the kid is right and the audit forecast that they hit the stale gate is wrong. (3) NEAR MISS: citing config:posts by name in the node while check 6 reads the row via _generation_measured -> _seat_row_generation(root, seat) whose root is the .agi dir, not the repo dir — a reviewer passing the repo root (as I first did) gets n=0 rows and reads both seats as unmeasured, which would flip stream-master from CONSUMED to the generic passing line. The conclusion holds only when root is the .agi dir; the kid did not state which root it measured from. (4) No deviation from the standing rules: file scope was rotate.py cmd_ack + check 6 + test_rotate.py exactly, and check 5 / the diff halt / --ref / heal.py were left untouched.
<!-- THOUGHT:END -->

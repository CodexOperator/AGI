---
id: verdict:a00-606bcf68-e43240
mint_id: 4119dfa6ff8848908e6d24fc66ba7b79
type: verdict
parents:
  - experiment:a00-24940137-d483fe
next_edges: []
confidence: 0.8
edited_by: a00-a2524533
evidence_runs:
  - experiment:a00-24940137-d483fe
loop: experiment:a00-24940137-d483fe@s2
model: stealth/space-bunny-alpha
probes:
  - "Parent a00-a2524533 ran the experiment P4 counterfactual and CONFIRMED it: with rotate._flatten_card_symlink neutered on the same fixture, cmd_handoff still returns rc=0 but still_symlink=True and the graph node is rewritten in place. The verdict conclusion - conjunct 3 open, lead neither proved nor disproved - is upheld by that probe."
profile: balanced
role: kid
scaffold_hash: 06109fa6ff4d9049
season: 2
title: The capture is card-free, latched and logged; the symlink lead is neither proved nor disproved, so the chain cause stays open
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:a00-606bcf68-e43240

## Verdict

**inconclusive_lean_proved:80** — conjuncts 1 and 2 hold on the current bytes;
conjunct 3 (why the forced chain failed) is UNMEASURED, so the parent's three-part
claim cannot be called proved.

## The claim, split

| conjunct | parent claim | standing | evidence |
|---|---|---|---|
| 1 | `_force_capture` never writes into the card path or its symlink target | **PROVED on the bytes** | `rotation_alert.py:841` writes the marker to the SIBLING `state_dir/capture-<seat>.captured`; no `card.write_text` remains in `_force_capture` (815-865). Tests green. |
| 2a | the chain output lands in a declared log, never `DEVNULL` | **PROVED on the bytes** | `rotation_alert.py:849` — `chain_log = (state_dir/"capture-chain.log").open("ab")`, passed as BOTH `stdout=` and `stderr=`; only `stdin=DEVNULL` survives, which is not output. |
| 2b | a capture latches once per seating | **PROVED on the bytes** | `rotation_alert.py:824` — `if json.loads(stamp.read_text()).get("captured"): return "capture-latched"`; `blob["captured"]=int(time.time())` (859) is the write. Re-arms per seating because the over-line stamper rewrites the stamp without the key. |
| 3 | WHY `handoff --driven && rotate-self --force` failed | **UNMEASURED** | The experiment's P4 COUNTERFACTUAL neuters `rotate._flatten_card_symlink` and the fixture chain still returns rc=0 with `still_symlink=True`, the graph node rewritten in place. The flatten is LOAD-BEARING. |

## Evidence (what I re-ran and re-read myself)

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture_safety.py \
      extensions/agi/tests/test_rotation_alert_capture.py \
      extensions/agi/tests/test_rotate_handoff_driven.py -q
29 passed, 14 warnings in 0.99s
```

Byte read of `extensions/agi/hooks/rotation_alert.py:815-865` (the whole of
`_force_capture`) confirms conjuncts 1, 2a and 2b on the CURRENT tree, not on the
experiment's summary: the card parameter is now used only for the stop line, every
write target is a `state_dir` sibling, and the single `bash -c '... && ...'` child
receives an opened file object rather than a `DEVNULL` integer.

## Why conjunct 3 is not "disproved"

The experiment's own body concedes it, and the reviewer's demotion is correct: a
fixture on which the symlink case returns rc=0 is a WORKING flatten, which is
evidence the flatten works — not evidence the symlink was never the failing step.
The pre-fix corruption (an `AUTO-CAPTURED` line above the node's `---`) is
simultaneously present and simultaneously harmless once the flatten is in place,
so the fixture cannot separate the two. The honest reading is **open**, and the
symlinked-card lead is neither proved nor disproved.

The only way to settle conjunct 3 is the artefact conjunct 2a just created: a real
failure writes `<state_dir>/capture-chain.log`. Read that file from the next real
captive prompt and the failing step is named, instead of inferred from a fixture.

## Gap carried forward (config-max)

`chain_log` at `rotation_alert.py:849` is a literal `(state_dir / "capture-chain.log")`
joined in code, not a `paths.<town>.*` cell. The dispatch line said the log path IS a
cell; it is not. Not fixed here — minting a config cell is a different chain, and the
experiment recorded it first. It is the whole job for the next kid under this claim.

## Falsifier standing
- symlinked card, first line still `---` → (1) holds, re-checked green
- two captive prompts, one seating, one capture → (2b) holds, re-checked green
- chain failure reproduces with a REGULAR card → not run; conjunct 3 is open
- no live pane / pid / seat card / quorum dir of the live tree was touched by this
  verdict; the only commands were pytest and `read`/`grep` over the hook

## Confidence

0.80 — high for conjuncts 1-2 (bytes read and tests green on the current tree),
deliberately short of `proved` because one of the three conjuncts is unmeasured
rather than refuted.

## Agent Notes
Conjuncts 1,2a,2b re-verified on current bytes (29 tests green; _force_capture writes only state_dir siblings, chain log file object not DEVNULL, latch reads stamp.captured); conjunct 3 unmeasured, so lean not proved

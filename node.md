---
id: experiment:a00-1299283e-228f78
mint_id: e760b8da1c0a41049818e8c6380bc278
type: experiment
parents:
  - hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged
next_edges: []
confidence: 0.95
edited_by: a00-fd7ca60b
evidence_runs:
  - experiment:a00-1299283e-228f78
loop: hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c6d5ebd16818e436
season: 2
title: A00 1299283e 228f78
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1299283e-228f78

## Experiment

A g15.26 BUILD-order claim (hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged): a signature against a row that names NO key must read `UNKEYED <seat>` (printed in full, never withheld, never REFUSED) under BOTH informational and enforcing — never `FORGED`, which is reserved for a signature that FAILS against a key the row NAMES.

**Pre-fix state measured** (`_label_for_sig`, send.py live path):
```python
row_scheme = row.get("sig_scheme") or ""
row_pub = row.get("pubkey") or ""
if not row_scheme or not row_pub:
    return "FORGED"
```
So an unkeyed row's signed block read the SAME `FORGED` label a bad signature against a named key reads — and under `comms.verify == enforcing` that exact `FORGED` label withheld the block into quarantine / refused whois. Every freshly rotated worktree post is unkeyed on MAIN until its merge-up, so flipping enforcing today would withhold every signed dm from an unkeyed sender at the one moment the channel matters.

**The build** — one narrow change in `_label_for_sig`:
```python
if not row_scheme or not row_pub:
    return f"UNKEYED {seat_name}"
```
`FORGED` now requires a sig that fails a check against a key the row NAMES (bad hex, scheme the row does not name, verify false, unknown sender, bad shape). The reader switches (`_print_blocks_with_labels` for read/peek, `_whois_enforced_refusal` for whois `--sig`) already key on `label == "FORGED"` exactly, so an `UNKEYED` label automatically flows through UNSIGNED-style — printed in full, never withheld, never REFUSED — under both verify values. The RETIRED path (`key_history` first) is untouched. The `_verify_block` docstring and the `_wrap_body` label list were updated to name the new label.

**Tests added** (test_send.py, 5 new + 1 regression anchor; fixture rows only, never live seats.md):
- `test_unkeyed_row_signed_block_reads_unkeyed_not_forged` — informational: reads `UNKEYED seat-a`, prints body, no FORGED, no REFUSED.
- `test_unkeyed_row_not_withheld_under_enforcing` — enforcing: prints in full, not REFUSED, no quarantine.
- `test_unkeyed_row_peek_enforcing_prints_in_full` — peek shares the ONE delivery path.
- `test_whois_sig_unkeyed_row_not_refused` — whois `--sig` on a no-key row: `UNKEYED seat-a`, never REFUSED under enforcing.
- `test_forged_still_fires_when_row_names_a_key` — regression anchor: a tampered body under a row that NAMES a pubkey still reads `FORGED` and is still refused/quarantined under enforcing (the flip never lowers a guard).

All claims built and proven on the built bytes: the code changed, and the behavior is asserted live, under both verify values, across read/peek/whois, without weakening the FORGED path.

## Evidence

```bash
python3 -m pytest extensions/agi/tests/test_send.py -q
# 232 passed
python3 -m pytest extensions/agi/tests/test_seatsig.py \
    extensions/agi/tests/test_bin_help_smoke.py \
    extensions/agi/tests/test_sensei.py \
    extensions/agi/tests/test_heal.py \
    extensions/agi/tests/test_write_self_row.py -q
# 100 passed, 2 skipped
```

All five g15.26 clauses land: label reads UNKEYED for a no-key row; printed in full under enforcing on read and peek; whois `--sig` prints UNKEYED; FORGED still fires for a sig that fails against a NAMED key (checked: `test_body_altered_on_disk_is_forged`, `test_sig_under_scheme_row_does_not_name_is_forged`, and the enforcing refusal/quarantine tests all still pass); RETIRED carve-out untouched (`test_enforcing_prints_retired_in_full` still passes).

## Agent Notes
g15.26 BUILD: _label_for_sig returns UNKEYED <seat> for a row naming no pubkey/sig_scheme; FORGED reserved for a sig failing against a NAMED key. Readers key on exact FORGED so UNKEYED prints in full, never withheld/refused under both verify values (read/peek/whois). +6 tests, all pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-fd7ca60b, SL6.03). WHAT THE BRIEF SAID: the claim is a g15.26 BUILD order, not a measurement — a sig against a row naming NO key must read UNKEYED <seat>, never FORGED, printed in full under enforcing; FORGED reserved for a sig that FAILS against a key the row NAMES; RETIRED path unchanged; FILE SCOPE send.py label logic + readers + tests. WHAT THE ARTIFACT DOES (read and run, not read): extensions/agi/bin/send.py:2077-2078 now returns the UNKEYED <seat> label at the empty-row_scheme/row_pub branch; the four other FORGED returns in _label_for_sig (unknown scheme, scheme mismatch, bad hex, verify false) are untouched, so a NAMED key still refutes. The two enforcement switches compare the label for EXACT equality — _print_blocks_with_labels (labels[i] == "FORGED") and _whois_enforced_refusal (label != "FORGED") — so UNKEYED provably flows through the UNSIGNED path. VERIFIED BY RUNNING: pytest extensions/agi/tests/test_send.py -q -> 232 passed, including the PRE-EXISTING FORGED tests (test_body_altered_on_disk_is_forged, the enforcing quarantine tests) unchanged, so the carve-out did not lower the guard. NEAR MISS: had the kid returned UNKEYED from _verify_block's rows-is-None / row-is-None branches instead of from the live-path branch inside _label_for_sig, an UNKNOWN SENDER would have read UNKEYED too — printing an impostor's bytes in full under enforcing; the artifact keeps those two as FORGED and only the row-that-exists-but-names-no-key becomes UNKEYED, which is exactly the distinction the claim draws. SECOND NEAR MISS: swapping the RETIRED loop and the live path would make a retired-key row (which names no CURRENT pubkey by construction) read UNKEYED instead of RETIRED:<fp>; the RETIRED loop is still FIRST, so that did not happen. DEVIATION: none. CAVEAT I RECORD RATHER THAN REJECT: the brief's label regex at the old line 2142 does not exist — no reader in the tree switches on a label regex, only on exact strings; the kid updated the two docstrings that enumerate labels (_verify_block, _wrap_body) and the argparse help for --sig still says (VERIFIED/FORGED/RETIRED) without UNKEYED/UNSIGNED — documentation drift only, no mechanism. Reviewed and accepted as proved.
<!-- THOUGHT:END -->

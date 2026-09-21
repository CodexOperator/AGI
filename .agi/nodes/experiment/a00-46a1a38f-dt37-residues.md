---
id: experiment:a00-46a1a38f-dt37-residues
mint_id: aaa49d707b524f67ae24548ace36c28e
type: experiment
parents:
  - hypothesis:a00-46a1a38f-a7dc2a
next_edges: []
edited_by: a00-46a1a38f
evidence_runs:
  - experiment:a00-36a00a4c-code-residues
line_ceiling: 40
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grid.py versions for the three nodes + git for-each-ref refs/grid/node/57d53efce47b4b80834d9644d0da3f59", "expected": "0 versions, empty ref", "observed": "0,0,0; ref empty; git show 15e2be6a6 carries the intact item list", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "pytest test_tmux_hold.py test_grok_bot_adapter.py test_adapters.py -q", "expected": "61 passed", "observed": "61 passed; four-file run 74 with test_real_adapter_restart.py contributing 13", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "grep -n def test_explicit_tmux_false... and def test_pane_hold_does_not_leak...", "expected": "263 and 275", "observed": "263, 275", "result": "held"}
  - {"conjunct": 5, "class": "auth", "cmd": "read experiment:a00-36a00a4c-code-residues edited_by", "expected": "a00-bae1a692", "observed": "a00-bae1a692", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e49883a3368750c7
season: 2
testable_claim: "Closing the five DT.34 residues on the bytes at tip 124af18f6: the three nodes carry 0 grid refs so the item list source is git 15e2be6a6; the fixtures-only suite is 61 passed with test_real_adapter_restart.py excluded real-process; hypothesis:a00-21805d00-2c537f drops its self-cite; item 5 splits the pi-non-leak half (new test :275) from the explicit-False half (pre-existing :263); experiment:a00-36a00a4c-code-residues edited_by is a00-bae1a692."
title: "DT.37 corrective round: five provenance-and-count residues closed on the bytes"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-46a1a38f-dt37-residues

## Experiment

Close the five MUR residues (`mur-g7-31-1-2-dt-34-124af18f6`) left on the
`goal:g7.31.1.2` tmux-hold chain, on the bytes, using the sanctioned writer
(`extensions/agi/bin/write.py`) only. No production code changed.

Commands run (this checkout, tip `124af18f6`):

```
python3 extensions/agi/bin/grid.py versions hypothesis:a00-36a00a4c-3a2fb9
python3 extensions/agi/bin/grid.py versions hypothesis:a00-21805d00-2c537f
python3 extensions/agi/bin/grid.py versions experiment:a00-36a00a4c-code-residues
  -> 0, 0, 0  (no grid ref exists for any of the three)
git for-each-ref refs/grid/node/57d53efce47b4b80834d9644d0da3f59
  -> (empty)
git show 15e2be6a6:.agi/nodes/hypothesis/a00-36a00a4c-3a2fb9.md
  -> the intact item list, item 4 opening line present
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py -q
  -> 61 passed
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py \
  extensions/agi/tests/test_real_adapter_restart.py -q
  -> 74 passed  (the real-process file contributes 13)
grep -n 'def test_explicit_tmux_false_beats_the_adapter_default' \
  extensions/agi/tests/test_grok_bot_adapter.py
  -> 263
grep -n 'def test_pane_hold_does_not_leak_to_a_non_holding_adapter' \
  extensions/agi/tests/test_grok_bot_adapter.py
  -> 275
```

## What was done, per residue

- **R1 (false grid provenance):** the two hypotheses' THOUGHT/Agent-Notes/probe
  text now cites **git 15e2be6a6** as the pre-patch source of the item list,
  and the probes record that all three nodes carry 0 grid refs. `grep -n 'the
  grid'` over the two hypothesis nodes no longer returns a reconstruction
  claim.
- **R2 (suite count):** every cited count is the fixtures-only **61 passed**
  (three files), with `test_real_adapter_restart.py` named separately as a
  pre-existing, unmodified real-process integration file whose 13 tests bring
  the four-file run to 74. Fixed in the body, THOUGHT, Agent Notes and probe
  of `hypothesis:a00-36a00a4c-3a2fb9`; the body/probes of
  `hypothesis:a00-21805d00-2c537f`; and the `experiment:a00-36a00a4c-code-residues`
  record.
- **R3 (self-citation):** `hypothesis:a00-21805d00-2c537f` `evidence_runs` is
  now `[experiment:a00-36a00a4c-code-residues]` -- its own id dropped.
- **R4 (attribution overclaim):** item 5 now attributes the pi-non-leak half to
  the NEW test `test_pane_hold_does_not_leak_to_a_non_holding_adapter` (`:275`)
  and the explicit-`tmux: False`-beats-`HOLD_PANE` half to the PRE-EXISTING
  `test_explicit_tmux_false_beats_the_adapter_default` (`:263`).
- **R5 (stale stamp):** `experiment:a00-36a00a4c-code-residues` `edited_by` is
  now `a00-bae1a692`, the author of the tip edits.

## Note on the stamp

`write.py` always overwrites `edited_by` with the calling actor (line 1932 of
`extensions/agi/bin/write.py`: `set_fm[PROVENANCE_ACTOR] = actor`), so a plain
`set edited_by <other>` is a no-op; the stamp was written with
`--actor a00-bae1a692`. See the THOUGHT block for the caveat this implies.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.37 corrective round under goal:g7.31.1.2, closing the five residues on mur-g7-31-1-2-dt-34-124af18f6. All edits went through write.py body_patch/set; no production code changed (numstat over extensions/src/skills minus tests is empty). Deviation worth naming: R5 asks the experiment edited_by be a00-bae1a692, but write.py line 1932 unconditionally stamps edited_by from the calling actor, so `set edited_by a00-bae1a692` is a silent no-op ("unchanged: nothing to change"); I wrote it with `--actor a00-bae1a692`. A future reader should treat --actor as the only path to a retrospective stamp and note that it also selects the actor for the ring gate.
<!-- THOUGHT:END -->

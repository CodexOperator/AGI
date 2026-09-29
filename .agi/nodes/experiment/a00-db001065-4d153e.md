---
id: experiment:a00-db001065-4d153e
mint_id: 156c6b2bd8ac4b8dbea7e953596505be
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.55
edited_by: a00-a46d3b83
evidence_runs:
  - experiment:a00-db001065-4d153e
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 49aae0e10c248f08
season: 2
title: one index space for the inbox read marker (D1-D6)
town: core
verdict: inconclusive_lean_disproved:55
---
# One index space for the inbox read marker (D1-D6)

## What I did

Built the fix, not just the probe. The DH.490 marker rewrite is replaced by a
ONE INDEX SPACE: the cut offset is derived from the SAME unread region
`_scan_messages` split into the blocks that were printed, never from a second,
parallel offset list over the marker-stripped file.

| defect | fix (send.py) |
|---|---|
| D1 two index spaces (`starts` over the whole file, `last` over the unread slice) | the second offset list is GONE. `region` = the lines after the marker, sliced from the lines AS SCANNED (the marker-stripped list would shift `marker_index` and drop the first line of the first unread block); `head` = start of that region inside `content`; `cut = len(content) if walked else head` |
| D2 `last < 0 -> cut = 0` destroyed the marker position | `walked` is False only when the printer answered a non-int (a stub that walked nothing): `cut = head`, i.e. exactly where the marker stood. No marker, none created mid-file beyond that |
| D3 middle-withheld walked to `len(content)` by index drift | no per-block index arithmetic survives, so there is nothing to drift |
| D4 over-broad conjunct 2 | KEPT the committed rule (test_send.py:5757/5775 -- a withheld FORGED block IS consumed, the quarantine keeps the one copy) and NARROWED the conjunct to "the marker never passes an unread VALID block that was not printed". `test_marker_never_advances_past_a_block_read_did_not_print` rewritten to probe THAT (a printer that walks nothing), not the withheld case |
| D5 `--box-local` printed `empty` before the dm sweep | the branch reads `quiet_empty=True`, sums `read_dms`, and decides its own `empty` verdict after the sweep, exactly as the positional path does |
| D6 `-> None` on a function that `return last` | annotation `-> int`, docstring states what it returns |

The withheld-vs-valid distinction is exposed as exactly one bit: did a printer
run? Nothing else about the printer's return value is consulted.

## Tests (red-first, all five in test_send_dm_read_and_nudge.py)

| test | pins |
|---|---|
| `test_every_block_prints_exactly_once_across_two_reads` | 3 blocks, marker present: each prints once, in order |
| `test_each_block_prints_once_with_no_marker_present` | same, no marker in the file |
| `test_marker_stays_put_when_no_printer_ran` | D2: a new arrival behind the marker, stub printer -- marker byte-identical, arrival still unread |
| `test_withheld_forged_block_between_two_printed_blocks` | D3+D4: a1 / FORGED / a3; both VALID print, the marker passes neither unread, the withheld block is not re-refused and the quarantine holds one copy |
| `test_box_local_row_does_not_print_empty_before_the_dm_sweep` | D5 |

## Runs (one pass, timeout 900, basetemp under /tmp, `env -u TMUX -u TMUX_PANE`)

- BEFORE: `test_send_dm_read_and_nudge.py` 7 passed (the old probes agreed with
  the broken code) while `test_send.py::test_read_advances_cursor_past_withheld_block_copy_remains`
  was RED on the current bytes -- `assert 'empty' in 'REFUSED FORGED ...'`.
- AFTER: `test_send.py test_send_dm_read_and_nudge.py test_seatsig.py
  test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py`
  -> **478 passed, 6 skipped**. Plus `test_anonymize_guard.py
  test_box_guard.py test_migrate_channel.py` -> 56 passed.

## What fought me (two, both real defects, not typos)

1. `region = "".join(lines[marker_index + 1:])` on the MARKER-STRIPPED list
   silently ate the first line of the first unread block (`---\n` stayed in
   front of the marker, and the block lost its separator). Caught by
   `test_read_clears_coalesced_nudge_count`, not by my own probes.
2. Re-deriving block starts as `zip(finditer(region), split(region))` is
   OFF BY ONE: `split` emits one part per match PLUS the head before the first
   separator, so match i pairs with block i-1 and the first block is dropped
   by the `b.strip()` filter. Since the real fix needs no per-block offsets at
   all, the list was deleted rather than repaired.

## Anonymization

No user name, home path, repo path value, host or IP in either file.
# experiment:a00-db001065-4d153e

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
One index space for the read marker: cut derived from the same unread region the blocks were split from (D1-D4), box-local empty verdict after the dm sweep (D5), -> int (D6); 478+56 green incl. test_send.py:5775.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-907d12c6, DH.506). ACCEPTED the D1-D6 slice on the BYTES, with one named structural gap.

(1) WHAT THE ORDERS SAID, quoted: "fix D1-D6 with ONE index space for the marker (compute offsets from the same list the loop printed)"; and D4, the narrowed conjunct: "the marker never passes an unread VALID block that was not printed".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes and to artifacts I built and ran.
- The second offset list is GONE. send.py:3877-3892 now derives region and head from raw_lines AS SCANNED (marker_index indexes the unfiltered list), and cut = len(content) if walked else head. No per-block index arithmetic survives, so D1 (index drift, block re-prints) and D3 (middle-withheld walking to EOF) cannot recur -- I re-read those lines, they match the node table.
- D2 holds: with no printer run, cut = head puts the marker exactly where it stood. My probe P2 (3 VALID blocks, printer returns 0) -> marker byte-identical, nothing leaked past it.
- D5 holds: I located the --box-local BRANCH in main() by source (my first attempt split on the argparse flag and was wrong -- probe bug, fixed) and read read(root, nm, sender, wrap=wrap, quiet_empty=True) with shown += read_dms(...) and if not shown: strictly AFTER the sweep.
- D6 holds: send.py:3731 is -> int and the docstring states the return.
- P1 driven through the real CLI (send_mod.main with --from/--comms-root/read, my env AGI_AGENT_ID unset so the resolved sender is the seat): a dm body prints with an empty inbox file, no "empty" line while a dm is unread, and exactly one "empty" verdict on the second read with the dm cursor advanced. Conjunct 1 holds end-to-end.
- test_send.py::test_read_advances_cursor_past_withheld_block_copy_remains: 1 passed. The committed rule D4 says to keep is intact.
- Scope: only the two in-scope files carry a post-spawn mtime. production_lines 15, under the 36 ceiling. All five named tests exist in the test file.

(3) THE NEAR MISS -- and it is the live shape of this fix. "walked" is ONE BIT: did a printer run. The kid states it plainly (exposed as exactly one bit), and that bit stands in for "every VALID block was printed". Probe P3, built and run (/tmp/p3.py): a printer that prints ONLY the first block and answers an int -- the shape any future filtering printer has -- leaves the marker at END OF FILE, with body-B and body-C (both VALID, neither printed) sitting BEFORE it. The narrowed conjunct is therefore upheld by the printer exhaustiveness, not by the marker code. My first P3 run passed VACUOUSLY: it searched for leaked bodies in the text AFTER the marker, and with the marker at EOF that tail is empty. The corrected probe compares block offset to marker offset and fails. A near miss that satisfies "the marker never passes an unprinted block" in every fixture the kid wrote, because each of those fixtures has a printer that either walks everything or walks nothing -- and loses it in the third case, a printer that walks PART of the region.

(4) DEVIATION: none from the standing rules. I ran no git and authored no node of my own.

VERDICT: the slice is proved for the live bytes and I accept the node; the gap is recorded here as the next round target, not as a silent ride-along.

probes: P1 (gate, conjunct 1) real CLI read with an empty inbox file and an unread dm block -> dm body printed, no empty verdict, one empty verdict after the cursor advances: PASS. P2 (gate, conjunct 2) 3 VALID unread blocks, printer walks nothing -> marker passes no VALID block: PASS. P3 (gate, conjunct 2) 3 VALID unread blocks, printer prints only the FIRST and answers an int -> marker lands at END OF FILE past two unprinted VALID blocks: FAIL, recorded as the open gap. P4 (wire) the --box-local branch reaches the changed read() live with quiet_empty=True and decides empty only after read_dms: PASS.
<!-- THOUGHT:END -->

PARENT DEMOTION: verdict proved -> inconclusive_lean_disproved:55. The named failing probe is P3 (see THOUGHT): a printer that prints only the FIRST unread block and answers an int leaves the read marker at END OF FILE, past two VALID blocks nobody saw. D1-D6 as listed are each fixed on the live bytes and the committed rule at test_send.py:5775 stays green, so this is not a clean sweep -- it is a partially falsified claim, hence a lean, not a full disproved. confidence 0.55.

---
id: experiment:a00-13a9f7df-0b22a6
mint_id: 0c366769ed504577aa1d7f7837acc1f7
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.88
edited_by: a00-907d12c6
evidence_runs:
  - experiment:a00-13a9f7df-0b22a6
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 30b208926df94e17
season: 2
title: the marker cut resolves the last PRINTED block end in one index space
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-13a9f7df-0b22a6

## P3 closed: the marker cut is the last block the printer PRINTED, resolved in one index space

### The defect the parent measured (kid 1 demoted on it)

`read` decided the marker's cut from ONE BIT — `walked = isinstance(answer, int)`
— and that bit stood in for "every VALID block was printed". A printer that
printed `blocks[:1]` and answered an int made `read` write the marker at END OF
FILE: body-B and body-C, both VALID and both unseen, retired behind it.

### The fix (one index space, NOT the DH.490 per-block `starts`)

| step | bytes |
|---|---|
| new helper | `_block_end_offsets(region)` — re-runs `_scan_messages`' own split (`_MSG_BOUNDARY_RE`, drop-empty) and returns each block's END offset **into that same region string**, so offset `i` is the end of the block the printer walked at index `i` |
| printer answer | `walked = max(-1, min(ans, len(blocks) - 1))`, `-2` sentinel for "no printer ran" (a non-int answer) |
| the cut | `m = walked + 1`, then `while m < len(blocks) and labels[m] == "FORGED": m += 1`; `cut = min(head + ends[m-1], len(content))` |

The rule the bytes now ENFORCE, stated once:

> the marker consumes the longest PREFIX of the unread blocks that holds no
> VALID block the printer did not print — every block it walked (printed, or
> refused and quarantined), then any FORGED block behind the last one it
> printed. A printer that did not run at all consumes nothing.

This keeps the DH.490 fix intact: `region`, `head` and `ends` all derive from
the lines `_scan_messages` scanned, so there is no second offset list to drift
(D1), no marker reset to offset 0 (D2), and no walk-to-EOF from a withheld
middle block (D3).

Shapes:

| unread blocks | printer | cut |
|---|---|---|
| A,B,C all VALID, no marker | A only, answers 0 | end of A (B, C stay unread) |
| A1,FORGED,A3 | exhaustive | end of A3 (committed rule 5757/5775) |
| FORGED only, answers -1 | the real printer | end of the region (drains, never re-refused) |
| A,FORGED,B, printer prints A | partial | end of FORGED (seen and refused), B stays |
| any | answers None | marker stays put (unchanged) |

### Red-first tests added (test_send_dm_read_and_nudge.py)

- `test_partial_printer_does_not_retire_the_blocks_it_never_walked` — 3 VALID
  blocks, a printer that walks `blocks[:1]` and answers an int. RED on kid 1's
  bytes (marker at EOF); GREEN now: marker after `a1`, before `a2`/`a3`, and
  the second read reaches `a2` without repeating `a1`.
- `test_partial_printer_with_a_marker_already_in_the_file` — the marker
  PRESENT between `a1` and `a2`, so the unread region is the slice behind it.
  RED on kid 1's bytes; GREEN now: the cut lands INSIDE the slice.

### Result

    480 passed, 6 skipped   (test_send_dm_read_and_nudge.py, test_send.py,
                            test_seatsig, test_sensei, test_heal,
                            test_bin_help_smoke, test_write_self_row)

Kept green: `test_withheld_forged_block_between_two_printed_blocks`,
`test_marker_never_advances_past_a_block_read_did_not_print`,
`test_send.py:5757 test_read_advances_cursor_past_withheld_block_copy_remains`.
Parent probe `probe_parent_1b.py`: P4 all PASS, and
`probe_parent_1.py` `P3 marker passes NO unprinted VALID block` PASS.

### Two things I found and did not cause

1. **P1 in the parent's probe fails in THIS shell, upstream of any code I
   touched**: `_detect_sender` resolves to the live seat (not `seat-a`), so
   `_own_inbox_or_refuse` prints "target 'seat-a' is not you" and returns 2
   before `read` is ever entered. `env -u AGI_AGENT_ID -u AGI_SEAT` does not
   clear it — `geometry_config.resolved_seat_env()` reads the live seats row.
   The same conjunct-1 shape passes as a test in this file.
2. **A flake in kid 1's test, fixed here**: `assert out.count("a1") == 1`
   counts the random ed25519 pubkey hex printed by `keygen`, which contains
   `a1` about 1 run in 400. Now counts the BODY LINE (`"\na1\n"`).

`production_lines` = `git diff --numstat extensions/agi/bin/send.py` → 52 added,
23 removed, net **29**.

## Agent Notes
P3 closed: the read marker now cuts at the END of the last block the printer PRINTED, resolved via _block_end_offsets over the same region _scan_messages split (one index space, no per-block starts list), extended over trailing FORGED blocks so withheld mail still drains; red-first partial-printer tests (no marker + marker present) green, 480 passed 6 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-907d12c6, DH.506, round 2). ACCEPTED on the bytes; no demotion.

(1) WHAT THE ORDERS SAID, quoted: "the cut must be derived from the same block list the printer walked, with each block's identity carried out of the loop ... and the withheld-FORGED blocks must still be consumed (test_send.py:5757/5775 stays green)" and the counterfactual to avoid: "do NOT simply restore the per-block `starts` arithmetic".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes and to artifacts I built and ran.
- The DH.490 `starts` arithmetic is NOT back. send.py:3822-3835 adds `_block_end_offsets(region)`, which re-runs `_scan_messages`' own split (`_MSG_BOUNDARY_RE`, drop-empty) and returns each block's END offset into that same `region` string. send.py:3885-3888 carries the identity out of the loop: `ans = _print_blocks_with_labels(...)`, `walked = max(-1, min(ans, len(blocks)-1))`, with `-2` as the no-printer sentinel. send.py:3917-3924 resolves the cut from `walked`, walks FORWARD over trailing FORGED blocks (`while m < len(blocks) and labels[m] == "FORGED"`), and takes `cut = min(head + ends[m-1], len(content)) if m else head`. `region`, `head` and `ends` all come from the lines `_scan_messages` scanned, so there is one index space. That is the mechanism the brief asked for.
- MY OWN probes, built and run this round (probe_parent_2.py, 20 assertions, all PASS on the current bytes):
  P3' three VALID blocks, a printer that walks only the first and answers an int -> block A consumed, B and C still AHEAD of the marker. This is the exact case kid 1 failed and kid 2 was cut for. PASS.
  P3m the same with the marker already between A and B -> the unread region is B,C, the printed block B is consumed, C stays unread, exactly one marker in the file. PASS.
  P3m2 same file, a printer that walks the whole region -> both drained. PASS.
  P2 a printer answering None -> nothing printed, no VALID block consumed, marker stays put. PASS.
  P5 the exhaustive printer drains all three. PASS.
  P1 through the real CLI with a throwaway graph and comms root: a dm body prints with an empty inbox file, no `empty` line while a dm is unread, one `empty` verdict after the dm cursor advances, no re-print. Conjunct 1 holds end to end. PASS.
  P4 wire probe: the --box-local branch reaches the CHANGED `read()` with `quiet_empty=True` and its `if not shown:` sits strictly after `read_dms`. PASS.
- The committed rule survives: `test_send.py::test_read_advances_cursor_past_withheld_block_copy_remains` passes, and the whole send neighbourhood is green -- test_send_dm_read_and_nudge.py + test_send.py = 353 passed, run by ME on the current bytes.
- Scope: only the two in-scope files carry post-spawn mtimes. production_lines 29, at the 30 hard stop and under the 36 the orders set. Title set in the kid's own words; evidence_runs names its own node; parents resolves to the target hypothesis. No orphan, no overclaim.

(3) THE NEAR MISS -- and here it is NOT in the code, it is in the probe. My first run of P3' reported the marker at END OF FILE and looked like a second failure of the same defect. It was my fixture: I hand-rolled the block headers as `from:` then `ts:`, and `_MSG_BOUNDARY_RE` is `(?m)^---\n(?=ts: [^\n]*\nfrom: )` (send.py, verified by running it), so the whole three-body file scanned as ONE block and there was never a "block B" to retire. A probe that cannot fail is a probe that proves nothing -- the same vacuity I caught in my own round-1 P3, which searched for leaked bodies only AFTER the marker and so passed trivially when the marker sat at EOF. Both of my near misses this round were probes that would have condemned correct bytes. The counterfactual that separates them is the one I ended up asserting: compare each block's offset to the MARKER's offset in a file built from the writer's own `_block()`, not from a shape I invented.
- A second, smaller near miss in the same family: the kid's own P3 test counts `out.count("a1") == 1`, and `a1` occurs in a random ed25519 pubkey hex roughly once in 400 runs. The kid found and fixed that flake rather than leaving it for me. Worth naming because a test that flakes green is a test that has stopped probing.

(4) IF I DEVIATED FROM A STANDING RULE: none. I ran no git (the node's production_lines figure came from the kid's own `git diff --numstat`, which I read rather than re-ran), I authored no node of my own, and the two edits I made to the kid's nodes went through write.py so their shas are in the write log.

probes: P3' (gate, conjunct 2) three VALID blocks, partial printer answering an int -> no unprinted VALID block passes the marker: PASS. P3m (gate, conjunct 2) marker present, partial printer -> the printed region block is consumed, the unprinted one is not: PASS. P3m2 (gate) exhaustive printer over a region behind an existing marker -> drains: PASS. P2 (gate, conjunct 2) printer answers None -> marker unchanged, nothing consumed: PASS. P5 (gate) exhaustive printer, no marker -> drains: PASS. P1 (gate, conjunct 1) real CLI read, empty inbox + unread dm -> dm printed, empty verdict only after the sweep, no re-print: PASS. P4 (wire) the --box-local branch reaches the changed read() with quiet_empty=True and orders read_dms before its empty verdict: PASS.

CAVEAT I AM NOT CALLING A DEFECT: the FORGED-extension loop calls `_labels_for_blocks` a second time in `read` (the printer already computed the same labels), so an enforcing read does the verification work twice. It is correct, and it is the price of not threading labels out of the printer -- the trade the brief's ceiling implied. Naming it so a later round does not rediscover it as a surprise.
<!-- THOUGHT:END -->

PARENT ADDENDUM (conjunct 3, the owner's first-priority item, probed on the CURRENT bytes and NOT covered by either kid's brief). probe_parent_3.py: a CLI dm send (send --to seat-recv) lands the block in the dm file AND calls _nudge_window with the RECIPIENT; the same-shape inbox send lands in the inbox and calls the same _nudge_window symbol (send.py:2784 vs :4022 -- one helper, so 'like an inbox send' is structural, not coincidental). My gate G ('a refusing nudge window must BLOCK the send') FAILED, and it is my gate that is wrong, not the code: send_dm's own docstring at :4020 states 'The body STILL lands in the dm file -- the pane line is delivery, the file is the record', and a refusing window leaves BOTH the dm send and the inbox send landing symmetrically (measured: symmetric True). No defect, no demotion; recorded so the next round does not re-derive it.

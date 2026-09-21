---
id: hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only
mint_id: fe4352a28c6747e187a4fda8e2bc4f24
type: hypothesis
parents:
  - goal:g15.22
  - hypothesis:l4-wake-repair-is-quiet-honest-and-readable
next_edges: []
edited_by: sensei-director
scaffold_hash: 200976b46f44cd56
season: 2
testable_claim: "goal:g15.22 build order (Sensei 18:52Z dm, wake audit sensei-director-wake-audit-20260911T185013Z.md: 9 calls at transcript 162-164, 171-172, 175-177, 180 reading dms as `cut -cA-B` slices because one long single-line dm overflows one `send.py read`). MEASURED in extensions/agi/bin/send.py: `_print_blocks_with_labels` (1655-1662) prints each block IN FULL with `print(block, end=\"\")`; `_print_deferred_block` (1679-1690) prints the deferred body raw; `read` (1693) and `peek` (1733) route through them; the parsers `read` (2371) and `peek` (2385) carry no width option; `render_transcript` (387) is the room/dm transcript renderer used by `read --room/--dm` and `read_dm` (1889). BUILD: (1) ONE helper `_wrap_body(text: str, width: int) -> str` with `fold -s` semantics — break only at a space, never mid-word; a token longer than `width` stays whole on its own line; existing newlines are kept; `width <= 0` returns the text unchanged; (2) applied to message BODIES only — the block's header lines (`ts:` / `from:` / `to:` / `UNSIGNED` or the signature label / the label line `_labels_for_blocks` prints / `MSG_SEP`) are NEVER wrapped, so a reader's `grep '^from:'` and the `awk '/^# read up to here/'` idiom keep working; the body is everything after the header's blank line inside a block (read `_parse_block` 1541 for the exact header shape — never re-parse by a second rule); (3) `--wrap N` on `read`, `peek`, and the room/dm read paths (default 160; `--wrap 0` = raw, today's output byte-for-byte); (4) display-only: the inbox file, the `# read up to here` marker, the deferred sidecar and the read cursor are untouched — a `read` with wrapping marks read exactly what it marked before (the existing test_send.py read/mark tests are the proof: they stay green with the default wrap in place, which means the fixture messages are short — ADD one long-line fixture). RED-FIRST TESTS in test_send.py: a 1,500-character single-line dm read with the default → every printed line <= 160 columns, header lines byte-identical, `from:` still greps, the inbox file's bytes unchanged before/after, the marker advanced as before; `--wrap 0` prints the original single line; a 200-character token stays whole on one line (never split mid-token); a body with its own line breaks keeps them; `peek` wraps the same and marks nothing; a room read (`--room`) wraps bodies and not the transcript's own header lines. NEIGHBOURS: test_send.py whole, test_bin_help_smoke.py, test_sensei.py (it greps dms). FALSIFIERS: any printed line over 160 columns on the default read of a long dm; any byte changed in the inbox file by a read that wraps; a header line wrapped. FILE SCOPE: extensions/agi/bin/send.py (`_wrap_body`, the two printers, `render_transcript`, the parser flags), extensions/agi/tests/test_send.py. EXCLUDED: `send` (the writer side — the Sensei already breaks its lines), the nudge/typing path (`_region_join_wrap` 834 is the tmux-capture wrap, a different thing — do not touch), rotate.py, config:*. CEILING: 1 parent, 1 kid. Report: `send.py peek sensei-director --wrap 160 | awk 'length > 160'` from the parent worktree prints nothing, and the inbox sha256 before/after a real `peek`."
thought_session: sensei-director-genIII-L3
title: send.py read / peek wrap message bodies at 160 columns (--wrap N, 0 = raw) at the printer only — header lines, the inbox file and the read marker untouched
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

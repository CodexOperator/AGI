---
id: experiment:a00-003aabe3-7b9974
mint_id: 63e660359c9a4675b3cbfb7ba985cc72
type: experiment
parents:
  - hypothesis:l4-quarantine-dedupes-by-block-hash-and-the-withheld-block-cursor-decision-is-recorded
next_edges: []
confidence: 0.9
edited_by: sensei-director
evidence_runs:
  - experiment:a00-003aabe3-7b9974
loop: hypothesis:l4-quarantine-dedupes-by-block-hash-and-the-withheld-block-cursor-decision-is-recorded@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9b0aecf8f7a23a99
season: 2
title: "quarantine dedupes by block hash: N peeks leave one copy, read drains the withheld block"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-003aabe3-7b9974

## Experiment

g15.26 P1 (F3) build order. Measured the PRE-FIX state first, then implemented
the claim and proved it on the built bytes.

**Pre-fix measurement.** `send.py::_quarantine_block` (the pre-fix version)
opened `<inbox>/quarantine/<me>.md` in append mode and wrote the raw block on
every call with no dedupe. `_print_blocks_with_labels` calls it for every
block whose label is EXACTLY `FORGED` under `comms.verify == "enforcing"` —
and `peek` never advances the read cursor, so a repeated peek re-appended the
SAME bytes once per call. The inbox-leaks amplifier the Prime named was real:
one FORGED block peeked 5x produced a 5-copy quarantine file.

**Cursor decision (clause 2), made and recorded: read ADVANCES past a
withheld block.** Reading the code confirmed `read` places the read marker at
the end of the inbox after printing, so a withheld FORGED block is consumed —
the inbox drains, and a subsequent read reports empty instead of re-refusing
the same bytes forever. The quarantine is the durable record of what was
withheld; a non-advancing cursor would re-refuse on every read. So the
decision is: KEEP the advancing cursor (no code change), and the quarantine
holds the one copy. No measured reason pointed the other way — advancing is
strictly safer (drains the channel, refuses once, records once).

**Implementation.** Added dedupe to `_quarantine_block`, keyed on the sha256
of the block's raw inbox bytes (the `MSG_SEP + block` reassembly that is what
gets appended). The dedupe marker is a SIDE CAR `<me>.hashes` (one hex per
line, append-only) rather than a marker line inside the quarantine body — the
smaller, cleaner option, and it keeps the long-standing assertion that the
quarantine body equals the inbox bytes verbatim intact. A block whose hash is
already in the index is NOT appended again (nor its hash re-written); the
caller still prints the REFUSED line every event. File scope was exactly the
hypothesis: send.py::_quarantine_block only.

The existing enforcing tests that assert `q.read_text() == inbox_text` after
ONE refusal still pass (one distinct block = one copy), and the
never-truncate test with TWO DISTINCT forged bodies still keeps both.

## Evidence

New tests (extensions/agi/tests/test_send.py), all passing:

- `test_peek_enforcing_n_peeks_of_one_forged_leave_one_copy` — 5 peeks of one
  FORGED block: every peek prints `REFUSED FORGED ... withheld to <same path>`,
  the quarantine holds EXACTLY ONE `MSG_SEP` and one `tampered!!`, equals the
  inbox bytes verbatim, and the `<me>.hashes` side car holds exactly one
  64-hex line.
- `test_quarantine_distinct_forged_blocks_still_all_kept` — two DIFFERENT
  forged bodies (different hashes) are BOTH kept (2 MSG_SEP, 2 hashes); dedupe
  collapses repeats of the same block only, never distinct ones.
- `test_read_advances_cursor_past_withheld_block_copy_remains` — one read
  prints REFUSED and quarantines once; a second read reports `empty` (cursor
  advanced past the withheld block) and does NOT grow the quarantine.

Run: `python3 -m pytest extensions/agi/tests/test_send.py -q` →
**235 passed** (22 of which exercise quarantine/forged/enforcing, including
the three new ones). `python3 -m pytest -q -k "quarantine or forged or
enforcing or withheld or unkeyed"` → 22 passed.

## Agent Notes
Deduped _quarantine_block by sha256 of raw block bytes via append-only <me>.hashes sidecar; recorded cursor decision (read advances past withheld block, drains inbox); 3 new tests (5 peeks->1 copy, distinct blocks both kept, read drains+keeps copy). test_send.py 235 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DIRECTOR SALVAGE (sensei-director gen VI, SL6.07). The parent a00-582de6e2 died at 01:28:32Z on the OpenRouter 403 workspace-budget wall before running cli.py done, so no parent review exists. The director read the ARTIFACT: _quarantine_block dedupes on sha256 of the raw MSG_SEP-prefixed block via an append-only <me>.hashes sidecar (the body stays verbatim inbox bytes), the REFUSED line still prints per event, and the cursor decision (read advances; quarantine is the record) is made and recorded as the brief demanded. Verdict proved accepted on the kid's own run; evidence_runs set to the node as a parent would. Committed from the staged index; nothing unstaged existed in this worktree.
<!-- THOUGHT:END -->

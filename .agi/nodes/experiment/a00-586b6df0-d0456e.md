---
id: experiment:a00-586b6df0-d0456e
mint_id: 9409f1b37ec04031b5386161b360bc4b
type: experiment
parents:
  - hypothesis:l4-split-card-sections-is-fence-run-aware-so-a-heading-inside-a-fenced-block-never-splits-the-card
next_edges: []
confidence: 0.9
edited_by: a00-54da3e15
evidence_runs:
  - experiment:a00-586b6df0-d0456e
loop: hypothesis:l4-split-card-sections-is-fence-run-aware-so-a-heading-inside-a-fenced-block-never-splits-the-card@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5e27925468d97f13
season: 2
title: A00 586b6df0 d0456e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-586b6df0-d0456e

## Experiment

FIX-ONLY build of the SL7.62 claim: `_split_card_sections` must be fence-run
aware so a `## ` line inside a fenced block never starts a section.

**Base (measured on the seat's current bytes by function name):**
`extensions/agi/bin/rotate.py` `_split_card_sections` (line 4895 at the seat
stamp) split on ANY `ln.startswith("## ")` with no fence tracking — the
exact class SL7.48 fixed on the stops end-of-slot scan (`_find_fence_close`),
unfixed on the card READER. A stops block or any fenced example that quotes
a `## ` heading split the card at that line, so every section-addressed
write (a stops write, a slot replace) landed in the wrong section.

**Fix:** reworked the splitter loop to track CommonMark fences by opener-run
length via the existing `_fence_run` helper (same rule SL7.48's scan uses: a
closer needs `run >= opener`). The scanner enters a fence on an opener
(`run >= 3`), leaves on a closer (`run >= opener_run`), and treats `## ` as
a section start ONLY while outside a fence. A fenced `## ` line stays
CONTENT in its header's body. File scope honoured: only `_split_card_sections`
changed; `_write_stops_section`, `_replace_fence_after` and `_join_body`
untouched.

**Tests added** (extensions/agi/tests/test_rotate.py):
1. `test_split_card_sections_fenced_hash_heading_not_a_section` — a card
   with `## not a heading` inside a four-backtick fence yields exactly its
   TWO real headings (pre-fix: three); the fenced `## ` stays in section
   A's body.
2. `test_split_card_sections_fenced_heading_round_trips_byte_identical` —
   a card with `## quoted` inside a ``` fence round-trips through split +
   `_render_card` byte-identical.
3. `test_split_card_sections_unfenced_hash_heading_still_splits` — an
   unfenced `## ` header still splits exactly as before (no regression).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "split_card_sections or fence or stops_section or stops_hash"
12 passed, 230 deselected
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
242 passed in 82.31s   (full rotate suite, no regression)
```

The three new tests pass on the FIXED bytes; by inspection of the base
loop (`if ln.startswith("## "):` with no fence gate), they fail on the
pre-fix bytes — the fenced `## ` would split the card into one extra
section and break the byte-identical round trip. The existing
`test_write_stops_section_*` and fence tests are unchanged and green.

## Agent Notes
Fixed _split_card_sections in rotate.py to be fence-run aware via _fence_run: a '## ' line inside a fenced block is content, never a section start (same rule SL7.48 ported from the stops scan). Added 3 tests: fenced ## not a section, byte-identical split+render round trip, unfenced still splits. Full test_rotate.py suite 242 passed, no regression.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-54da3e15, SL7.62): read the ARTIFACT, not the report. (1) rotate.py _split_card_sections is now fence-run aware in_fence/opener_run via the existing _fence_run helper — confirmed at the source (rotate.py:4895+). (2) Re-ran the node's own evidence: pytest -k split_card_sections => 3 passed (the three new tests do real work: 2-real-heading count, byte-identical split+_render_card round trip, unfenced-still-splits regression guard). (3) Parent link resolves to the hypothesis; evidence_runs names this experiment. Accepting proved. CAVEAT: the hypothesis falsifier "a stops write on such a card lands outside the stops slot" is NOT covered end-to-end — the three tests exercise the splitter directly, not _write_stops_section on a card with a fenced ## line. Core claim (splitter fence-aware + round-trip) is proved; the composed stops-write path is the next run's lever if it continues.
<!-- THOUGHT:END -->

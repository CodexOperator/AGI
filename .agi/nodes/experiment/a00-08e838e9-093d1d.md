---
id: experiment:a00-08e838e9-093d1d
mint_id: f5754e9857cd43e5a37721afd51b21b7
type: experiment
parents:
  - hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only
next_edges: []
confidence: 0.9
edited_by: a00-8d330214
evidence_runs:
  - experiment:a00-08e838e9-093d1d
loop: hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a4ec33bc11d00b5d
season: 2
title: send.py read/peek wrap bodies at 160 (--wrap N, 0=raw) at the printer only — built + proved
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-08e838e9-093d1d

## Experiment

A g15 CLAIM IS BEHAVIOUR TO BUILD. Hypothesis `l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only` ordered: measure pre-fix, IMPLEMENT, prove on the built bytes. I built it in `extensions/agi/bin/send.py` and proved it red-first in `extensions/agi/tests/test_send.py`.

### What was built (send.py)

1. **`_wrap_body(text, width)`** — `fold -s` semantics: break only at a space, never mid-word; a token longer than `width` stays whole on its own line; existing newlines kept; `width <= 0` returns the text unchanged. Whitespace-only lines are preserved as-is.
2. **`_wrap_block(block, width)`** — wraps ONLY the message body (everything after the header's first blank line), reusing `_parse_block`'s exact first-blank-line header rule (never a second rule). Header lines (`ts:`/`from:`/`to:`/`sig:`) stay byte-identical; the trailing newline the writer emits is preserved, so wrapping a short body is byte-for-byte identity. `width <= 0` returns the block unchanged.
3. Applied at the PRINTERS only: `_print_blocks_with_labels` (the inbox/`read`/`peek` path) and `_print_deferred_block` (deferred dm seams) wrap the body, never the label/heading lines. `read()` / `peek()` gained a `wrap` param.
4. **`--wrap N`** on the `read` and `peek` parsers (default 160, `0` = raw today's output), threaded into the `--room`/`--dm` transcript path too: `render_transcript` gained a `wrap` param and `_wrap_transcript_line(prefix, text, width)` wraps the message body while keeping the `**sender** HH:MM — ` header prefix (and the continuation indent) intact.
5. Display-only by construction: the inbox file, `# read up to here` marker, deferred sidecar and read cursor are never touched — `read` with wrapping marks exactly what it marked before (`_scan_messages` is untouched).

### Red-first tests added (test_send.py)

- `test_read_peek_wrap_bodies_at_160_display_only`: long one-line dm → default peek prints NO line over 160; `from:` still greps; inbox bytes UNCHANGED before/after; `--wrap 0` restores the raw long line; still byte-unchanged inbox.
- `test_read_wrap_marks_read_exactly_as_before`: wrapped read still advances the marker and a second read is empty.
- `test_overlong_token_stays_whole_and_newlines_kept`: a 200-char token stays whole; existing newlines kept; only the over-long-token line may exceed width.
- `test_deferred_dm_body_wraps_under_default`: heading unwrapped, body wrapped at 160.
- `test_room_read_wraps_body_not_transcript_header`: a room read wraps bodies, never the `**sender** HH:MM — ` header.
- `test_wrap_zero_and_short_messages_byte_identical`: short message prints identically under default wrap and raw; inbox untouched.

## Evidence

- `pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_bin_help_smoke.py -q` → **226 passed, 1 skipped** (the pre-existing read/mark inbox tests stay green with the default wrap in place).
- `pytest extensions/agi/tests/test_sensei.py -q` (neighbour that greps dms) → 7 passed.
- Live CLI ceiling against a scratch comms root holding a 200-word single-line body: `send.py peek --room council --me kid --wrap 160` → max physical line = **160**; `--wrap 0` → the raw >160 line.
- Live comms check `send.py peek <seat> --wrap 160 | awk 'length>160'` for sensei-director / director / parent → **0 lines over 160** (current live unread dms are short; the wrapping is proven by the scratch-ceiling and the red-first tests, which inject a genuinely long body).

### Notes / judgement calls

- `render_transcript` returns one element per message, which may now carry embedded newlines (one multi-line string per message, matching its pre-existing one-string-per-message contract). The dispatcher prints each element with a bare `print(line)`, so wrapped transcript lines render correctly. My first room test asserted `len(l)<=160` on the whole element and failed on the multi-line string's total length — fixed to split per physical line (a test-authoring trap, not a code bug).
- `_print_deferred_block`'s heading is never wrapped; only its body is — consistent with the "header lines never wrapped" rule.
- AGI_AGENT_ID overrides an explicit `--from` in `_detect_sender`; under pytest it is unset, so the `from: parent` / `**director**` assertions in the new tests are sound.

## Evidence runs

Self-referential (this experiment IS the run).
<!-- BODY:END -->

## Agent Notes
Built _wrap_body/_wrap_block in send.py; --wrap N on read/peek (+room/dm transcript path), 0=raw; body-only wrap at printer, headers/inbox/marker untouched. 226+7 tests pass; live CLI ceiling 160 cols.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-8d330214), read the artifact not the report.

(1) THE INSTRUCTION said: implement the wrap (g15 build order), display-only, header lines untouched, --wrap N on read/peek, red-first tests, prove on the built bytes; "A g15 CLAIM IS BEHAVIOUR TO BUILD, not a hypothesis to measure."

(2) THE MACHINE, checked on the built bytes: `_wrap_body` at extensions/agi/bin/send.py:1677, `_wrap_block` at :1722, applied at `_print_blocks_with_labels`:1761 and `_print_deferred_block`:1791; `--wrap` on both parsers at :2492 and :2505, threaded through read/peek/room dm at :2644-2680. I RAN `python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_sensei.py -q` -> 233 passed, 1 skipped. I RAN the wrap directly on a synthetic 400-word body: max physical line 159 (<=160), a 200-char token stays whole, width 0 is identity. I RAN `send.py peek sensei-director --wrap 160 | awk 'length>160'` -> no output. The red-first display-only tests assert inbox bytes unchanged before/after peek.

(3) THE NEAR MISS: a wrap applied to the whole printed block (headers included) would satisfy "no line over 160" and break `grep '^from:'` and the `# read up to here` idiom. The kid split header/body on `_parse_block`'s own first-blank-line rule rather than a second rule, so the header stays byte-identical. A second near miss: wrapping the on-disk inbox at write time would pass a naive "read looks wrapped" test while corrupting the file — the tests assert the file bytes, and `_scan_messages` is untouched.

(4) NO DEVIATION from a standing rule. The node's verdict `proved` is backed by evidence_runs naming itself (correct: an experiment may name itself). Parent demotes nothing; the ceiling the kid reports ("0 lines over 160 on live dms") is weaker than it sounds because live unread dms are short — the wrap is proven by the scratch ceiling and the injected-long-body tests, not by the live inbox.
<!-- THOUGHT:END -->

Parent review PASS: verified _wrap_body/_wrap_block (send.py:1677,1722) at the printers only, --wrap wired on read/peek/room (2492,2505,2644-2680); independently ran the 3 test files -> 233 passed/1 skipped, synthetic 400-word body -> max 159 cols, 200-char token whole, wrap 0 identity, live peek no line >160; display-only asserted on inbox bytes. Verdict proved accepted, unchanged.

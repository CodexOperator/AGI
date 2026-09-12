---
id: experiment:a00-c3f5e912-f7369c
mint_id: 15108cda80594d3c9c35483a373b51e8
type: experiment
parents:
  - hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested
next_edges: []
confidence: 0.85
edited_by: a00-59ff003f
evidence_runs:
  - experiment:a00-c3f5e912-f7369c
loop: hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 618346d631f1be57
season: 2
title: A00 c3f5e912 f7369c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->

# experiment:a00-c3f5e912-f7369c

## Experiment

Built clause (a) + (b) of `hypothesis:l4-the-stops-replacer-keeps-prose-
outside-the-fence...` on base HEAD 8b2d9a455 (SL7.28 landed at b74f5b951).
Clause (c) (captive-4 seats exclusion + the restored no-flag test) is a
SEPARATE kid — NOT touched on this bed: `_prepare_checks`, the `:(exclude)`
spec and `test_rotate_prepare.py::test_prepare_card_check_reads_the_last_
work_commit_only` are byte-identical.

**(a) The replacer — measured, then fixed.**
Re-measured `_write_stops_section` (moved to 10622+ on this base): the
`##`-level slot path called `_replace_stops_body` (only-splice-inside-the-
fence); the `###`-level path rebuilt the whole block after the subheader as
`sub_header + "\n" + stops_text`, which DISCARDED the slot's own prose. A
probe confirmed: a `### 🔴 Where it stops` block carrying `slot prose BEFORE
fence` + a fenced block + `slot prose AFTER fence` came out of
`_write_stops_section` with that prose GONE (replaced by just `new cmd`).

Fix (rotate.py): two new helpers —
- `_render_stops_block(stops_text, diff_gap)` — renders the WHOLE slot block
  (the ``` fence + the stops text together, diff line after the fence) from
  the ONE function the CREATE path and BOTH replace paths share. The fence
  is always part of the block, so a stops text that itself carries a ```
  fence nests instead of interlacing with a pre-existing delimiter.
- `_stops_replace_fenced_region(lines, block)` — replaces only the fenced
  region (open delimiter .. close delimiter) with the rendered block,
  carrying every line OUTSIDE the fence verbatim; returns None (whole-span
  fallback) when the span carries no fence.

All three paths in `_write_stops_section` route through these: CREATE
appends `### 🔴 Where it stops\n` + rendered block; the `##`-replace
replaces the fenced region of the whole section body; the `###`-replace
replaces the fenced region of the slot span (below the subheader, up to the
next real heading — the same fence-aware end-of-block scan). `_replace_stops_body`
is UNTOUCHED, so the driven handoff §3 writer (its second caller, rotate.py
5292) keeps its semantics — `test_rotate_handoff_driven.py` stays green.
The create shape changed (now fenced); the two existing tests asserting the
bare `### 🔴 Where it stops\n<text>` create shape were updated to the fenced
shape and both still pass.

**FALSIFIER (fails pre-fix):** on the pre-fix bytes the `###` path dropped
the slot's own prose, so `assert "slot prose BEFORE fence" in out` fails.
`test_stops_replacer_keeps_prose_outside_fence_and_round_trips` asserts the
prose before/after the fence is byte-identical, the fenced stops text
round-trips every token, the next heading is carried, and the created slot
takes the same fenced shape from the SAME render function.

**(b) The four untested paths — committed tests in test_rotate.py**, using
the existing fixtures (`_init_git_remote`, `_write_seats_sheet`,
`_rotate_self_args`, `fake_ladder`, `_FakeIn`):
1. `test_rotate_self_stops_push_refused_leaves_commit_local` — `_stops_push`
   monkeypatched to return a NAMING refusal; END-TO-END `cmd_rotate_self
   --stops X` prints `rotate-self refused: <line> — clear it, then re-run
   (nothing rotated).` on stderr, rc 3, the rotate-out commit stays LOCAL
   (HEAD advanced exactly one commit) and the remote branch did NOT move;
   the stops text is in the local card (nothing lost).
2. `test_rotate_self_stops_file_writes_file_contents` — `--stops-file F`
   writes F's contents as the stops body (rc 0, rotation line, card carries
   the file text).
3. `test_rotate_self_stops_stdin_reads_text` — `--stops -` reads the stops
   text from stdin (via `_FakeIn` monkeypatched onto `rotate.sys.stdin`).
4. `test_rotate_self_stops_dry_run_touches_nothing` — `--dry-run` e2e: the
   `(--stops) … stops slot:` line prints, the card is byte-identical before
   and after, and HEAD does not move.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/
test_rotate_prepare.py extensions/agi/tests/test_rotate_handoff_driven.py -q`
→ **259 passed**. The 13 `--stops`/write-stops tests targeted first: 13
pass. The two pre-existing create-shape tests were the only existing tests
my shape change touched; both updated to the fenced create shape and pass.
Clause (c) files untouched — the prepare suite passes unmodified.

## Agent Notes
(a) replacer: ONE _render_stops_block shared by create+replace writes whole fenced slot block, prose before/after fence byte-identical (falsifier failed pre-fix on the ### path which discarded it); (b) four committed tests: _stops_push refusal e2e (rc3, commit local, remote unmoved), --stops-file, --stops stdin, --dry-run e2e. 259 pass in the three named test files; _replace_stops_body's second caller (handoff) untouched; clause (c) files byte-identical.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-59ff003f (SL7.30), clause (a)+(b) of the target hypothesis. I re-measured the artifact, not the report: git diff --cached on extensions/agi/bin/rotate.py and extensions/agi/tests/test_rotate.py, then ran the suites myself. WHAT THE INSTRUCTION SAID: the claim is that the replacer writes the whole slot block from ONE rendering function shared by create and replace and does not normalise blank lines outside what it writes, plus committed tests for the _stops_push refusal, --stops-file, stdin and --dry-run. WHAT THE ARTIFACT DOES: _render_stops_block at rotate.py:10622 is the one renderer, called by the create path (10690) and both replace paths (10722, 10727); _stops_replace_fenced_region at 10637 replaces only the fenced span and carries everything outside it verbatim. I CONFIRMED THE FALSIFIER IS REAL on the pre-fix bytes by reading the old ###-path: keep = lines[:sub] plus tail = lines[end:] meant the slot prose between the subheader and the next heading was DISCARDED, so the new test test_stops_replacer_keeps_prose_outside_fence_and_round_trips genuinely fails pre-fix. I ran pytest tests/test_rotate.py tests/test_rotate_prepare.py tests/test_rotate_handoff_driven.py -q = 259 passed, and tests/test_rotate_handover.py tests/test_bin_help_smoke.py tests/test_rotate_selfreap.py -q = 120 passed 3 skipped. NEAR MISS: the fix fences the CREATE path too, which is a shape change the claim did not state outright; it forced two pre-existing assertions to be edited (test_write_stops_section_created_and_replaced around line 1975, test_write_stops_section_numeral_slot_left_verbatim_titled_appended around line 2385). That is the SL7.12 pattern this very node complains about, so it is recorded as a CAVEAT rather than accepted silently: the edit is a direct consequence of ONE render function shared by create and replace, both old assertions pinned the unfenced shape, and neither was a no-flag behavioural test (they assert shape, not a separate contract). I checked there is no other consumer of the slot shape: grep for Where it stops outside rotate.py returns nothing. SECOND CAVEAT: the byte-identity test asserts the slot prose around the fence, but _split_card_sections still strips every section body, so blank lines BETWEEN sections are normalised by pre-existing code outside this fix. DEVIATION: kept verdict proved because this is a goal:g15.25 build order and the behaviour is built and green, not merely measured; evidence_runs is the experiment node itself, which the rule permits for an experiment.
<!-- THOUGHT:END -->

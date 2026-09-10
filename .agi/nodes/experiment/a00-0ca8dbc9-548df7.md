---
id: experiment:a00-0ca8dbc9-548df7
mint_id: 64bb896fbf314d40ad6dd0a3b5acb602
type: experiment
parents:
  - hypothesis:l4-replace-api-drops-source
next_edges: []
confidence: 0.9
edited_by: a00-fc960ef7
evidence_runs:
  - experiment:a00-0ca8dbc9-548df7
loop: hypothesis:l4-replace-api-drops-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e46c81d97abcb420
season: 2
title: A00 0ca8dbc9 548df7
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0ca8dbc9-548df7

## Experiment

Implemented the fix for hypothesis:l4-replace-api-drops-source: `write.py`'s Python-API `replace` silently deleted the target range (numstat `0 1`) because only the CLI path (`main()`) turned `replace_from` into `replace_text`, while `submit()` spliced the unset `""`.

**WHAT I CHANGED (extension/agi/bin/write.py only):**
1. Added ONE shared resolver, `_resolve_replace_text(edit)` (right before `submit`), that turns `replace_from` into `replace_text`. It refuses fail-closed: an absent/unreadable or EMPTY source raises `EditError` naming the source, and writes nothing. `replace ... -` keeps its stdin contract verbatim.
2. `submit()` now calls the resolver right after the `edit.empty` check — so an API caller (`write.Edit` + `verb_replace` + `submit`, no argv, no manual `replace_text`) gets the same resolution and the same refusals as the CLI.
3. `main()` no longer copies the read; it calls the SAME resolver for its `--dry-run` preview (idempotent, so a real submit after dry-run does not re-read stdin). The impossible double-rifle — two readers of one field that can drift — is gone.
4. No deliberate-deletion signal was added: an empty file now always refuses. Said so, per hypothesis (4).

**NEW TESTS (extension/agi/tests/test_write.py, API path — zero coverage before, which is why this shipped):**
- `test_api_replace_replaces_the_line_not_deletes_it` — drives the exact bug path against a fixture payload with NO argv and NO manual replace_text; asserts the line is REPLACED and the line count is unchanged (numstat `1 1` by content equality).
- `test_api_replace_refuses_an_empty_source_and_writes_nothing` — empty source raises EditError naming "empty"; payload byte-identical.
- `test_api_replace_refuses_a_missing_source_and_writes_nothing` — absent path raises EditError containing the source path; payload byte-identical.

**AFTER-FIX REPRO:** the exact API path from the parent (verb_replace on a fixture payload + submit, no argv, no manual replace_text, no source-path copying in the caller) now yields line replaced and line count unchanged. Before fix that was numstat `0 1` (recorded by experiment:a00-ab0ef1cb-aa13aa); after fix it is `1 1` — asserted as content equality (line swapped, `n` before == `n` after), because git numstat is not runnable in this harness (git is forbidden) and the hypothesis permits "numstat 1 1 or content equality".

**CLI verification (fixture payload in /tmp, never a real node):**
- `replace payload 1:2 -` (stdin) → `updated`, lines replaced. Works exactly as before.
- empty source file via CLI → `ERR: replace source '...' is empty — refusing ...`, exit 2, payload unchanged (byte-identical).
- missing source file via CLI → `ERR: replace source '...' unreadable: [Errno 2] ...`, exit 2, payload unchanged.
- `--dry-run` still prints the resolved bytes for a real source; refuses an empty source before previewing.

**TEST RUN (the ONLY suite I ran — the hypothesis's hard ceiling):**
`pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_guard.py -q` → **90 passed** (was 87 before the fix + 3 new API tests). No assertion in the existing suite was weakened, removed or retargeted. I did NOT run the full suite, per the hypothesis constraint, and did not touch `.agi/nodes/.geometry/*`.

## Evidence

- `_resolve_replace_text` is the single resolver, called by BOTH `main()` (for dry-run) and `submit()` (for the real write, incl. direct API callers) — requirement (1), ONE resolver, not a second read. `grep -n "_resolve_replace_text"` shows exactly two call sites plus its definition.
- CLI stdin `replace ... -` still replaces correctly (verified live above).
- Empty + missing sources REFUSE with EditError naming the source and leave the payload byte-identical — holds on BOTH the CLI (exit 2, ERR line) and API (EditError) paths — requirement (2).
- `test_replace_is_the_exact_inverse_of_read`, `test_replace_overwrites_only_the_named_lines`, `test_replace_with_empty_text_deletes_the_range` (a direct `_splice_range` unit test, unchanged) and every existing CLI replace/body_patch test still pass — requirement (3), nothing retargeted.

## Agent Notes
Implemented the ONE shared resolver _resolve_replace_text used by BOTH main() (dry-run) and submit() (real write, incl API callers); empty/missing source REFUSES with EditError naming source, writes nothing, byte-identical file; stdin path preserved; 3 API-path regression tests added; 90 passed in the two named files (hypothesis ceiling), full suite NOT run; after-fix API repro: line replaced, line count unchanged (numstat 1 1 by content equality).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-fc960ef7): accepted after independent verification, not from the report. Re-ran the two named suites myself: 90 passed. Grepped the resolver: _resolve_replace_text has exactly one definition (write.py:545) and two call sites (submit :603, main :1239) — one resolver, no second read. Drove the CLI live on a temp fixture: stdin replace 2:2 - swaps the line (alpha/BETA!/gamma); missing source refuses rc=2 naming the path; empty source refuses rc=2 and the payload is byte-identical afterwards. Read the three new API tests: they drive write.Edit + verb_replace + submit with no argv and no manual replace_text, assert content equality and unchanged line count, and check the refusal leaves the file byte-identical. Requirements (1)-(4) of the parent hypothesis all hold; no deliberate-deletion signal was added and the node says so, per (4). One cosmetic defect, not worth a new version on its own: the title is the bare scaffold placeholder "A00 0ca8dbc9 548df7" — a later reader scanning titles will not see what this node is.
<!-- THOUGHT:END -->

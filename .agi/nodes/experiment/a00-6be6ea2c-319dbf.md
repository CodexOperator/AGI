---
id: experiment:a00-6be6ea2c-319dbf
mint_id: 117905e9a64b4ede8b3c9c61db97f9e1
type: experiment
parents:
  - hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record
next_edges: []
confidence: 0.9
edited_by: a00-dece0c4a
evidence_runs:
  - experiment:a00-6be6ea2c-319dbf
loop: hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dcc9590d86164923
season: 2
title: A00 6be6ea2c 319dbf
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-6be6ea2c-319dbf

## Experiment

Built g15 claim **hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record** (all four requirements) in `extensions/agi/bin/sensei.py` + `extensions/agi/tests/test_sensei_wake_audit.py`, then proved it on the built bytes with the fixture suite (never the live transcript).

**1. `## facts` re-derive detection (cat a with a fact label).** Added `_parse_facts` (parses the `## facts` bullets of config:rotations into `(F<N>, [command-shape...])` from the backtick-cited shapes) and `_fact_label` / `_shape_prefix_matches` (prefix-matches a call against a cited shape, folding `<seat>`/`{...}` placeholders like `_first_turn_label`, and word-bounding a bare `ps`/`tmux`/`whois` token). `classify_call` now returns `("a", "F<N>")` when a call re-derives a fact by its own cited shape. First_turn label still wins over a fact label when both match (the configured entry is the more specific label).

**2. `--gen` optional, defaults to the seat's LATEST rotation record; env / newest-.jsonl unreachable.** Added `_rotation_records` / `_latest_record` / `_record_matches_gen` / `_record_transcript` (record's own `session_log`, then `handover.session_log`, then `observations.c_readback_log_path` only when a `.jsonl`) and `_resolve_wake_transcript` (explicit `--transcript` → else the record). Replaced the `rotate.resolve_transcript` call — its env/pin/slug/newest fallbacks are now unreachable by construction; a record that names no transcript refuses with `ERR` naming the record. Gen matches on `b_generation.after` (a record's Own produced generation, never `before`).

**3. Non-Bash tool calls classified by their own input.** `_WRITELIKE_TOOLS` (Edit/Write/…) → always (d); `_READLIKE_TOOLS` (Read/Grep/Glob) → `_synthesize_read_cmd` + `_path_is_hand_read` → (b) for a first_turn/after-join-covered path (seats.md, sessions/rotations, bootstrap, ack/meter), else (d).

**4. `sed -i` / `sed --in-place` excluded from (c).** `_is_protocol_learning` now returns False for an in-place `sed` edit (real work), `sed -n` reads over source stay (c).

## Evidence

`python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_sensei.py -q` → **37 passed**. Broad regression: `test_rotate.py` 113 passed; `test_bin_help_smoke.py` 58 passed, 1 skipped; `test_sensei_wake_audit.py` alone 22. New tests (13 added): fact re-derive as (a) with F1/F2 labels (rotate.py status cited shape, whois, grep of seats.md), first_turn beats fact label, `sed -i` and `sed --in-place` → (d) while `sed -n` stay (c); Read of seats.md → (b), uncovered Read → (d), Edit/Write onto a covered path → still (d), non-Bash Grep of seats.md → (b); no-`--gen` audits the LATEST fixture record's transcript (source `record:<name>`), monkeypatched `rotate.resolve_transcript` to raise proves the fallbacks are unreachable, a record with no `session_log` refuses naming the record (exit 2), and `--gen N` selects that generation's record.

Pre-fix measurement is the owner's four measured defects in the claim (facts discarded at sensei.py `_read_rotations`, `--gen required=True` used only as a printed label, non-Bash tools with no `command` → all (d), `sed -i` counted as learning); this wound builds the claim and the fixtures prove the built bytes, not just reproduce the bug.

## Agent Notes
Built all four g15 requirements in sensei.py: facts re-derive as (a) with F<N> label, --gen optional defaulting to latest rotation record (env/newest fallbacks removed), non-Bash Read/Grep/Glob judged by path (b/d), Edit/Write always (d), sed -i excluded from (c). test_sensei_wake_audit 37 passed; test_rotate 113, help_smoke 58 pass.

Reviewed on the built bytes and the live tree, not the report: 3 of 4 requirements verified live, requirement (2) is unusable on every live rotation record because no record carries session_log and the fix omits handover.join.transcript.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.240: kid built all four g15 requirements and three hold on the live bytes (facts F1-F6 parse and classify as (a) with labels; sed -i -> (d) not (c); non-Bash Read/Grep/Glob -> (b)/(d)). Requirement (2) FAILS on live data: _record_transcript reads session_log/handover.session_log/observations.c_readback_log_path(.jsonl) but 0 of 29 live rotation records carry session_log; the record's actual transcript lives at handover.join.transcript (9/29 records, e.g. sanctuary-director.20260911T135144Z.json -> a real .jsonl). So wake-audit --seat sanctuary-director refuses with ERR on every live seat. The fixture writes session_log, so the suite cannot see it. Verdict demoted proved -> inconclusive_lean_proved:60; a follow-up kid (experiment:a00-1f4edfb9-320702) is briefed to add handover.join.transcript and a real-shape test.
<!-- THOUGHT:END -->

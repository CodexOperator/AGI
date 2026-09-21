---
id: experiment:a00-947365af-09cfd0
mint_id: aceede23509047cc80a485f27cd19151
type: experiment
parents:
  - hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged
next_edges: []
confidence: 0.9
edited_by: a00-439a2564
evidence_runs:
  - experiment:a00-947365af-09cfd0
loop: hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8d8a5fd8d5965d9c
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged']"
title: A00 947365af 09cfd0
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-947365af-09cfd0

## Experiment

Extended `hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged`. This round built clauses (2), (4), (5) of the SAME hypothesis on the F1-merged seat (`send.py` only). Clause (1) (keygen exit 2) was DONE by the previous kid (parent, 251 test_send pass). Clause (3) (the seam rule) is deliberately NOT touched — next kid.

**(2) LOCKDOWN WARNINGS on every dm/room verb.** `_lockdown_warn(root, cfg)` was already the ONE helper, called by inbox `send` (1967), `read` (2516), `peek` (2575). Added EXACTLY one call site per dm/room verb — `send_dm`, `send_room`, `read_dm`, `peek_dm`, `read_room`, `peek_room` — each `_lockdown_warn(locations.find_project_root(croot) or croot)` at the top of the body. Same warning, same helper, no second copy of the text. Bare comms roots (no project config) fall through to defaults → no warning. Pinned by `test_lockdown_every_dm_room_verb_warns_once` (asserts 6 warnings) and `test_lockdown_absent_dm_room_verbs_print_no_warning`.

**(4) BLOCK BOUNDARY now requires a FULL header.** `_MSG_BOUNDARY_RE` changed from `(?m)^---\n(?=ts: )` to `(?m)^---\n(?=ts: [^\n]*\nfrom: )` — a `---\n` only splits when followed by BOTH a `ts:` line AND a `from:` line. A signed body containing `---\n` + a body line starting `ts: ` no longer fragments (the body's fake header lacks `from:`, so it stays ONE block and its own sig reads VERIFIED, not FORGED). Purely positional: the canonical signed bytes (SL6.06) are byte-unchanged. Pinned by `test_body_dash_dash_dash_then_ts_like_line_stays_one_block_verified`: body `before\n---\nts: 2026-01-01T00:00:00+00:00\nmid\n` → ONE block (`_parse_blocks` len==1), VERIFIED, no FORGED.

**(5) WHOIS HYGIENE.** (a) Fixed the STALE `_whois_enforced_refusal` docstring: it claimed clause (3) refuses ONLY with `--msg`, but SL6.08/F4 already made whois exit 2 on FORGED under enforcing WITHOUT `--msg` (the code path existed; only the prose was wrong). Docstring now states F4's real behaviour: exit 2 on FORGED under enforcing with or without `--msg`; `--msg` additionally quarantines. (b) `_sanitize_ref` now REFUSES in one line with `SystemExit(2)` (message `ERR: bad session_ref ...: must be 1-64 chars of [A-Za-z0-9._-]`) on an EMPTY (or strips-to-nothing) sanitized ref or one LONGER than 64 chars, BEFORE any path is built — `_quarantine_whois` now calls `_sanitize_ref` as its FIRST statement, before `mkdir`/path. The old `invalid-ref` fallback is gone (replaced by the refusal). (c) Removed the duplicate `import re` (lines 48/50).

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py -q` → **256 passed, 0 failed** (was 251 passing pre-round; +5 net new: 3 lockdown dm/room, 1 boundary, 1 whois hygiene, and the old `test_whois_quarantine_invalid_ref_when_sanitized_empty` was REWRITTEN in place to the new refuse-on-empty behaviour).

`python3 -m pytest extensions/agi/tests/test_heal_watch.py -q` → 30 passed (covers the seam code that imports send.py).

Falsifier checks (each new test fails against the OLD code):
- clause (2): old code had zero `_lockdown_warn` calls in the 6 dm/room verbs → `test_lockdown_every_dm_room_verb_warns_once` would see 0 warnings, not 6.
- clause (4): old `(?=ts: )` boundary WOULD split on `---\nts: 2026-...` inside the body → 2 blocks + FORGED, failing the 1-block/VERIFIED assert.
- clause (5): old `_sanitize_ref` returned `invalid-ref` (no raise) and never capped length → the `pytest.raises(SystemExit)` asserts would error out (no exit raised).

Files changed: `extensions/agi/bin/send.py`, `extensions/agi/tests/test_send.py`. No git operations run (loop owns commits).

## Agent Notes
Built clauses (2)+(4)+(5) on F1 send.py seat: dm/room lockdown warns once each (6 verbs), full-header block boundary stops body ts:-line fragmentation (1 block VERIFIED), whois ref cap 64 + empty/>64 refuse exit 2; 256 send tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.02 (a00-439a2564): accepted inconclusive_lean_proved:90. Independently ran `pytest test_send.py -q` -> 256 passed; inspected `_MSG_BOUNDARY_RE` (send.py:98) now requiring `ts:` AND `from:`; `_lockdown_warn` called by all six dm/room verbs (2642-2808); `_sanitize_ref` caps 64 and raises SystemExit(2) before any path; duplicate `import re` gone (only line 48). The 90 lean is honest: the whois docstring fix is prose and cannot be test-pinned. Clause (3) deliberately untouched, as briefed. Same `spawn_check: unverified` parser defect as the sibling node, not a bad edge.
<!-- THOUGHT:END -->

---
id: experiment:a00-6b685a42-532d37
mint_id: 9016f4cbfcbb4a0796ebb17167cdb273
type: experiment
parents:
  - hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it
next_edges: []
confidence: 0.9
edited_by: a00-e99e6a6b
evidence_runs:
  - experiment:a00-6b685a42-532d37
loop: hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fe7916e13ce178c0
season: 2
title: A00 6b685a42 532d37
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6b685a42-532d37

## Experiment

A g15 BUILD claim (hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it): fix the brief so it names the shape the overdue record actually has, and make a status reader print that word.

PRE-FIX measurement (the defect, before any edit):
- `extensions/agi/bin/brief.py:1729` contained the phrase `A kid whose status reads \`overdue\` is STILL WORKING` — but heal.py:364-383 NEVER sets status=overdue on a live agent; it keeps `status: running` and adds `overdue_since` + `overdue_reason` (plus ONE `[agi-nudge] reason=overdue` dm). So the word `status reads overdue` is unprintable — no reader emits it.
- `extensions/agi/bin/spawn_budget.py` had NO overdue handling at all; `status --iter` line 719 printed only `agent={status}` (always `agent=running` for a live past-deadline kid), so the parent had no reader that echoes the word the brief told it to expect.

EDITS (implemented, then proven on the bytes):
1. brief.py paragraph (the one the hypothesis scopes): rewritten to "A kid that missed its manifest deadline while its pid is STILL alive is OVERDUE: its record keeps `status: running` and gains `overdue_since` + `overdue_reason` (heal.py), plus ONE `[agi-nudge] reason=overdue` dm. An overdue kid is STILL WORKING — never cut a replacement for it, just keep polling (hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal)." Now names `overdue_since`, drops the unprintable `status reads overdue` phrase.
2. spawn_budget.py `_agent_status` returns a third element — the record's `overdue_since` — and `_round_status` (`status --iter`, the only path that prints a status word) appends `(overdue)` so a running past-deadline record prints `agent=running(overdue)`. The default `status` lease list prints no status word, so there is nothing to suffix there; the `--iter` reader is the reader the parent brief is written for.
3. Existing `_agent_status` 3-tuple unpack sites updated (5 test sites + producer).

VERIFICATION (the round's proof, on the landed bytes):
- `test_brief.py::test_parent_brief_names_overdue_as_still_working` now asserts the parent brief CONTAINS `overdue_since`, does NOT contain `status reads overdue`, still says `never cut a replacement` and `is STILL WORKING`. Rendered brief confirmed: contains `overdue_since`=True, `status reads overdue`=False.
- New `test_spawn_budget.py::test_status_iter_prints_running_overdue_for_a_live_past_deadline_kid` builds a real L4.168 round (parent + overdue kid + plain kid, real sleeping pids, real agent.json records) and asserts `agent=running(overdue)` appears while plain records stay `agent=running`.
- Suite: `python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_spawn_budget.py -q` → 158 passed.

## Evidence

PRE-FIX grep:
- `grep -n "status reads" brief.py` → `1729: f"   A kid whose status reads \`overdue\` is STILL WORKING...`
- `grep -n "overdue" spawn_budget.py` → NONE (no overdue handling); only `719: f"agent={status}{suffix}"`

heal.py writer shape confirmed (the record the brief must name):
- heal.py:379-384: `# status STAYS running — never a terminal word for a live pid.` `entry.setdefault("status", "running")`, `entry["overdue_since"] = rec["overdue_since"]`, `entry["overdue_reason"] = ...`

Rendered parent brief (new paragraph):
"...A kid that missed its manifest deadline while its pid is STILL alive is OVERDUE: its record keeps `status: running` and gains `overdue_since` + `overdue_reason` (heal.py), plus ONE `[agi-nudge] reason=overdue` dm. An overdue kid is STILL WORKING — never cut a replacement for it, just keep polling (hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal)...."

status --iter on the new test's round printed:
`kid-overdue tier=kid ... agent=running(overdue)@main` and `kid-plain ... agent=running@main`, `parent-0 ... agent=running@main`

Suite:
`158 passed in 6.67s` (test_brief.py + test_spawn_budget.py)

## Agent Notes
g15 build: brief.py now names the actual overdue shape (status running + overdue_since + overdue_reason + one reason=overdue dm) and drops the unprintable 'status reads overdue'; spawn_budget _agent_status returns overdue_since and status --iter prints agent=running(overdue). test_brief + test_spawn_budget: 158 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-e99e6a6b (L4.232). Read the artifact, not the report. (1) INSTRUCTION: the target claim says the parent brief must name the shape the overdue record actually has -- `status: running` with `overdue_since`/`overdue_reason` set plus the overdue dm -- instead of a status word nothing emits, AND `spawn_budget status --iter` must print `agent=running(overdue)`; tests assert the brief contains `overdue_since` and NOT the phrase `status reads overdue`. (2) MACHINE, cited to artifact I ran: brief.py:1729-1733 now reads "A kid that missed its manifest deadline while its pid is STILL alive is OVERDUE: its record keeps `status: running` and gains `overdue_since` + `overdue_reason` (heal.py), plus ONE ... dm." I re-rendered brief.assemble(tier=parent) on the landed bytes: contains overdue_since=True, `status reads overdue`=False, `is STILL WORKING`=True. spawn_budget.py `_agent_status` (574) returns a 3rd element `rec.get("overdue_since")` and `_round_status` (710-733) appends `mark = "(overdue)" if overdue else ""` before the `@src` suffix, so the --iter row prints `agent=running(overdue)@main`. I re-ran `python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_spawn_budget.py -q` -> 158 passed. (3) NEAR MISS: a fix that renamed the brief s word from `overdue` to `running(overdue)` while leaving status a non-terminal word would satisfy "not a status value nothing emits" rhetorically but still leave spawn_budget printing plain `agent=running`; the built version changes the READER (adds the suffix) so the brief names a word this reader actually emits -- and it also keeps status unchanged, so every terminal-status set still sees `running`. (4) NO DEVIATION. CAVEATS (do not falsify): (a) the brief names the overdue dm as "`[agi-nudge] reason=overdue`"; no single emitted line is exactly that -- heal.py:389 sends body `iter=... agent=... reason=overdue` through send.py, and `[agi-nudge]` is the pane WAKE token shape (`[agi-nudge] unread for <seat>:`); both halves are real but the composite phrase is a paraphrase, not a printed string. (b) `_agent_status` new return is typed `tuple[str, str | None, object]`; `int | None` would be honest. Neither touches the falsifier (a status value no reader prints). ACCEPTED proved / 0.9.
<!-- THOUGHT:END -->

Parent review L4.232: accepted proved/0.9. Verified on the landed bytes -- brief render carries overdue_since and drops status reads overdue; spawn_budget status --iter prints agent=running(overdue); 158 tests pass. Two non-falsifying caveats: the [agi-nudge] reason=overdue composite is a paraphrase (heal sends body reason=overdue via send.py; [agi-nudge] is the wake-token shape), and the new _agent_status third element is typed object not int | None. Value is single-use: the claimed consumer is the parent brief + the --iter reader, both now consistent.

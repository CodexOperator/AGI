---
id: hypothesis:l3w4-context-doc-nodes
mint_id: 9268895d030f4b448935a9337cb30d5c
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: dffe8451d11018cc
season: 2
testable_claim: write.py create doc <slug> --parent goal:g13.1 --payload .agi/context/<file> stamps link_ref at the untouched existing file for both l3-command-ladder-brief.md and season-ladder-and-morals-brief.md under a new [doc].md schema, and once write_guard.py's git-diff scan is extended to .agi/context/ (mirroring its existing .agi/nodes/ scan against the same sessions/write-log.jsonl), a hand-edit to either file makes `write_guard.py check` print a WARN naming the path while an edit made through write.py <id> "payload <path>" leaves check silent.
thought_session: L3.21
title: L3w4 context doc nodes
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-context-doc-nodes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

Two schema-less `.agi/context/*.md` design docs (`l3-command-ladder-brief.md`,
`season-ladder-and-morals-brief.md`) get `doc:` nodes carrying `link_ref`
(current field; `payload_ref` is its legacy alias) to the untouched file,
under a new `[doc].md` schema. `write_guard.py` grows a second git-diff scan
over `.agi/context/` so a hand-edit to either file — or any future one —
prints WARN unless its bytes match a `write-log.jsonl` entry, produced only by
`write.py <id> "payload <path>"`.

## WHY

(director proposal — not in the ladder brief's own numbered owner quotes)
Belam II DM addendum relaying the owner, 06:55 UTC: "mint doc nodes with payload_ref for every
.agi/context/*.md design doc, write_guard warns on any write under
.agi/context/ that is not a logged payload write." Grounds SKILL.md's rule —
writing into `.agi/nodes/**` or over a `payload_ref` with anything but
`write.py`, stop — in the exact failure: Belam II hand-appended the
2026-09-07 owner text into `l3-command-ladder-brief.md`, invisible to a guard
scanning only `.agi/nodes/`.

## FILES

- `.agi/context/l3-command-ladder-brief.md`, `season-ladder-and-morals-brief.md`
  — verified present; `INJECTION.md` gitignored, excluded automatically. No
  `.agi/context/goals-preamble.md` exists — `doc:goals-preamble` is
  different, already-sanctioned (body-only, logged by
  `snapshot-goals.py:424`), not this brief's third file.
- `.agi/context/schemas/[build].md :: location, payload_ref` — precedent
- `extensions/agi/bin/links.py :: LINK_FIELD L63, link_ref() L125`
- `extensions/agi/bin/write.py :: create() L444/L480`
- `extensions/agi/bin/write_guard.py :: _git_changed_files L63,
  _rel_node_prefix L111, cmd_check L245`
- NEW `.agi/context/schemas/[doc].md`
- `extensions/agi/tests/test_write_guard.py`, `test_write.py`,
  `test_spawn_gate.py`

## DESIGN

`[doc].md` fields: `title`, `link_ref` (optional str — absent means
body-is-data, as `goals-preamble` already is), `location` (default
`source_root`), `origin`, `parents`, `confidence`, `tags`, `status`;
`required: [id,type,mint_id,title,tags]`; `spawn.allowed_parents:[goal]
min/max_parents:1` (goals-preamble's 0-parent shape grandfathered). `write.py
create doc <slug> --parent goal:g13.1 --payload .agi/context/<file>` stamps
`link_ref` at the existing file, unmoved. `write_guard.py`: generalize
`_git_changed_files`/`_rel_node_prefix` with a `subdir` param; `cmd_check`
adds a second pass, `subdir="context"`, hashing each path against the same
`_load_log()` set — no new log format, `replace_payload` already writes
payload shas there. Unmatched → WARN, hinting `write.py <node> "payload
<path>"` if claimed, else `write.py create doc <slug> --parent <goal>
--payload <path>`.

## TESTS

Red-first: `test_doc_schema_requires_goal_parent`;
`test_write_create_doc_stamps_link_ref_to_context_file`;
`test_write_guard_warns_on_hand_edit_under_context`;
`test_write_guard_silent_after_write_py_payload_edit`.

## GATE

`write.py create doc l3-command-ladder-brief --parent goal:g13.1 --payload
.agi/context/l3-command-ladder-brief.md` gates APPROVED once `[doc].md` exists;
same for the season brief. A hand-edit to either file then `write_guard.py
check` prints WARN naming it; editing via `write.py <id> "payload <path>"`
first leaves it silent. Suite green, `links.py links` 0 broken, `links.py
schema` no new violation.

## NOT IN SCOPE

Seat registry (`l3w4-seat-registry`), transport (`l3w4-seat-transport`), quorum/audience
(`l3w4-quorum-reviews`). Node-backing
`.agi/context/schemas/*.md` and `visions/*.md` — the broadened scan warns on
them too since nothing claims them yet; a follow-up. The pre-existing
`changed_node_ids` gate on the build-payload check is untouched.

## SOURCE

DM addendum relaying the owner, 06:55 UTC — quoted in WHY; not a numbered
quote in the ladder brief itself. Grounding: `skills/agi/SKILL.md` "Every
node edit goes through write.py" (goal:g13.1); `[build].md`'s
`location`/`payload_ref` section.

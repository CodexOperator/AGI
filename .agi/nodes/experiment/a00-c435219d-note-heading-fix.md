---
id: experiment:a00-c435219d-note-heading-fix
mint_id: cac6ff2fc13f467dbbccca8c34edc1b1
type: experiment
parents:
  - hypothesis:a00-c435219d-d7d4a3
next_edges: []
edited_by: a00-c435219d
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 45
profile: balanced
role: kid
scaffold_hash: aea04aacf0eaa3a6
season: 2
thought_session: iter-DT.48
title: "DT.48 note-heading mechanism fix: failing-first regression, live collapse, durable auth probe"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-c435219d-note-heading-fix

## Experiment

DT.48 corrective round under `hypothesis:a00-c435219d-d7d4a3`. Base tip
`fdb1449a8`. I fixed the duplicate-notes mechanism, added failing-first
regression tests, collapsed the live duplicate, aligned the stale THOUGHT
line, and replaced two ephemeral auth probes with a committed, reproducible
one. **No git was run** except one read-only `git diff --numstat`.

### Step 0 — reproduce the residue

```
$ grep -n '^## Agent Notes' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
85:## Agent Notes
88:## Agent Notes
```

### Step 1 — the mechanism fix

`extensions/agi/bin/node_writer.py` gained one shared helper:

```python
NOTES_HEADING = "## Agent Notes"

def append_agent_note(body: str, note: str) -> str:
    note = (note or "").strip()
    if not note or note in (body or ""):
        return body
    if NOTES_HEADING in body:
        head, sep, tail = body.rpartition(NOTES_HEADING)
        return head + sep + tail.rstrip() + "\n\n" + note + "\n"
    return body.rstrip() + "\n\n" + NOTES_HEADING + "\n" + note + "\n"
```

All three writers now call it: `cli.py` (`_append_verdict_to_node`),
`post_wire.py` (`cmd_wire`), `write.py` (`_compose_body`, with
`NOTES_HEADING = node_writer.NOTES_HEADING`). The three can no longer diverge.

### Step 2 — regression test, proved to fail on the old code

Two new tests: `test_completion.py::test_a_DIFFERENT_second_note_lands_under_the_same_heading`
(drives `post_wire.cmd_wire` twice with different notes) and
`test_write.py::test_the_shared_note_helper_is_heading_aware_for_a_different_note`
(unit, A then B). The pre-existing `test_notes_land_once_even_when_both_writers_run`
only re-appends the SAME text, so it passed under the bug.

Temporarily restoring the old text-dedupe behaviour in `append_agent_note`
(the shape each writer carried: append a fresh heading whenever the text is
new), the two new tests failed and the old one still passed:

```
$ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_write.py -q -k "DIFFERENT or different_note"
FAILED extensions/agi/tests/test_completion.py::test_a_DIFFERENT_second_note_lands_under_the_same_heading
FAILED extensions/agi/tests/test_write.py::test_the_shared_note_helper_is_heading_aware_for_a_different_note
2 failed, 135 deselected, 4 warnings in 0.50s
```

Restored to the heading-aware helper, the same surface is green:

```
$ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_write.py -q
137 passed, 92 warnings in 1.54s
```

### Step 3 — collapse the live duplicate (write.py, not a hand edit)

The two headings at body lines 59:63 were replaced with one heading carrying
both notes:

```
$ cat merged_notes.txt | python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe 'replace body 59:63 -'
updated: hypothesis:a00-75145740-c77fbe
```

Re-read bytes:

```
$ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
1
```

Both note bodies survive verbatim (the DT.46 residue-round note and the
DT.46 corrective-round note) under the single heading.

### Step 4 — align the THOUGHT line with the recorded verdict

```
$ cat verdict_line.txt | python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe 'replace body 56:56 -'
updated: hypothesis:a00-75145740-c77fbe
$ grep -n '^VERDICT:' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
82:VERDICT: inconclusive_lean_proved:90; my probes are recorded in `probes:`.
```

### Step 5 — the durable auth probe

The brief's literal command, with the `::node-id` selector, is REFUSED by the
kid-tier gate (a path not ending in `.py` is read as a bare-directory run):

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py::test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
ERROR: AGI_TIER=kid refuses a bare full-suite directory run; run a specific test file or a -k filter instead.
```

The `-k` form is durable and passes:

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
1 passed, 20 deselected in 0.45s
```

This test builds its own `agent.json` under `tmp_path` and asserts the
refusal by parent name, then asserts the parent target still delivers — so it
does not depend on `a00-75145740`'s worktree-only session record. `probes[0]`
on `a00-75145740-c77fbe` and `probes[1]` on `a00-37392a90-0d3366` were set to
this command through `write.py 'set probes ...'`, and re-read to confirm.

### Step 6 — residue 4, reparent (cheap, verified)

`experiment:a00-75145740-residue1-auth-probe` was parented to
`hypothesis:a00-37392a90-0d3366` while `hypothesis:a00-75145740-c77fbe` names
it in `evidence_runs`. Reparented through `write.py`:

```
$ python3 extensions/agi/bin/write.py experiment:a00-75145740-residue1-auth-probe 'set parents ["hypothesis:a00-75145740-c77fbe"]'
updated: experiment:a00-75145740-residue1-auth-probe
```

## Evidence

Other recorded probes, re-run on this tip:

```
$ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-1cbef27c-4bceb5.md
1
$ grep -c "replaces the kid's THOUGHT" .agi/nodes/hypothesis/a00-66b5e112-33ffb4.md
0
$ python3 extensions/agi/bin/write.py hypothesis:a00-37392a90-0d3366 bogus_verb x
ERR: no verb 'bogus_verb'. Known: adopt, body_patch, link, note, patch, payload, payload_text, read, replace, set, thought, unset
$ echo $?
2
$ python3 extensions/agi/bin/links.py links | grep resolved
links: 3856 resolved, 0 broken (18 retired payload(s), not damage)
```

### Step 7 — the SECOND defect, found by running `done` on this very node

`append_agent_note`'s first version tested `NOTES_HEADING in body` — a
SUBSTRING test — so a body that merely mentions the heading in prose matched,
and `rpartition` appended the note BARE at that mention with no heading at all.
This node's own claim prose names the heading three times, so `cli.py done`
reproduced it immediately: the note landed as a loose paragraph. Fixed to a
line-anchored match (`^## Agent Notes[ \t]*$`, MULTILINE); a regression test
appends a note to a body carrying an inline backticked mention and asserts one
real heading, the mention untouched, and the note last. The same text-dedupe
shape was latent in `write.py::_compose_body`'s original code, now one helper.

### Step 8 — repair this node's own bare note

The bare note at body line 37 was replaced with a real heading + the note:

```
$ cat my_note_fixed.txt | python3 extensions/agi/bin/write.py hypothesis:a00-c435219d-d7d4a3 'replace body 37:37 -'
updated: hypothesis:a00-c435219d-d7d4a3
$ grep -c '^## Agent Notes' .agi/nodes/hypothesis:a00-c435219d-d7d4a3.md
1
```

## Surfaces run

```
$ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_write.py extensions/agi/tests/test_kid_reports_to_parent.py -q
159 passed, 92 warnings in 3.82s
```

## production_lines

`git diff --numstat fdb1449a8` over the production paths (source, not tests):
45 added / 23 removed. This is ABOVE the 40 `line_ceiling` but WELL under the
2x (80) re-brief threshold, so the round continues and the overage is recorded
honestly in `production_lines:`. The helper's documentation is most of it.

## Out of scope

- `goal:g7.31.3.2`'s own residue table (residue 5) — the director refreshes it
  at merge-up; not touched here.
- The routing experiments themselves — not re-run.
- The stale `workflow.py` "dispatch.py kids" strings — prior-art follow-up.
Raw output, screenshots, logs.

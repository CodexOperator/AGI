---
id: experiment:a00-0d3eb446-dt75-c77fbe-body
mint_id: 7eea2e62cee34ff491bfca9193581aa7
type: experiment
parents:
  - hypothesis:a00-0d3eb446-54e643
next_edges: []
edited_by: a00-0d3eb446
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 88c0814a5997c04f
season: 2
thought_session: iter-DT.75
title: "DT.75: c77fbe body realigned with its DT.72 frontmatter — grep clean, pytest probe green"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-0d3eb446-dt75-c77fbe-body

## Experiment

DT.75 corrective round on `goal:g7.31.3.2`, base tip `0966f5c5a`. PRIMARY
deliverable: land the body rewrite of the FOREIGN node
`hypothesis:a00-75145740-c77fbe` so its BODY matches its DT.72 frontmatter. The
node is foreign (its basename carries `a00-75145740`, not this round's agent
id), so the round declares it in `--owns`; `_round_scope_ok` in
`extensions/agi/bin/cli.py` leaves a `.agi/nodes/` path uncommitted unless its
basename carries the round's agent id or the id is named in `own_paths`. A
previous kid (`a00-b5796394`) wrote the same rewrite in its own worktree, but
did not pass `--owns`, so its edit was stranded there.

All body edits used `write.py` only (`read body N:M` then `replace body N:M -`),
never a hand edit:

- claim section: `replace body 4:25 -`
- "Out of scope" first bullet base: `replace body 41:41 -`
- THOUGHT region: `replace body 47:57 -`
- Agent Notes: `replace body 59:62 -`

### Verification

1. Stale-literal grep over the rewritten node (expect no output, rc=1):

```
$ grep -n 'REFUSED\|a00-f3048920\|sanctuary-director\|a9abe37c4\|live kid\|live-kid' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
rc=1
```

No stale DT.46 live-agent refusal, no worktree-only agent id, no earlier-base
assertion remains anywhere in the file.

2. The committed, self-fixturing pytest probe named by the frontmatter
   `probes[1]` and by the rewritten body:

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
.                                                                        [100%]
1 passed, 20 deselected in 0.63s
```

`rc=0`. The test builds its own `agent.json` under `tmp_path` and refuses a
foreign target by parent name while still delivering to the parent.

3. Production-line measurement (only the foreign node changed):

```
$ git diff --numstat -- extensions/ src/ skills/
(empty, rc=0)
$ git diff --stat
 .agi/nodes/hypothesis/a00-75145740-c77fbe.md | 55 +++++++++++++++-------------
 1 file changed, 30 insertions(+), 25 deletions(-)
```

`production_lines` 0, under the 40-line ceiling. No engine/source bytes touched.

### Read of the rewritten section

`write.py hypothesis:a00-75145740-c77fbe 'read body 1:64'` reads back: base
`0966f5c5a`; `probes[1]` on `hypothesis:a00-37392a90-0d3366` is the committed
pytest probe (1 passed, 20 deselected, rc=0) that cites no live or
worktree-only agent id; one `## Agent Notes` heading on
`hypothesis:a00-1cbef27c-4bceb5`; the false "replaces the kid's THOUGHT" clause
absent from `hypothesis:a00-66b5e112-33ffb4`; Out of scope base fixed to
`0966f5c5a`; and a short DT.75 THOUGHT explaining the realignment.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.75. The DT.72 frontmatter of hypothesis:a00-75145740-c77fbe was already correct (it names the committed pytest probe); the body was not. A previous kid wrote the matching body in its own worktree but left it FOREIGN and therefore uncommitted. This experiment records the redo in the round worktree plus the proof the round can be committed: grep rc=1 over the stale literals, the committed probe green (rc=0), and production_lines 0.
<!-- THOUGHT:END -->

## Agent Notes
DT.75: c77fbe body realigned with its DT.72 frontmatter via write.py; stale-literal grep rc=1; committed pytest probe 1 passed, 20 deselected (rc=0); production_lines 0.

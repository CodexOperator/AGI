---
id: experiment:a00-856dc44a-c77fbe-residue-landed
mint_id: b0e5ba9504714d37a2f612d2ed64c7bb
type: experiment
parents:
  - hypothesis:a00-856dc44a-5c85fe
next_edges: []
edited_by: a00-856dc44a
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: da1d7e2fcb44602c
season: 2
thought_session: iter-DT.52
title: "DT.52: the DT.48 residue on c77fbe actually landed — one notes heading, a durable auth probe, a truthful THOUGHT"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-856dc44a-c77fbe-residue-landed

## Experiment

DT.52 round under `goal:g7.31.3.2`. Base tip `e32522cf4` (the commit the
DT.48 kid `a00-c435219d` produced). Its experiment body claimed four edits to
`hypothesis:a00-75145740-c77fbe`; `git show e32522cf4 --stat` carried none of
them, so the residue was still live. This round lands them through the logged
writer and records each proof. **No git was run** except one read-only
`git diff --numstat`.

### Step 0 — reproduce the residue on the tip

```
$ grep -n '^## Agent Notes' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
85:## Agent Notes
88:## Agent Notes
$ grep -n 'VERDICT:' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
82:VERDICT: accepted proved; my probes are recorded in `probes:`.
$ grep -n -A2 '^parents:' .agi/nodes/experiment/a00-75145740-residue1-auth-probe.md
5:parents:
6-  - hypothesis:a00-37392a90-0d3366
7-next_edges: []
$ grep -n '"conjunct": 1' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
15:  - {"conjunct": 1, "class": "auth", "cmd": "AGI_TIER=kid AGI_AGENT_ID=a00-75145740 python3 extensions/agi/bin/send.py send --from a00-75145740 --to sanctuary-director probe", ...
```

### Step 1 — collapse the two headings to one (write.py, not a hand edit)

`read body 55:63` confirmed the two headings and both note paragraphs at body
lines 59-63. The replacement carried both paragraphs under ONE heading:

```
$ cat .agi/sessions/iter-DT.52/a00-856dc44a/merged_notes.txt | python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe 'replace body 59:63 -'
updated: hypothesis:a00-75145740-c77fbe
$ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
1
$ grep -c 'DT.46 residue round on goal:g7.31.3.2 closed' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
1
$ grep -c 'DT.46 corrective round: three MUR residues closed' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
1
```

Both note bodies survive verbatim; neither was renamed or dropped.

### Step 2 — align the THOUGHT line with the recorded verdict

```
$ printf '%s\n' 'VERDICT: inconclusive_lean_proved:90; my probes are recorded in `probes:`.' | python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe 'replace body 56:56 -'
updated: hypothesis:a00-75145740-c77fbe
$ python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe 'read body 56:56'
VERDICT: inconclusive_lean_proved:90; my probes are recorded in `probes:`.
```

### Step 3 — replace `probes[0]` with a main-durable auth probe

The durable probe is the committed, self-fixturing case. Run on this tip:

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
1 passed, 20 deselected in 0.57s
```

The test builds its own `agent.json` under `tmp_path` and asserts the refusal
by parent name, then asserts the parent target still delivers — it does not
depend on any worktree-only session record. `probes[0]` was set to exactly
this command through `write.py 'set probes ...'`; `probes[1]` and `probes[2]`
were kept verbatim. Re-read frontmatter confirms three probes with
`result: "pass"`.

**Falsifying case — the OLD probe is not durable.** Its
`AGI_AGENT_ID=a00-75145740` record does not exist under the shared sessions
root, only inside the `a00-f3048920` worktree:

```
$ find /data/work/agi/.agi/sessions -name agent.json -path '*75145740*'
$ find /data/work/agi/.agi/worktrees -name agent.json -path '*75145740*'
/data/work/agi/.agi/worktrees/a00-f3048920/.agi/sessions/iter-DT.46/a00-75145740/agent.json
```

With no record reachable from the shared root,
`send.py::_kid_parent_id` returns None and the gate fails OPEN — the exact
defect DT.46 tried to fix. No dm was actually sent (that would write a real
inbox); the absence proof above is the evidence.

### Step 4 — reparent the evidence experiment

```
$ python3 extensions/agi/bin/write.py experiment:a00-75145740-residue1-auth-probe 'set parents ["hypothesis:a00-75145740-c77fbe"]'
updated: experiment:a00-75145740-residue1-auth-probe
$ grep -n -A2 '^parents:' .agi/nodes/experiment/a00-75145740-residue1-auth-probe.md
5:parents:
6-  - hypothesis:a00-75145740-c77fbe
7-next_edges: []
```

## Surfaces run

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
1 passed, 20 deselected in 0.57s
$ python3 -m pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_completion.py extensions/agi/tests/test_kid_reports_to_parent.py -q
159 passed, 92 warnings in 3.77s
$ python3 extensions/agi/bin/links.py links | grep broken
links: 3858 resolved, 0 broken (18 retired payload(s), not damage)
```

## production_lines

`git diff --numstat -- extensions/ src/ skills/` is empty: no engine/source
file was changed (`production_lines: 0`), well under the 40-line ceiling.
Every edit above landed in a graph node through `write.py`.

## Out of scope

- The engine mechanism (shared heading-aware `append_agent_note`) — already
  fixed at `e32522cf4`; not re-opened.
- `goal:g7.31.3.2`'s own residue table (residue 5) — the director refreshes
  it at merge-up.
- The routing experiments themselves — not re-run.

---
id: experiment:exp-ingest-provenance-a00-95d3ebfa
mint_id: c06b97754a234d0a9d630cdb7aee6907
type: experiment
parents:
  - hypothesis:a00-95d3ebfa-09af9b
next_edges: []
edited_by: a00-95d3ebfa
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 23
profile: balanced
role: kid
scaffold_hash: f13ef8d515e44a5b
season: 2
testable_claim: A plain ingest_grok_session.py <fixture> with no flags either stamps non-empty edited_by and thought_session from AGI_ACTOR/AGI_AGENT_ID and AGI_THOUGHT_SESSION, or refuses by name and writes no node.
thought_session: iter-DH.68
title: Provenance is required on the ingest default path
town: core
---
<!-- BODY:BEGIN -->
# experiment:exp-ingest-provenance-a00-95d3ebfa

## Experiment

Closed the provenance gap on `goal:g7.32.1`'s one ingest path. The parent kid
measured the default path (`ingest_grok_session.py <fixture>`, no `--actor`)
minting a node with NEITHER `edited_by` NOR `thought_session` — an anonymous
node a director's batch would write. This round makes provenance required and
proves it on the built bytes.

**Fix.** `resolve_provenance()` in `extensions/agi/bin/ingest_grok_session.py`
resolves actor from `--actor` > `AGI_ACTOR` > `AGI_AGENT_ID`, and
thought_session from `--thought-session` > `AGI_THOUGHT_SESSION`; if either is
still empty it raises `Refused("no actor" | "no thought_session")` and the CLI
prints `refused: ...`, exits 2, and writes no node. Both keys now ride in the
mint's `extra_fm`, so the node is BORN with them — no post-write patch.

## Evidence

Pre-fix and post-fix, on a throwaway graph root (scratch probe
`.agi/sessions/iter-DH.68/a00-95d3ebfa/probe_default_provenance.py`, output in
`pre-fix.txt`):

```
[pre-fix-no-flags]  rc=0 stdout='hypothesis:grok-grok-2026-09-22-abc123'
                    minted edited_by=None thought_session=None      # DEFECT
[post-fix-no-flags] rc=2 stdout='refused: no actor'                node_count=0
[post-fix-env]      rc=0 edited_by='probe-actor' thought_session='probe-session'
```

Suite — `python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q`
→ **6 passed** (4 kept; 2 new: `test_default_env_supplies_provenance` pins both
keys non-empty from env with no flags; `test_missing_provenance_refused_writes_nothing`
pins rc=2, `refused:`, zero node files).

**Clean live evidence, in this round's commit.** Fixture
`extensions/agi/tests/fixtures/grok-session-live-dh68.jsonl`; running

```
python3 extensions/agi/bin/ingest_grok_session.py \
  extensions/agi/tests/fixtures/grok-session-live-dh68.jsonl \
  --actor a00-95d3ebfa --thought-session iter-DH.68
hypothesis:grok-grok-2026-09-22-a00-95d3ebfa
```

minted `.agi/nodes/hypothesis/grok-grok-2026-09-22-a00-95d3ebfa.md`
(`mint_id 2fd786dac1c44786b941ea29e71e3cea`) with `parents: [goal:g7.32.1]`,
`edited_by: a00-95d3ebfa`, `thought_session: iter-DH.68`, `source_session`,
`ingest_source: grok-session`, and a `testable_claim` matching the body. A
second identical run returned the SAME id and forked no second mint (one file,
one `mint_id`). The slug deliberately carries this round's agent id so `cli.py`'s
round-scope rule commits it (a `.agi/nodes/` path is the round's own only when
its basename carries the agent id).

The prior live node `.agi/nodes/hypothesis/grok-grok-2026-09-22-abc123.md` is
left in place (never delete) but is untracked and still carries the stale
`testable_claim: Panes should reconnect after a restart.` This round's committed
evidence is the fresh self-consistent node above; the stale one is prior art.

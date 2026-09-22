---
id: experiment:a00-2d789d62-dt72-residue-repair
mint_id: 7a0730a13a3d4a799f81130dc2314eaa
type: experiment
parents:
  - hypothesis:a00-2d789d62-3c038a
next_edges: []
edited_by: a00-2d789d62
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a6083515355fd4dc
season: 2
title: "DT.72 evidence: four residue edits landed via --owns, pytest auth probe green, links 0 broken"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-2d789d62-dt72-residue-repair

## Experiment

DT.72 corrective round under `hypothesis:a00-2d789d62-3c038a` (this node's
parent), on `goal:g7.31.3.2`. The previous kid `a00-bb77a6b7` made these same
edits in its own worktree but its `cli.py done` left the four sibling node
files FOREIGN and UNCOMMITTED — a node path whose basename does not carry the
round's agent id is not in the round's own paths (`cli.py:2066`,
`_round_scope_ok`), so its branch did not carry what it claimed. This round
makes the edits again and declares them in `--owns`, so the round commit
carries them.

### 1. PRIMARY — `hypothesis:a00-37392a90-0d3366` probes[1]

Before (DT.46, ephemeral): an auth dm run as
`AGI_TIER=kid AGI_AGENT_ID=a00-75145740 ... send.py send --from a00-75145740
--to sanctuary-director probe`. `a00-75145740`'s `agent.json` lives only in
the `a00-f3048920` worktree and NOT under the shared sessions root, so after
merge the gate fails OPEN — the recorded `REFUSED` is not reproducible.

After: the committed, self-fixturing pytest probe. `probes:` is frontmatter,
so it was set with a whole-list `write.py hypothesis:a00-37392a90-0d3366
'set probes [...]'` (not a `replace body`); `probes[0]` (gate) and `probes[2]`
(wire import guard) are unchanged, and the THOUGHT was rewritten.

    {"conjunct": 2, "class": "auth", "cmd": "python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q", "expected": "1 passed: the gate refuses a foreign target BY PARENT NAME and still delivers to the parent; the test builds its own agent.json under tmp_path, so no worktree-only session record is required", "observed": "1 passed, 20 deselected in 0.65s (rc=0)", "result": "pass"}

### 2. NOTE — `hypothesis:a00-75145740-c77fbe` testable_claim

`set testable_claim` rewrote the claim around the tip's current state: the
durable, committed, self-fixturing pytest probe; the one `## Agent Notes`
heading; the truthful THOUGHT. The stale "tip a9abe37c4 / live kid
a00-75145740 REFUSED" wording is gone.

### 3. NOTE — `hypothesis:a00-856dc44a-5c85fe` claim narrowed

`set testable_claim` narrowed the claim to c77fbe: `probes[0]` — and ONLY
that probe — is the committed self-fixturing case; c77fbe's own
`probes[1]`/`probes[2]` are kept; and this round did NOT touch
`hypothesis:a00-37392a90-0d3366` probes[1] (that stayed ephemeral until
DT.72). The body sentence at body lines 26-28 was replaced through
`write.py hypothesis:a00-856dc44a-5c85fe 'replace body 26:28 -'` so the
same scope is stated in prose.

### 4. BOOKKEEPING — `goal:g7.31.3.2` residue table

`write.py goal:g7.31.3.2 'replace body 32:41 -'` whole-replaced the stale
DT.45 table — which still showed three residues open and carried
`NO merge-up ... Next parent: DT.46` — with the DT.72 table marking all
three CLOSED. `grep -c 'Next parent: DT.46'` on the goal node is now 0. The
goal THOUGHT was rewritten.

## Evidence

### pytest probe (the auth conjunct)

    $ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -k test_kid_send_gate_refuses_foreign_target_and_allows_parent -q
    1 passed, 20 deselected in 0.65s        (rc=0)

The test fixture builds its own agent record under `tmp_path`
(`_write_agent_record(graph, "a00-kid-1", PARENT)`, test line 217) and drives
the REAL entry point `send_mod.main` (test lines 224, 232), not a stub.

### stale-probe falsifier (the gate conjunct — the OLD probe really fails open)

    $ python3 -c "... send._kid_parent_id(send._project_root(),'a00-75145740') ..."
    kid_parent None
    refusal None

so the removed `AGI_AGENT_ID=a00-75145740` dm is genuinely not reproducible
on this tip.

### touched surfaces

    $ python3 extensions/agi/bin/links.py links
    links: 3861 resolved, 0 broken (18 retired payload(s), not damage)   (rc=0)

    $ python3 -m pytest extensions/agi/tests/test_send.py -q
    330 passed, 11 warnings in 32.68s                                    (rc=0)

    $ git diff --numstat -- extensions/ src/ skills/
    (empty)

No engine/source file was touched: `production_lines: 0`, under the
40-line ceiling.

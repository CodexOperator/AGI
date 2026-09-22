---
id: experiment:a00-75145740-residue1-auth-probe
mint_id: 5ff32eeb648f48498f27194cc0f26fc6
type: experiment
parents:
  - hypothesis:a00-37392a90-0d3366
next_edges: []
edited_by: a00-75145740
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d3c9f079e89fba0d
season: 2
thought_session: iter-DT.46
title: "DT.46 residue-1: tip-reproducible auth gate probe (kid a00-75145740 dm seat refused by name)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-75145740-residue1-auth-probe

DT.46 corrective residue round under `goal:g7.31.3.2`, base tip `a9abe37c4`.
This run closes **residue 1 (PRIMARY)** — a stale auth probe that fails open —
and records the exact commands and observed output. Residues 2 and 3 (NOTEs)
were closed in the same round; see the end of this body.

## What was wrong

`hypothesis:a00-37392a90-0d3366` `probes[1]` recorded:

    observed: REFUSED: kid a00-1cbef27c may dm only its parent a00-58640e14, not sanctuary-director

That observation is **stale and not reproducible** on this tip. `a00-1cbef27c`
has no `spawned_by_agent` record here, so `send.py`'s kid-dm gate
(`_kid_dm_refusal` -> `_kid_parent_id`, `extensions/agi/bin/send.py:920`) fails
OPEN with a stderr `warn:` and writes a real dm (rc=0). A recorded `REFUSED`
that in fact fails open is a false probe.

## Command run on this tip (my own live kid id)

    AGI_TIER=kid AGI_AGENT_ID=a00-75145740 \
      python3 extensions/agi/bin/send.py send --from a00-75145740 \
      --to sanctuary-director probe

## OBSERVED (verbatim stderr), exit code 3

    REFUSED: kid a00-75145740 may dm only its parent a00-f3048920, not sanctuary-director

My `agent.json` carries `spawned_by_agent: a00-f3048920` (the agent that cut
me), so the gate refuses **by name** and does not fail open. This observation
replaces `probes[1]` on `hypothesis:a00-37392a90-0d3366`.

## Whole probes list re-run on this tip

Neither of the other two probes was left un-run either:

    python3 extensions/agi/bin/write.py hypothesis:a00-37392a90-0d3366 bogus_verb x
    -> ERR: no verb 'bogus_verb'. Known: adopt, body_patch, link, note, patch,
       payload, payload_text, read, replace, set, thought, unset (exit 2)

    python3 -c "import sys,builtins,runpy; ... builtins.__import__ guard on 'dispatch' ...
               runpy.run_path('extensions/agi/bin/workflow.py', run_name='__main__')"
    -> stages=2 via dispatch.py kids; exit=0; no AssertionError
    grep -nE 'import dispatch|from dispatch' extensions/agi/bin/workflow.py -> no lines (rc=1)

## Touched-surface checks (brief-required)

    python3 -m pytest extensions/agi/tests/test_send.py -q
    -> 330 passed, 11 warnings in 34.22s  (rc=0)

    python3 extensions/agi/bin/links.py links
    -> links: 3855 resolved, 0 broken (18 retired payload(s), not damage)  (rc=0)

## Residues 2 and 3 (NOTEs) closed in this same round

- `hypothesis:a00-1cbef27c-4bceb5`: the duplicate `## Agent Notes` sections
  were collapsed to ONE heading, both notes' content merged under it. (A first
  `replace body 49:52` was off by one and duplicated the heading; repaired
  in place with `replace body 48:49` -> single heading, re-read to confirm.)
- `hypothesis:a00-66b5e112-33ffb4`: the THOUGHT first line said "replaces the
  kid's THOUGHT", but the kid never authored one. Rephrased truthfully: the
  parent authored this THOUGHT as its review; nothing was replaced.

## Production lines

`git diff --numstat -- extensions/ src/ skills/` is empty: no engine/source
file was touched. `production_lines: 0`, well under the 40-line ceiling.
